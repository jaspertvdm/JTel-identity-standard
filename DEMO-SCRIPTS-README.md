# ☕ TIBET Demo Scripts - Client & Server

**Praktische voorbeelden hoe client TIBETs stuurt en server ze ontvangt**

---

## 🎯 Scripts Overzicht

### 1. `demo_shoot_tibet.py` - Client Kant
**Stuurt een TIBET intent naar server**

```bash
python demo_shoot_tibet.py
```

**Wat het doet:**
- ✅ Verbindt met BETTI Router
- ✅ Zet trust op tussen client ↔ server
- ✅ Stuurt "maak_koffie" TIBET intent
- ✅ Laat zien wat server ontvangt
- ✅ Toont complete flow + event history

**Output:**
```
☕ KOFFIE TIBET DEMO
1️⃣  Connecting to BETTI Router...
   ✅ BETTI Router: healthy
2️⃣  Establishing trust: client ↔ koffie_server...
   ✅ Trust established!
   📋 FIR/A ID: abc-123-xyz
3️⃣  Shooting TIBET intent: 'maak_koffie' ☕...
   ✅ TIBET sent!
📥 WAT DE SERVER ONTVANGT:
🎯 INTENT: maak_koffie
📦 CONTEXT: cappuccino, groot, havermelk, extra shot
```

---

### 2. `server_tibet_handler.py` - Server Kant
**Ontvangt en verwerkt TIBETs**

```bash
python server_tibet_handler.py
```

**Wat het doet:**
- ✅ Simuleert TIBET ontvangst
- ✅ Parse intent & context
- ✅ Voert actie uit (maakt koffie!)
- ✅ Returnt result
- ✅ Logt naar database

**Output:**
```
📥 TIBET ONTVANGEN om 09:20:51
🎯 Intent: maak_koffie
📦 Context: cappuccino, groot, havermelk, extra shot
🤖 SERVER ACTIE:
☕ Start maken: CAPPUCCINO
   [1/5] Grinding beans... ⚙️
   [2/5] Heating water... 🔥
   [3/5] Brewing espresso... ☕
   [4/5] Adding havermelk... 🥛
   [5/5] Finishing up... ✨
✅ Cappuccino klaar voor Jasper! ☕
```

---

## 🚀 Complete Flow Demo

### Stap 1: Start BETTI Router

```bash
cd tbet-router
node src/index.js
```

### Stap 2: Shoot TIBET (Client)

```bash
python demo_shoot_tibet.py
```

Dit stuurt een TIBET intent naar de BETTI Router.

### Stap 3: Server Handler (Demo Mode)

```bash
python server_tibet_handler.py
```

Dit simuleert hoe de server de TIBET ontvangt en verwerkt.

---

## 💡 Integratie in Jouw App

### Client Kant (Jouw App)

```python
from tibet_betti_client import TibetBettiClient, TimeWindow

# Initialize
client = TibetBettiClient(
    betti_url="http://localhost:18081",
    kit_url="http://localhost:8000",
    secret="denDolder_2024!"
)

# Establish trust (eenmalig per device/user)
rel = client.establish_trust("my_app", "server")

# Shoot TIBET (elke keer als je iets wil)
client.send_tibet(
    relationship_id=rel.id,
    intent="maak_koffie",
    context={
        "type": "cappuccino",
        "user": "Jasper",
        "size": "groot"
    },
    time_window=TimeWindow.immediate(),
    humotica="User requested coffee via app"
)
```

### Server Kant (Jouw Backend)

```python
from server_tibet_handler import ServerTibetHandler

# Initialize handler
server = ServerTibetHandler("my_app_server")

# FastAPI example
@app.post("/intents/execute")
async def execute_intent(intent_data: dict):
    """Receive TIBET from BETTI Router"""
    result = server.handle_tibet(intent_data)
    return result

# WebSocket example
@app.websocket("/ws/tibet")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        result = server.handle_tibet(data)
        await websocket.send_json(result)
```

