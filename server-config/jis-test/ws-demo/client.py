#!/usr/bin/env python3
import asyncio
import json
import os
import websockets

"""
WebSocket demo client:
- Connects to WS server
- Sends initial message with fir_a_id + intent
- Receives continuity_hash, then sends a follow-up intent using continuity_hash_prev
"""

BASE = os.getenv("WS_URL", "ws://localhost:9000")
FIR = os.getenv("FIR_A_ID", "demo-fir-a-id")


async def main():
    async with websockets.connect(BASE) as ws:
        # Init
        init_msg = {"fir_a_id": FIR, "intent": "ws_hello", "context": {"msg": "hi from client"}}
        await ws.send(json.dumps(init_msg))
        resp = json.loads(await ws.recv())
        print("INIT RESP:", resp)

        hsh = resp.get("continuity_hash")

        # Next intent
        msg2 = {
            "fir_a_id": FIR,
            "intent": "ws_followup",
            "context": {"step": 2},
            "continuity_hash_prev": hsh,
        }
        await ws.send(json.dumps(msg2))
        resp2 = json.loads(await ws.recv())
        print("FOLLOW RESP:", resp2)


if __name__ == "__main__":
    asyncio.run(main())
