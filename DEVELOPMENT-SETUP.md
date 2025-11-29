# 🛠️ Development Setup: APP + BETTI Databases

**Complete development environment met beide databases apart**

---

## 🎯 Setup Overzicht

```
Development Environment:
├── APP Database (port 5432) - JOUW DB
├── BETTI Database (port 5433) - BETTI ROUTER DB
├── KIT API (port 8000) - JOUW API
└── BETTI Router (port 18081) - BETTI SERVICE
```

---

## 📦 Docker Compose Setup

### docker-compose.yml

```yaml
version: '3.8'

services:
  # ═══════════════════════════════════════════════════════════════
  # APP DATABASE - Jouw bestaande database
  # ═══════════════════════════════════════════════════════════════
  app-db:
    image: postgres:15
    container_name: my_app_db
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: my_app_db
      POSTGRES_USER: app_user
      POSTGRES_PASSWORD: your_app_password
      PGDATA: /var/lib/postgresql/data/pgdata
    volumes:
      - app-db-data:/var/lib/postgresql/data
      - ./migrations/app-db:/docker-entrypoint-initdb.d
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app_user -d my_app_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ═══════════════════════════════════════════════════════════════
  # BETTI DATABASE - Aparte database voor trust & routing
  # ═══════════════════════════════════════════════════════════════
  betti-db:
    image: postgres:15
    container_name: betti_router_db
    ports:
      - "5433:5432"  # Andere port!
    environment:
      POSTGRES_DB: betti_router_db
      POSTGRES_USER: betti_user
      POSTGRES_PASSWORD: your_betti_password
      PGDATA: /var/lib/postgresql/data/pgdata
    volumes:
      - betti-db-data:/var/lib/postgresql/data
      - ./migrations/betti-db:/docker-entrypoint-initdb.d
    networks:
      - betti-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U betti_user -d betti_router_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ═══════════════════════════════════════════════════════════════
  # KIT API - Jouw bestaande API
  # ═══════════════════════════════════════════════════════════════
  kit-api:
    build:
      context: ./kit-api
      dockerfile: Dockerfile
    container_name: kit_api
    ports:
      - "8000:8000"
    environment:
      # APP DATABASE CONNECTION
      DATABASE_URL: postgresql://app_user:your_app_password@app-db:5432/my_app_db

      # API Settings
      SECRET_KEY: example_secret_123
      ENVIRONMENT: development
      DEBUG: "true"

      # BETTI Integration
      BETTI_ROUTER_URL: http://betti-router:18081
    volumes:
      - ./kit-api:/app
      - kit-logs:/app/logs
    networks:
      - app-network
      - betti-network
    depends_on:
      app-db:
        condition: service_healthy
      betti-router:
        condition: service_healthy
    restart: unless-stopped

  # ═══════════════════════════════════════════════════════════════
  # BETTI ROUTER - Trust & Intent Router
  # ═══════════════════════════════════════════════════════════════
  betti-router:
    build:
      context: ./tbet-router
      dockerfile: Dockerfile
    container_name: betti_router
    ports:
      - "18081:18081"
    environment:
      # BETTI DATABASE CONNECTION
      DATABASE_URL: postgresql://betti_user:your_betti_password@betti-db:5432/betti_router_db

      # Router Settings
      SECRET: example_secret_123
      PORT: 18081
      NODE_ENV: development

      # Trust & Security
      MAX_CONVERSATION_DEPTH: 5
      DEFAULT_TIMEBOX_SECONDS: 30
      TRUST_TOKEN_EXPIRY_DAYS: 365
    volumes:
      - ./tbet-router:/app
      - betti-logs:/app/logs
    networks:
      - betti-network
    depends_on:
      betti-db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:18081/health"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # ═══════════════════════════════════════════════════════════════
  # DEVELOPMENT TOOLS (optional)
  # ═══════════════════════════════════════════════════════════════

  # pgAdmin - Database management UI
  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: pgadmin
    ports:
      - "5050:80"
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@localhost.com
      PGADMIN_DEFAULT_PASSWORD: admin
    volumes:
      - pgadmin-data:/var/lib/pgadmin
    networks:
      - app-network
      - betti-network
    depends_on:
      - app-db
      - betti-db

networks:
  app-network:
    driver: bridge
  betti-network:
    driver: bridge

volumes:
  app-db-data:
  betti-db-data:
  kit-logs:
  betti-logs:
  pgadmin-data:
```

