#!/usr/bin/env python3
import asyncio
import json
import os
import websockets

"""
Simple WS client for the ws-bridge (port 9000).
The bridge expects messages of shape:
  {"type": "fira_init", "payload": {...}}
  {"type": "ift", "payload": {...}}
  {"type": "nir_notify", "payload": {...}}
  {"type": "nir_confirm", "payload": {...}}
Bridge forwards to router and returns the router response.
"""

WS_URL = os.getenv("WS_URL", "ws://localhost:9000")

async def main():
    async with websockets.connect(WS_URL) as ws:
        # 1) FIR/A init
        init_payload = {
            "initiator": "ws-bridge-client",
            "responder": "router",
            "roles": ["client", "server"],
            "context": {"channel": "ws"}
        }
        await ws.send(json.dumps({"type": "fira_init", "payload": init_payload}))
        resp = json.loads(await ws.recv())
        print("INIT RESP:", resp)
        if resp.get("status") != "ok":
            return
        data = resp["data"]
        fir = data["fir_a_id"]
        hsh = data["continuity_hash"]

        # 2) IFT
        ift_payload = {
            "fir_a_id": fir,
            "intent": "ws_bridge_test",
            "context": {"msg": "hello"},
            "continuity_hash_prev": hsh,
        }
        await ws.send(json.dumps({"type": "ift", "payload": ift_payload}))
        resp2 = json.loads(await ws.recv())
        print("IFT RESP:", resp2)


if __name__ == "__main__":
    asyncio.run(main())
