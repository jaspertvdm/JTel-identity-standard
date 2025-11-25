# JIS Test Stack (reversibel)

Doel: snel een testpad tussen server ↔ app met een semantische “router” die FIR/A + IFT + NIR events accepteert. Alles draait in Docker en is veilig te verwijderen.

## Starten
```
cd server-config/jis-test
# pas eventueel de secret aan in docker-compose.yml (JIS_SHARED_SECRET)
docker compose up -d --build
```

Services:
- Router (FastAPI) op poort 8081
- Postgres op 5432 (nog niet gebruikt, wel gereserveerd)
- Redis op 6379 (nog niet gebruikt, wel gereserveerd)

## Endpoints (router)
- `POST /fira/init` — genesis van een relatie. Body: initiator, responder, roles, context, humotica?
- `POST /ift` — intent + timebox. Body: fir_a_id, intent, context, timebox_seconds, continuity_hash_prev.
- `POST /nir/notify` — flag/notificatie. Body: fir_a_id, reason, suggested_method?, continuity_hash_prev.
- `POST /nir/confirm` — confirm/rectify. Body: fir_a_id, method, result, continuity_hash_prev.
- `GET /health` — status.

Authenticatie: header `X-JIS-SECRET: <JIS_SHARED_SECRET>` (standaard `changeme` in compose).

Continuity: elke call retourneert `continuity_hash`; stuur die mee als `continuity_hash_prev` bij de volgende call om ketenconsistentie te bewaken.

## Sneltest (curl)
```
SECRET=changeme
BASE=http://localhost:8081

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
- Geen echte opslag van events (in-memory). Postgres/Redis staan klaar om aan te haken.
- Geen mTLS of rate limiting; enkel shared secret header.
- Geen app-agent code; app kan direct POST’en met het shared secret.
