# TIBET + BETTI: The Complete Framework

**Time Intent Based Event Token + Behavior-Enhanced Trusted Telephony Interactions**

Version: 2.0.0
Date: 2025-11-27
Status: Official Naming

---

## 🎯 The Names

### TIBET
**Time Intent Based Event Token**

**What it is:**
The protocol for declaring intents with time windows and context.

**Structure:**
```
T - Time:        Time-windowed execution
I - Intent:      Clear purpose/goal
B - Based:
E - Event:       Actionable event
T - Token:       Carries trust/auth
```

**Example TIBET:**
```json
{
  "tibet_id": "tibet_550e8400",
  "intent": "lights_on",
  "time_window": {
    "start": "2025-11-27T18:00:00Z",
    "end": "2025-11-27T18:30:00Z"
  },
  "context": {
    "reason": "user_arriving_home",
    "ambient_light": "45_lux",
    "preference": "warm_white"
  },
  "constraints": {
    "max_brightness": "80%",
    "safe_fail": "notify_user"
  },
  "trust_token_ref": "fira_abc123"
}
```

### BETTI
**Behavior-Enhanced Trusted Telephony Interactions**

**What it is:**
The universal coordinator that:
- Receives TIBET intents
- Validates trust tokens (FIR/A)
- Routes to correct recipients
- Prevents loops
- Enforces safe fails
- Creates audit trails (humotica)

**Role:**
The brain that makes sense of all TIBET intents and coordinates everything.

---

## 🔄 How They Work Together

```
┌─────────────────────────────────────────────────┐
│              DEVICES/SERVICES                   │
│  (Phone, Car, Lights, Robots, etc.)            │
└─────────────────────────────────────────────────┘
                    ↓
        Send TIBET intents
                    ↓
┌─────────────────────────────────────────────────┐
│            BETTI COORDINATOR                    │
│                                                 │
│  1. Receives TIBET intents                     │
│  2. Validates trust tokens (FIR/A)             │
│  3. Checks time windows                        │
│  4. Prevents loops                             │
│  5. Routes to recipients                       │
│  6. Creates audit trail                        │
└─────────────────────────────────────────────────┘
                    ↓
        Coordinated actions
                    ↓
┌─────────────────────────────────────────────────┐
│         RECIPIENT DEVICES/SERVICES              │
│  (Execute intents within constraints)          │
└─────────────────────────────────────────────────┘
```

---

## 📖 Complete Terminology

### Core Components

| Term | Full Name | Description |
|------|-----------|-------------|
| **TIBET** | Time Intent Based Event Token | The intent declaration protocol |
| **BETTI** | Behavior-Enhanced Trusted Telephony Interactions | The universal coordinator |
| **FIR/A** | Formalized Intent Relationship Acknowledged | The trust token ("we know each other") |
| **DID** | Device Identity | Device's cryptographic identity |
| **HID** | Human Identity | Human biometric binding |
| **Humotica** | Human Intent Trace | Human-readable audit trail |

### Flow Terms

| Term | Description |
|------|-------------|
| **TIBET Declaration** | Device/service declares intent with time window |
| **BETTI Routing** | Router coordinates and routes the intent |
| **Trust Verification** | Checking FIR/A relationship validity |
| **Loop Prevention** | Automatic depth limit enforcement |
| **Safe Fail** | Guaranteed graceful degradation |
| **Continuity Hash** | Tamper-proof event chain link |

---

## 🎯 Example Scenarios

### Scenario 1: Smart Home Morning Routine

**TIBET Intent from Phone:**
```json
{
  "tibet_id": "morning_routine_001",
  "intent": "morning_routine",
  "time_window": {
    "start": "2025-11-28T06:30:00Z",
    "end": "2025-11-28T07:00:00Z"
  },
  "context": {
    "weekday": true,
    "user": "jasper",
    "location": "home"
  },
  "sub_intents": [
    {
      "intent": "coffee_machine_start",
      "offset_minutes": 0
    },
    {
      "intent": "lights_gradual_on",
      "offset_minutes": 5
    },
    {
      "intent": "thermostat_to_21C",
      "offset_minutes": 10
    }
  ],
  "trust_token_ref": "fira_phone_home_001"
}
```

