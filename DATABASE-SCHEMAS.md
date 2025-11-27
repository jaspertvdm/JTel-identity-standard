# 🗄️ Database Schemas: APP vs BETTI

**Complete database schema's en hoe ze samenwerken**

---

## 📊 Overzicht

```
┌─────────────────────────────┐         ┌─────────────────────────────┐
│     APP DATABASE            │         │    BETTI DATABASE           │
│  (jouw bestaande DB)        │         │  (aparte router DB)         │
├─────────────────────────────┤         ├─────────────────────────────┤
│                             │         │                             │
│  • users                    │         │  • fira_relationships       │
│  • devices                  │         │  • intent_history           │
│  • settings                 │         │  • conversation_state       │
│  • preferences              │         │  • audit_log                │
│  • sense_rules (optioneel)  │         │  • trust_tokens             │
│  • locations                │         │  • continuity_chain         │
│  • activities               │         │                             │
│  • app_audit_log            │         │                             │
│                             │         │                             │
└──────────┬──────────────────┘         └──────────┬──────────────────┘
           │                                       │
           │  KIT API leest/schrijft               │  BETTI Router
           │  jouw business logic                  │  trust & routing
           │                                       │
           └───────────────┬───────────────────────┘
                          │
                    SDK verbindt ze
```

---

## 1️⃣ APP DATABASE Schema

**Jouw bestaande database - blijft apart voor ontwikkeling!**

### Core Tables (jouw bestaande structuur)

```sql
-- Users (jouw app users)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    location VARCHAR(100),
    timezone VARCHAR(50),
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Devices (user devices)
CREATE TABLE devices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    device_type VARCHAR(50) NOT NULL,  -- phone, tablet, smart_home, etc.
    device_name VARCHAR(100),
    status VARCHAR(20) DEFAULT 'active',  -- active, inactive, offline
    capabilities JSONB DEFAULT '[]',
    last_seen TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Settings (user settings)
CREATE TABLE settings (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    category VARCHAR(50) NOT NULL,  -- privacy, notifications, automation
    key VARCHAR(100) NOT NULL,
    value JSONB NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, category, key)
);

-- Locations (user locations/zones)
CREATE TABLE locations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,  -- Home, Work, Gym
    type VARCHAR(50),  -- home, work, public
    coordinates JSONB,  -- {lat, lng, radius}
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Activities (user activities/logs)
CREATE TABLE activities (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    activity_type VARCHAR(100) NOT NULL,
    context JSONB DEFAULT '{}',
    timestamp TIMESTAMP DEFAULT NOW(),
    INDEX idx_activities_user_time (user_id, timestamp DESC)
);
```

### Sense Rules (optioneel in APP DB)

```sql
-- Sense Rules (automatic intent triggers)
CREATE TABLE sense_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,  -- NULL for global rules
    name VARCHAR(100) NOT NULL,
    description TEXT,
    conditions JSONB NOT NULL,  -- {location: "home", time_of_day: "evening"}
    intent VARCHAR(100) NOT NULL,
    priority INTEGER DEFAULT 5,
    enabled BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_sense_rules_user ON sense_rules(user_id, enabled, priority DESC);

-- Example sense rule data
INSERT INTO sense_rules (name, conditions, intent, priority) VALUES
('Evening Lights',
 '{"location": "home", "time_of_day": "evening", "ambient_light": {"lt": 100}}'::jsonb,
 'turn_on_lights',
 7),
('Morning Routine',
 '{"location": "home", "time_of_day": "morning", "day_type": "weekday"}'::jsonb,
 'morning_briefing',
 8);
```

### BETTI Integration Tables (optioneel, voor performance)

```sql
-- Cache FIR/A tokens (actual tokens zijn in BETTI DB!)
CREATE TABLE user_trust_tokens (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    device_id UUID REFERENCES devices(id) ON DELETE CASCADE,
    fira_id VARCHAR(255) NOT NULL,  -- Reference to BETTI DB!
    token_type VARCHAR(50) DEFAULT 'device_trust',
    created_at TIMESTAMP DEFAULT NOW(),
    last_used TIMESTAMP,
    UNIQUE(user_id, device_id)
);

-- BETTI intent log (for your app audit)
CREATE TABLE betti_intent_log (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    fira_id VARCHAR(255),  -- Reference to BETTI DB
    intent VARCHAR(100) NOT NULL,
    context JSONB DEFAULT '{}',
    status VARCHAR(50) DEFAULT 'sent',  -- sent, executed, failed
    timestamp TIMESTAMP DEFAULT NOW(),
    INDEX idx_betti_log_user_time (user_id, timestamp DESC)
);
```

