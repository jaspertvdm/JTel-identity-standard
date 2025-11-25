#!/usr/bin/env python3
import json
import os
from typing import Any, Dict

import httpx
import paho.mqtt.client as mqtt

MQTT_HOST = os.getenv("MQTT_HOST", "mqtt")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_IN_TOPIC = os.getenv("MQTT_IN_TOPIC", "jis/in")
MQTT_OUT_TOPIC = os.getenv("MQTT_OUT_TOPIC", "jis/out")

ROUTER_BASE = os.getenv("ROUTER_BASE", "http://router:8081")
SHARED_SECRET = os.getenv("JIS_SHARED_SECRET", "")
JWT_TOKEN = os.getenv("JWT_TOKEN", "")


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
        return {"code": resp.status_code, "data": data}


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe(MQTT_IN_TOPIC)
        print(f"Connected to MQTT {MQTT_HOST}:{MQTT_PORT}, subscribed {MQTT_IN_TOPIC}")
    else:
        print(f"MQTT connect failed with code {rc}")


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
    except json.JSONDecodeError:
        client.publish(MQTT_OUT_TOPIC, json.dumps({"status": "error", "detail": "invalid json"}))
        return

    mtype = payload.get("type")
    body = payload.get("payload", {})

    path = None
    if mtype == "fira_init":
        path = "/fira/init"
    elif mtype == "ift":
        path = "/ift"
    elif mtype == "nir_notify":
        path = "/nir/notify"
    elif mtype == "nir_confirm":
        path = "/nir/confirm"

    if not path:
        client.publish(MQTT_OUT_TOPIC, json.dumps({"status": "error", "detail": "unknown type"}))
        return

    import asyncio
    result = asyncio.run(call_router(path, body))
    status = "ok" if result["code"] < 400 else "error"
    client.publish(MQTT_OUT_TOPIC, json.dumps({"status": status, "response": result}))


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.loop_forever()


if __name__ == "__main__":
    main()
