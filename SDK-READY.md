# ✅ TIBET-BETTI Python SDK - READY TO USE!

**Status:** Production-ready and tested ✓

## 🚀 Start in 3 Stappen

### Stap 1: Installeer (2 minuten)

```bash
cd client-sdk/python/tibet_betti_client
pip install -r requirements.txt
```

### Stap 2: Test (30 seconden)

```bash
python test_installation.py
```

Verwachte output:
```
🎉 SDK is ready to use!
```

### Stap 3: Gebruik in je App

```python
from tibet_betti_client import TibetBettiClient

# Initialize
client = TibetBettiClient(
    betti_url="http://localhost:18081",  # BETTI router
    kit_url="http://localhost:8000",      # JOUW KIT API!
    secret="denDolder_2024!"
)

# Establish trust (eenmalig per relatie)
rel = client.establish_trust("my_app", "user_device")

# DE MAGIE: Context → Sense → TIBET (automatisch!)
results = client.context_to_tibet(
    relationship_id=rel.id,
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

print(f"{len(results)} TIBETs automatically sent!")
```

## 📚 Documentatie Locaties

1. **Quick Start Guide:** `QUICK-START-TOMORROW.md`
2. **Complete README:** `client-sdk/python/tibet_betti_client/README.md`
3. **Hello World:** `client-sdk/python/tibet_betti_client/examples/hello_world.py`
4. **Complete Example:** `client-sdk/python/tibet_betti_client/examples/complete_example.py`

## 🔥 Wat je KRIJGT

✅ **Complete TIBET-BETTI SDK**
- Trust token management (FIR/A)
- Time-windowed intents (TIBET)
- Loop prevention built-in
- Full audit trails (humotica)

✅ **Directe KIT API Integratie**
- POST /context/update → `client.update_context()`
- GET /context/{user_id} → `client.get_context()`
- POST /sense/rules → `client.create_sense_rule()`
- POST /sense/evaluate → `client.evaluate_sense()`
- WS /ws/{user_id} → `client.connect_websocket()`

✅ **Magic Combined Flow**
- `client.context_to_tibet()` - Context → Sense → TIBET automatic!

✅ **Production Ready**
- No crypto dependencies required for basic use
- Comprehensive error handling
- Tested and validated
- Ready for immediate integration

## 🎯 Belangrijkste Features

### Trust Tokens ("Wij Kennen Elkaar")

```python
# Establish relationship once
rel = client.establish_trust("app", "device")

# Use many times - relationship has history!
client.send_tibet(rel.id, "intent_1", {...})
client.send_tibet(rel.id, "intent_2", {...})
client.send_tibet(rel.id, "intent_3", {...})
```

### Time Windows

```python
from tibet_betti_client import TimeWindow

# Immediate (30 sec)
TimeWindow.immediate()

# Next X hours/minutes
TimeWindow.from_now(hours=2)
TimeWindow.from_now(minutes=30)

# Scheduled
TimeWindow.scheduled(start_datetime, duration_minutes=60)
```

### Sense Rules (Auto-Trigger)

```python
# Create rule
client.create_sense_rule(
    name="evening_lights",
    conditions={
        "time_of_day": "evening",
        "location": "home",
        "ambient_light": {"lt": 100}
    },
    intent="turn_on_lights",
    priority=7
)

# Context update automatically triggers!
client.context_to_tibet(
    relationship_id=rel.id,
    user_id="user_123",
    context_update={"location": "home", "time_of_day": "evening"}
)
# → turn_on_lights TIBET automatically sent!
```

## 🔧 Requirements

- Python 3.8+
- BETTI Router running (http://localhost:18081)
- Your KIT API running (http://localhost:8000)

## 💡 Use Cases

### Smart Home
```python
# User arrives home → automatic welcome sequence
client.context_to_tibet(
    rel.id,
    "user_123",
    {"location": "home", "time": "evening"}
)
# → Automatically triggers: lights, heating, music!
```

### AI Assistant
```python
# AI sends intent with full context
client.send_tibet(
    rel.id,
    "schedule_meeting",
    context={"attendees": 5, "time": "morning"},
    humotica="User requested team meeting, preferably morning"
)
```

### IoT Automation
```python
# Device state change → automatic actions
client.context_to_tibet(
    rel.id,
    "device_123",
    {"battery_level": 15, "location": "home"}
)
# → Triggers: charging reminder!
```

## 🎉 KLAAR!

De SDK is volledig getest en klaar voor gebruik. Je kan morgen direct beginnen met integreren in je app!

**TIBET declares. BETTI coordinates. Your KIT API automates. 🚀**

---

**Last Updated:** 2025-11-27
**Version:** 1.0.0
**Status:** Production Ready ✓