**BETTI Coordinates:**
1. Receives TIBET intent
2. Validates FIR/A: Phone ←→ Home ✓
3. Schedules sub-intents with time offsets
4. 06:30: Coffee machine → TIBET "start_brewing"
5. 06:35: Lights → TIBET "gradual_on_30min"
6. 06:40: Thermostat → TIBET "set_temp_21C"

**Result:**
- Seamless morning routine
- All coordinated via BETTI
- Full audit trail (humotica)

---

### Scenario 2: Robot Warehouse Coordination

**TIBET Intent from Robot A:**
```json
{
  "tibet_id": "pick_task_123",
  "intent": "navigate_and_pick",
  "time_window": {
    "start": "immediate",
    "deadline": "2025-11-27T14:30:00Z"
  },
  "context": {
    "source": "shelf_A_row_5",
    "destination": "packing_station_3",
    "item_id": "SKU-12345",
    "priority": 7
  },
  "constraints": {
    "max_retries": 3,
    "collision_avoidance": true,
    "battery_threshold": "30%"
  },
  "trust_token_ref": "fira_robotA_warehouse_001"
}
```

**BETTI Coordinates:**
1. Receives TIBET from Robot A
2. Validates FIR/A: Robot A ←→ Warehouse ✓
3. Checks conflicts: Robot B at shelf A?
4. Robot B sends TIBET: "I'm at shelf A, ETA 2 min"
5. BETTI negotiates:
   - Robot B priority 5 < Robot A priority 7
   - Robot B: "Waiting for Robot A"
6. Robot A executes, updates BETTI
7. Robot A completes → BETTI notifies Robot B
8. Robot B resumes

**Result:**
- No collision
- No deadlock
- Priority respected
- Full coordination log

---

### Scenario 3: Bank Calls Customer

**TIBET Intent from Bank:**
```json
{
  "tibet_id": "financial_advice_456",
  "intent": "financial_advice_call",
  "time_window": {
    "appointment_start": "2025-11-27T14:30:00Z",
    "appointment_end": "2025-11-27T15:00:00Z",
    "strict": true
  },
  "context": {
    "institution": "ING Bank Nederland",
    "license": "AFM-12345",
    "advisor": "J. Smit",
    "customer_account_ref": "****4567",
    "subject": "Hypotheek bespreking",
    "appointment_id": "appt_20251127_1430"
  },
  "constraints": {
    "trust_level": 3,
    "recording_mandatory": true,
    "mifid_compliance": true,
    "outside_window": "block_and_log"
  },
  "trust_token_ref": "fira_ing_customer_789"
}
```

**BETTI Coordinates:**
1. Receives TIBET from Bank at 14:32
2. Checks time window: 14:32 within 14:30-15:00 ✓
3. Validates FIR/A: Bank ←→ Customer ✓
4. Validates appointment exists ✓
5. Routes to customer phone
6. Customer phone displays:
   ```
   🏦 VERIFIED BANK
   ING Bank Nederland
   Account: ****4567
   Appointment: 14:30 ✓
   [Accept] [Reject]
   ```
7. Customer accepts
8. BETTI creates audit trail (humotica)

**If bank calls at 15:05 (outside window):**
- BETTI blocks: "Outside appointment window"
- Logs breach attempt
- Notifies customer: "Bank tried to call outside window"

---

## 🌟 Why This Naming Works

### 1. TIBET is Universal

**Not limited to telephony:**
- ✅ Smart Home: TIBET for automation
- ✅ Robotics: TIBET for coordination
- ✅ IoT: TIBET for device communication
- ✅ AI Agents: TIBET for multi-agent tasks
- ✅ And yes, telephony too!

### 2. Clear Responsibilities

**TIBET = Declare**
- "I want to do X"
- "Between time Y and Z"
- "Because of reason W"
- "With constraints V"

