#!/usr/bin/env python3
"""
Minimal Asterisk AGI script that:
- Reads AGI env for caller/extension.
- Calls JTel router /fira/init and /ift with intent "call_setup".
Prereqs: Python stdlib only; env vars JIS_BASE (e.g. http://router:8081) and JIS_SECRET.
Dialplan: exten => _X.,n,AGI(/path/to/agi_router.py)
"""

import json
import os
import sys
import urllib.request
import urllib.error


def agi_env():
    env = {}
    for line in sys.stdin:
        line = line.strip()
        if line == "":
            break
        if ":" in line:
            k, v = line.split(":", 1)
            env[k.strip()] = v.strip()
    return env


def post_json(url, payload, headers=None):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers or {}, method="POST")
    with urllib.request.urlopen(req, timeout=5) as resp:
        body = resp.read().decode("utf-8")
        return json.loads(body)


def main():
    base = os.getenv("JIS_BASE", "http://router:8081")
    secret = os.getenv("JIS_SECRET", "")
    headers = {"Content-Type": "application/json"}
    if secret:
        headers["X-JIS-SECRET"] = secret

    env = agi_env()
    caller = env.get("agi_callerid", "unknown")
    exten = env.get("agi_extension", "unknown")

    try:
        init_resp = post_json(
            f"{base}/fira/init",
            {
                "initiator": "sip-gateway",
                "responder": "pbx",
                "roles": ["telephony_core"],
                "context": {"caller": caller, "callee": exten},
            },
            headers=headers,
        )
        fir = init_resp["fir_a_id"]
        hsh = init_resp["continuity_hash"]

        ift_resp = post_json(
            f"{base}/ift",
            {
                "fir_a_id": fir,
                "intent": "call_setup",
                "context": {"caller": caller, "callee": exten},
                "continuity_hash_prev": hsh,
            },
            headers=headers,
        )
        sys.stdout.write(f'EXEC Verbose "JIS OK fir={fir} seq={ift_resp.get("events")}"\n')
    except (urllib.error.HTTPError, urllib.error.URLError, KeyError, json.JSONDecodeError) as e:
        sys.stdout.write(f'EXEC Verbose "JIS ERROR {e}"\n')
    sys.stdout.flush()


if __name__ == "__main__":
    main()
