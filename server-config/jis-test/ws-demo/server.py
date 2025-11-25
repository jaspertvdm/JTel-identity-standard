#!/usr/bin/env python3
import asyncio
import json
import os
import websockets
from typing import Dict, Any

"""
WebSocket demo server that reuses the continuity_hash flow:
- Client connects and sends JSON messages with:
    { "fir_a_id": "...", "continuity_hash_prev": "...", "intent": "..." , "context": {...} }
- Server maintains an in-memory continuity_hash per fir_a_id (for demo only) and replies with:
    { "status": "ok", "fir_a_id": "...", "continuity_hash": "...", "seq": n }
- If continuity_hash_prev mismatches, server replies with status=conflict.
"""

STATE: Dict[str, Dict[str, Any]] = {}


def incremental_hash(prev_hash: str, event: Dict[str, Any]) -> str:
    from hashlib import sha256

    payload = json.dumps({"prev": prev_hash, "event": event}, sort_keys=True, separators=(",", ":"))
    return sha256(payload.encode("utf-8")).hexdigest()


async def handler(websocket):
    async for message in websocket:
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            await websocket.send(json.dumps({"status": "error", "detail": "invalid json"}))
            continue

        fir_a_id = data.get("fir_a_id")
        intent = data.get("intent")
        context = data.get("context", {})
        prev = data.get("continuity_hash_prev")

        if not fir_a_id or not intent:
            await websocket.send(json.dumps({"status": "error", "detail": "fir_a_id and intent required"}))
            continue

        state = STATE.get(fir_a_id)
        if not state:
            # First message for this FIR/A
            event = {"type": "ws_init", "intent": intent, "context": context}
            hsh = incremental_hash("", event)
            STATE[fir_a_id] = {"hash": hsh, "seq": 1}
            await websocket.send(json.dumps({"status": "ok", "fir_a_id": fir_a_id, "continuity_hash": hsh, "seq": 1}))
            continue

        # Existing chain
        last_hash = state["hash"]
        if prev and prev != last_hash:
            await websocket.send(json.dumps({"status": "conflict", "detail": "continuity_hash_prev mismatch", "fir_a_id": fir_a_id, "expected": last_hash}))
            continue

        event = {"type": "ws_intent", "intent": intent, "context": context}
        new_hash = incremental_hash(last_hash, event)
        state["hash"] = new_hash
        state["seq"] += 1
        await websocket.send(json.dumps({"status": "ok", "fir_a_id": fir_a_id, "continuity_hash": new_hash, "seq": state["seq"]}))


async def main():
    port = int(os.getenv("WS_PORT", "9000"))
    async with websockets.serve(handler, "0.0.0.0", port):
        print(f"WebSocket demo server listening on 0.0.0.0:{port}")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
