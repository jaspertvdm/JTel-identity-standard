# ⚡ Quick Answer: Hoe Integreert TIBET-BETTI met Jouw App?

**TL;DR: Twee aparte databases, één SDK, perfect gescheiden! 🎯**

---

## 🎨 De Simpele Visual

```
┌─────────────────────────────────────────────────────────────────┐
│                         JOUW APP                                │
│                                                                 │
│  ┌─────────────┐                                               │
│  │   APP DB    │ ◄─┐ Jouw bestaande database                   │
│  │  (port 5432)│   │ • users, devices, settings                │
│  └──────┬──────┘   │ • sense_rules (optioneel)                 │
│         │          │ • Blijft volledig apart!                   │
│         ▼          │                                            │
│  ┌─────────────────┴──────┐                                    │
│  │     KIT API (8000)     │  Jouw bestaande API!               │
│  │                        │                                     │
│  │  📥 Context Layer      │  Leest uit APP DB                  │
│  │  🧠 Sense Layer        │  Evalueert rules uit APP DB        │
│  │  ⚡ Intent Layer       │  Schrijft naar APP DB              │
│  └────────────┬───────────┘                                    │
│               │                                                 │
│               │ TIBET-BETTI SDK                                │
│               │ (Python client)                                │
└───────────────┼─────────────────────────────────────────────────┘
                │
                ▼
┌───────────────────────────────────────────────────────────────────┐
│                    BETTI ROUTER (18081)                          │
│                                                                   │
│  ┌─────────────┐                                                │
│  │  BETTI DB   │  Aparte database!                              │
│  │ (port 5433) │  • Trust tokens (FIR/A)                        │
│  └─────────────┘  • Intent routing                              │
│                   • Audit trails                                 │
│                   • Conversation state                           │
└───────────────────────────────────────────────────────────────────┘
```

---

## ✅ Jouw Vraag Beantwoord

### "Sense layer moet hierop aansluiten"
👉 **Antwoord:** Sense layer zit in **jouw KIT API**
- Leest context uit **jouw APP DB**
- Sense rules kunnen in **jouw APP DB** of in code
- Evalueert rules en triggered intents
- **Geen directe connectie met BETTI DB!**

```python
# In jouw KIT API
@app.post("/sense/evaluate")
def evaluate_sense(user_id: str):
    # 1. Lees context uit JOUW APP DB
    context = get_context_from_app_db(user_id)

    # 2. Lees sense rules uit JOUW APP DB
    rules = app_db.query(SenseRule).filter_by(user_id=user_id).all()

    # 3. Evaluate
    triggered_intents = []
    for rule in rules:
        if matches(context, rule.conditions):
            triggered_intents.append(rule.intent)

    return triggered_intents
```

### "Context core moet ook aansluiten"
👉 **Antwoord:** Context layer zit in **jouw KIT API**
- Leest data uit **jouw APP DB**
- Aggregeert user context
- Geen directe BETTI DB connectie!

```python
# In jouw KIT API
@app.post("/context/update")
def update_context(user_id: str, context: dict):
    # 1. Lees uit JOUW APP DB
    user = app_db.query(User).filter_by(id=user_id).first()
    devices = app_db.query(Device).filter_by(user_id=user_id).all()

    # 2. Aggregeer
    full_context = {
        "location": user.location,
        "devices": [d.to_dict() for d in devices],
        **context
    }

    # 3. Cache (in memory of Redis)
    context_store[user_id] = full_context

    return full_context
```

### "Intent layer ook"
👉 **Antwoord:** Intent execution in **jouw KIT API**
- Executed intents schrijven naar **jouw APP DB**
- Business logic blijft in jouw app!

```python
# In jouw KIT API
@app.post("/intents/execute")
def execute_intent(intent: str, context: dict):
    if intent == "turn_on_lights":
        # Update JOUW APP DB
        device = app_db.query(Device).filter_by(
            user_id=context['user_id'],
            type='lights'
        ).first()

        device.status = 'on'
        app_db.commit()
```

### "Hoe moet huidige DB hiermee werken?"
👉 **Antwoord:** Jouw DB blijft **volledig apart**!

**Jouw APP DB:**
- Draait op port 5432
- Alle bestaande tabellen blijven hetzelfde
- KIT API leest/schrijft zoals altijd
- **Niks verandert aan jouw bestaande code!**

**BETTI DB:**
- Nieuwe, aparte database op port 5433
- Alleen voor trust tokens & routing
- Jouw app heeft **geen directe queries** naar BETTI DB
- Via SDK alleen!

```python
# JOUW CODE BLIJFT HETZELFDE
from your_app import db  # Jouw APP DB

user = db.query(User).filter_by(id=user_id).first()
devices = db.query(Device).filter_by(user_id=user_id).all()

# ALLEEN TOEVOEGEN: BETTI SDK voor intents
from tibet_betti_client import TibetBettiClient

betti = TibetBettiClient(
    betti_url="http://localhost:18081",
    kit_url="http://localhost:8000",  # JOUW API!
    secret="denDolder_2024!"
)

# Establish trust (gaat naar BETTI DB)
rel = betti.establish_trust("app", "device")

# Send intent (gaat via BETTI, executed in jouw app)
betti.send_tibet(rel.id, "turn_on_lights", {...})
```

