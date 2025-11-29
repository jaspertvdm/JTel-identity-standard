# JIS Quick Reference - Cheatsheet

**Alle commando's die je nodig hebt op één pagina**

## 🚀 Setup & Start

```bash
# 1. Repo setup
cd /pad/naar/JTel-identity-standard
git pull origin claude/security-layer-integration-014bYZy9HuEysgqUVDaJhUqM

# 2. Start router
cd server-config/jis-test
docker compose up -d --build

# 3. Installeer SDK
cd ../../client-sdk/python  # Let op: terug naar root eerst!
pip install -e .

# 4. Test
python examples/live_demo.py
```

---

## 📁 Navigatie

```bash
# Repo root
cd /pad/naar/JTel-identity-standard

# Server setup
cd server-config/jis-test

# SDK
cd client-sdk/python

# Van server naar SDK
cd ../../client-sdk/python

# Van SDK naar server
cd ../../server-config/jis-test
```

---

## 🐳 Docker Commando's

```bash
# Start alles
docker compose up -d

# Start en rebuild
docker compose up -d --build

# Stop alles
docker compose down

# Stop + verwijder volumes (clean slate)
docker compose down -v

# Logs bekijken
docker compose logs -f router

# Status checken
docker compose ps

# Restart specifieke service
docker compose restart router

# Exec in container
docker compose exec router bash
```

---

## 🔍 Status Checks

```bash
# Health check
curl http://localhost:18081/health
# Verwacht: {"status":"ok","version":"0.4.0"}

# Readiness (met DB/Redis checks)
curl http://localhost:18081/health/ready
# Verwacht: {"status":"ready","checks":{...}}

# Metrics
curl http://localhost:18081/metrics
# Verwacht: {"total_relationships":...,"total_events":...}

# Admin UI
# Browser: http://localhost:18081/
# Login: JIS_SHARED_SECRET (default: example_secret_123)
```

---

## 🐍 Python SDK

### Installatie
```bash
cd /pad/naar/JTel-identity-standard/client-sdk/python
pip install -e .
```

### Test Import
```bash
python -c "from jis_client import JISClient, DIDKey, HIDKey; print('✓ OK')"
```

### Voorbeelden
```bash
# Simpel (5 regels)
python examples/simple_app.py

# Volledig (met alle features)
python examples/basic_usage.py

# Live demo (interactive)
python examples/live_demo.py
```

### Basis Gebruik
```python
from jis_client import JISClient, DIDKey, HIDKey

client = JISClient("http://localhost:18081", secret="example_secret_123")
did, hid = DIDKey.generate(), HIDKey.generate()

fir_a = client.init_relationship(
    "app", "server", ["client"],
    did_key=did, hid_key=hid
)

client.send_intent(fir_a.id, "test", {})
```

---

## ⚙️ Configuratie

### Secrets Aanpassen

```bash
# Eerste keer
cd server-config/jis-test
cp .env.example .env
nano .env

# Pas aan:
JIS_SHARED_SECRET=jouw_secret
POSTGRES_PASSWORD=jouw_password

# Restart
docker compose restart
```

### Whitelists Instellen

```bash
# Edit .env
nano .env

# Voeg toe:
ALLOWED_INTENTS=unlock_door,verify_identity
ALLOWED_ROLES=client,server

# Restart
docker compose restart router
```

---

## 🔧 Troubleshooting

### Router start niet
```bash
docker compose logs router
docker compose restart router
```

### SDK niet gevonden
```bash
# Check locatie
pwd
ls -la client-sdk/python

# Ga naar juiste directory
cd /pad/naar/JTel-identity-standard/client-sdk/python
pip install -e .
```

### Admin UI 401 error
```bash
# Check secret in .env
cat server-config/jis-test/.env | grep JIS_SHARED_SECRET

# Of in compose file
cat server-config/jis-test/docker-compose.yml | grep JIS_SHARED_SECRET
```

### Database reset
```bash
cd server-config/jis-test
docker compose down -v
docker compose up -d
# Migraties draaien automatisch opnieuw
```

---

## 📊 Monitoring

### Logs Live Volgen
```bash
docker compose logs -f router        # Router logs
docker compose logs -f db            # Database logs
docker compose logs -f               # Alle logs
```

### Resource Usage
```bash
docker stats
```

### Database Inspectie
```bash
# Connect
docker compose exec db psql -U jis -d jis

# Queries
SELECT COUNT(*) FROM events;
SELECT COUNT(DISTINCT fir_a_id) FROM events;
SELECT * FROM schema_migrations;
\q  # Exit
```

---

## 🧪 Testing

### Curl Tests
```bash
SECRET="example_secret_123"
BASE="http://localhost:18081"

# Health
curl $BASE/health

# Create FIR/A
curl -X POST "$BASE/fira/init" \
  -H "X-JIS-SECRET: $SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "initiator": "test-client",
    "responder": "test-server",
    "roles": ["client"]
  }'

# Send Intent
curl -X POST "$BASE/ift" \
  -H "X-JIS-SECRET: $SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "fir_a_id": "YOUR_FIR_A_ID",
    "intent": "test_action"
  }'
```

### Python Quick Test
```python
from jis_client import JISClient
client = JISClient("http://localhost:18081", secret="example_secret_123")
print(client.health_check())
```

---

## 🔐 Security

### Genereer Sterke Secrets
```bash
# Random secret
openssl rand -base64 32

# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### JWT Setup
```bash
# Generate JWT secret
JWT_SECRET=$(openssl rand -base64 64)

# Add to .env
echo "JWT_SECRET=$JWT_SECRET" >> .env
echo "JWT_AUDIENCE=jis-router" >> .env

# Restart
docker compose restart router
```

---

## 📁 Important Files

```
server-config/jis-test/
├── docker-compose.yml      # Services config
├── .env                    # Secrets (create from .env.example)
├── DEPLOYMENT.md           # Production guide
└── router/
    ├── main.py             # Router code
    ├── migrations/         # DB migrations
    └── static/             # Admin UI

client-sdk/python/
├── jis_client/             # SDK code
├── examples/               # Test scripts
└── README.md               # SDK docs
```

---

## 🌐 URLs

**Lokaal:**
- Admin UI: http://localhost:18081/
- API: http://localhost:18081/health
- WebSocket: ws://localhost:9000/
- MQTT: mqtt://localhost:31883/

**Remote (vervang YOUR_IP):**
- Admin UI: http://YOUR_IP:18081/
- API: http://YOUR_IP:18081/health

---

## 💾 Backup

```bash
# Database backup
docker compose exec db pg_dump -U jis jis > backup_$(date +%Y%m%d).sql

# Restore
docker compose exec -T db psql -U jis jis < backup_20250126.sql

# Volume backup
docker run --rm \
  -v jis-test_postgres_data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/postgres_$(date +%Y%m%d).tar.gz -C /data .
```

---

## 📞 Support

- **Full docs:** `GETTING-STARTED.md`
- **Deployment:** `server-config/jis-test/DEPLOYMENT.md`
- **SDK:** `client-sdk/python/README.md`
- **Examples:** `client-sdk/python/examples/`

---

**Print deze pagina en hang naast je monitor! 🖨️**
