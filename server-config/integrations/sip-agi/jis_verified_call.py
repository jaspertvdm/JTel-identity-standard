#!/usr/bin/env python3
"""
JIS Verified Calling - Asterisk AGI Script
==========================================

Features:
- DID/HID key verification
- Anti-spoofing via HID binding
- Caller identity validation
- TBET intent routing
- Real-time verification display

Setup:
1. Place in /var/lib/asterisk/agi-bin/
2. chmod +x jis_verified_call.py
3. Set env: JIS_BASE, JIS_SECRET
4. Dialplan: AGI(jis_verified_call.py)

Example Dialplan:
[verified-calling]
exten => _X.,1,NoOp(JIS Verified Call)
 same => n,AGI(jis_verified_call.py)
 same => n,GotoIf($["${JIS_VERIFIED}"="true"]?verified:unverified)
 same => n(verified),Playback(call-from-verified-caller)
 same => n,Set(CALLERID(name)=✓ ${JIS_CALLER_NAME})
 same => n,Dial(SIP/${EXTEN},30)
 same => n,Hangup()
 same => n(unverified),Playback(unverified-caller)
 same => n,Hangup()
"""

import json
import os
import sys
import urllib.request
import urllib.error
from typing import Dict, Optional, Tuple


class AGIEnvironment:
    """Parse AGI environment variables"""

    def __init__(self):
        self.env = {}
        self._read_env()

    def _read_env(self):
        """Read AGI environment from stdin"""
        for line in sys.stdin:
            line = line.strip()
            if line == "":
                break
            if ":" in line:
                key, value = line.split(":", 1)
                self.env[key.strip()] = value.strip()

    def get(self, key: str, default: str = "") -> str:
        """Get environment variable"""
        return self.env.get(key, default)

    @property
    def caller_number(self) -> str:
        """Get caller phone number"""
        return self.get("agi_callerid", "unknown")

    @property
    def callee_number(self) -> str:
        """Get called number (extension)"""
        return self.get("agi_extension", "unknown")

    @property
    def caller_name(self) -> str:
        """Get caller name (if available)"""
        return self.get("agi_calleridname", "Unknown")

    @property
    def unique_id(self) -> str:
        """Get unique call ID"""
        return self.get("agi_uniqueid", "")


