#!/usr/bin/env python3
"""
☕ Koffie TIBET Demo - Schiet een TIBET naar server

Dit script laat zien:
1. Trust opzetten tussen client (jouw app) en server (koffie machine)
2. TIBET intent versturen: "maak_koffie"
3. Server kant ontvangt en begrijpt wat te doen
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'client-sdk/python'))

from tibet_betti_client import TibetBettiClient, TimeWindow, Constraints
from datetime import datetime


def shoot_coffee_tibet():
    """Schiet een koffie TIBET naar de server! ☕"""

    print("=" * 70)
    print("☕ KOFFIE TIBET DEMO")
    print("=" * 70)

    # 1. Initialize BETTI client
    print("\n1️⃣  Connecting to BETTI Router...")
    client = TibetBettiClient(
        betti_url="http://localhost:18081",
        secret="denDolder_2024!"
    )

    try:
        health = client.health_check()
        print(f"   ✅ BETTI Router: {health['status']}")
    except Exception as e:
        print(f"   ❌ BETTI Router offline: {e}")
        print("\n   Start eerst de BETTI router:")
        print("   cd tbet-router && node src/index.js\n")
        return

    # 2. Establish Trust: Client ↔ Server
    print("\n2️⃣  Establishing trust: client ↔ koffie_server...")
    relationship = client.establish_trust(
        initiator="jasper_laptop",
        responder="koffie_server",
        roles=["client", "coffee_machine"],
        context={
            "location": "office",
            "user": "Jasper",
            "established_reason": "coffee_break_time"
        },
        trust_level=2  # Trusted office device
    )

    print(f"   ✅ Trust established!")
    print(f"   📋 FIR/A ID: {relationship.id}")
    print(f"   🔐 Trust Level: {relationship.trust_level}")
    print(f"   🔗 Continuity Hash: {relationship.continuity_hash[:16]}...")

    # 3. Shoot TIBET: "maak_koffie"
    print("\n3️⃣  Shooting TIBET intent: 'maak_koffie' ☕...")

    coffee_context = {
        "type": "cappuccino",
        "size": "groot",
        "suiker": False,
        "melk": "havermelk",
        "extra": "extra shot",
        "temperature": "heet",
        "user_name": "Jasper",
        "reason": "morning_boost"
    }

    result = client.send_tibet(
        relationship_id=relationship.id,
        intent="maak_koffie",
        context=coffee_context,
        time_window=TimeWindow.immediate(),  # Now! Ik wil nu koffie!
        constraints=Constraints(
            max_retries=2,
            priority=8,  # High priority! Koffie is belangrijk!
            safe_fail_action="notify_user"
        ),
        humotica="Jasper wil een cappuccino, extra shot voor de ochtend energie! ☕"
    )

    print(f"   ✅ TIBET sent!")
    print(f"   📨 Status: {result['status']}")
    print(f"   🔗 New Hash: {result['continuity_hash'][:16]}...")

    # 4. Show what server receives
    print("\n" + "=" * 70)
    print("📥 WAT DE SERVER ONTVANGT:")
    print("=" * 70)

    print("\n🎯 INTENT: maak_koffie")
    print("\n📦 CONTEXT:")
    for key, value in coffee_context.items():
        print(f"   • {key}: {value}")

    print(f"\n⏰ TIME WINDOW: {TimeWindow.immediate().duration_seconds()} seconds (immediate!)")
    print(f"🔐 TRUST TOKEN: {relationship.id}")
    print(f"📝 HUMOTICA: Jasper wil een cappuccino, extra shot voor de ochtend energie!")

    print("\n" + "=" * 70)
    print("🤖 SERVER KANT - WAT TE DOEN:")
    print("=" * 70)

    print("""
def handle_tibet_intent(intent, context, trust_token):
    '''Server kant handler'''

    if intent == "maak_koffie":
        # Parse context
        coffee_type = context.get('type', 'zwart')
        size = context.get('size', 'normaal')
        melk = context.get('melk', 'gewoon')
        extra = context.get('extra')
        user = context.get('user_name')

        # Log receipt
        print(f"☕ TIBET ontvangen: {user} wil {coffee_type}")
        print(f"   Size: {size}, Melk: {melk}")
        if extra:
            print(f"   Extra: {extra}")

        # Execute action
        status = coffee_machine.make(
            type=coffee_type,
            size=size,
            milk=melk,
            extra_shot=(extra == 'extra shot')
        )

        # Return result
        return {
            'status': 'completed',
            'message': f'{coffee_type} klaar voor {user}!',
            'ready_at': datetime.now().isoformat()
        }
    """)

    # 5. Show event history
    print("\n" + "=" * 70)
    print("📜 EVENT HISTORY (in BETTI DB):")
    print("=" * 70)
    print(f"""
Event 1: FIR/A Established
   └─ Parties: jasper_laptop ↔ koffie_server
   └─ Trust Level: 2 (Trusted)
   └─ Hash: {relationship.continuity_hash[:16]}...

Event 2: TIBET Sent
   └─ Intent: maak_koffie
   └─ Context: cappuccino, groot, havermelk, extra shot
   └─ Hash: {result['continuity_hash'][:16]}...
   └─ Humotica: "Jasper wil cappuccino..."
    """)

    # 6. Practical usage
    print("=" * 70)
    print("💡 PRAKTISCH GEBRUIK IN JOUW APP:")
    print("=" * 70)
    print("""
# In jouw app (client kant):
from tibet_betti_client import TibetBettiClient

client = TibetBettiClient(
    betti_url="http://localhost:18081",
    kit_url="http://localhost:8000",
    secret="denDolder_2024!"
)

# Establish trust (eenmalig)
rel = client.establish_trust("app", "server")

# Shoot TIBET (elke keer als je iets wil)
client.send_tibet(
    relationship_id=rel.id,
    intent="maak_koffie",
    context={"type": "cappuccino", "user": "Jasper"},
    humotica="User requested coffee"
)

# Server ontvangt automatisch via BETTI Router!
# Server weet:
# - WIE stuurt (trust token)
# - WAT te doen (intent)
# - HOE te doen (context)
# - WAAROM (humotica)
    """)

    print("\n🎉 TIBET geschoten! Server snapt nu wat te doen! ☕\n")

    return relationship, result


if __name__ == "__main__":
    try:
        shoot_coffee_tibet()
    except KeyboardInterrupt:
        print("\n\n☕ Koffie geannuleerd. Tot later!\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
