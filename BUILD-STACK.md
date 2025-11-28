# JTel Identity Standard - Complete Stack Build Guide

**Universal intent coordination system for autonomous devices, telephony, and application orchestration.**

Build guide for deploying the complete JTel Identity Standard stack - a revolutionary system that enables secure, intent-based coordination between robots, telephony systems, IoT devices, and applications through BETTI (9 natural laws) and JIS protocols.

## What This System Does

The JTel stack enables:
- **Robot & IoT Control** - Coordinate autonomous devices with semantic intent validation
- **Telephony Integration** - SIP/VoIP orchestration with context-aware call handling
- **Application Orchestration** - Secure intent-based API coordination across distributed systems
- **Real-time Decision Making** - Context/Sense/Intent layers with BETTI natural law validation
- **Cryptographic Trust** - DID/HID key management with FIR/A relationship protocols
- **Immutable Audit Trail** - Continuity chains for complete interaction tracking

## Stack Architecture

### Core Services

1. **Brain API** (Python/FastAPI)
   - BETTI coordination engine with 9 natural laws
   - Context/Sense/Intent decision layers
   - Security layers: SNAFT, BALANS, HICSS, Fail2Flag
   - Auto-provisioning with SIP extension assignment
   - Port: Configurable (default 8010)

2. **JIS Router** (Docker)
   - FIR/A (Flag/Identify/Request/Accept) protocol handler
   - DID/HID cryptographic key management
   - Intent-First Transmission (IFT)
   - NIR (Notify/Identify/Rectify) error handling
   - Continuity chain validation
   - Port: Configurable (default 8081)

3. **ntfy Push Server** (Docker)
   - Real-time push notifications
   - Multi-platform delivery (iOS, Android, Web)
   - Topic-based subscription
   - Port: Configurable (default 80)

### Python SDKs

4. **TIBET-BETTI Client SDK**
   - Modern Python library for BETTI integration
   - Time-boxed Intent-Based Exchange Tokens
   - WebSocket support for real-time updates
   - Async/await compatible

5. **JIS Client SDK**
   - Legacy JIS protocol support
   - DID/HID key generation and management
   - FIR/A relationship handling
   - Continuity chain tracking

### Supporting Infrastructure (Docker Compose)

6. **PostgreSQL** - Primary data store for both Brain API and JIS Router
7. **Redis** - Caching, timeboxing, and session management
8. **MQTT Broker** - Event messaging for IoT/device communication
9. **WebSocket Bridge** - Real-time bidirectional communication
10. **Matrix Integration** (Optional) - Pantalaimon proxy for Matrix protocol support

## Prerequisites

- **OS**: Linux (Debian/Ubuntu recommended) or Docker-compatible system
- **Python**: 3.9+ (3.11+ recommended)
- **Database**: PostgreSQL 13+
- **Container Runtime**: Docker + Docker Compose
- **Network**: Static IP or domain name for production deployment

## Installation Guide

### 1. Database Setup

#### Install PostgreSQL

```bash
# Debian/Ubuntu
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Start and enable service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### Create Brain API Database

```bash
sudo -u postgres psql << 'EOF'
CREATE DATABASE jtel_brain;
CREATE USER jtel_brain_user WITH PASSWORD 'CHANGE_THIS_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE jtel_brain TO jtel_brain_user;
\c jtel_brain
CREATE EXTENSION IF NOT EXISTS pgcrypto;
EOF
```

#### Run BETTI Migration

```bash
cd Backend-server-JTel/brain_api
psql -U jtel_brain_user -d jtel_brain -f betti_migration.sql
```

**Creates:**
- `sense_rules` - BETTI Sense layer decision rules
- `betti_intent_log` - Complete intent execution history
- `user_context_cache` - Contextual state management
- `provisioning_codes` - User/device provisioning with auto SIP assignment (1050-1500)
- `identities` - Matrix/VOIP identity mappings

### 2. Brain API Deployment

#### Clone Repository

```bash
git clone https://github.com/jaspertvdm/Backend-server-JTel.git
cd Backend-server-JTel/brain_api
```

#### Setup Python Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Dependencies:**
- FastAPI 0.121+ - Modern async web framework
- Uvicorn - ASGI server
- Pydantic - Data validation
- psycopg2-binary - PostgreSQL driver
- WebSockets - Real-time communication

#### Configure Environment

Create `.env` file:

```bash
# Database Configuration
BRAIN_DB_HOST=localhost
BRAIN_DB_PORT=5432
BRAIN_DB_NAME=jtel_brain
BRAIN_DB_USER=jtel_brain_user
BRAIN_DB_PASSWORD=CHANGE_THIS_PASSWORD