**BETTI = Coordinate**
- "I received your TIBET"
- "I verified your trust token"
- "I'll route it correctly"
- "I'll prevent loops"
- "I'll create audit trail"

### 3. Memorable & Meaningful

**TIBET:**
- Time ✓
- Intent ✓
- Event ✓
- Token ✓

**BETTI:**
- Behavior (intent-based) ✓
- Enhanced (better than traditional) ✓
- Trusted (FIR/A tokens) ✓
- (originally Telephony, now universal) ✓
- Interactions ✓

---

## 🔄 Migration from TBET

### Old (TBET)
```
TBET = Targeting Telephony Behavior
→ Too telephony-specific
→ "Behavior" unclear
```

### New (TIBET)
```
TIBET = Time Intent Based Event Token
→ Universal applicability
→ Clear components
→ Better describes what it is
```

### Impact
- All documentation updated
- TBET → TIBET throughout
- Backward compatibility maintained (alias)
- SDK function names updated

---

## 📋 Complete Stack

```
┌─────────────────────────────────────────┐
│         APPLICATION LAYER               │
│  (Smart Home, Robots, Telephony, etc.)  │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│         TIBET INTENT LAYER              │
│  Declare intents with time windows      │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│      BETTI COORDINATION LAYER           │
│  Route, validate, prevent loops         │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│       TRUST TOKEN LAYER (FIR/A)         │
│  "We know each other" relationships     │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│     IDENTITY LAYER (DID/HID)            │
│  Device + Human cryptographic identity  │
└─────────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│         TRANSPORT LAYER                 │
│  (HTTP/WebSocket/MQTT/Neural/Mesh)      │
└─────────────────────────────────────────┘
```

---

## 🎯 The Complete Framework

### Components

1. **TIBET** - Intent declaration
2. **BETTI** - Coordination router
3. **FIR/A** - Trust tokens
4. **DID/HID** - Identity binding
5. **Humotica** - Audit trails

### Principles

1. **Intent-Based**: Everything has purpose
2. **Time-Windowed**: Everything has bounds
3. **Trust-Verified**: Relationships matter
4. **Loop-Free**: Automatic prevention
5. **Safe-Fail**: Graceful degradation
6. **Auditable**: Full transparency

### Applications

- Smart Homes
- Robotics
- IoT
- Telephony
- Autonomous Vehicles
- Industrial Automation
- Healthcare Coordination
- AI Agent Swarms
- And anything else autonomous!

---

## 🚀 The Vision

**"Every autonomous interaction uses TIBET + BETTI"**

By 2030:
- ✅ TIBET is the standard intent protocol
- ✅ BETTI routers everywhere (cloud, edge, embedded)
- ✅ FIR/A trust tokens ubiquitous
- ✅ "TIBET/BETTI Inside" certification
- ✅ Universal interoperability

**From telephony to the world.**
**From TBET to TIBET.**
**The future of autonomous coordination. 🌍**

---

## 📖 Quick Reference

### Send a TIBET Intent

```python
from betti_client import BettiClient

client = BettiClient("http://betti-router:8080")

# Establish trust (FIR/A)
relationship = client.establish_trust(
    initiator="my_phone",
    responder="my_car"
)

# Send TIBET intent
client.send_tibet(
    trust_token=relationship.token,
    intent="unlock_car",
    time_window={"immediate": True},
    context={"location": "home"}
)
```

### Receive TIBET Intent

```python
from betti_server import BettiServer

server = BettiServer()

@server.on_tibet("unlock_car")
def handle_unlock(tibet):
    # Verify trust token
    if not verify_fira(tibet.trust_token_ref):
        return {"status": "unauthorized"}

    # Check time window
    if not tibet.in_time_window():
        return {"status": "outside_window"}

    # Execute
    car.unlock()

    return {
        "status": "unlocked",
        "humotica": "Car unlocked via TIBET intent from trusted phone"
    }
```

---

**TIBET + BETTI = The Future! 🔥**