---

## 🗄️ Database Migrations

### migrations/app-db/01_init.sql

```sql
-- APP DATABASE INITIALIZATION
-- Jouw bestaande schema

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    location VARCHAR(100),
    timezone VARCHAR(50) DEFAULT 'Europe/Amsterdam',
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Devices
CREATE TABLE devices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    device_type VARCHAR(50) NOT NULL,
    device_name VARCHAR(100),
    status VARCHAR(20) DEFAULT 'active',
    capabilities JSONB DEFAULT '[]',
    last_seen TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Settings
CREATE TABLE settings (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    category VARCHAR(50) NOT NULL,
    key VARCHAR(100) NOT NULL,
    value JSONB NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, category, key)
);

-- Sense Rules
CREATE TABLE sense_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    conditions JSONB NOT NULL,
    intent VARCHAR(100) NOT NULL,
    priority INTEGER DEFAULT 5,
    enabled BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- BETTI Integration (cache)
CREATE TABLE user_trust_tokens (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    device_id UUID REFERENCES devices(id) ON DELETE CASCADE,
    fira_id VARCHAR(255) NOT NULL,
    token_type VARCHAR(50) DEFAULT 'device_trust',
    created_at TIMESTAMP DEFAULT NOW(),
    last_used TIMESTAMP,
    UNIQUE(user_id, device_id)
);

-- BETTI Intent Log (your audit)
CREATE TABLE betti_intent_log (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    fira_id VARCHAR(255),
    intent VARCHAR(100) NOT NULL,
    context JSONB DEFAULT '{}',
    status VARCHAR(50) DEFAULT 'sent',
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_devices_user ON devices(user_id, status);
CREATE INDEX idx_sense_rules_user ON sense_rules(user_id, enabled, priority DESC);
CREATE INDEX idx_betti_log_user_time ON betti_intent_log(user_id, timestamp DESC);

-- Sample Data
INSERT INTO users (name, email, location) VALUES
('Test User', 'test@example.com', 'home'),
('Demo User', 'demo@example.com', 'work');

INSERT INTO sense_rules (name, conditions, intent, priority) VALUES
('Evening Lights', '{"location": "home", "time_of_day": "evening", "ambient_light": {"lt": 100}}'::jsonb, 'turn_on_lights', 7),
('Morning Routine', '{"location": "home", "time_of_day": "morning", "day_type": "weekday"}'::jsonb, 'morning_briefing', 8);
```

### migrations/betti-db/01_init.sql