---

## 📊 Wat Gebeurt Er?

```
┌─────────────────┐
│  JOUW APP       │  python demo_shoot_tibet.py
│  (Client)       │
└────────┬────────┘
         │ 1. Establish trust
         │ 2. Send TIBET: "maak_koffie"
         ▼
┌─────────────────┐
│  BETTI ROUTER   │  http://localhost:18081
│  (Coordinator)  │
└────────┬────────┘
         │ 3. Route TIBET to server
         │ 4. Validate trust token
         ▼
┌─────────────────┐
│  SERVER         │  python server_tibet_handler.py
│  (Executor)     │
└─────────────────┘
         │ 5. Receive TIBET
         │ 6. Parse intent & context
         │ 7. Execute action
         │ 8. Return result
         └─► ✅ Cappuccino klaar!
```

---

## 🎯 Ondersteunde Intents (in demo)

De `server_tibet_handler.py` ondersteunt:

1. **`maak_koffie`** ☕
   - Context: type, size, melk, suiker, extra
   - Action: Simuleert koffie maken

2. **`turn_on_lights`** 💡
   - Context: room, brightness
   - Action: Lights aan in opgegeven kamer

3. **`schedule_meeting`** 📅
   - Context: attendees, time, duration
   - Action: Meeting inplannen

4. **`morning_briefing`** 📰
   - Context: (none required)
   - Action: Morning briefing genereren

### Eigen Intent Toevoegen

```python
# In server_tibet_handler.py

def handle_your_custom_intent(self, context: dict, fira_id: str):
    """Handle: your_custom_intent"""
    print("🤖 CUSTOM INTENT HANDLER")

    # Parse context
    param1 = context.get('param1')
    param2 = context.get('param2')

    # Execute action
    result = your_business_logic(param1, param2)

    # Return result
    return {
        'status': 'completed',
        'message': 'Action completed!',
        'data': result
    }

# Register in handle_tibet()
if intent == "your_custom_intent":
    return self.handle_your_custom_intent(context, fira_id)
```

---

## 🔧 Testing

### Test Complete Flow

```bash
# Terminal 1: Start BETTI Router
cd tbet-router && node src/index.js

# Terminal 2: Shoot TIBET
python demo_shoot_tibet.py

# Terminal 3: Server handler (demo mode)
python server_tibet_handler.py
```

### Test met Live Router

```bash
# 1. Start BETTI Router
cd tbet-router && node src/index.js

# 2. Shoot real TIBET
python demo_shoot_tibet.py

# Check router logs to see TIBET received!
```

---

## 📝 Tips

1. **Trust Token Reuse**
   - Establish trust eenmalig
   - Cache FIR/A ID in je app
   - Hergebruik voor alle volgende TIBETs

2. **Context is Key**
   - Zet alle benodigde info in context
   - Server gebruikt dit om actie uit te voeren
   - Maak context zo specifiek mogelijk

3. **Humotica**
   - Altijd toevoegen voor audit trails
   - Leg uit WAAROM de intent gestuurd wordt
   - Human-readable explanation

4. **Error Handling**
   - Server returnt status in result
   - Check result.status voor success/failure
   - Handle errors gracefully

---

## 🎉 Samenvatting

**Client:** Shoot TIBET via SDK
```python
client.send_tibet(rel.id, "maak_koffie", {...})
```

**BETTI:** Routes to server (automatic!)

**Server:** Ontvangt & verwerkt
```python
server.handle_tibet(tibet_data)
```

**Result:** Actie uitgevoerd + result returned! ✅

---

## 📚 Zie Ook

- [SDK-READY.md](SDK-READY.md) - SDK installation
- [QUICK-START-TOMORROW.md](QUICK-START-TOMORROW.md) - Complete guide
- [INTEGRATION-ARCHITECTURE.md](INTEGRATION-ARCHITECTURE.md) - Architecture

**TIBET declares. BETTI coordinates. Server executes! ☕🚀**