# Optional: LLM Integration (Ollama)
USE_OLLAMA=0
OLLAMA_MODEL=phi3:mini
OLLAMA_HOST=http://localhost:11434
OLLAMA_TIMEOUT=15

# Push Notifications (ntfy)
NTFY_SERVER=http://your-ntfy-server
NTFY_DEFAULT_TOPIC=jtel-notifications
NTFY_ENABLED=1

# Provisioning
PROVISIONING_FILE=/path/to/provisioning.json
```

#### Start Brain API

```bash
# Development Mode (auto-reload)
uvicorn main:app --host 0.0.0.0 --port 8010 --reload

# Production Mode (multi-worker)
uvicorn main:app --host 0.0.0.0 --port 8010 --workers 4
```

#### Verify Deployment

```bash
curl http://localhost:8010/health
# Expected: {"status":"healthy","betti":"enabled"}

curl http://localhost:8010/admin
# Admin UI should be accessible
```

### 3. JIS Router Deployment (Docker)

The JIS Router runs as a Docker Compose stack with all supporting services.

#### Docker Compose Configuration

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  jis-router:
    image: jis-router:latest
    ports:
      - "8081:8081"
    environment:
      - DB_HOST=jis-db
      - DB_PORT=5432
      - DB_NAME=jis_db
      - DB_USER=jis_user
      - DB_PASSWORD=CHANGE_THIS
      - REDIS_URL=redis://jis-redis:6379
    depends_on:
      - jis-db
      - jis-redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8081/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  jis-db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=jis_db
      - POSTGRES_USER=jis_user
      - POSTGRES_PASSWORD=CHANGE_THIS
    volumes:
      - jis-db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U jis_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  jis-redis:
    image: redis:7-alpine
    volumes:
      - jis-redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  jis-mqtt:
    image: eclipse-mosquitto:2
    ports:
      - "1883:1883"
    volumes:
      - ./mosquitto.conf:/mosquitto/config/mosquitto.conf
      - jis-mqtt-data:/mosquitto/data
    healthcheck:
      test: ["CMD", "mosquitto_sub", "-t", "$$SYS/#", "-C", "1", "-i", "healthcheck", "-W", "3"]
      interval: 30s
      timeout: 10s
      retries: 3

  jis-ws-bridge:
    image: jis-ws-bridge:latest
    ports:
      - "9000:9000"
    environment:
      - MQTT_HOST=jis-mqtt
      - MQTT_PORT=1883

volumes:
  jis-db-data:
  jis-redis-data:
  jis-mqtt-data:
```

#### Deploy Stack

```bash
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f jis-router
```

### 4. ntfy Push Server

```bash
# Deploy ntfy
docker run -d \
  --name ntfy \
  -p 80:80 \
  -v /var/cache/ntfy:/var/cache/ntfy \
  binwiederhier/ntfy \
  serve

# Verify
curl http://localhost/v1/health
# Expected: {"healthy":true}
```

### 5. Python SDK Installation

#### TIBET-BETTI SDK (Recommended)

```bash
cd JTel-identity-standard/client-sdk/python/tibet_betti_client
pip install -e .
```

**Example Usage:**

```python
from tibet_betti_client import TibetBettiClient

# Initialize client
client = TibetBettiClient(
    betti_url="http://your-brain-api:8010",
    secret="your-shared-secret"
)

# Establish trust relationship
relationship = client.establish_trust(
    initiator="robot_arm_01",
    responder="factory_controller"
)

# Send intent (robot control)
client.send_tibet(
    relationship_id=relationship.id,
    intent="move_to_position",
    context={
        "x": 150.5,
        "y": 200.0,
        "z": 75.0,
        "speed": "normal"
    }
)

# Send intent (telephony)
client.send_tibet(
    relationship_id=relationship.id,
    intent="initiate_call",
    context={
        "from_extension": "1050",
        "to_number": "+31612345678",
        "trunk": "sip-trunk-01"
    }
)
```

