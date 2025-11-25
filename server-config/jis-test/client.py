#!/usr/bin/env python3
"""
Kleine client om FIR/A + IFT + NIR calls te doen naar de JIS router.
Gebruikt alleen de Python-stdlib (urllib), dus geen extra dependencies nodig.

Gebruik:
    BASE=http://localhost:18081 SECRET=changeme python3 client.py
Of met LAN-IP:
    BASE=http://<pi-ip>:18081 SECRET=<secret> python3 client.py
"""

import json
import os
import sys
import urllib.error
import urllib.request

BASE = os.getenv("BASE", "http://localhost:18081")
SECRET = os.getenv("SECRET", "changeme")
HEADERS = {
    "Content-Type": "application/json",
    "X-JIS-SECRET": SECRET,
}


def post(path: str, payload: dict):
    url = f"{BASE}{path}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.HTTPError as e:
        sys.stderr.write(f"HTTPError {e.code} on {path}: {e.read().decode('utf-8')}\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"Error calling {path}: {e}\n")
        sys.exit(1)


def get(path: str):
    url = f"{BASE}{path}"
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode("utf-8")
        return json.loads(body)


def main():
    print(f"Using BASE={BASE}")
    health = get("/health")
    print("Health:", health)

    init = post(
        "/fira/init",
        {
            "initiator": "app-client",
            "responder": "server-core",
            "roles": ["client", "server"],
            "context": {"channel": "test", "humotica": "natural_language"},
        },
    )
    print("FIR/A:", init)
    fir = init["fir_a_id"]
    hsh = init["continuity_hash"]

    ift = post(
        "/ift",
        {
            "fir_a_id": fir,
            "intent": "unlock_door",
            "context": {"humotica": "natural_language"},
            "continuity_hash_prev": hsh,
        },
    )
    print("IFT:", ift)
    hsh = ift["continuity_hash"]

    nir = post(
        "/nir/notify",
        {
            "fir_a_id": fir,
            "reason": "unusual_time",
            "continuity_hash_prev": hsh,
        },
    )
    print("NIR notify:", nir)
    hsh = nir["continuity_hash"]

    conf = post(
        "/nir/confirm",
        {
            "fir_a_id": fir,
            "method": "pin",
            "result": "confirmed",
            "continuity_hash_prev": hsh,
        },
    )
    print("NIR confirm:", conf)


if __name__ == "__main__":
    main()
