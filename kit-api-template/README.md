# 🔧 KIT API Template

**Complete FastAPI template voor TIBET-BETTI integratie**

Dit is de API layer tussen jouw APP DB en BETTI Router.
Implementeert Context, Sense en Intent layers.

---

## 🚀 Quick Start

### 1. Installeer Dependencies

```bash
cd kit-api-template
pip install -r requirements.txt
```

### 2. Start de API

```bash
python main.py
```

API draait op: http://localhost:8000

### 3. Test de Endpoints

```bash
# Health check
curl http://localhost:8000/health

# View all endpoints
curl http://localhost:8000/
```

---

## 📋 Endpoints

### Context Layer

#### POST /context/update
Update user context en optioneel trigger sense evaluation

```bash
curl -X POST http://localhost:8000/context/update \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "context": {
      "location": "home",
      "time_of_day": "evening",
      "ambient_light": 50
    },
    "evaluate_sense": true
  }'
```

**Response:**
```json
{
  "status": "updated",
  "context": {
    "user_id": "user_123",
    "location": "home",
    "time_of_day": "evening",
    "ambient_light": 50,
    "timestamp": "2025-11-27T10:00:00Z"
  },
  "triggered_intents": ["turn_on_lights"]
}
```

#### GET /context/{user_id}
Get current context for user

```bash
curl http://localhost:8000/context/user_123
```

---

### Sense Layer

#### POST /sense/rules
Create a new sense rule

```bash
curl -X POST http://localhost:8000/sense/rules \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Evening Lights",
    "conditions": {
      "location": "home",
      "time_of_day": "evening",
      "ambient_light": {"lt": 100}
    },
    "intent": "turn_on_lights",
    "priority": 7
  }'
```

#### GET /sense/rules
List all sense rules

```bash
curl http://localhost:8000/sense/rules
curl http://localhost:8000/sense/rules?user_id=user_123
```

#### POST /sense/evaluate
Evaluate sense rules for context

```bash
curl -X POST http://localhost:8000/sense/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "context": {
      "location": "home",
      "time_of_day": "evening",
      "ambient_light": 50
    }
  }'
```

**Response:**
```json
{
  "user_id": "user_123",
  "triggered_intents": ["turn_on_lights", "set_temperature"],
  "context": {...}
}
```

---

### Intent Layer

#### POST /intents/execute
Execute an intent

```bash
curl -X POST http://localhost:8000/intents/execute \
  -H "Content-Type: application/json" \
  -d '{
    "intent": "turn_on_lights",
    "context": {
      "room": "living_room",
      "brightness": 80
    },
    "fira_id": "fira-abc-123",
    "user_id": "user_123"
  }'
```

**Response:**
```json
{
  "status": "completed",
  "intent": "turn_on_lights",
  "room": "living_room",
  "brightness": 80,
  "message": "Lights in living_room turned on"
}
```

---

### WebSocket

#### WS /ws/{user_id}
WebSocket connection for real-time updates

```javascript
// JavaScript example
const ws = new WebSocket('ws://localhost:8000/ws/user_123');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);

  if (data.type === 'intent_executed') {
    console.log('Intent executed:', data.intent);
    console.log('Result:', data.result);
  }
};
```

```python
# Python example
from tibet_betti_client import TibetWebSocket

ws = TibetWebSocket(
    url="ws://localhost:8000/ws/user_123",
    on_message=lambda msg: print(f"Received: {msg}")
)
ws.start()
```

---

## 🔧 Aanpassen voor Jouw App

### 1. Database Integratie

**Vervang in-memory storage met jouw database:**

```python
# Huidige (demo):
context_store: Dict[str, Dict] = {}

# Vervang met:
from your_app.database import db, User, Device

# In get_context():
user = db.query(User).filter_by(id=user_id).first()
devices = db.query(Device).filter_by(user_id=user_id).all()
```

### 2. Sense Rules in Database

```python
# Vervang list met database query:
from your_app.models import SenseRule

sense_rules = db.query(SenseRule)\
    .filter((SenseRule.user_id == user_id) | (SenseRule.user_id.is_(None)))\
    .order_by(SenseRule.priority.desc())\
    .all()
```

### 3. Intent Handlers

Voeg je eigen intent handlers toe:

```python
@app.post("/intents/execute")
async def execute_intent(req: IntentExecute):
    if req.intent == "your_custom_intent":
        return await execute_your_custom_intent(req.context, req.user_id)
    # ... existing handlers

async def execute_your_custom_intent(context: Dict, user_id: str):
    # Jouw business logic hier
    # Update jouw database
    # Return result
    return {
        "status": "completed",
        "message": "Custom intent executed"
    }
```

