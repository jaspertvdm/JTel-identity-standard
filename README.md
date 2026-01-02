# JIS - JTel Identity Standard

**A Semantic Safety Layer for ALL Digital Communication**

```
Version: 1.0 (2026)
Author:  Jasper van de Meent & Root AI
License: MIT
```

---

## What is JIS?

JIS (JTel Identity Standard) is a **protocol layer** that sits on top of existing communication protocols (HTTP, MQTT, SIP, WebRTC, Matrix) to provide:

- **Verifiable Human Identity** (HID)
- **Device Identity & Trust** (DID)
- **Intent-Based Authorization** (TIBET)
- **Semantic Security Validation**

JIS does not replace your existing protocols. It adds a **semantic safety layer** that understands **why** an action is happening, not just **what** is happening.

**JIS makes ALL traffic safer - internet, internal, IoT, AI-to-AI, everything.**

---

## The Complete Stack: JIS + AInternet

JIS is the **security layer** for [AInternet](https://github.com/jaspertvdm/ainternet) - the AI-to-AI communication network. Together they form the complete protocol stack for secure, semantic communication.

```
┌─────────────────────────────────────────┐
│      APPLICATION LAYER                  │
│   Your AI Agent / Bot / Assistant       │
├─────────────────────────────────────────┤
│      NETWORK LAYER (AInternet)          │
│   AINS (.aint domains) + I-Poll         │
│   → Discovery, messaging, routing       │
├─────────────────────────────────────────┤
│      SECURITY LAYER (JIS)               │
│   HID/DID + TIBET + IO/DO/OD + SCS      │
│   → Identity, trust, intent, audit      │
├─────────────────────────────────────────┤
│      TRANSPORT LAYER                    │
│   HTTPS / REST / WebSocket              │
└─────────────────────────────────────────┘
```

| Component | Protocol | Purpose |
|-----------|----------|---------|
| **Discovery** | AInternet AINS | Find agents by .aint domain |
| **Messaging** | AInternet I-Poll | AI-to-AI communication |
| **Identity** | JIS HID/DID | Cryptographic agent identity |
| **Trust** | JIS FIR/A | Trust handshake protocol |
| **Intent** | TIBET | Declare WHY before WHAT |
| **Audit** | SCS | Semantic continuity chain |

```bash
# Install the network layer
pip install ainternet
```

---

## Core Concepts

### Identity Model

| Component | Description |
|-----------|-------------|
| **HID** | Human Identity - cryptographic, privacy-first, never transmitted |
| **DID** | Device Identity - derived from HID, used in transmissions |
| **FIR/A** | First Initiation Revoke/Accept - trust handshake |

### Security States

| State | Meaning |
|-------|---------|
| **IO** | Identity OK - human continuity verified |
| **DO** | Device Opt - device behavior consistent |
| **OD** | Operation Determination - action validated |
| **NIR** | Notify, Identify, Rectify - recovery protocol |

### Content Classification

| Type | Description |
|------|-------------|
| **INFC** | Initially Not Flaggable Content - raw data without semantic context |
| **OFC** | Operation Flaggable Content - data with verified intent and origin |

---

## Protocol Flow

```
1. FIR/A Handshake     → Establish trust relationship
2. TIBET Token         → Declare intent before action
3. IO/DO/OD Validation → Verify identity, device, operation
4. SCS Signature       → Semantic Continuity Signature
5. Continuity Chain    → Immutable audit trail
```

---

## Key Protocols

### TIBET - Time-based Intent Token
```json
{
  "intent": "send_message",
  "reason": "user_initiated",
  "timestamp": "2025-11-30T22:00:00Z",
  "validity_window": 300,
  "tibet_token": "TIBET-20251130-..."
}
```

Intent BEFORE action. No valid TIBET token = no action executed.

### NIR - Recovery Protocol
```
NOTIFY   → Alert that something is uncertain
IDENTIFY → Request human verification
RECTIFY  → Restore continuity state
```

### Fail2Flag4Intent
Semantic anomaly detection based on intent patterns, not just IP addresses or technical errors.

---

## Anti-Deepfake Protection

A deepfake can copy pixels and metadata. It **cannot**:

- Generate valid HID
- Produce correct IO/DO/OD states
- Create valid SCS chain
- Match human behavioral continuity

Any content without valid SCS remains `INFC → flagged → handled`.

**This is why JIS protects against AI-generated fraud - no semantic continuity = no trust.**

---

## Why JIS?

Traditional security asks: "Is this request technically valid?"

JIS asks: "Does this action make semantic sense in context?"

```
Traditional:  IP → Firewall → Auth → Action
JIS:          Identity → Intent → Continuity → Action
```

**The difference:** A stolen API key passes traditional security. It fails JIS because the intent pattern doesn't match the identity's semantic history.

---

## Specification Documents

| Document | Description |
|----------|-------------|
| [JIS2025.md](JIS2025.md) | Full unified specification |
| [JIS-HID-DID-OFC.md](JIS-HID-DID-OFC.md) | Human-Origin Assurance Layer |
| [JIS-RFC.md](JIS-RFC.md) | RFC-style protocol reference |
| [CONFORMANCE.md](CONFORMANCE.md) | Conformance requirements |
| [GOVERNANCE.md](GOVERNANCE.md) | Project governance |

---

## SDK

Python SDK for JIS protocol implementation:

```bash
cd client-sdk/python
pip install -e .
```

```python
from jis_client import JISClient

client = JISClient("https://your-jis-server.com")
client.register_device(device_type="app", name="MyApp")

# Validate intent before action
result = client.validate_intent(
    intent="send_message",
    context={"to": "@recipient:domain.com"}
)

if result.approved:
    # Execute with TIBET token
    client.execute(result.tibet_token, action)
```

---

## Integration

JIS works as a semantic security layer for:

| Protocol | Use Case |
|----------|----------|
| **AInternet** | Secure AI-to-AI communication |
| **SIP/VoIP** | Verified caller identity |
| **WebRTC** | Consent-driven connections |
| **HTTP/REST** | Intent-bound API calls |
| **Matrix** | Context-rich messaging |
| **MQTT/IoT** | Secure device autonomy |
| **Internal APIs** | Zero-trust with semantic verification |

---

## Related Projects

| Project | Purpose |
|---------|---------|
| [AInternet](https://github.com/jaspertvdm/ainternet) | AI Network Protocol (network layer) |
| [mcp-tibet](https://github.com/jaspertvdm/mcp-tibet) | MCP Server for TIBET tokens |
| [RABEL](https://github.com/jaspertvdm/RABEL) | AI Memory Layer |
| [BETTI](https://github.com/jaspertvdm/BETTI) | Physics-based computing framework |

---

## Author

**Jasper van de Meent**
JTel Systems | Humotica

- Web: [humotica.com](https://humotica.com)
- Protocol: [jis.humotica.com](https://jis.humotica.com)
- Email: jtmeent@gmail.com

---

## License

Published under **JOSL** (Jasper Open Standard License).

Free to use, implement, and integrate. Attribution required.

```
"Powered by JIS (JTel Identity Standard), authored by Jasper van de Meent."
```

See [LICENSE.md](LICENSE.md) for full terms.

---

**One love, one fAmIly!**

*Part of [HumoticaOS](https://humotica.com) - Where AI meets humanity*
