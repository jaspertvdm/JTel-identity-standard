# JTel Identity Standard - Acronyms & Terminology

Complete reference for all acronyms and terminology used in the JTel ecosystem.

## Core Protocols & Architectures

### TIBET
**Time Intent Based Event Token**

Time-boxed intent declarations with event-driven coordination.

- Evolved from earlier concept "TBET" (Time Boxed Event Token)
- Declares intents with time constraints
- Event-driven coordination protocol
- Used in TIBET-BETTI client SDK

**Usage:** "Send TIBET intent", "TIBET protocol", "TIBET-BETTI coordination"

---

### BETTI
**Base Event Token Time Intent**

Universal intent coordination framework implementing 9 natural laws.

- Brain coordination engine
- Validates intents through natural law principles
- Context/Sense/Intent decision layers
- Security layer orchestration

**Usage:** "BETTI coordinator", "BETTI 9 laws", "BETTI validation"

**9 Natural Laws:**
1. Pythagoras - Dimensional structure mapping
2. Einstein - Time and priority relativity
3. Euler - Multi-path resolution
4. Fourier - Pattern detection
5. Maxwell - Context propagation
6. Schrödinger - Intent superposition
7. TCP - State transitions
8. Thermodynamics - System evolution
9. Logarithms - Complexity reduction

---

### JIS
**JTel Identity Standard**

Semantic security layer providing identity and continuity management over existing protocols.

- Works alongside HTTP, MQTT, Matrix, SIP, etc.
- Provides semantic fabric for protocol interoperability
- Identity relationship management
- Continuity chain validation

**Usage:** "JIS protocol", "JIS Router", "JIS Client SDK"

---

## Identity & Cryptography

### FIR/A
**First Initiation Revoke/Accept**

Initial trust token establishment - the first "handshake" between entities.

- **First Initiation** - Initial contact and identity exchange (DID/HID)
- **Revoke/Accept** - Decision point: accept relationship or revoke/reject

Creates genesis moments between entities. Regardless of outcome (revoke or accept), trust can be built from this point forward - there can always be issues, but the relationship started here.

The FIR/A is the beginning of the trust token - the moment entities first interact and establish whether they'll work together.

**Usage:** "FIR/A handshake", "FIR/A relationship", "FIR/A genesis moment"

---

### DID
**Device Identity**

Ed25519 key pairs for device authentication.

- Public key can be shared
- Private key stays on device
- Used for cryptographic signatures
- Device-to-device trust establishment

**Usage:** "DID key", "DID public key", "generate DID"

---

### HID
**Human Identity**

X25519 key pairs for human-device binding.

- **CRITICAL:** Never transmitted over network
- Creates binding hash with DID
- Only binding hash is shared
- Proves human authorization without exposing identity

**Usage:** "HID key", "HID binding", "HID-DID attestation"

---

### IFT
**Intent-First Transmission**

Semantic packet sent before data transmission.

- Declares intent and context before payload
- Creates expected semantic framework
- Enables validation before processing
- Payload-agnostic communication

**Usage:** "Send IFT", "IFT declaration", "Intent-First protocol"

---

### NIR
**Notify / Identify / Rectify**

Three-phase error handling and recovery protocol.

- **Notify** - Flag unexpected behavior or anomaly
- **Identify** - Determine cause and verify identity
- **Rectify** - Resolve issue with human confirmation if needed

Frictionless correction mechanism with human-in-the-loop option.

**Usage:** "Trigger NIR", "NIR recovery", "NIR notification"

---

## Security Layers

### SNAFT
**System Not Authorized For That**

Factory-level security firewall.

- Pre-deployment validation
- Authorization boundary enforcement
- Prevents unauthorized operations at source
- First line of defense

**Implementation:** `betti_snaft.py`

**Usage:** "SNAFT check", "SNAFT validation", "SNAFT blocked"

---

### BALANS
**BETTI Autonomous Layer Analysis Network System**

