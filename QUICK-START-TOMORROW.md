# QUICK START - Integreer TIBET-BETTI in je App MORGEN! 🚀

**Ready-to-use Python SDK voor jouw KIT API**

---

## ⚡ Installeer de SDK (5 minuten)

```bash
cd client-sdk/python/tibet_betti_client

# Optie 1: Installeer dependencies alleen
pip install -r requirements.txt

# Optie 2: Installeer als package (development mode)
pip install -e .
```

**Dependencies worden automatisch geïnstalleerd:**
- `requests` (voor HTTP)
- `websocket-client` (voor real-time)

### ✅ Test de Installatie

```bash
# Verifieer dat alles werkt
python test_installation.py
```

Je zou moeten zien:
```
🎉 SDK is ready to use!
```

### 🚀 Hello World Test

```bash
# Simpelste voorbeeld (vereist BETTI router running)
python examples/hello_world.py
```

---

## 🎯 Gebruik in je App

### 1. Basis Setup

```python
from tibet_betti_client import TibetBettiClient

# Initialize (verbind met BETTI router + jouw KIT API)
client = TibetBettiClient(
    betti_url="http://localhost:18081",  # BETTI router
    kit_url="http://localhost:8000",     # JOUW KIT API!
    secret="denDolder_2024!"
)

# Check of alles werkt
health = client.health_check()  # BETTI router
kit_health = client.kit_health_check()  # Jouw KIT API
print(f"✓ BETTI: {health['status']}")
print(f"✓ KIT: {kit_health['status']}")
```

### 2. Establish Trust (Eénmalig per Relatie)

```python
# User's app ←→ User's AI assistant
relationship = client.establish_trust(
    initiator="user_app",
    responder="ai_assistant",
    trust_level=2,
    context={"user_id": "user_123"}
)

# Bewaar relationship.id voor hergebruik!
relationship_id = relationship.id
```

### 3. Send TIBET Intents

```python
# Basic intent
client.send_tibet(
    relationship_id=relationship_id,
    intent="turn_on_lights",
    context={"room": "living_room", "brightness": 80}
)

# Met time window
from tibet_betti_client import TimeWindow

client.send_tibet(
    relationship_id=relationship_id,
    intent="schedule_meeting",
    context={"attendees": 5, "duration": 60},
    time_window=TimeWindow.from_now(hours=24)  # Binnen 24u
)
```

### 4. Gebruik JOUW KIT API Endpoints

**De SDK integreert direct met jouw bestaande endpoints!**

```python
# POST /context/update
client.update_context(
    user_id="user_123",
    context_data={
        "location": "home",
        "time_of_day": "evening",
        "activity": "relaxing"
    }
)

# GET /context/{user_id}
context = client.get_context("user_123")
print(context.data)  # {"location": "home", ...}

# POST /sense/rules
rule = client.create_sense_rule(
    name="evening_lights",
    conditions={
        "time_of_day": "evening",
        "location": "home",
        "ambient_light": {"lt": 100}
    },
    intent="turn_on_lights",
    priority=7
)

# POST /sense/evaluate
triggered_intents = client.evaluate_sense("user_123")
print(triggered_intents)  # ["turn_on_lights", "set_temperature"]
```

### 5. DE MAGIE: Context → Sense → TIBET (Automatisch!)

**Dit is de killer feature voor jouw app:**

```python
# User arrives home (of willekeurige context update)
results = client.context_to_tibet(
    relationship_id=relationship_id,
    user_id="user_123",
    context_update={
        "location": "home",
        "time_of_day": "evening",
        "ambient_light": 50
    }
)

# Automatisch gebeurt:
# 1. Context updated in KIT (/context/update)
# 2. Sense rules evaluated (/sense/evaluate)
# 3. Matched intents → TIBET verzonden!
#    → turn_on_lights (matched evening + home + low light)
#    → set_temperature (matched home)
#    → start_music (matched evening + home)

print(f"{len(results)} TIBETs automatically sent!")
```

### 6. WebSocket (Real-Time Updates)

```python
# WS /ws/{user_id}
def handle_message(msg):
    print(f"Received: {msg['type']}")

def handle_tibet(tibet_data):
    intent = tibet_data['intent']
    print(f"TIBET: {intent}")
    # Handle intent in your app

ws = client.connect_websocket(
    user_id="user_123",
    on_message=handle_message,
    on_tibet=handle_tibet
)

# Start in background
ws.start(block=False)

# Your app continues running...

# Close when done
ws.close()
```

---

## 🎨 Voorbeeld Use Cases voor JOUW App

### Use Case 1: AI Assistant met Context

```python
# AI krijgt intent van user
user_says = "Schedule a meeting with the team tomorrow morning"

# Update context (AI interpreteert)
client.update_context(
    user_id="user_123",
    context_data={
        "intent": "schedule_meeting",
        "attendees": ["team"],
        "time_preference": "morning",
        "date_preference": "tomorrow"
    }
)

# Sense rule triggert automatisch "schedule_meeting" intent
# TIBET wordt verzonden met volledige context
# BETTI routeert naar calendar service
# Done!
```

### Use Case 2: Smart Home Automation

