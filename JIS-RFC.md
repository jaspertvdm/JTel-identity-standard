# JTel Semantic Safety Protocol — RFC-stijl Draft

## 1. Terminologie
- HID: menselijke sleutel (niet verzenden/exporteren).
- DID: device-afgeleide voor sessies/content.
- FIR/A: eerste relatie (Flag→Identify→Accept/Revoke), levert fir_a_id.
- ContinuityHash: incremental hash over chain events (prev_hash + event).
- IO/DO/OD/NIR: mens/device/operatie/notify-identify-rectify.
- INFC/OFC: content zonder/ met semantische context (na intent + SCS).

## 2. Headers / Metadata
- HTTP: `X-JIS-SECRET` of `Authorization: Bearer <jwt>` (HS256).
- WS/MQTT: payloadvelden `fir_a_id`, `continuity_hash_prev`, `intent`, `context`.
- Opcodes/intents/roles bij voorkeur uit registry (versiebeleid: semver).

## 3. API Endpoints (HTTP)
- `POST /fira/init` body: initiator, responder, roles, context, humotica? → returns fir_a_id, continuity_hash, events=1.
- `POST /ift` body: fir_a_id, intent, context, timebox_seconds, continuity_hash_prev.
- `POST /nir/notify` body: fir_a_id, reason, suggested_method?, continuity_hash_prev.
- `POST /nir/confirm` body: fir_a_id, method, result, continuity_hash_prev.
- `GET /relation/{fir_a_id}` → laatste hash + eventcount.

## 4. Message Formats (WS/MQTT bridge)
```
{ "type": "fira_init", "payload": { ... } }
{ "type": "ift", "payload": { ... } }
{ "type": "nir_notify", "payload": { ... } }
{ "type": "nir_confirm", "payload": { ... } }
```
Bridge post deze payloads 1:1 naar de router endpoints.

## 5. Foutcodes
- 401/403: auth-fout (secret/jwt ongeldig).
- 409: continuity_hash_prev mismatch → start NIR of nieuwe FIR/A.
- 400: intent/role niet toegestaan (whitelist).
- 429: rate limit overschreden (Redis).

## 6. Veiligheid
- Auth: mTLS of JWT; shared secret alleen voor test.
- HID nooit op de lijn; alleen DID/OFC-metavelden.
- continuity_hash_prev verplicht bij elke stap; mismatch → 409.
- Ratelimiting per IP/agent; intent/role-whitelists per service.

## 7. Privacy
- Geen biometrie of HID in transmissie/logs.
- Minimaal context loggen; PIA vereist per implementatie.

## 8. Registries / Versiebeleid
- Intents, roles, context keys: beheerde lijst (semver releases).
- Backwards compat: nieuwe velden optioneel; geen breuken zonder major bump.

## 9. Conformance
- Testvectors: good/bad chains (zie CONFORMANCE.md).
- Clients moeten: laatste continuity_hash bewaren en meesturen; errors correct afhandelen.

## 10. Extensies
- Protocol bindingen: HTTP, WS, MQTT, SIP (call_setup intent), SMTP (send/recv intent), WebRTC signaling.
- Eventtypes uitbreidbaar; NIR/custom flags mogelijk, mits chain intact.
