# JIS Router - Production Deployment Guide

Complete gids voor het deployen van de JIS Router in productie.

## 📋 Inhoud

- [Quick Start](#quick-start)
- [Productie Configuratie](#productie-configuratie)
- [Security Hardening](#security-hardening)
- [Monitoring](#monitoring)
- [Backup & Recovery](#backup--recovery)
- [Scaling](#scaling)
- [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Vereisten

- Docker 24.0+ met Compose V2
- 2GB+ RAM beschikbaar
- Linux/macOS/Windows met WSL2

### Basis Deployment

```bash
cd server-config/jis-test

# 1. Configureer environment
cp .env.example .env
nano .env  # Pas secrets aan!

# 2. Start de stack
docker compose up -d

# 3. Controleer status
docker compose ps
docker compose logs -f router

# 4. Test de setup
curl http://localhost:18081/health/ready
```

### Admin UI Toegang

Open browser: `http://localhost:18081/`

Login met de `JIS_SHARED_SECRET` uit je `.env` file.

---

## 🔧 Productie Configuratie

### Environment Variables

Verplicht aan te passen in `.env`:

```bash
# Database - gebruik sterke wachtwoorden!
POSTGRES_PASSWORD=<genereer-sterk-wachtwoord>

# Router Security
JIS_SHARED_SECRET=<genereer-sterke-secret>  # min. 32 chars
JWT_SECRET=<optioneel-voor-jwt-auth>        # voor Bearer tokens

# Rate Limiting (aanpassen naar je load)
RATE_LIMIT=100
RATE_WINDOW=60

# Whitelists voor productie
ALLOWED_INTENTS=unlock_door,verify_identity,send_message
ALLOWED_ROLES=client,server,device,admin
```

### Genereren van Secrets

```bash
# Sterke random secret genereren
openssl rand -base64 32

# Of met Python
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### JWT Authentication (Optioneel)

Voor productie is JWT aangeraden boven shared secret:

```bash
# 1. Genereer JWT secret
JWT_SECRET=$(openssl rand -base64 64)

# 2. Configureer in .env
echo "JWT_SECRET=$JWT_SECRET" >> .env
echo "JWT_AUDIENCE=jis-router" >> .env
echo "JWT_ISSUER=jis-production" >> .env

# 3. Genereer tokens voor clients
python3 << EOF
import jwt
import datetime

secret = "$JWT_SECRET"
token = jwt.encode({
    "sub": "client-app",
    "aud": "jis-router",
    "iss": "jis-production",
    "exp": datetime.datetime.utcnow() + datetime.timedelta(days=365)
}, secret, algorithm="HS256")

print(f"Authorization: Bearer {token}")
EOF
```

---

## 🔒 Security Hardening

### 1. TLS/HTTPS Setup

Voor productie draai achter een reverse proxy (Nginx/Traefik):

```nginx
# nginx.conf voorbeeld
upstream jis_router {
    server localhost:18081;
}

server {
    listen 443 ssl http2;
    server_name jis.example.com;

    ssl_certificate /etc/letsencrypt/live/jis.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/jis.example.com/privkey.pem;

    location / {
        proxy_pass http://jis_router;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 2. mTLS (Mutual TLS)

Voor service-to-service authenticatie:

```bash
# Genereer CA en certificaten
openssl req -x509 -newkey rsa:4096 -keyout ca-key.pem -out ca-cert.pem -days 365 -nodes

# Mount in docker-compose.yml
volumes:
  - ./certs:/app/certs:ro

environment:
  TLS_CERT_FILE: /app/certs/server-cert.pem
  TLS_KEY_FILE: /app/certs/server-key.pem
  TLS_CA_FILE: /app/certs/ca-cert.pem
  TLS_REQUIRE_CLIENT_CERT: "true"
```

### 3. Network Isolation

```yaml
# docker-compose.yml - voeg netwerken toe
networks:
  backend:
    internal: true  # Geen internet toegang
  frontend:

services:
  db:
    networks:
      - backend  # Alleen intern toegankelijk

  router:
    networks:
      - backend
      - frontend  # Publiek toegankelijk
```

### 4. Firewall Rules

```bash
# UFW voorbeeld
ufw allow 18081/tcp  # Router
ufw allow 443/tcp    # HTTPS via nginx
ufw deny 55433/tcp   # Postgres niet publiek!
ufw deny 36381/tcp   # Redis niet publiek!
```

---

## 📊 Monitoring

### Health Checks

```bash
# Liveness (is de app running?)
curl http://localhost:18081/health/live

# Readiness (kan de app traffic aan?)
curl http://localhost:18081/health/ready

# Metrics
curl http://localhost:18081/metrics
```

### Prometheus Integration

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'jis-router'
    static_configs:
      - targets: ['router:8081']
    metrics_path: '/metrics'
```

### Logging

Logs bekijken:

```bash
# Alle services
docker compose logs -f

# Alleen router
docker compose logs -f router

# Met timestamps en laatste 100 regels
docker compose logs --tail=100 -t router
```

Logs naar file:

```bash
# In docker-compose.yml
services:
  router:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Alerting

Basis health check monitoring:

```bash
#!/bin/bash
# healthcheck.sh - draai via cron elke 5 min

HEALTH=$(curl -s http://localhost:18081/health/ready | jq -r .status)

if [ "$HEALTH" != "ready" ]; then
    echo "JIS Router is NOT READY!" | mail -s "JIS Alert" admin@example.com
fi
```

---

## 💾 Backup & Recovery

### Database Backups

Automatische backups:

```bash
#!/bin/bash
# backup.sh - draai via cron dagelijks

BACKUP_DIR="/backups/jis"
DATE=$(date +%Y%m%d_%H%M%S)

docker compose exec -T db pg_dump -U jis jis > "$BACKUP_DIR/jis_$DATE.sql"

# Houd laatste 7 dagen
find $BACKUP_DIR -name "jis_*.sql" -mtime +7 -delete
```

Recovery:

```bash
# Restore vanuit backup
docker compose exec -T db psql -U jis jis < /backups/jis/jis_20250126_120000.sql
```

### Volume Backups

```bash
# Backup persistent volume
docker run --rm \
  -v jis-test_postgres_data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/postgres_volume_$(date +%Y%m%d).tar.gz -C /data .

# Restore
docker run --rm \
  -v jis-test_postgres_data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar xzf /backup/postgres_volume_20250126.tar.gz -C /data
```

---

## 📈 Scaling

### Horizontal Scaling (Meerdere Routers)

```yaml
# docker-compose.yml
services:
  router:
    deploy:
      replicas: 3  # 3 router instances

  nginx:
    # Load balancer
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    ports:
      - "443:443"
```

Load balancer config:

```nginx
upstream jis_routers {
    least_conn;
    server router_1:8081;
    server router_2:8081;
    server router_3:8081;
}
```

### Database Scaling

Voor high load:

1. **PostgreSQL replicatie** (read replicas)
2. **Connection pooling** via PgBouncer
3. **Partitionering** van events table per maand

```sql
-- Voorbeeld partitionering
CREATE TABLE events_2025_01 PARTITION OF events
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
```

### Redis Clustering

Voor high availability:

```yaml
services:
  redis-master:
    image: redis:7-alpine

  redis-replica-1:
    image: redis:7-alpine
    command: redis-server --slaveof redis-master 6379

  redis-sentinel:
    image: redis:7-alpine
    command: redis-sentinel /etc/sentinel.conf
```

---

## 🔍 Troubleshooting

### Veelvoorkomende Problemen

#### Router start niet

```bash
# Check logs
docker compose logs router

# Vaak: database nog niet ready
# Oplossing: wacht op healthcheck
docker compose up -d  # health checks zorgen voor juiste volgorde
```

#### Database connectie fails

```bash
# Test handmatig
docker compose exec db psql -U jis -d jis -c "SELECT 1;"

# Check network
docker compose exec router ping db
```

#### Hoge CPU/Memory

```bash
# Resource usage bekijken
docker stats

# Logs naar disk i.p.v. stdout
# Rate limiting verhogen
# Connection pool grootte aanpassen
```

#### Continuity Hash Mismatches

```bash
# Check event chain
curl -H "X-JIS-SECRET: $SECRET" \
  http://localhost:18081/relation/$FIR_A_ID/events | jq

# Laatste hash opvragen
curl -H "X-JIS-SECRET: $SECRET" \
  http://localhost:18081/relation/$FIR_A_ID | jq .continuity_hash
```

### Debug Mode

```yaml
# docker-compose.yml
services:
  router:
    environment:
      LOG_LEVEL: DEBUG  # Meer verbose logging
    command: python main.py --reload  # Auto-reload bij code changes
```

### Performance Tuning

```bash
# PostgreSQL tuning
docker compose exec db psql -U jis -d jis -c "
  ALTER SYSTEM SET shared_buffers = '256MB';
  ALTER SYSTEM SET effective_cache_size = '1GB';
  ALTER SYSTEM SET maintenance_work_mem = '64MB';
"

docker compose restart db
```

---

## 📝 Maintenance

### Updates

```bash
# Pull nieuwe images
docker compose pull

# Rebuild services
docker compose build --no-cache

# Rolling update (zero downtime met replicas)
docker compose up -d --no-deps --build router
```

### Database Migrations

Nieuwe migratie toevoegen:

```bash
# 1. Maak nieuwe SQL file
cat > router/migrations/002_add_indexes.sql << EOF
-- Migration 002: Add performance indexes
CREATE INDEX IF NOT EXISTS idx_events_payload_type ON events((payload->>'type'));

INSERT INTO schema_migrations (version, description)
VALUES (2, 'Add payload type index')
ON CONFLICT (version) DO NOTHING;
EOF

# 2. Restart router (migraties draaien bij startup)
docker compose restart router
```

### Cleanup

```bash
# Verwijder oude images
docker image prune -a

# Verwijder oude logs (ouder dan 30 dagen)
find /var/lib/docker/containers -name "*.log" -mtime +30 -delete

# Database VACUUM (wekelijks)
docker compose exec db psql -U jis -d jis -c "VACUUM ANALYZE events;"
```

---

## 🎯 Production Checklist

Voor go-live:

- [ ] Sterke secrets gegenereerd en in `.env` gezet
- [ ] JWT auth geconfigureerd (niet shared secret)
- [ ] TLS/HTTPS via reverse proxy
- [ ] ALLOWED_INTENTS en ALLOWED_ROLES whitelists ingesteld
- [ ] Rate limiting aangepast aan verwachte load
- [ ] Database backups ingericht (dagelijks)
- [ ] Monitoring en alerting actief
- [ ] Logs naar centraal systeem (ELK/Splunk)
- [ ] Firewall rules ingesteld
- [ ] Network segmentatie (db/redis niet publiek)
- [ ] Health checks getest
- [ ] Disaster recovery plan gedocumenteerd
- [ ] Admin UI alleen toegankelijk via VPN/whitelist

---

## 📚 Extra Resources

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [PostgreSQL Performance Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [Prometheus Monitoring](https://prometheus.io/docs/introduction/overview/)

---

**Support:** Voor vragen, zie de main README of open een issue op GitHub.