class JISClient:
    """Simplified JIS Router client for AGI"""

    def __init__(self, base_url: str, secret: str):
        self.base_url = base_url.rstrip('/')
        self.secret = secret
        self.headers = {
            "Content-Type": "application/json",
            "X-JIS-SECRET": secret
        }

    def _request(self, endpoint: str, payload: Dict) -> Dict:
        """Make POST request to JIS Router"""
        url = f"{self.base_url}{endpoint}"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=self.headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body)
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            raise Exception(f"HTTP {e.code}: {error_body}")
        except urllib.error.URLError as e:
            raise Exception(f"Connection error: {e}")

    def init_call_relationship(
        self,
        caller: str,
        callee: str,
        caller_did_public: Optional[str] = None,
        hid_binding: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Initialize FIR/A for call with optional DID/HID

        Returns: (fir_a_id, continuity_hash)
        """
        payload = {
            "initiator": f"caller_{caller}",
            "responder": f"callee_{callee}",
            "roles": ["caller", "telephony"],
            "context": {
                "caller_number": caller,
                "callee_number": callee,
                "call_type": "voice"
            },
            "humotica": f"Voice call from {caller} to {callee}"
        }

        # Add DID key if provided
        if caller_did_public:
            payload["initiator_did"] = {
                "did_public": caller_did_public,
                "hid_did_binding": hid_binding
            }

        response = self._request("/fira/init", payload)
        return response["fir_a_id"], response["continuity_hash"]

    def send_call_intent(
        self,
        fir_a_id: str,
        intent: str,
        context: Dict,
        continuity_hash_prev: str
    ) -> Dict:
        """Send call-related intent"""
        payload = {
            "fir_a_id": fir_a_id,
            "intent": intent,
            "context": context,
            "timebox_seconds": 60,
            "continuity_hash_prev": continuity_hash_prev
        }

        return self._request("/ift", payload)

    def get_caller_identity(self, phone_number: str) -> Optional[Dict]:
        """
        Get registered caller identity from router

        This queries the router for a pre-registered phone number
        Returns DID keys and verified name if available
        """
        # In production, this would be a GET endpoint
        # For now, we'll use a convention: check for FIR/A with this phone
        # In real implementation, add GET /identities/{phone_number} endpoint
        return None  # TODO: Implement identity lookup endpoint


class AGIInterface:
    """Communicate with Asterisk via AGI protocol"""

    @staticmethod
    def verbose(message: str, level: int = 1):
        """Send verbose message to Asterisk"""
        sys.stdout.write(f'VERBOSE "{message}" {level}\n')
        sys.stdout.flush()

    @staticmethod
    def set_variable(name: str, value: str):
        """Set channel variable"""
        sys.stdout.write(f'SET VARIABLE {name} "{value}"\n')
        sys.stdout.flush()

    @staticmethod
    def get_variable(name: str) -> str:
        """Get channel variable"""
        sys.stdout.write(f'GET VARIABLE {name}\n')
        sys.stdout.flush()
        result = sys.stdin.readline().strip()
        # Parse result (200 result=1 (value))
        if "(" in result and ")" in result:
            return result.split("(")[1].split(")")[0]
        return ""


def main():
    """Main AGI script logic"""

    # Initialize
    agi = AGIInterface()
    env = AGIEnvironment()

    # Configuration
    jis_base = os.getenv("JIS_BASE", "http://router:8081")
    jis_secret = os.getenv("JIS_SECRET", "")
    tbet_enabled = os.getenv("TBET_ENABLED", "true").lower() == "true"

    if not jis_secret:
        agi.verbose("ERROR: JIS_SECRET not configured", 1)
        agi.set_variable("JIS_VERIFIED", "false")
        agi.set_variable("JIS_ERROR", "no_secret")
        return

    agi.verbose(f"JIS Verified Calling: {env.caller_number} -> {env.callee_number}", 2)

    try:
        client = JISClient(jis_base, jis_secret)

        # Step 1: Check if caller is pre-registered with DID/HID
        caller_identity = client.get_caller_identity(env.caller_number)

        if caller_identity:
            agi.verbose(f"✓ Caller {env.caller_number} is VERIFIED (has DID/HID)", 2)
            verified = True
            caller_name = caller_identity.get("name", env.caller_name)
            did_public = caller_identity.get("did_public")
            hid_binding = caller_identity.get("hid_binding")
        else:
            agi.verbose(f"⚠ Caller {env.caller_number} is UNVERIFIED (no DID/HID)", 2)
            verified = False
            caller_name = env.caller_name
            did_public = None
            hid_binding = None

        # Step 2: Initialize FIR/A relationship
        fir_a_id, continuity_hash = client.init_call_relationship(
            env.caller_number,
            env.callee_number,
            did_public,
            hid_binding
        )

        agi.verbose(f"✓ FIR/A created: {fir_a_id}", 2)

        # Step 3: Send call setup intent (TBET)
        intent = "verified_call_setup" if verified else "unverified_call_setup"

        if tbet_enabled:
            # TBET: Intent-based routing
            # The intent determines call handling policy
            agi.verbose(f"TBET Intent: {intent}", 2)

        call_response = client.send_call_intent(
            fir_a_id,
            intent,
            {
                "caller_number": env.caller_number,
                "caller_name": caller_name,
                "callee_number": env.callee_number,
                "verified": verified,
                "has_did": did_public is not None,
                "has_hid_binding": hid_binding is not None,
                "call_id": env.unique_id
            },
            continuity_hash
        )

        # Step 4: Set Asterisk variables for dialplan
        agi.set_variable("JIS_VERIFIED", "true" if verified else "false")
        agi.set_variable("JIS_FIR_A_ID", fir_a_id)
        agi.set_variable("JIS_CALLER_NAME", caller_name)
        agi.set_variable("JIS_INTENT", intent)
        agi.set_variable("JIS_CONTINUITY_HASH", call_response["continuity_hash"])

        # Success message
        status = "VERIFIED ✓" if verified else "UNVERIFIED ⚠"
        agi.verbose(f"JIS Call Setup Complete: {status}", 1)
        agi.verbose(f"  FIR/A: {fir_a_id}", 1)
        agi.verbose(f"  Intent: {intent}", 1)
        agi.verbose(f"  Caller: {caller_name}", 1)

    except Exception as e:
        agi.verbose(f"JIS ERROR: {e}", 1)
        agi.set_variable("JIS_VERIFIED", "false")
        agi.set_variable("JIS_ERROR", str(e))


if __name__ == "__main__":
    main()