---

## 2️⃣ BETTI DATABASE Schema

**Aparte database voor trust & routing (in BETTI router)**

### Core BETTI Tables

```sql
-- FIR/A Relationships (Trust Tokens)
CREATE TABLE fira_relationships (
    id VARCHAR(255) PRIMARY KEY,  -- UUID
    initiator VARCHAR(255) NOT NULL,
    responder VARCHAR(255) NOT NULL,
    roles JSONB DEFAULT '[]',
    trust_level INTEGER DEFAULT 1,  -- 0-5
    continuity_hash VARCHAR(64) NOT NULL,
    context JSONB DEFAULT '{}',
    established_at TIMESTAMP DEFAULT NOW(),
    last_interaction TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'active',  -- active, suspended, revoked
    INDEX idx_fira_parties (initiator, responder),
    INDEX idx_fira_trust (trust_level, status)
);

-- Intent History (all TIBET transmissions)
CREATE TABLE intent_history (
    id BIGSERIAL PRIMARY KEY,
    fira_id VARCHAR(255) REFERENCES fira_relationships(id) ON DELETE CASCADE,
    intent VARCHAR(100) NOT NULL,
    context JSONB DEFAULT '{}',
    timebox_seconds INTEGER NOT NULL,
    continuity_hash_prev VARCHAR(64),
    continuity_hash_new VARCHAR(64) NOT NULL,
    conversation_depth INTEGER DEFAULT 0,
    timestamp TIMESTAMP DEFAULT NOW(),
    INDEX idx_intent_fira_time (fira_id, timestamp DESC),
    INDEX idx_intent_depth (conversation_depth, fira_id)
);

-- Conversation State (loop prevention)
CREATE TABLE conversation_state (
    id SERIAL PRIMARY KEY,
    fira_id VARCHAR(255) REFERENCES fira_relationships(id) ON DELETE CASCADE,
    conversation_id VARCHAR(255) NOT NULL,
    current_depth INTEGER DEFAULT 0,
    max_depth INTEGER DEFAULT 5,
    started_at TIMESTAMP DEFAULT NOW(),
    last_exchange TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'active',  -- active, completed, expired
    UNIQUE(fira_id, conversation_id),
    INDEX idx_conv_status (status, expires_at)
);

-- Audit Log (Humotica - why things happened)
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    fira_id VARCHAR(255) REFERENCES fira_relationships(id) ON DELETE SET NULL,
    event_type VARCHAR(100) NOT NULL,  -- trust_established, intent_sent, etc.
    intent VARCHAR(100),
    humotica TEXT,  -- Human-readable explanation
    context JSONB DEFAULT '{}',
    trust_level INTEGER,
    timestamp TIMESTAMP DEFAULT NOW(),
    INDEX idx_audit_fira_time (fira_id, timestamp DESC),
    INDEX idx_audit_type (event_type, timestamp DESC)
);

-- Trust Token Metadata
CREATE TABLE trust_tokens (
    id SERIAL PRIMARY KEY,
    fira_id VARCHAR(255) UNIQUE REFERENCES fira_relationships(id) ON DELETE CASCADE,
    did_public TEXT,  -- DID public key
    hid_did_binding TEXT,  -- HID-DID binding
    key_metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Continuity Chain (for verification)
CREATE TABLE continuity_chain (
    id BIGSERIAL PRIMARY KEY,
    fira_id VARCHAR(255) REFERENCES fira_relationships(id) ON DELETE CASCADE,
    sequence_number INTEGER NOT NULL,
    hash_prev VARCHAR(64),
    hash_current VARCHAR(64) NOT NULL,
    event_type VARCHAR(50) NOT NULL,  -- init, intent, response
    timestamp TIMESTAMP DEFAULT NOW(),
    UNIQUE(fira_id, sequence_number),
    INDEX idx_chain_fira (fira_id, sequence_number DESC)
);
```

---

## 🔄 Hoe Ze Samenwerken

### Voorbeeld Flow met Beide Databases