### "Dit moet ook aparte blijven voor ontwikkeling"
👉 **Antwoord:** JA! Beide DB's volledig apart!

```yaml
# docker-compose.yml
services:
  app-db:
    ports:
      - "5432:5432"  # Jouw DB
    volumes:
      - app-data:/var/lib/postgresql/data

  betti-db:
    ports:
      - "5433:5432"  # BETTI DB (andere port!)
    volumes:
      - betti-data:/var/lib/postgresql/data

volumes:
  app-data:     # Jouw data
  betti-data:   # BETTI data (apart!)
```

---

## 🎯 Wat Je NIET Hoeft Te Doen

❌ **GEEN** migratie van jouw bestaande database
❌ **GEEN** aanpassingen aan bestaande tabellen
❌ **GEEN** nieuwe kolommen in jouw users/devices tables
❌ **GEEN** directe queries naar BETTI DB
❌ **GEEN** wijzigingen aan jouw bestaande business logic

---

## ✅ Wat Je WEL Doet

✅ **Start** BETTI database apart (port 5433)
✅ **Start** BETTI router (port 18081)
✅ **Installeer** TIBET-BETTI SDK in jouw app
✅ **Gebruik** SDK voor trust tokens & intents
✅ **Optioneel:** Voeg sense_rules table toe aan APP DB
✅ **Optioneel:** Cache FIR/A IDs in APP DB voor performance

---

## 🚀 Complete Integration Flow

```python
# 1. Setup (eenmalig)
from tibet_betti_client import TibetBettiClient
from your_app import db  # JOUW APP DB

betti = TibetBettiClient(
    betti_url="http://localhost:18081",
    kit_url="http://localhost:8000",
    secret="denDolder_2024!"
)

# 2. User arrives home (jouw app detecteert dit)
@app.on_event("location_changed")
def on_location_change(user_id, location):
    if location == "home":
        # A. Get trust token (from JOUW APP DB cache)
        token = db.execute(
            "SELECT fira_id FROM user_trust_tokens WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        # B. Context + Sense + TIBET (automatic!)
        results = betti.context_to_tibet(
            relationship_id=token.fira_id,  # Trust token from BETTI
            user_id=user_id,
            context_update={
                "location": "home",
                "time_of_day": "evening"
            }
        )

        # Dit gebeurt automatisch:
        # 1. POST /context/update → leest uit JOUW APP DB
        # 2. POST /sense/evaluate → rules uit JOUW APP DB
        # 3. Send TIBETs → via BETTI router
        # 4. Intent executed → schrijft naar JOUW APP DB

        # C. Log in JOUW APP DB (optioneel)
        for result in results:
            db.execute(
                "INSERT INTO betti_intent_log (user_id, intent) VALUES (?, ?)",
                (user_id, result['intent'])
            )
        db.commit()
```

---

## 📊 Data Flow Visualized

```
User arrives home
      │
      ▼
[JOUW APP detecteert]
      │
      ▼
┌─────────────────────────────────────┐
│ Read context from APP DB:           │
│ • user.location = "home"            │
│ • time = "evening"                  │
│ • devices = [lights, heating]       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Read sense rules from APP DB:       │
│ Rule: location=home + evening       │
│   → turn_on_lights                  │
│ Rule: evening + home                │
│   → set_heating                     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Get trust token from APP DB cache:  │
│ fira_id = "abc-123-xyz"             │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Send TIBETs via SDK:                │
│ → BETTI DB: Store intent + audit    │
│ → BETTI Router: Route to device     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Device receives + executes:         │
│ → Execute intent                    │
│ → Write result to APP DB            │
└─────────────────────────────────────┘
```

---

## 🎉 Samenvatting

**Jouw Vraag:** Hoe sluiten sense/context/intent layers aan op mn DB?

**Antwoord:**
1. **Sense layer** = endpoint in jouw KIT API, leest uit JOUW APP DB
2. **Context layer** = endpoint in jouw KIT API, leest uit JOUW APP DB
3. **Intent layer** = endpoint in jouw KIT API, schrijft naar JOUW APP DB
4. **BETTI DB** = volledig aparte database, alleen trust & routing
5. **SDK** = verbindt alles via API calls (niet direct queries!)

**Jouw APP DB blijft volledig apart voor ontwikkeling! 🚀**

---

## 📚 Documentatie

- **INTEGRATION-ARCHITECTURE.md** - Complete architectuur uitleg
- **DATABASE-SCHEMAS.md** - Alle schema's + query voorbeelden
- **DEVELOPMENT-SETUP.md** - Docker compose + setup
- **SDK-READY.md** - SDK quick start

**Het is zo goed, en het blijft zo goed - volledig gescheiden! 🎊**