Pre-execution decision engine with risk assessment.

- Analyzes intent before execution
- Risk scoring and validation
- Context-aware decision making
- Autonomous safety layer

**Implementation:** `betti_balans.py`

**Usage:** "BALANS validation", "BALANS risk score", "BALANS approval"

---

### HICSS
**Halt Intent Change Switch Stop**

Human-in-Control emergency override mechanism.

- Emergency stop for all autonomous operations
- Human intervention layer
- Immediate intent cancellation
- Safety override switch

**Implementation:** `betti_hicss.py`

**Usage:** "HICSS trigger", "HICSS override", "HICSS emergency stop"

---

### Fail2Flag4Intent
**Failure-to-Flag for Intent** (evolved from Fail2Flag)

Automatic anomaly detection and intent flagging system.

- Detects unusual patterns in intent execution
- Automatic flagging for review
- Behavioral anomaly detection
- Triggers NIR when needed

**Implementation:** `betti_fail2flag.py`

**Usage:** "Fail2Flag4Intent detection", "F2F4I trigger", "anomaly flagged"

---

## Continuous Verification (IO/DO/OD)

### IO
**Identity OK**

Continuous human identity verification - "Is the human still who they claim to be?"

- Not just login verification - continuous checking
- Behavioral analysis and pattern matching
- Biometric spot-checks when needed
- Flags suspicious deviations
- Human continuity state

**Implementation:** `io_do_od.py`

**Usage:** "IO check", "IO=OK", "IO flagged", "human continuity"

---

### DO
**Device OK / Device Opt**

Continuous device trustworthiness verification - "Is the device still trustworthy?"

- Device continuity state monitoring
- Internal consistency checks
- Hardware/software integrity validation
- Detects device compromises
- Apparatus continuity state

**Implementation:** `io_do_od.py`

**Usage:** "DO check", "DO=OK", "device continuity", "apparatus state"

---

### OD
**Operation Device / Operation Determination**

Operation validation - "Is this operation allowed on this device?"

- Validates operation against device role
- Checks operation-device compatibility
- Context-aware operation approval
- External consistency between devices
- Operational logic validation

**Implementation:** `io_do_od.py`

**Usage:** "OD check", "OD validation", "operation allowed", "OD rejection"

---

## Content Security (INFC/OFC/SCS)

### INFC
**Initially Not Flaggable Content**

Content without semantic meaning - raw digital objects before intent declaration.

- Photos, documents, media files without context
- Meaningless until paired with intent (IFT)
- Cannot be validated without semantic framework
- Always assessed via DO → OD → IO after mapping

**Flow:** INFC → IFT → OFC

**Usage:** "INFC object", "raw content", "semantically undefined"

---

### OFC
**Operation Flaggable Content**

Content with semantic meaning after intent declaration.

- INFC becomes OFC after receiving IFT + SCS
- Carries semantic provenance (not just crypto)
- Can be validated against intent
- Includes context, origin, and continuity signature
- Flaggable if mismatched with declared intent

**Flow:** INFC + IFT + SCS → OFC

**Components:**
- Original INFC object
- IFT (Intent-First Transmission)
- SCS (Semantic Continuity Signature)
- Context and origin metadata

**Usage:** "OFC validation", "semantic content", "flaggable object"

---

### SCS
**Semantic Continuity Signature**

External, non-forgeable semantic signature for content provenance.

- NOT embedded in the object itself
- Links to continuity chain
- Proves human/device origin without exposing biometrics
- Uses DID derivatives (not HID directly)
- Enables tamper detection through semantic verification

**Key Properties:**
- External to content
- Tied to continuity chain
- Human-origin proof without biometric leakage
- Deepfake/AI-imitation resistant

**Usage:** "SCS verification", "semantic signature", "continuity proof"

---

## System Architecture

### Context/Sense/Intent Layers

Three-layer BETTI decision architecture:

