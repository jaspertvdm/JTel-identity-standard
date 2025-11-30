# JIS - JTel Identity Standard

**A Semantic Safety Layer for Human-Machine Interaction**

```
Version: 1.0 Draft (2025)
Author:  Jasper van de Meent
License: JOSL (Jasper Open Standard License)
```

---

## What is JIS?

JIS (JTel Identity Standard) is a **protocol layer** that sits on top of existing communication protocols (HTTP, MQTT, SIP, WebRTC, Matrix) to provide:

- **Verifiable Human Identity** (HID)
- **Device Identity & Trust** (DID)
- **Intent-Based Authorization** (TIBET)
- **Semantic Security Validation**

JIS does not replace your existing protocols. It adds a **semantic safety layer** that understands **why** an action is happening, not just **what** is happening.

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

JIS works as a semantic layer on top of:

| Protocol | Use Case |
|----------|----------|
| **SIP/VoIP** | Verified caller identity |
| **WebRTC** | Consent-driven connections |
| **HTTP/REST** | Intent-bound API calls |
| **Matrix** | Context-rich messaging |
| **MQTT/IoT** | Secure device autonomy |

---

## Related Projects

- [Humotica/BETTI](https://github.com/jaspertvdm/Humotica) - Physics-based computing framework
- [JOSL License](https://josl.humotica.com) - Jasper Open Standard License

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