```sql
-- BETTI DATABASE INITIALIZATION
-- Trust & Routing schema

-- FIR/A Relationships
CREATE TABLE fira_relationships (
    id VARCHAR(255) PRIMARY KEY,
    initiator VARCHAR(255) NOT NULL,
    responder VARCHAR(255) NOT NULL,
    roles JSONB DEFAULT '[]',
    trust_level INTEGER DEFAULT 1,
    continuity_hash VARCHAR(64) NOT NULL,
    context JSONB DEFAULT '{}',
    established_at TIMESTAMP DEFAULT NOW(),
    last_interaction TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'active'
);

-- Intent History
CREATE TABLE intent_history (
    id BIGSERIAL PRIMARY KEY,
    fira_id VARCHAR(255) REFERENCES fira_relationships(id) ON DELETE CASCADE,
    intent VARCHAR(100) NOT NULL,
    context JSONB DEFAULT '{}',
    timebox_seconds INTEGER NOT NULL,
    continuity_hash_prev VARCHAR(64),
    continuity_hash_new VARCHAR(64) NOT NULL,
    conversation_depth INTEGER DEFAULT 0,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Conversation State
CREATE TABLE conversation_state (
    id SERIAL PRIMARY KEY,
    fira_id VARCHAR(255) REFERENCES fira_relationships(id) ON DELETE CASCADE,
    conversation_id VARCHAR(255) NOT NULL,
    current_depth INTEGER DEFAULT 0,
    max_depth INTEGER DEFAULT 5,
    started_at TIMESTAMP DEFAULT NOW(),
    last_exchange TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    UNIQUE(fira_id, conversation_id)
);

-- Audit Log
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    fira_id VARCHAR(255) REFERENCES fira_relationships(id) ON DELETE SET NULL,
    event_type VARCHAR(100) NOT NULL,
    intent VARCHAR(100),
    humotica TEXT,
    context JSONB DEFAULT '{}',
    trust_level INTEGER,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Trust Tokens
CREATE TABLE trust_tokens (
    id SERIAL PRIMARY KEY,
    fira_id VARCHAR(255) UNIQUE REFERENCES fira_relationships(id) ON DELETE CASCADE,
    did_public TEXT,
    hid_did_binding TEXT,
    key_metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Continuity Chain
CREATE TABLE continuity_chain (
    id BIGSERIAL PRIMARY KEY,
    fira_id VARCHAR(255) REFERENCES fira_relationships(id) ON DELETE CASCADE,
    sequence_number INTEGER NOT NULL,
    hash_prev VARCHAR(64),
    hash_current VARCHAR(64) NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW(),
    UNIQUE(fira_id, sequence_number)
);

-- Indexes
CREATE INDEX idx_fira_parties ON fira_relationships(initiator, responder);
CREATE INDEX idx_fira_trust ON fira_relationships(trust_level, status);
CREATE INDEX idx_intent_fira_time ON intent_history(fira_id, timestamp DESC);
CREATE INDEX idx_intent_depth ON intent_history(conversation_depth, fira_id);
CREATE INDEX idx_conv_status ON conversation_state(status, expires_at);
CREATE INDEX idx_audit_fira_time ON audit_log(fira_id, timestamp DESC);
CREATE INDEX idx_audit_type ON audit_log(event_type, timestamp DESC);
CREATE INDEX idx_chain_fira ON continuity_chain(fira_id, sequence_number DESC);
```

---

## 🚀 Gebruik

### Start Everything

```bash
# Start alle services
docker-compose up -d

# Check status
docker-compose ps

# Logs bekijken
docker-compose logs -f kit-api
docker-compose logs -f betti-router
```

### Database Connections

```bash
# Connect to APP DB
psql postgresql://app_user:your_app_password@localhost:5432/my_app_db

# Connect to BETTI DB
psql postgresql://betti_user:your_betti_password@localhost:5433/betti_router_db

# Via pgAdmin
# Open: http://localhost:5050
# Login: admin@localhost.com / admin
```

### Test Setup

```python
# test_setup.py
from tibet_betti_client import TibetBettiClient
import psycopg2

def test_databases():
    """Test both databases are running"""

    # Test APP DB
    app_conn = psycopg2.connect(
        "postgresql://app_user:your_app_password@localhost:5432/my_app_db"
    )
    app_cursor = app_conn.cursor()
    app_cursor.execute("SELECT COUNT(*) FROM users")
    print(f"✓ APP DB: {app_cursor.fetchone()[0]} users")
    app_conn.close()

    # Test BETTI DB
    betti_conn = psycopg2.connect(
        "postgresql://betti_user:your_betti_password@localhost:5433/betti_router_db"
    )
    betti_cursor = betti_conn.cursor()
    betti_cursor.execute("SELECT COUNT(*) FROM fira_relationships")
    print(f"✓ BETTI DB: {betti_cursor.fetchone()[0]} relationships")
    betti_conn.close()

    # Test BETTI Router
    client = TibetBettiClient(
        betti_url="http://localhost:18081",
        kit_url="http://localhost:8000",
        secret="example_secret_123"
    )
    health = client.health_check()
    print(f"✓ BETTI Router: {health['status']}")

    # Test KIT API
    kit_health = client.kit_health_check()
    print(f"✓ KIT API: {kit_health.get('status', 'ok')}")

    print("\n🎉 All systems operational!")

if __name__ == "__main__":
    test_databases()
```

Run test:
```bash
python test_setup.py
```

---

## 🔧 Environment Variables

### .env file (voor development)

