#!/usr/bin/env python3
import asyncio
import json
import os
from typing import Any, Dict

import httpx
import websockets

"""
WebSocket → HTTP bridge that reuses the router's continuity flow.

Message format from client (examples):
  {"type": "fira_init", "payload": {"initiator": "...", "responder": "...", "roles": [...], "context": {...}}}
  {"type": "ift", "payload": {"fir_a_id": "...", "intent": "...", "context": {...}, "continuity_hash_prev": "..."}}
  {"type": "nir_notify", "payload": {"fir_a_id": "...", "reason": "...", "continuity_hash_prev": "..."}}
  {"type": "nir_confirm", "payload": {"fir_a_id": "...", "method": "...", "result": "...", "continuity_hash_prev": "..."}}

Bridge forwards to router endpoints and returns the router JSON response or error.
"""

ROUTER_BASE = os.getenv("ROUTER_BASE", "http://router:8081")
SHARED_SECRET = os.getenv("JIS_SHARED_SECRET", "")
JWT_TOKEN = os.getenv("JWT_TOKEN", "")
WS_PORT = int(os.getenv("WS_PORT", "9000"))


async def call_router(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    url = f"{ROUTER_BASE}{path}"
    headers = {"Content-Type": "application/json"}
    if JWT_TOKEN:
        headers["Authorization"] = f"Bearer {JWT_TOKEN}"
    elif SHARED_SECRET:
        headers["X-JIS-SECRET"] = SHARED_SECRET

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(url, headers=headers, json=payload)
        try:
            data = resp.json()
        except ValueError:
            data = {"detail": resp.text}
        if resp.status_code >= 400:
            return {"status": "error", "code": resp.status_code, "detail": data}
        return {"status": "ok", "data": data}


async def handler(websocket):
    async for message in websocket:
        try:
            msg = json.loads(message)
        except json.JSONDecodeError:
            await websocket.send(json.dumps({"status": "error", "detail": "invalid json"}))
            continue

        mtype = msg.get("type")
        payload = msg.get("payload", {})

        if mtype == "fira_init":
            result = await call_router("/fira/init", payload)
        elif mtype == "ift":
            result = await call_router("/ift", payload)
        elif mtype == "nir_notify":
            result = await call_router("/nir/notify", payload)
        elif mtype == "nir_confirm":
            result = await call_router("/nir/confirm", payload)
        else:
            result = {"status": "error", "detail": "unknown type"}

        await websocket.send(json.dumps(result))


async def main():
    async with websockets.serve(handler, "0.0.0.0", WS_PORT):
        print(f"WS bridge listening on 0.0.0.0:{WS_PORT}, forwarding to {ROUTER_BASE}")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