---

## 📊 Built-in Intents

De template bevat voorbeelden voor:

1. **turn_on_lights** - Smart lighting control
   ```json
   {
     "intent": "turn_on_lights",
     "context": {"room": "living_room", "brightness": 80}
   }
   ```

2. **maak_koffie** - Coffee machine
   ```json
   {
     "intent": "maak_koffie",
     "context": {"type": "cappuccino", "size": "groot"}
   }
   ```

3. **schedule_meeting** - Calendar integration
   ```json
   {
     "intent": "schedule_meeting",
     "context": {"attendees": 5, "time": "morning"}
   }
   ```

4. **morning_briefing** - AI briefing
   ```json
   {
     "intent": "morning_briefing",
     "context": {}
   }
   ```

---

## 🔄 Complete Flow Test

```bash
# 1. Update context
curl -X POST http://localhost:8000/context/update \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "context": {"location": "home", "time_of_day": "evening", "ambient_light": 50},
    "evaluate_sense": true
  }'

# Response shows triggered intents:
# {"triggered_intents": ["turn_on_lights"]}

# 2. Execute intent (usually done by BETTI Router)
curl -X POST http://localhost:8000/intents/execute \
  -H "Content-Type: application/json" \
  -d '{
    "intent": "turn_on_lights",
    "context": {"room": "living_room", "brightness": 80},
    "fira_id": "test-fira",
    "user_id": "user_123"
  }'

# Response:
# {"status": "completed", "message": "Lights in living_room turned on"}
```

---

## 🧪 Testing

### Test Sense Rule Matching

```python
# Test script
import requests

# Create rule
requests.post('http://localhost:8000/sense/rules', json={
    "name": "Test Rule",
    "conditions": {"location": "home", "time": "evening"},
    "intent": "test_intent",
    "priority": 5
})

# Test evaluation
result = requests.post('http://localhost:8000/sense/evaluate', json={
    "user_id": "test_user",
    "context": {"location": "home", "time": "evening"}
})

print(result.json())
# Should show: {"triggered_intents": ["test_intent"]}
```

### Test with TIBET-BETTI SDK

```python
from tibet_betti_client import TibetBettiClient

client = TibetBettiClient(
    betti_url="http://localhost:18081",
    kit_url="http://localhost:8000",
    secret="denDolder_2024!"
)

# Test complete flow
rel = client.establish_trust("test_client", "test_server")

results = client.context_to_tibet(
    relationship_id=rel.id,
    user_id="user_123",
    context_update={
        "location": "home",
        "time_of_day": "evening",
        "ambient_light": 50
    }
)

print(f"Triggered {len(results)} TIBETs")
```

---

## 🔐 Security

### Add Authentication

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(credentials = Depends(security)):
    # Implement your JWT verification
    token = credentials.credentials
    # Verify token...
    return user_id

@app.post("/context/update")
async def update_context(req: ContextUpdate, user_id = Depends(verify_token)):
    # Now authenticated!
    pass
```

### Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/context/update")
@limiter.limit("10/minute")
async def update_context(request: Request, req: ContextUpdate):
    pass
```

---

## 📈 Production Deployment

### Environment Variables

```bash
# .env
DATABASE_URL=postgresql://user:pass@localhost/mydb
REDIS_URL=redis://localhost:6379
BETTI_ROUTER_URL=http://localhost:18081
LOG_LEVEL=INFO
```

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t kit-api .
docker run -p 8000:8000 kit-api
```

---

## 📚 Documentatie

### Interactive API Docs

FastAPI genereert automatisch API documentatie:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Zie Ook

- **[SENSE-CONTEXT-INTENT-EXPLAINED.md](../SENSE-CONTEXT-INTENT-EXPLAINED.md)** - Complete uitleg
- **[INTEGRATION-ARCHITECTURE.md](../INTEGRATION-ARCHITECTURE.md)** - Architectuur
- **[DATABASE-SCHEMAS.md](../DATABASE-SCHEMAS.md)** - Database design

---

## ✅ Checklist

- [ ] Dependencies geïnstalleerd
- [ ] API start zonder errors
- [ ] Database connectie geconfigureerd
- [ ] Sense rules aangepast voor jouw use case
- [ ] Intent handlers geïmplementeerd
- [ ] WebSocket connectie getest
- [ ] Geïntegreerd met TIBET-BETTI SDK
- [ ] Logging geconfigureerd
- [ ] Security toegevoegd (auth, rate limiting)
- [ ] Production deployment voorbereid

---

**KIT API: De brug tussen jouw app en TIBET-BETTI! 🌉**