1. **Context Layer** - Environmental awareness, state tracking
2. **Sense Layer** - Rule-based decision making (conditions → intents)
3. **Intent Layer** - Action execution and validation

**Usage:** "Context/Sense/Intent flow", "CSI layers", "Sense rules"

---

### Continuity Chain

Immutable audit trail using SHA-256 linked hashing.

- Every interaction creates hash (incremental continuity_hash)
- Each hash links to previous: `prev_hash + event → new_hash`
- Blockchain-like tamper-evident history
- Complete traceability of all interactions
- Stores IO/DO/OD status, IFT, and OFC/INFC metadata
- HID stays private, only DID/OFC info in chain

**Database:** `continuity_event` table with `continuity_hash_prev` linking

**Usage:** "Continuity chain", "continuity hash", "chain validation", "prev_hash"

---

### Trust Token

Trust relationship token established through FIR/A.

- Begins with FIR/A genesis moment
- Tracked through continuity chain
- Can be built regardless of initial accept/revoke
- Enables relationship history and reputation
- Cryptographically verifiable

**Usage:** "Trust token", "relationship token", "FIR/A token"

---

### Humotica
**Human-Machine Semantic Interaction Layer**

International standard for human-machine communication.

- Semantic interaction protocol
- Human-readable context in every transaction
- Explains "why" behind actions
- International standard for trust

**Usage:** "Humotica context", "Humotica field", "human-readable intent"

---

## System Components

### Brain API
BETTI coordination server (Python/FastAPI).

- Port: 8010 (default)
- BETTI 9 laws implementation
- Security layers orchestration
- PostgreSQL backend

---

### JIS Router
Identity and relationship router (Docker).

- Port: 8081 (default)
- FIR/A protocol handler
- DID/HID key management
- Continuity chain validation

---

## Evolution & Naming

### Historical Changes

- **TBET** → **TIBET** (Time Boxed Event Token evolved to Time Intent Based Event Token)
- **Fail2Flag** → **Fail2Flag4Intent** (More specific to intent validation)

### Consistent Usage

**Correct:**
- TIBET-BETTI protocol
- FIR/A handshake
- DID/HID keys
- BETTI 9 natural laws
- SNAFT/BALANS/HICSS security layers

**Avoid:**
- TBET (outdated)
- Fail2Flag (use Fail2Flag4Intent)
- "TIBET protocol" alone (specify TIBET-BETTI)

---

## Quick Reference Table

| Acronym | Full Name | Category | Key Function |
|---------|-----------|----------|--------------|
| TIBET | Time Intent Based Event Token | Protocol | Time-boxed intent coordination |
| BETTI | Base Event Token Time Intent | Framework | Universal intent validation |
| JIS | JTel Identity Standard | Standard | Semantic security layer |
| FIR/A | First Initiation Revoke/Accept | Protocol | Trust token genesis |
| DID | Device Identity | Crypto | Device authentication |
| HID | Human Identity | Crypto | Human-device binding |
| IFT | Intent-First Transmission | Protocol | Semantic-first communication |
| NIR | Notify/Identify/Rectify | Protocol | Error recovery |
| IO | Identity OK | Verification | Human continuity |
| DO | Device OK/Opt | Verification | Device continuity |
| OD | Operation Device/Determination | Verification | Operation validation |
| INFC | Initially Not Flaggable Content | Content | Semantically undefined object |
| OFC | Operation Flaggable Content | Content | Semantic content with intent |
| SCS | Semantic Continuity Signature | Content | External semantic signature |
| SNAFT | System Not Authorized For That | Security | Factory firewall |
| BALANS | BETTI Autonomous Layer Analysis | Security | Pre-execution validation |
| HICSS | Halt Intent Change Switch Stop | Security | Emergency override |
| F2F4I | Fail2Flag4Intent | Security | Anomaly detection |

---

**Author:** Jasper van de Meent
**Last Updated:** November 2025
**Version:** 1.0.0
