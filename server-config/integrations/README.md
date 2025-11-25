# Integraties (SIP, SMTP, MQTT) met JTel Router

Doel: minimale haakjes om intent/continuity_hash naar de router te sturen, zonder volledige implementatie.

## SIP (Asterisk dialplan/AGI)
- Vereist: curl + jq op de PBX.
- Dialplan-sjabloon:
```
[default]
exten => _X.,1,NoOp(JIS: call setup)
 same => n,Set(JIS_SECRET=denDolder_2024!)                 ; pas aan
 same => n,Set(JIS_BASE=http://router:8081)                ; of http://192.168.4.76:18081
 same => n,Set(FIR=${SHELL(curl -s -X POST -H "X-JIS-SECRET: ${JIS_SECRET}" \
   -H "Content-Type: application/json" \
   -d '{"initiator":"sip-gateway","responder":"pbx","roles":["telephony_core"],"context":{"caller":"${CALLERID(num)}","callee":"${EXTEN}"}}' \
   ${JIS_BASE}/fira/init | jq -r .fir_a_id)})
 same => n,Set(HASH=${SHELL(curl -s -X POST -H "X-JIS-SECRET: ${JIS_SECRET}" \
   -H "Content-Type: application/json" \
   -d "{\"fir_a_id\":\"${FIR}\",\"intent\":\"call_setup\",\"context\":{\"caller\":\"${CALLERID(num)}\",\"callee\":\"${EXTEN}\"},\"continuity_hash_prev\":\"\"}" \
   ${JIS_BASE}/ift | jq -r .continuity_hash)})
 same => n,Dial(SIP/${EXTEN})
```
- Productie: gebruik ARI/AGI-script voor betere foutafhandeling; bij 409/401 → flag/NIR.

## SMTP (conceptueel)
- Inkomend/uitgaand e-mail event naar router posten vóór accept/relay:
  - Endpoint: `/ift` met intent `"smtp_send"` of `"smtp_recv"` en context (from/to/message-id).
  - Headers aan mail toevoegen: `X-JIS-FIR-A-ID`, `X-JIS-CH-PREV`, `X-JIS-INTENT`.
- Implementatie-opties:
  - Postfix milter of smtpd-proxy (bijv. aiosmtpd) die vóór relay de router callt en bij mismatch 4xx/5xx geeft.

## MQTT (conceptueel)
- Gebruik publish/subscribe met verplichte metadata:
  - Properties (v5) of payload met: `fir_a_id`, `continuity_hash_prev`, `intent`, `context`.
- Bridge/broker flow:
  - Bij publish: broker/bridge roept `/ift` aan met intent = topic/actie; mismatch → reject/flag.
  - Bij subscribe: eerste connect kan `/fira/init` triggeren (initiator=responder=client-id, rol mqtt_client).
- Minimal client-patroon (pseudo):
```
payload = {
  "fir_a_id": "...",
  "continuity_hash_prev": "...",
  "intent": "mqtt_publish",
  "context": {"topic": topic}
}
# POST naar router /ift, en nieuw continuity_hash bewaren
```

## Aanpassingen nodig voor echte inzet
- mTLS/JWT per agent, niet alleen shared secret.
- Strakke intent/role-whitelists per service.
- Rate limits per IP/client-id.
- Logging/audit naar Postgres (reeds in router).

Gebruik dit als startpunt; voor volledige implementaties (milters, ARI/AGI scripts, MQTT bridge) moet per platform een eigen daemon/bridge worden opgezet die de router-API aanroept met fir_a_id + continuity_hash_prev.