```bash
# APP DATABASE
APP_DATABASE_URL=postgresql://app_user:your_app_password@localhost:5432/my_app_db

# BETTI DATABASE
BETTI_DATABASE_URL=postgresql://betti_user:your_betti_password@localhost:5433/betti_router_db

# API URLs
KIT_API_URL=http://localhost:8000
BETTI_ROUTER_URL=http://localhost:18081

# Secrets
APP_SECRET_KEY=example_secret_123
BETTI_SECRET=example_secret_123

# Development
DEBUG=true
LOG_LEVEL=debug
```

### In je app code

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # APP DATABASE
    APP_DATABASE_URL = os.getenv('APP_DATABASE_URL')

    # BETTI Integration
    BETTI_ROUTER_URL = os.getenv('BETTI_ROUTER_URL')
    KIT_API_URL = os.getenv('KIT_API_URL')
    BETTI_SECRET = os.getenv('BETTI_SECRET')

# Usage
from config import Config
from sqlalchemy import create_engine

# APP DB connection
app_engine = create_engine(Config.APP_DATABASE_URL)

# BETTI SDK
from tibet_betti_client import TibetBettiClient
betti_client = TibetBettiClient(
    betti_url=Config.BETTI_ROUTER_URL,
    kit_url=Config.KIT_API_URL,
    secret=Config.BETTI_SECRET
)
```

---

## 📊 Monitoring

### Database Stats

```sql
-- APP DB: Check table sizes
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- BETTI DB: Check activity
SELECT
    COUNT(*) as total_relationships,
    COUNT(*) FILTER (WHERE status = 'active') as active,
    AVG(trust_level) as avg_trust
FROM fira_relationships;

SELECT
    COUNT(*) as total_intents,
    COUNT(DISTINCT fira_id) as unique_relationships,
    MAX(conversation_depth) as max_depth
FROM intent_history
WHERE timestamp > NOW() - INTERVAL '24 hours';
```

### Health Check Script

```bash
#!/bin/bash
# check_health.sh

echo "Checking system health..."

# APP DB
if psql postgresql://app_user:your_app_password@localhost:5432/my_app_db -c "SELECT 1" > /dev/null 2>&1; then
    echo "✓ APP DB: OK"
else
    echo "✗ APP DB: FAILED"
fi

# BETTI DB
if psql postgresql://betti_user:your_betti_password@localhost:5433/betti_router_db -c "SELECT 1" > /dev/null 2>&1; then
    echo "✓ BETTI DB: OK"
else
    echo "✗ BETTI DB: FAILED"
fi

# KIT API
if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
    echo "✓ KIT API: OK"
else
    echo "✗ KIT API: FAILED"
fi

# BETTI Router
if curl -sf http://localhost:18081/health > /dev/null 2>&1; then
    echo "✓ BETTI Router: OK"
else
    echo "✗ BETTI Router: FAILED"
fi
```

---

## 🎯 Development Workflow

### 1. Start Development Environment

```bash
# Clone repo
git clone your-repo
cd your-repo

# Start databases + services
docker-compose up -d

# Verify
python test_setup.py
```

### 2. Develop in Your App

```bash
# Work on your app (uses APP DB)
cd kit-api
python manage.py runserver  # or your dev command

# APP DB migrations
python manage.py makemigrations
python manage.py migrate
```

### 3. BETTI Integration

```python
# In your app code
from tibet_betti_client import TibetBettiClient

client = TibetBettiClient(
    betti_url="http://localhost:18081",
    kit_url="http://localhost:8000",
    secret="example_secret_123"
)

# Use it!
rel = client.establish_trust("app", "device")
client.send_tibet(rel.id, "intent", {...})
```

### 4. Stop Environment

```bash
# Stop all services (preserves data)
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v
```

---

## ✅ Checklist

- [ ] `docker-compose up -d` succeeds
- [ ] APP DB accessible on port 5432
- [ ] BETTI DB accessible on port 5433
- [ ] KIT API responds on port 8000
- [ ] BETTI Router responds on port 18081
- [ ] `python test_setup.py` passes
- [ ] Can connect via psql to both databases
- [ ] Can create FIR/A via SDK
- [ ] Can send TIBET intents
- [ ] Can query APP DB for sense rules
- [ ] Can query BETTI DB for audit trails

**Klaar voor ontwikkeling! Beide databases draaien apart en perfect! 🚀**
