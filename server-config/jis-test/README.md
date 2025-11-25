# JIS Test Stack (reversibel)

Doel: snel een testpad tussen server ↔ app met een semantische “router” die FIR/A + IFT + NIR events accepteert. Alles draait in Docker en is veilig te verwijderen.

## Starten
```
cd server-config/jis-test
# pas eventueel de secret aan in docker-compose.yml (JIS_SHARED_SECRET)
docker compose up -d --build
```

Services (hostpoorten):
- Router (FastAPI) op 18081 → container 8081
- Postgres op 55433 → container 5432 (nu gebruikt voor events)
- Redis op 36380 → container 6379 (gebruikt voor rate limiting)

## Endpoints (router)
- `POST /fira/init` — genesis van een relatie. Body: initiator, responder, roles, context, humotica?
- `POST /ift` — intent + timebox. Body: fir_a_id, intent, context, timebox_seconds, continuity_hash_prev.
- `POST /nir/notify` — flag/notificatie. Body: fir_a_id, reason, suggested_method?, continuity_hash_prev.
- `POST /nir/confirm` — confirm/rectify. Body: fir_a_id, method, result, continuity_hash_prev.
- `GET /relation/{fir_a_id}` — laatste hash + eventcount.
- `GET /health` — status.

Authenticatie: header `X-JIS-SECRET: <JIS_SHARED_SECRET>` (standaard `changeme` in compose).
- Optioneel JWT: zet `JWT_SECRET` in docker-compose en stuur `Authorization: Bearer <jwt>` (HS256). Audience/issuer kun je instellen met `JWT_AUDIENCE`/`JWT_ISSUER`.

Continuity: elke call retourneert `continuity_hash`; stuur die mee als `continuity_hash_prev` bij de volgende call om ketenconsistentie te bewaken.

Whitelists/rate limiting:
- Intents/rollen kun je beperken met `ALLOWED_INTENTS` en `ALLOWED_ROLES` (comma separated).
- Rate limit via Redis: `RATE_LIMIT` req per `RATE_WINDOW` seconden (default 60/60).

TLS/mTLS (optioneel):
- Zet `TLS_CERT_FILE` en `TLS_KEY_FILE` op pad naar cert/key (mount ze in de container).
- Client-verificatie: `TLS_CA_FILE` + `TLS_REQUIRE_CLIENT_CERT=true` voor mTLS.

## Sneltest (curl)
```
SECRET=changeme
BASE=http://localhost:18081

# 1) FIR/A init
INIT=$(curl -s -X POST "$BASE/fira/init" \
  -H "X-JIS-SECRET: $SECRET" -H "Content-Type: application/json" \
  -d '{"initiator":"app-client","responder":"server-core","roles":["client","server"],"context":{"channel":"test"} }')
echo "$INIT"
FIR=$(echo "$INIT" | jq -r .fir_a_id)
HASH=$(echo "$INIT" | jq -r .continuity_hash)

# 2) Intent
IFT=$(curl -s -X POST "$BASE/ift" \
  -H "X-JIS-SECRET: $SECRET" -H "Content-Type: application/json" \
  -d "{\"fir_a_id\":\"$FIR\",\"intent\":\"unlock_door\",\"continuity_hash_prev\":\"$HASH\"}")
echo "$IFT"
HASH=$(echo "$IFT" | jq -r .continuity_hash)

# 3) NIR notify
NIR=$(curl -s -X POST "$BASE/nir/notify" \
  -H "X-JIS-SECRET: $SECRET" -H "Content-Type: application/json" \
  -d "{\"fir_a_id\":\"$FIR\",\"reason\":\"unusual_time\",\"continuity_hash_prev\":\"$HASH\"}")
echo "$NIR"
```

## Opruimen
```
docker compose down -v
rm -rf server-config/jis-test  # alleen als je alles wil verwijderen
```

## Wat ontbreekt (bewust)
- Geen mTLS/TLS, enkel shared secret header (voor productie: mTLS of gesigneerde tokens toevoegen).
- Geen app-agent code; app kan direct POST’en met het shared secret.
