# FOSDEM 2025 Talk Proposal

## Track
Security / Privacy / Decentralization (of: Real Time Communications)

---

## Title

**"Hello World" — But Actually Secure: Building Trust Infrastructure from First Principles**

---

## Subtitle

How a chat app became a new paradigm for provable, human-centric digital communication

---

## Abstract (max 500 words)

A few months ago, I wrote `<html>Hello World</html>` and thought: "What if I could say this to the entire world — and actually prove it was me?"

That question led me down a rabbit hole. Not into blockchain maximalism or zero-trust corporate frameworks, but into something different: What would digital communication look like if we started from human intent rather than security theater?

The result is JTel — an open protocol stack for provable, unforgeable, human-centric communication. Not a product. Infrastructure.

**The core insight:** Traditional security asks "how do we stop bad actors?" But that's the wrong question. The right question is: "how do we make trust buildable, continuous, and provable?"

**What emerged:**

- **JIS (JTel Identity Standard)**: DIDs for devices, HIDs for humans, linked but separate. Your identity isn't your phone — it's you.

- **FIR/A (Flag → Identify → Revoke/Accept)**: Relationships aren't binary. Trust builds through interaction, provably, over time.

- **TBET/BETTI (Time Based Event Tokens)**: Want to make a legally binding call? Declare your intent BEFORE the communication. Both parties commit. The proof exists before you even speak.

- **IO/DO/OD (Identity OK / Device OK / Operation Device)**: Not "login once, trusted forever" but continuous verification. Typing pattern changed? Spot check. Location jumped impossibly? Face verify. The system keeps checking.

- **ContinuityChain**: Every interaction builds on the last. Unbroken proof of everything that happened, without a centralized authority.

**The radical part:** This scales from two friends chatting to government-grade certified communication. Same code. Same protocols. Different configuration. A "Hello World" between friends uses basic FIR/A. A legally binding call between citizen and municipality adds TBET attestation and full chain logging. The architecture doesn't change.

**What this enables:**

- Spoofing becomes structurally impossible (not just "difficult")
- "Registered mail" for any digital communication
- Temporary verified credentials (lost your ID? Police issues you a time-limited verified copy)
- Intent declaration before sensitive operations (no more "the bank called me" scams)
- Privacy AND security (you control your data, cryptographic proof of interactions)

**Running code, not vaporware.** The demo shows three nodes: a phone (Kit app), a Raspberry Pi (edge device with local LLM), and a backend (Brein). Live FIR/A handshake. Live intent verification. Live failover between communication channels. Live IO/DO/OD verification.

This talk is for anyone who thinks digital identity is broken, who's tired of "just trust us" security models, or who wants to see what happens when you design communication infrastructure around humans instead of against them.

The question isn't whether we need this. The question is why we've accepted anything less.

---

## Duration

25 minutes + 5 minutes Q&A (or 45+10 if available)

---

## Speaker Bio

Jasper van de Meent is an independent developer building Kit — a human-centric communication platform — and the JTel protocol stack. He started with "I want a chat app that feels human" and accidentally designed trust infrastructure. Based in the Netherlands. First-time FOSDEM speaker. Has strong opinions about how software should treat people.

---

## Technical Requirements

- HDMI projector connection
- Internet connection (for live demo)
- Raspberry Pi + phone for demo (bringing own hardware)

---

## Outline

1. **The Hook** (3 min)
   - "Hello World" story
   - Why I started building this
   
2. **The Problem** (5 min)
   - Current state of digital identity (broken)
   - Why security-first thinking fails
   - What "trust" actually means

3. **The Architecture** (10 min)
   - JIS: DID-KEY + HID-KEY
   - FIR/A and NIR: Building and flagging trust
   - TBET/BETTI: Pre-declared intent
   - IO/DO/OD: Continuous verification
   - ContinuityChain: Provable history
   - How they fit together

4. **Live Demo** (5 min)
   - Phone ↔ Raspberry Pi ↔ Backend
   - FIR/A handshake
   - Intent verification
   - Spot check trigger

5. **Implications** (3 min)
   - What this enables
   - What changes if this exists
   - The "Hello World" moment

6. **Q&A** (5 min)

---

## Why FOSDEM?

FOSDEM is where infrastructure gets built. Not products — infrastructure. The people in this room understand that protocols matter more than apps, that open beats closed, and that the best security is the kind users don't fight against.

JTel is open. The code exists. It runs. And it needs eyes on it — people who will poke holes, suggest improvements, and maybe build on top of it.

This isn't a pitch. It's an invitation.

---

## Links

- Code: [GitHub link - to be added]
- Documentation: [To be added]
- Contact: [email]

---

## Keywords

identity, decentralized, privacy, security, communication, trust, protocol, open-source, DID, verification

---

*"The command line of the future is not a command line. It's a conversation."*