#### JIS Client SDK (Legacy)

```bash
cd JTel-identity-standard/client-sdk/python
pip install -e .
```

**Example Usage:**

```python
from jis_client import JISClient, DIDKey, HIDKey

# Initialize
client = JISClient("http://your-jis-router:8081", secret="your-secret")

# Generate identity keys
did = DIDKey.generate()  # Device Identity
hid = HIDKey.generate()  # Human Identity

# Establish FIR/A relationship
fir_a = client.init_relationship(
    initiator="mobile_app",
    responder="api_server",
    roles=["client", "authenticated"],
    did_key=did,
    hid_key=hid
)

# Send intent
client.send_intent(
    fir_a_id=fir_a.id,
    intent="unlock_door",
    context={"location": "home", "verified": True}
)
```

## Production Deployment

### Systemd Service (Brain API)

Create `/etc/systemd/system/jtel-brain.service`:

```ini
[Unit]
Description=JTel Brain API - BETTI Coordination Engine
After=network.target postgresql.service

[Service]
Type=simple
User=jtel
Group=jtel
WorkingDirectory=/opt/jtel/brain_api
Environment="PATH=/opt/jtel/brain_api/.venv/bin"
ExecStart=/opt/jtel/brain_api/.venv/bin/uvicorn main:app \
    --host 0.0.0.0 \
    --port 8010 \
    --workers 4 \
    --log-config logging.json
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable jtel-brain
sudo systemctl start jtel-brain
sudo systemctl status jtel-brain
```

### Reverse Proxy (Nginx)

```nginx
# Brain API
upstream brain_api {
    server 127.0.0.1:8010;
}

server {
    listen 80;
    server_name brain.yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name brain.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/brain.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/brain.yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://brain_api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # WebSocket endpoint
    location /ws {
        proxy_pass http://brain_api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 86400;
    }
}

# JIS Router
server {
    listen 443 ssl http2;
    server_name jis.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/jis.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/jis.yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## BETTI Architecture

### 9 Natural Laws

The Brain API implements universal coordination through 9 natural laws:

1. **Pythagoras** - Dimensional structure mapping and geometric relationships
2. **Einstein** - Relativity of time and priority in distributed systems
3. **Euler** - Multi-path intent resolution and graph theory
4. **Fourier** - Pattern detection and signal transformation
5. **Maxwell** - Field theory for context propagation
6. **Schrödinger** - Superposition of intent states before execution
7. **TCP** - Reliable state transitions with error correction
8. **Thermodynamics** - Entropy management and system evolution
9. **Logarithms** - Complexity reduction and scaling

**Implementation:** `betti_endpoints.py` (52KB), `betti_complexity.py`

### Security Layers

Four-layer security architecture:

- **SNAFT** - Factory-level security firewall (pre-deployment validation)
- **BALANS** - Pre-execution decision engine with risk assessment
- **HICSS** - Human-in-Control Stop Switch for emergency override
- **Fail2Flag** - Automatic anomaly detection and flagging

**Implementation:** `betti_snaft.py`, `betti_balans.py`, `betti_hicss.py`, `betti_fail2flag.py`

### Context/Sense/Intent Layers

Three-layer decision architecture:

1. **Context Layer** - Environmental awareness, state tracking, user/device profiling
2. **Sense Layer** - Rule-based decision making (conditions → intents)
3. **Intent Layer** - Action execution, logging, and validation

**Flow:**
```
Input Context → Sense Rules Evaluation → Intent Generation →
BETTI Validation → Security Layers → Execution → Continuity Chain Update
```

### JIS Protocol Features

- **FIR/A (Flag/Identify/Request/Accept)** - Cryptographic relationship establishment
- **DID (Device Identity)** - Ed25519 key pairs for device authentication
- **HID (Human Identity)** - X25519 key pairs for human binding (never transmitted)
- **IFT (Intent-First Transmission)** - Semantic-first, payload-agnostic communication
- **NIR (Notify/Identify/Rectify)** - Three-phase error handling and recovery
- **Continuity Chains** - SHA-256 linked audit trail of all interactions

## Use Cases

### Robot Control

```python
# Industrial robot arm coordination
client.send_tibet(
    relationship_id=robot_rel.id,
    intent="pick_and_place",
    context={
        "object": "component_A",
        "from": {"x": 100, "y": 200, "z": 50},
        "to": {"x": 300, "y": 400, "z": 75},
        "force_limit": 50  # Newtons
    }
)
```

### Telephony Orchestration

```python
# Context-aware call routing
client.send_tibet(
    relationship_id=pbx_rel.id,
    intent="route_call",
    context={
        "caller": "+31612345678",
        "time": "09:30",
        "caller_history": "vip_customer",
        "route_to": "sales_team_priority_queue"
    }
)
```

### IoT Device Coordination

```python
# Smart home automation
client.send_tibet(
    relationship_id=home_rel.id,
    intent="adjust_environment",
    context={
        "room": "living_room",
        "temperature": 21.5,
        "lighting": "warm",
        "occupancy": True
    }
)
```

## Development Workflow

### Create Provisioning Code

```bash
curl -X POST http://localhost:8010/admin/users \
  -H "Content-Type: application/json" \
  -d '{
    "code": "ROBOT001",
    "username": "robot_arm_01",
    "display_name": "Factory Robot Arm 01",
    "role": "device",
    "team": "Production Floor"
  }'