```python
from your_app import db as app_db  # YOUR APP DB
from betti_router import db as betti_db  # BETTI DB

def handle_user_arrives_home(user_id: str):
    """
    User arrives home - uses BOTH databases
    """

    # 1. READ FROM APP DB - Get user context
    user = app_db.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()

    devices = app_db.execute(
        "SELECT * FROM devices WHERE user_id = ? AND status = 'active'",
        (user_id,)
    ).fetchall()

    settings = app_db.execute(
        "SELECT * FROM settings WHERE user_id = ? AND category = 'automation'",
        (user_id,)
    ).fetchall()

    # 2. READ FROM APP DB - Get sense rules
    sense_rules = app_db.execute(
        """
        SELECT * FROM sense_rules
        WHERE (user_id = ? OR user_id IS NULL)
        AND enabled = true
        ORDER BY priority DESC
        """,
        (user_id,)
    ).fetchall()

    # 3. EVALUATE - Which intents to trigger?
    context = {
        "location": "home",
        "time_of_day": "evening",
        "ambient_light": 50,  # From device sensor
        "devices_available": len(devices)
    }

    triggered_intents = []
    for rule in sense_rules:
        if matches_conditions(context, rule.conditions):
            triggered_intents.append(rule.intent)

    # 4. READ FROM APP DB - Get trust token (cached)
    token_cache = app_db.execute(
        "SELECT fira_id FROM user_trust_tokens WHERE user_id = ? LIMIT 1",
        (user_id,)
    ).fetchone()

    fira_id = token_cache.fira_id

    # 5. VALIDATE IN BETTI DB - Check trust token still valid
    fira = betti_db.execute(
        "SELECT * FROM fira_relationships WHERE id = ? AND status = 'active'",
        (fira_id,)
    ).fetchone()

    if not fira:
        raise Exception("Trust token invalid or revoked")

    # 6. SEND INTENTS - Write to BETTI DB
    for intent in triggered_intents:
        # Calculate continuity hash
        prev_hash = betti_db.execute(
            """
            SELECT continuity_hash_new FROM intent_history
            WHERE fira_id = ?
            ORDER BY timestamp DESC LIMIT 1
            """,
            (fira_id,)
        ).fetchone()

        new_hash = calculate_hash(prev_hash, intent, context)

        # INSERT INTO BETTI DB
        betti_db.execute(
            """
            INSERT INTO intent_history
            (fira_id, intent, context, timebox_seconds,
             continuity_hash_prev, continuity_hash_new, conversation_depth)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (fira_id, intent, json.dumps(context), 30,
             prev_hash, new_hash, 0)
        )

        # INSERT INTO BETTI AUDIT
        betti_db.execute(
            """
            INSERT INTO audit_log (fira_id, event_type, intent, humotica, context)
            VALUES (?, 'intent_sent', ?, ?, ?)
            """,
            (fira_id, intent,
             f"Auto-triggered when user arrived home in evening",
             json.dumps(context))
        )

        # 7. LOG IN APP DB (your audit)
        app_db.execute(
            """
            INSERT INTO betti_intent_log (user_id, fira_id, intent, context, status)
            VALUES (?, ?, ?, ?, 'sent')
            """,
            (user_id, fira_id, intent, json.dumps(context))
        )

        # 8. UPDATE APP DB - Update last activity
        app_db.execute(
            """
            INSERT INTO activities (user_id, activity_type, context)
            VALUES (?, 'betti_intent', ?)
            """,
            (user_id, json.dumps({"intent": intent, "triggered_by": "arrival"}))
        )

    app_db.commit()
    betti_db.commit()

    return {
        "triggered_intents": triggered_intents,
        "fira_id": fira_id
    }
```

---

## 📈 Query Examples

### Queries op APP DB (jouw queries blijven hetzelfde!)

```sql
-- Get user's active sense rules
SELECT * FROM sense_rules
WHERE user_id = 'user-uuid'
AND enabled = true
ORDER BY priority DESC;

-- Get user's recent activities
SELECT * FROM activities
WHERE user_id = 'user-uuid'
ORDER BY timestamp DESC
LIMIT 50;

-- Get user's BETTI intent history (your audit)
SELECT
    bil.intent,
    bil.status,
    bil.timestamp,
    u.name as user_name
FROM betti_intent_log bil
JOIN users u ON bil.user_id = u.id
WHERE bil.user_id = 'user-uuid'
ORDER BY bil.timestamp DESC;

-- Get all automation settings
SELECT
    s.key,
    s.value,
    sr.name as rule_name,
    sr.intent
FROM settings s
LEFT JOIN sense_rules sr ON sr.user_id = s.user_id
WHERE s.user_id = 'user-uuid'
AND s.category = 'automation';
```

