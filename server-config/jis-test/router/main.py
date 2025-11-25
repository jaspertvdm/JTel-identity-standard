import hashlib
import json
import os
import time
import uuid
from typing import Any, Dict, List, Optional

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="JIS Test Router", version="0.1.0")


class FIRInit(BaseModel):
    initiator: str = Field(..., description="Originating entity, e.g. app/device")
    responder: str = Field(..., description="Counterparty entity")
    roles: List[str] = Field(..., description="Declared roles for this relationship")
    context: Dict[str, Any] = Field(default_factory=dict, description="Context at genesis")
    humotica: Optional[str] = Field(
        None, description="Optional human/intent trace for the FIR/A genesis"
    )


class IFT(BaseModel):
    fir_a_id: str
    intent: str
    context: Dict[str, Any] = Field(default_factory=dict)
    timebox_seconds: int = Field(30, description="Soft window for this intent")
    continuity_hash_prev: Optional[str] = None


class NIRNotice(BaseModel):
    fir_a_id: str
    reason: str
    suggested_method: Optional[str] = None
    continuity_hash_prev: Optional[str] = None


class NIRConfirm(BaseModel):
    fir_a_id: str
    method: str
    result: str
    continuity_hash_prev: Optional[str] = None


class EventResponse(BaseModel):
    fir_a_id: str
    continuity_hash: str
    events: int


def require_secret(x_jis_secret: Optional[str] = Header(None)) -> None:
    expected = os.getenv("JIS_SHARED_SECRET")
    if not expected:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Router secret not configured",
        )
    if x_jis_secret != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid shared secret"
        )


def canonical_hash(data: Dict[str, Any]) -> str:
    payload = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


# In-memory store for test purposes only; persistence can be wired to Postgres later.
STATE: Dict[str, Dict[str, Any]] = {}


def append_event(fir_a_id: str, event: Dict[str, Any], continuity_hash_prev: Optional[str]) -> str:
    state = STATE.get(fir_a_id)
    if not state:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown FIR/A")

    last_hash = state["continuity_hash"]
    if continuity_hash_prev and continuity_hash_prev != last_hash:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="continuity_hash_prev mismatch; start NIR or re-init FIR/A",
        )

    events: List[Dict[str, Any]] = state["events"]
    event_with_meta = {**event, "ts": time.time(), "seq": len(events)}
    events.append(event_with_meta)

    new_hash = canonical_hash({"fir_a_id": fir_a_id, "events": events})
    state["continuity_hash"] = new_hash
    return new_hash


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/fira/init", response_model=EventResponse, dependencies=[Depends(require_secret)])
def fira_init(body: FIRInit) -> EventResponse:
    fir_a_id = str(uuid.uuid4())
    genesis_event = {
        "type": "fira_init",
        "initiator": body.initiator,
        "responder": body.responder,
        "roles": body.roles,
        "context": body.context,
        "humotica": body.humotica,
    }
    events = [genesis_event]
    continuity_hash = canonical_hash({"fir_a_id": fir_a_id, "events": events})
    STATE[fir_a_id] = {"events": events, "continuity_hash": continuity_hash}
    return EventResponse(fir_a_id=fir_a_id, continuity_hash=continuity_hash, events=1)


@app.post("/ift", response_model=EventResponse, dependencies=[Depends(require_secret)])
def ift(body: IFT) -> EventResponse:
    event = {
        "type": "ift",
        "intent": body.intent,
        "context": body.context,
        "timebox_seconds": body.timebox_seconds,
    }
    new_hash = append_event(body.fir_a_id, event, body.continuity_hash_prev)
    events_count = len(STATE[body.fir_a_id]["events"])
    return EventResponse(fir_a_id=body.fir_a_id, continuity_hash=new_hash, events=events_count)


@app.post("/nir/notify", response_model=EventResponse, dependencies=[Depends(require_secret)])
def nir_notify(body: NIRNotice) -> EventResponse:
    event = {
        "type": "nir_notify",
        "reason": body.reason,
        "suggested_method": body.suggested_method,
    }
    new_hash = append_event(body.fir_a_id, event, body.continuity_hash_prev)
    events_count = len(STATE[body.fir_a_id]["events"])
    return EventResponse(fir_a_id=body.fir_a_id, continuity_hash=new_hash, events=events_count)


@app.post("/nir/confirm", response_model=EventResponse, dependencies=[Depends(require_secret)])
def nir_confirm(body: NIRConfirm) -> EventResponse:
    event = {
        "type": "nir_confirm",
        "method": body.method,
        "result": body.result,
    }
    new_hash = append_event(body.fir_a_id, event, body.continuity_hash_prev)
    events_count = len(STATE[body.fir_a_id]["events"])
    return EventResponse(fir_a_id=body.fir_a_id, continuity_hash=new_hash, events=events_count)