# Response includes auto-assigned SIP extension (1050-1500)
```

### Add BETTI Sense Rule

```bash
curl -X POST http://localhost:8010/betti/sense/rules \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Production Hours Only",
    "conditions": {
      "time_range": ["06:00", "22:00"],
      "days": ["mon", "tue", "wed", "thu", "fri"]
    },
    "intent": "allow_robot_operation",
    "priority": 5,
    "enabled": true
  }'
```

### Monitor Intent Execution

```bash
# Recent intents
curl http://localhost:8010/betti/intent/history?limit=20

# User/device context
curl http://localhost:8010/betti/context/robot_arm_01

# Active WebSocket clients
curl http://localhost:8010/ws/clients
```

## Documentation

- **[GETTING-STARTED.md](GETTING-STARTED.md)** - Conceptual overview and philosophy
- **[SENSE-CONTEXT-INTENT-EXPLAINED.md](SENSE-CONTEXT-INTENT-EXPLAINED.md)** - Deep dive into BETTI layers
- **[INTEGRATION-ARCHITECTURE.md](INTEGRATION-ARCHITECTURE.md)** - System integration patterns
- **[TBET-BETTI-ARCHITECTURE.md](TBET-BETTI-ARCHITECTURE.md)** - TIBET-BETTI protocol specification
- **[VISION-UNIVERSAL-BETTI.md](VISION-UNIVERSAL-BETTI.md)** - Future vision and roadmap
- **[README-DOCS.md](README-DOCS.md)** - Complete documentation index

## Support & Community

- **GitHub**: https://github.com/jaspertvdm/JTel-identity-standard
- **Backend**: https://github.com/jaspertvdm/Backend-server-JTel
- **Issues**: Report bugs and feature requests via GitHub Issues
- **License**: See LICENSE.md for terms

## Credits

**JTel Identity Standard & BETTI Coordination System**

Designed and developed by **Jasper van de Meent**

- Architecture and implementation of BETTI 9 natural laws
- JIS protocol specification (FIR/A, DID/HID, IFT, NIR)
- Context/Sense/Intent decision layers
- TIBET-BETTI time-boxed intent coordination
- Security layers (SNAFT, BALANS, HICSS, Fail2Flag)
- Python SDKs and reference implementations

---

**Version**: 1.0.0
**Last Updated**: November 2025
**Status**: Production Ready
**Stack**: Python 3.11+ | FastAPI | PostgreSQL | Redis | MQTT | Docker
**License**: See LICENSE.md
