"""
KIT API - Template voor TIBET-BETTI Integration

Dit is de API die tussen jouw APP DB en BETTI Router zit.
Implementeert Context, Sense en Intent layers.

Endpoints:
- POST /context/update      - Update user context
- GET  /context/{user_id}   - Get current context
- POST /sense/rules         - Create sense rule
- GET  /sense/rules         - List sense rules
- POST /sense/evaluate      - Evaluate sense rules
- POST /intents/execute     - Execute intent
- WS   /ws/{user_id}        - WebSocket for real-time
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from datetime import datetime
import json
import logging

# Deze zou je vervangen met jouw echte database
# from your_app.database import db, User, Device, SenseRule
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="KIT API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# DATA MODELS
# ============================================================================

class ContextUpdate(BaseModel):
    """Context update request"""
    user_id: str
    context: Dict[str, Any]
    evaluate_sense: bool = True


class SenseRuleCreate(BaseModel):
    """Create sense rule"""
    name: str
    conditions: Dict[str, Any]
    intent: str
    priority: int = 5
    user_id: Optional[str] = None  # None = global rule


class SenseEvaluate(BaseModel):
    """Evaluate sense rules"""
    user_id: str
    context: Optional[Dict[str, Any]] = None


class IntentExecute(BaseModel):
    """Execute intent"""
    intent: str
    context: Dict[str, Any]
    fira_id: str
    user_id: Optional[str] = None


# ============================================================================
# IN-MEMORY STORAGE (vervang met echte database!)
# ============================================================================

# Context store (in productie: Redis of cache)
context_store: Dict[str, Dict[str, Any]] = {}

# Sense rules (in productie: database tabel)
sense_rules: List[Dict[str, Any]] = [
    {
        "id": "rule_001",
        "name": "Evening Lights",
        "conditions": {
            "location": "home",
            "time_of_day": "evening",
            "ambient_light": {"lt": 100}
        },
        "intent": "turn_on_lights",
        "priority": 7,
        "user_id": None  # Global rule
    },
    {
        "id": "rule_002",
        "name": "Morning Routine",
        "conditions": {
            "location": "home",
            "time_of_day": "morning",
            "day_type": "weekday"
        },
        "intent": "morning_briefing",
        "priority": 8,
        "user_id": None
    },
    {
        "id": "rule_003",
        "name": "Coffee Time",
        "conditions": {
            "location": "office",
            "time_of_day": "morning",
            "energy_level": {"lt": 50}
        },
        "intent": "maak_koffie",
        "priority": 6,
        "user_id": None
    }
]

# WebSocket connections
ws_connections: Dict[str, List[WebSocket]] = {}


# ============================================================================
# CONTEXT LAYER - Aggregeert user context uit APP DB
# ============================================================================

@app.post("/context/update")
async def update_context(req: ContextUpdate):
    """
    Update user context

    In productie: Dit leest uit JOUW APP DATABASE
    """
    user_id = req.user_id
    context = req.context

    logger.info(f"Context update for user {user_id}")

    # HIER: Lees uit JOUW APP DATABASE
    # user = db.query(User).filter_by(id=user_id).first()
    # devices = db.query(Device).filter_by(user_id=user_id).all()

    # Voor demo: simuleer database read
    user_from_db = {
        "id": user_id,
        "name": "Demo User",
        "location": context.get("location", "unknown"),
        "preferences": {"theme": "dark", "language": "nl"}
    }

    # Aggregeer context
    full_context = {
        "user_id": user_id,
        "user_name": user_from_db["name"],
        "location": user_from_db["location"],
        "preferences": user_from_db["preferences"],
        "timestamp": datetime.utcnow().isoformat(),
        **context  # Merge incoming context
    }

    # Store in cache (in productie: Redis)
    context_store[user_id] = full_context

    logger.info(f"Context updated: {json.dumps(full_context, indent=2)}")

    # Evaluate sense rules if requested
    triggered_intents = []
    if req.evaluate_sense:
        triggered_intents = await evaluate_sense_internal(user_id, full_context)

    return {
        "status": "updated",
        "context": full_context,
        "triggered_intents": triggered_intents
    }


@app.get("/context/{user_id}")
async def get_context(user_id: str):
    """
    Get current context for user

    Returns cached context + fresh data from APP DB
    """
    # Get from cache
    cached = context_store.get(user_id, {})

    # HIER: Refresh from JOUW APP DATABASE
    # user = db.query(User).filter_by(id=user_id).first()

    # Voor demo: return cached
    if not cached:
        raise HTTPException(status_code=404, detail="Context not found")

    return {
        "user_id": user_id,
        "context": cached,
        "cached_at": cached.get("timestamp")
    }


# ============================================================================
# SENSE LAYER - Pattern matching & auto-trigger rules
# ============================================================================

@app.post("/sense/rules")
async def create_sense_rule(rule: SenseRuleCreate):
    """
    Create a sense rule

    In productie: Store in JOUW APP DATABASE
    """
    rule_id = f"rule_{len(sense_rules) + 1:03d}"

    rule_data = {
        "id": rule_id,
        "name": rule.name,
        "conditions": rule.conditions,
        "intent": rule.intent,
        "priority": rule.priority,
        "user_id": rule.user_id,
        "created_at": datetime.utcnow().isoformat()
    }

    # HIER: Insert into JOUW APP DATABASE
    # db_rule = SenseRule(**rule_data)
    # db.add(db_rule)
    # db.commit()

    # Voor demo: add to memory
    sense_rules.append(rule_data)

    logger.info(f"Sense rule created: {rule.name} → {rule.intent}")

    return rule_data


@app.get("/sense/rules")
async def list_sense_rules(user_id: Optional[str] = None):
    """
    List sense rules

    In productie: Query from JOUW APP DATABASE
    """
    # HIER: Query from database
    # rules = db.query(SenseRule).filter(
    #     (SenseRule.user_id == user_id) | (SenseRule.user_id.is_(None))
    # ).order_by(SenseRule.priority.desc()).all()

    # Filter rules
    filtered = [
        r for r in sense_rules
        if r["user_id"] is None or r["user_id"] == user_id
    ]

    # Sort by priority
    filtered.sort(key=lambda x: x["priority"], reverse=True)

    return {
        "rules": filtered,
        "count": len(filtered)
    }


@app.post("/sense/evaluate")
async def evaluate_sense(req: SenseEvaluate):
    """
    Evaluate sense rules for user

    Returns list of triggered intents
    """
    user_id = req.user_id
    context = req.context

    # Get context if not provided
    if not context:
        cached = context_store.get(user_id)
        if not cached:
            raise HTTPException(status_code=404, detail="Context not found")
        context = cached

    triggered = await evaluate_sense_internal(user_id, context)

    return {
        "user_id": user_id,
        "triggered_intents": triggered,
        "context": context
    }


async def evaluate_sense_internal(user_id: str, context: Dict[str, Any]) -> List[str]:
    """
    Internal sense evaluation logic
    """
    triggered_intents = []

    # Get rules for user (global + user-specific)
    applicable_rules = [
        r for r in sense_rules
        if r["user_id"] is None or r["user_id"] == user_id
    ]

    # Sort by priority
    applicable_rules.sort(key=lambda x: x["priority"], reverse=True)

    logger.info(f"Evaluating {len(applicable_rules)} rules for user {user_id}")

    # Evaluate each rule
    for rule in applicable_rules:
        if matches_conditions(context, rule["conditions"]):
            logger.info(f"✓ Rule matched: {rule['name']} → {rule['intent']}")
            triggered_intents.append(rule["intent"])
        else:
            logger.debug(f"✗ Rule not matched: {rule['name']}")

    return triggered_intents


def matches_conditions(context: Dict[str, Any], conditions: Dict[str, Any]) -> bool:
    """
    Check if context matches all conditions

    Supports:
    - Exact match: {"key": "value"}
    - Comparisons: {"key": {"lt": 100, "gt": 50}}
    - Lists: {"key": ["val1", "val2"]}
    """
    for key, expected in conditions.items():
        actual = context.get(key)

        # Key not in context
        if actual is None:
            return False

        # Exact match
        if isinstance(expected, (str, int, float, bool)):
            if actual != expected:
                return False

        # Comparison operators
        elif isinstance(expected, dict):
            if "lt" in expected and not (actual < expected["lt"]):
                return False
            if "gt" in expected and not (actual > expected["gt"]):
                return False
            if "lte" in expected and not (actual <= expected["lte"]):
                return False
            if "gte" in expected and not (actual >= expected["gte"]):
                return False
            if "eq" in expected and not (actual == expected["eq"]):
                return False
            if "ne" in expected and not (actual != expected["ne"]):
                return False

        # List (any match)
        elif isinstance(expected, list):
            if actual not in expected:
                return False

    return True


# ============================================================================
# INTENT LAYER - Execute intents
# ============================================================================

@app.post("/intents/execute")
async def execute_intent(req: IntentExecute):
    """
    Execute an intent

    This is where YOUR business logic runs!
    Updates YOUR APP DATABASE based on intent
    """
    intent = req.intent
    context = req.context
    fira_id = req.fira_id
    user_id = req.user_id

    logger.info(f"Executing intent: {intent} for user {user_id}")
    logger.info(f"Context: {json.dumps(context, indent=2)}")

    # Route to specific handler
    if intent == "turn_on_lights":
        result = await execute_lights(context, user_id)
    elif intent == "maak_koffie":
        result = await execute_coffee(context, user_id)
    elif intent == "schedule_meeting":
        result = await execute_meeting(context, user_id)
    elif intent == "morning_briefing":
        result = await execute_briefing(context, user_id)
    else:
        result = {
            "status": "error",
            "error": "unknown_intent",
            "message": f"Intent '{intent}' not supported"
        }

    # HIER: Log to YOUR APP DATABASE
    # db.execute(
    #     "INSERT INTO betti_intent_log (user_id, fira_id, intent, status) "
    #     "VALUES (?, ?, ?, ?)",
    #     (user_id, fira_id, intent, result['status'])
    # )
    # db.commit()

    # Notify via WebSocket
    await notify_websocket(user_id, {
        "type": "intent_executed",
        "intent": intent,
        "result": result
    })

    return result


async def execute_lights(context: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    """Execute: turn_on_lights"""
    room = context.get("room", "living_room")
    brightness = context.get("brightness", 100)

    logger.info(f"💡 Turning on lights in {room} at {brightness}%")

    # HIER: Update YOUR APP DATABASE
    # device = db.query(Device).filter_by(user_id=user_id, type='lights', room=room).first()
    # device.status = 'on'
    # device.brightness = brightness
    # db.commit()

    return {
        "status": "completed",
        "intent": "turn_on_lights",
        "room": room,
        "brightness": brightness,
        "message": f"Lights in {room} turned on"
    }


async def execute_coffee(context: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    """Execute: maak_koffie"""
    coffee_type = context.get("type", "zwart")
    size = context.get("size", "normaal")

    logger.info(f"☕ Making {coffee_type} ({size})")

    # HIER: Update YOUR APP DATABASE / Trigger coffee machine

    return {
        "status": "completed",
        "intent": "maak_koffie",
        "coffee_type": coffee_type,
        "size": size,
        "message": f"{coffee_type} ({size}) ready!"
    }


async def execute_meeting(context: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    """Execute: schedule_meeting"""
    attendees = context.get("attendees", 2)
    time_pref = context.get("time", "morning")

    logger.info(f"📅 Scheduling meeting for {attendees} people")

    # HIER: Insert into YOUR APP DATABASE
    # meeting = Meeting(user_id=user_id, attendees=attendees, time=time_pref)
    # db.add(meeting)
    # db.commit()

    return {
        "status": "scheduled",
        "intent": "schedule_meeting",
        "attendees": attendees,
        "time": time_pref,
        "message": f"Meeting scheduled for {attendees} people"
    }


async def execute_briefing(context: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    """Execute: morning_briefing"""
    logger.info(f"📰 Generating morning briefing")

    # HIER: Query YOUR APP DATABASE for briefing data

    return {
        "status": "completed",
        "intent": "morning_briefing",
        "briefing": {
            "weather": "Sunny, 18°C",
            "meetings": "2 today",
            "tasks": "3 high priority"
        },
        "message": "Morning briefing ready"
    }


# ============================================================================
# WEBSOCKET - Real-time updates
# ============================================================================

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """
    WebSocket for real-time TIBET/intent updates
    """
    await websocket.accept()

    # Store connection
    if user_id not in ws_connections:
        ws_connections[user_id] = []
    ws_connections[user_id].append(websocket)

    logger.info(f"WebSocket connected: {user_id}")

    try:
        while True:
            # Wait for messages from client
            data = await websocket.receive_json()

            # Echo back or process
            await websocket.send_json({
                "type": "ack",
                "received": data
            })

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {user_id}")
        ws_connections[user_id].remove(websocket)
        if not ws_connections[user_id]:
            del ws_connections[user_id]


async def notify_websocket(user_id: str, message: Dict[str, Any]):
    """Send message to user's websocket connections"""
    if user_id in ws_connections:
        for ws in ws_connections[user_id]:
            try:
                await ws.send_json(message)
            except:
                pass


# ============================================================================
# HEALTH & INFO
# ============================================================================

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "service": "KIT API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "KIT API",
        "version": "1.0.0",
        "endpoints": {
            "context": [
                "POST /context/update",
                "GET /context/{user_id}"
            ],
            "sense": [
                "POST /sense/rules",
                "GET /sense/rules",
                "POST /sense/evaluate"
            ],
            "intents": [
                "POST /intents/execute"
            ],
            "websocket": [
                "WS /ws/{user_id}"
            ]
        }
    }


# ============================================================================
# RUN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