```python
# Sense rules voor verschillende scenarios
rules = [
    {
        "name": "morning_routine",
        "conditions": {
            "time_of_day": "morning",
            "location": "home",
            "weekday": True
        },
        "intent": "morning_routine"
    },
    {
        "name": "leaving_home",
        "conditions": {
            "location": "leaving",
            "previous_location": "home"
        },
        "intent": "secure_home"
    },
    {
        "name": "arriving_home",
        "conditions": {
            "location": "home",
            "time_of_day": "evening"
        },
        "intent": "welcome_home"
    }
]

# Create all rules
for rule_data in rules:
    client.create_sense_rule(**rule_data)

# Now, any context update automatically triggers intents!
client.context_to_tibet(
    relationship_id=home_rel.id,
    user_id="user_123",
    context_update={"location": "home", "time_of_day": "evening"}
)
# → welcome_home TIBET sent automatically!
```

### Use Case 3: AI-Driven Task Automation

```python
# AI analyzes user patterns and creates sense rules
client.create_sense_rule(
    name="low_battery_charge",
    conditions={
        "device": "phone",
        "battery_level": {"lt": 20},
        "location": "home"
    },
    intent="remind_charge_phone"
)

# Context update triggers reminder
client.update_context(
    user_id="user_123",
    context_data={"battery_level": 15, "location": "home"}
)
# → remind_charge_phone TIBET sent!
```

---

## 🔥 Integration Checklist

### Stap 1: Installeer SDK
- [ ] `pip install -e client-sdk/python/tibet_betti_client`

### Stap 2: Initialize Client
```python
from tibet_betti_client import TibetBettiClient

client = TibetBettiClient(
    betti_url="http://localhost:18081",
    kit_url="http://localhost:8000",  # Jouw API!
    secret="denDolder_2024!"
)
```

### Stap 3: Establish Trust Relationships
```python
# Voor elke user/device combinatie
rel = client.establish_trust("user_app", "ai_assistant")
# Bewaar rel.id in database!
```

### Stap 4: Gebruik Bestaande KIT Endpoints
```python
# POST /context/update
client.update_context(user_id, context_data)

# POST /sense/rules
client.create_sense_rule(name, conditions, intent)

# POST /sense/evaluate
client.evaluate_sense(user_id)
```

### Stap 5: Gebruik Combined Flow
```python
# De magie: Context → Sense → TIBET
results = client.context_to_tibet(
    relationship_id=rel.id,
    user_id=user_id,
    context_update=new_context
)
```

### Stap 6: WebSocket voor Real-Time
```python
ws = client.connect_websocket(user_id, on_message, on_tibet)
ws.start(block=False)
```

---

## 💡 Belangrijke Concepten

### Trust Tokens = "Wij Kennen Elkaar"

```python
# Eenmalig establish
rel = client.establish_trust("app", "device")

# Daarna altijd hergebruiken
client.send_tibet(rel.id, "intent_1", {...})
client.send_tibet(rel.id, "intent_2", {...})
client.send_tibet(rel.id, "intent_3", {...})

# Relationship heeft historie, context, continuity!
```

### Time Windows = Wanneer mag het?

```python
from tibet_betti_client import TimeWindow

# Nu (30 sec)
TimeWindow.immediate()

# Binnen X tijd
TimeWindow.from_now(hours=2)
TimeWindow.from_now(minutes=30)

# Gepland
from datetime import datetime
start = datetime(2025, 11, 28, 14, 30)
TimeWindow.scheduled(start, duration_minutes=60)
```

### Constraints = Hoe safe?

```python
from tibet_betti_client import Constraints

constraints = Constraints(
    max_retries=3,              # Max 3 pogingen
    max_duration_seconds=300,   # Max 5 min
    safe_fail_action="notify_user",  # Bij error: notify
    priority=7                  # Priority 7/10
)
```

### Context Matching = Automatisch triggeren

```python
# Sense rule conditions
conditions = {
    "location": "home",              # Exact match
    "temperature": {"lt": 18},       # Less than
    "battery": {"gte": 30},          # Greater than or equal
    "time_of_day": {"in": ["morning", "evening"]}  # In list
}

# Automatisch triggered als context matches!
```

---

## 🚀 Run de Complete Example

```bash
cd client-sdk/python/tibet_betti_client
python examples/complete_example.py
```

Dit test:
- ✅ BETTI router connectie
- ✅ KIT API connectie
- ✅ Trust establishment
- ✅ TIBET intents
- ✅ Context updates
- ✅ Sense rules
- ✅ Combined flow
- ✅ WebSocket

---

## 📞 Troubleshooting

### Import Error

```python
# Als import fails:
import sys
sys.path.insert(0, 'path/to/client-sdk/python')
from tibet_betti_client import TibetBettiClient
```

### Connection Error

```bash
# Check BETTI router draait
curl http://localhost:18081/health

# Check KIT API draait
curl http://localhost:8000/health
```

### WebSocket Error

```bash
# Install websocket-client
pip install websocket-client
```

---

## 🎯 Klaar voor Morgen!

**Je hebt nu:**
- ✅ Complete TIBET-BETTI SDK
- ✅ Integratie met jouw KIT API
- ✅ Trust token management
- ✅ Context → Sense → TIBET flow
- ✅ WebSocket real-time
- ✅ Working examples
- ✅ Complete docs

**Morgen in je app:**

```python
from tibet_betti_client import TibetBettiClient

client = TibetBettiClient(
    betti_url="http://localhost:18081",
    kit_url="http://localhost:8000",
    secret="denDolder_2024!"
)

# Establish trust once
rel = client.establish_trust("my_app", "user_device")

# Use everywhere
client.context_to_tibet(
    relationship_id=rel.id,
    user_id="user_123",
    context_update=new_context
)

# Magic happens! 🎉
```

---

**TIBET declares. BETTI coordinates. Your KIT API automates. 🚀**

**Succes morgen!** 🔥
