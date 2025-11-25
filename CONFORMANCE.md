# Conformance Testvectors (concept)

## Hash-chain (good)
- Step0: prev="" event={"type":"init"} → h0 = sha256(prev+event_json)
- Step1: prev=h0 event={"type":"ift","intent":"unlock"} → h1
- Expect router to accept when continuity_hash_prev == h0 at step1.

## Hash-chain (bad/mismatch)
- Send step1 with continuity_hash_prev="bogus" → expect 409.

## Intent whitelist
- Configure ALLOWED_INTENTS=unlock_door
- Send intent "unlock_door" → 200
- Send intent "reboot_core" → 400 (not allowed)

## Auth
- No/invalid secret or JWT → 401
- Valid secret/JWT → 200

## Rate limit
- RATE_LIMIT=2 per 60s; send 3 quick requests → expect 429 on 3rd.

## WS-bridge
- Send fira_init + ift messages with matching continuity_hash_prev → ok + new hash.
- Send ift with wrong continuity_hash_prev → bridge returns error from router (409).

## MQTT-bridge
- Publish to `jis/in` fira_init → expect response on `jis/out` with status ok.
- Publish ift with wrong hash → expect status error/code 409 on `jis/out`.

## Required fields
- Missing fir_a_id/intent in ift → 400
- Missing roles in fira_init → 400
