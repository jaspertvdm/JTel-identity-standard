# JTel Identity Standard (JIS) – Governance Model
Version: v1.0  
Author: Jasper van de Meent (JTel Systems)  
Contact: jtmeent@gmail.com  
Status: Active

---

## 1. Purpose of Governance
This governance model ensures that JIS:

- evolves consistently  
- preserves its security foundations  
- maintains interoperability across all implementations  
- remains clearly attributed to its author  
- avoids fragmentation  

---

## 2. Roles

### 2.1 Lead Maintainer
**Jasper van de Meent**  
- Maintains the official JIS specification  
- Oversees registries (intents, roles, context keys, flags)  
- Reviews and decides on RFC proposals  
- Manages versioning and releases  
- Approves official bindings (SIP, HTTP, WebRTC, MQTT, IoT, etc.)

### 2.2 Contributors
Contributors may submit:

- Pull Requests  
- RFCs  
- bug reports  
- improvements  
- protocol bindings  

Contributors **do not** have authority to change the standard without approval.

---

## 3. Change Process (RFC)
All non-trivial modifications MUST follow the RFC process:

1. Create a file: `rfcs/NNNN-title.md`  
2. Include motivation, technical details, security impact  
3. Submit via GitHub Pull Request  
4. Review by Lead Maintainer  
5. Lead Maintainer accepts/rejects  
6. Upon acceptance: merged + added to changelog

---

## 4. Versioning
JIS uses **Semantic Versioning (SemVer)**:

- **MAJOR** – breaking changes in semantics or protocol  
- **MINOR** – new features or extensions  
- **PATCH** – clarifications, typo fixes, non-breaking changes  

Each release MUST contain:

- Release notes  
- Updated spec documents  
- A Git tag  
- Registry changes if applicable

---

## 5. Registries
The Lead Maintainer manages:

- Intent Registry  
- Role Registry  
- Context Key Registry  
- Device Operation Types (DO/OD)  
- Flag / Notice / Handle codes  
- TBET categories  
- FIR/A attributes  

Registries cannot be overridden by third parties; only extended by RFC.

---

## 6. Forks
Forks are permitted, but MUST:

- use different naming (not "JIS")  
- not claim official status  
- declare non-conformance  
- remain distinguishable  

Forks aiming for compatibility are welcome via the RFC process.

---

## 7. Ownership & Continuity
The JIS standard is authored and maintained by:

**Jasper van de Meent (JTel Systems)**  
📧 **jtmeent@gmail.com**

Governance may be transferred only by explicit, public announcement by the Lead Maintainer.

---

## 8. Security Considerations
All proposals must consider:

- semantic integrity  
- continuity-chain impact  
- flag/notice/handle logic  
- NIR pathways  
- privacy  
- identity leakage  
- concurrency  
- inter-protocol consistency  

Security is central to JIS.

---