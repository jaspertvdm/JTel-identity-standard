import hashlib
import json
import os
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple

import psycopg
import redis
from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from pydantic import BaseModel, Field

app = FastAPI(title="JIS Test Router", version="0.2.0")


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


def incremental_hash(prev_hash: str, event: Dict[str, Any]) -> str:
    """Compute continuity hash from previous hash + current event."""
    payload = json.dumps({"prev": prev_hash, "event": event}, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def with_timestamp(event: Dict[str, Any]) -> Dict[str, Any]:
    return {**event, "ts": time.time()}


# --- Persistence: Postgres -------------------------------------------------
PG_HOST = os.getenv("PGHOST", "db")
PG_USER = os.getenv("PGUSER", "jis")
PG_PASSWORD = os.getenv("PGPASSWORD", "jis")
PG_DATABASE = os.getenv("PGDATABASE", "jis")
PG_PORT = os.getenv("PGPORT", "5432")
PG_DSN = f"host={PG_HOST} port={PG_PORT} dbname={PG_DATABASE} user={PG_USER} password={PG_PASSWORD}"

pool = psycopg.ConnectionPool(PG_DSN, min_size=1, max_size=5)


def init_db() -> None:
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    id BIGSERIAL PRIMARY KEY,
                    fir_a_id UUID NOT NULL,
                    seq INTEGER NOT NULL,
                    continuity_hash TEXT NOT NULL,
                    payload JSONB NOT NULL,
                    ts TIMESTAMPTZ DEFAULT NOW()
                );
                CREATE INDEX IF NOT EXISTS idx_events_fir ON events(fir_a_id, seq DESC);
                """
            )
        conn.commit()


def fetch_last(fir_a_id: str) -> Optional[Tuple[int, str]]:
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT seq, continuity_hash FROM events WHERE fir_a_id = %s ORDER BY seq DESC LIMIT 1",
                (fir_a_id,),
            )
            row = cur.fetchone()
            if row:
                return row[0], row[1]
    return None


def append_event_db(fir_a_id: str, event: Dict[str, Any], continuity_hash_prev: Optional[str]) -> Tuple[str, int]:
    last = fetch_last(fir_a_id)
    if not last:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown FIR/A")

    last_seq, last_hash = last
    if continuity_hash_prev and continuity_hash_prev != last_hash:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="continuity_hash_prev mismatch; start NIR or re-init FIR/A",
        )

    event_with_meta = with_timestamp(event)
    new_hash = incremental_hash(last_hash, event_with_meta)
    new_seq = last_seq + 1

    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO events (fir_a_id, seq, continuity_hash, payload) VALUES (%s, %s, %s, %s)",
                (fir_a_id, new_seq, new_hash, json.dumps(event_with_meta)),
            )
        conn.commit()

    return new_hash, new_seq


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


# --- Basic rate limiting via Redis (per IP per window) ---------------------
RATE_LIMIT = int(os.getenv("RATE_LIMIT", "60"))  # requests
RATE_WINDOW = int(os.getenv("RATE_WINDOW", "60"))  # seconds
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def rate_limit(request: Request) -> None:
    # Very simple sliding window using Redis key with expiry.
    ip = request.client.host if request.client else "unknown"
    key = f"rl:{ip}"
    try:
        current = redis_client.incr(key)
        if current == 1:
            redis_client.expire(key, RATE_WINDOW)
        if current > RATE_LIMIT:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="rate limit exceeded",
            )
    except redis.RedisError:
        # If Redis is down, fail open (no rate limit) but log in response detail.
        pass


@app.post(
    "/fira/init",
    response_model=EventResponse,
    dependencies=[Depends(require_secret), Depends(rate_limit)],
)
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
    event_with_meta = with_timestamp(genesis_event)
    continuity_hash = incremental_hash("", event_with_meta)

    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO events (fir_a_id, seq, continuity_hash, payload) VALUES (%s, %s, %s, %s)",
                (fir_a_id, 1, continuity_hash, json.dumps(event_with_meta)),
            )
        conn.commit()

    return EventResponse(fir_a_id=fir_a_id, continuity_hash=continuity_hash, events=1)


@app.post(
    "/ift",
    response_model=EventResponse,
    dependencies=[Depends(require_secret), Depends(rate_limit)],
)
def ift(body: IFT) -> EventResponse:
    event = {
        "type": "ift",
        "intent": body.intent,
        "context": body.context,
        "timebox_seconds": body.timebox_seconds,
    }
    new_hash, seq = append_event_db(body.fir_a_id, event, body.continuity_hash_prev)
    return EventResponse(fir_a_id=body.fir_a_id, continuity_hash=new_hash, events=seq)


@app.post(
    "/nir/notify",
    response_model=EventResponse,
    dependencies=[Depends(require_secret), Depends(rate_limit)],
)
def nir_notify(body: NIRNotice) -> EventResponse:
    event = {
        "type": "nir_notify",
        "reason": body.reason,
        "suggested_method": body.suggested_method,
    }
    new_hash, seq = append_event_db(body.fir_a_id, event, body.continuity_hash_prev)
    return EventResponse(fir_a_id=body.fir_a_id, continuity_hash=new_hash, events=seq)


@app.post(
    "/nir/confirm",
    response_model=EventResponse,
    dependencies=[Depends(require_secret), Depends(rate_limit)],
)
def nir_confirm(body: NIRConfirm) -> EventResponse:
    event = {
        "type": "nir_confirm",
        "method": body.method,
        "result": body.result,
    }
    new_hash, seq = append_event_db(body.fir_a_id, event, body.continuity_hash_prev)
    return EventResponse(fir_a_id=body.fir_a_id, continuity_hash=new_hash, events=seq)


@app.get(
    "/relation/{fir_a_id}",
    dependencies=[Depends(require_secret), Depends(rate_limit)],
)
def relation_info(fir_a_id: str) -> Dict[str, Any]:
    last = fetch_last(fir_a_id)
    if not last:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown FIR/A")
    seq, hsh = last
    return {"fir_a_id": fir_a_id, "events": seq, "continuity_hash": hsh}


@app.on_event("startup")
def on_startup() -> None:
    init_db()