### Queries op BETTI DB (trust & routing)

```sql
-- Get active trust relationships for a user
SELECT * FROM fira_relationships
WHERE (initiator LIKE 'user_%' OR responder LIKE 'user_%')
AND status = 'active';

-- Get intent history for a relationship
SELECT
    ih.intent,
    ih.context,
    ih.conversation_depth,
    ih.timestamp,
    al.humotica
FROM intent_history ih
LEFT JOIN audit_log al ON al.fira_id = ih.fira_id
    AND al.intent = ih.intent
    AND al.timestamp = ih.timestamp
WHERE ih.fira_id = 'fira-uuid'
ORDER BY ih.timestamp DESC
LIMIT 100;

-- Check conversation depth (loop prevention)
SELECT * FROM conversation_state
WHERE fira_id = 'fira-uuid'
AND status = 'active'
AND expires_at > NOW();

-- Audit trail with humotica
SELECT
    event_type,
    intent,
    humotica,
    timestamp
FROM audit_log
WHERE fira_id = 'fira-uuid'
ORDER BY timestamp DESC;

-- Verify continuity chain
SELECT
    sequence_number,
    hash_prev,
    hash_current,
    event_type,
    timestamp
FROM continuity_chain
WHERE fira_id = 'fira-uuid'
ORDER BY sequence_number ASC;
```

### Cross-Database Queries (via application layer!)

```python
# Via je app code - niet direct SQL!

def get_user_complete_history(user_id):
    """
    Combines data from BOTH databases
    """
    # From APP DB
    user = app_db.query(User).filter_by(id=user_id).first()
    activities = app_db.query(Activity).filter_by(user_id=user_id).all()

    # Get FIR/A IDs from APP DB cache
    fira_ids = app_db.execute(
        "SELECT fira_id FROM user_trust_tokens WHERE user_id = ?",
        (user_id,)
    ).fetchall()

    # From BETTI DB
    betti_history = []
    for fira_id in fira_ids:
        history = betti_db.execute(
            """
            SELECT ih.*, al.humotica
            FROM intent_history ih
            LEFT JOIN audit_log al ON al.fira_id = ih.fira_id
            WHERE ih.fira_id = ?
            ORDER BY ih.timestamp DESC
            """,
            (fira_id,)
        ).fetchall()
        betti_history.extend(history)

    return {
        "user": user,
        "app_activities": activities,
        "betti_intents": betti_history
    }
```

---

## 🎯 Best Practices

### 1. Database Scheiding
✅ **Nooit** direct queries tussen databases
✅ Gebruik application layer (KIT API) als brug
✅ Cache FIR/A IDs in APP DB voor performance
✅ Beide databases kunnen apart backuppen

### 2. Sense Rules Locatie
```python
# Optie A: In APP DB (flexible, per-user customization)
sense_rules_table = app_db.Table('sense_rules')

# Optie B: In code/config (simpler, global rules)
SENSE_RULES = [...]

# Optie C: Mix (global in code, custom in DB)
def get_sense_rules(user_id):
    global_rules = GLOBAL_SENSE_RULES
    user_rules = app_db.query(SenseRule).filter_by(user_id=user_id).all()
    return global_rules + user_rules
```

### 3. Audit Logging
```python
# In APP DB: Application audit
app_db.log_activity(user_id, "user_action", context)

# In BETTI DB: Trust & routing audit
betti_db.log_audit(fira_id, "intent_sent", humotica)

# Both are valuable! Different purposes
```

### 4. Performance Caching
```sql
-- APP DB: Cache frequently used FIR/A IDs
CREATE TABLE user_trust_tokens (
    user_id UUID,
    fira_id VARCHAR(255),  -- Cache from BETTI DB
    last_used TIMESTAMP
);

-- Update cache on each use
UPDATE user_trust_tokens
SET last_used = NOW()
WHERE user_id = ? AND fira_id = ?;
```

---

## ✅ Samenvatting

| Aspect | APP DATABASE | BETTI DATABASE |
|--------|-------------|----------------|
| **Eigenaar** | Jouw app | BETTI router |
| **Purpose** | Business logic | Trust & routing |
| **Data** | Users, devices, settings | FIR/A, intents, audit |
| **Queries** | Jouw app queries | Via SDK/router |
| **Backup** | Jouw backup strategie | BETTI backup |
| **Development** | Volledig onder controle | Separate service |

**Beide databases blijven volledig apart en werken perfect samen via de SDK! 🚀**
