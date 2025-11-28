# JTel Identity Standard (JIS)
**Author:** Jasper van de Meent (JTel Systems)  
**Contact:** jtmeent@gmail.com  
**License:** Jasper Open Standard License (JOSL)  
**Status:** Draft v0.1 (Public Preview)  
**Year:** 2025

JIS is a **semantic safety and identity layer** designed to secure, verify and humanize
every form of communication and autonomy in the digital world.  
It operates **on top of any protocol**, across humans, devices, AI systems, IoT networks
and autonomous agents.

Traditional authentication proves *who* you are.  
JIS proves **who**, **why**, **in what context**, **with what continuity**,  
and **whether the action makes human sense**.

---

# 🌐 Why JIS?
Modern digital communication is fragmented across ~40 different channels:

- SIP / telephony  
- WebRTC  
- messaging apps  
- email  
- IoT protocols  
- cloud services  
- AI agents  
- identity providers  
- device-to-device traffic  
- autonomous robotics  

All of them authenticate in different ways, lack shared semantics,
and cannot verify **intent**, **context**, or **human continuity**.

JIS solves this by creating a universal semantic layer:

> **Identity + Intent + Context + Continuity + Safety  
> as a single, protocol-agnostic standard.**

---

# 🔐 JIS Building Blocks

## 🟣 1. HID / DID (Human & Device Identity)
- **HID** = Human Identity Key  
- **DID** = Device Identity Key  
- Cryptographic, privacy-first, no raw PII on the wire.  
- Enables human ↔ device ↔ service trust without exposing identity.

---

## 🟣 2. FIR/A — First Intent Relationship Anchor
The “genesis event” of any relationship.

A FIR/A defines:

- roles  
- context  
- participating identities  
- the first continuity hash  
- the semantic meaning of the relationship  

Everything in JIS hangs off a FIR/A.

---

## 🟣 3. Continuity Chains
Every interaction extends the chain.

Each step includes:

- previous hash  
- new hash  
- event type  
- intent  
- context snapshot  

If continuity breaks → **flag**.

If something feels wrong → **notice**.

If something unsafe emerges → **handle** (lockdown or confirm).

---

## 🟣 4. F2F4I — Fail2Flag4Intent  
The **semantic firewall** of JIS.

Flow:

1. **Flag** — Something is off  
2. **Notice** — Something might be off  
3. **Handle** — Action blocked or confirmed  
4. **NIR** — Notify → Identify → Rectify

Unlike Fail2ban, this evaluates **human intention mismatches**, not IP addresses.

---

## 🟣 5. NIR — Notify · Identify · Rectify  
Human-friendly doubt resolution.

JIS escalates to NIR when:

- intent does not match behavior  
- context is unusual  
- timing is suspicious  
- device behavior deviates  
- identity might not be the same human  

Humans confirm through:

- biometrics  
- vocal pattern  
- authenticator  
- context-matching  
- quick HID-proof  

---

## 🟣 6. BETTI — Base Event Token / Task Envelope
A **macro-level permission envelope** describing:

- purpose  
- scope  
- context  
- allowed operations  
- time window  
- safety profile  
- continuity expectations  

BETTI summarises large tasks (calls, workflows, procedures, robotic routines).

---

## 🟣 7. TIBET — Time Intent Based Event Token  
Micro-level permissions, each grounded in time, identity and intent.

TIBET tokens:

- represent *every small step*  
- expire quickly  
- are bound to HID/DID  
- carry continuity hashes  
- serialize autonomy safely  

TIBET = the heartbeat of safe autonomy.

---

## 🟣 8. Humotica — Human Meaning Layer (v1)
Humotica is the semantic understanding of:

- human language  
- tone  
- behavioural patterns  
- context  
- long-term preference models  
- intent modelling  
- safety heuristics  

JIS uses Humotica to answer:

> “Is this action humanly logical, safe, intended, and continuous?”

---

# 🛠 Protocol Bindings
JIS is **protocol-agnostic** and can be applied to any stack:

### 🔉 SIP / VoIP
- Verified calling  
- Aangetekend bellen  
- Caller identity matching  
- TIBET-controlled call setup  
- FIR/A-based caller verification

### 📞 WebRTC
- Verified peer connections  
- Consent & safety envelopes  
- Semantic ‘go/no go’ decisions

### 🔄 HTTP / REST / Webhooks
- Intent-bound requests  
- Safety-aware APIs  
- Non-spoofable action chains

### 🕸 Matrix
- Context-rich events  
- Identity-safe bridging  
- Safety-aware bot logic

### 📡 MQTT / IoT / Robotics
- Device ↔ Device → Human mediation  
- DO/OD semantic role verification  
- Safe autonomy through TIBET chains  
- Anti-hijacking by semantic mismatch detection

---

# 📊 Repository Structure

---

# 📄 Documents Included
- **Overview** – high-level explanation  
- **Identity & FIR/A** – key material, anchors  
- **Fail2Flag4Intent** – semantic firewall  
- **BETTI / TIBET** – autonomy structure  
- **Humotica v1** – human semantics layer  

Each spec is progressively versioned and part of the JOSL.

---

# ⚙ Upcoming Components
- Android SDK (Kit-integrated)  
- Python client library  
- SIP binding via PJSIP/ARI  
- WebRTC negotiation hook  
- IoT/MQTT binding  
- NIR Radar module  
- JIS router (reference implementation)  

---

# 🤝 Governance & Contributions
JIS is governed under the rules in:

**`GOVERNANCE.md`**

All major changes must go through the RFC process in `/rfcs/`.

---

# 🔒 License
JIS is published under the:

### **Jasper Open Standard License (JOSL)**  
(see `LICENSE.md`)

This ensures:

- free implementation  
- open usage  
- preserved authorship  
- no fragmentation  
- safe, unified evolution  

---

# 📬 Contact
**Jasper van de Meent (JTel Systems)**  
📧 **jtmeent@gmail.com**

Open to collaboration, research partnerships, security review, academic work and inter-protocol integration.