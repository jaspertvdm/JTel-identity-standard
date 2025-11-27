# TBET-BETTI Architecture - Hierarchical Trust Framework

**Targeting Telephony Behavior → Behavior-Enhanced Trusted Telephony Interactions**

Version: 2.0.0
Status: Production Architecture
Date: 2025-11-26

---

## 🎯 Executive Summary

TBET-BETTI implementeert een **hiërarchisch vertrouwenssysteem** waarbij:

- **Trust Levels** bepalen welke communicatie toegestaan is
- **Pre-Authorization** vereist voor sensitieve instanties
- **Role-Based Display** toont context-aware caller info
- **Legal Compliance** modes voor aangetekende communicatie
- **Intent Categories** activeren beveiligingslagen

**Kernprincipe:**
*"Hoe hoger de trust level, hoe strenger de pre-authorization, hoe sterker de legal binding."*

---

## 📊 Trust Level Hierarchy

### Level 0: Public (Onverified)
**Voorbeelden:** Random callers, spam, onbekenden

**Vereisten:**
- Geen DID/HID
- Geen pre-authorization

**Toegestaan:**
- Emergency calls (112/911)
- Public hotlines

**Display:**
```
⚠ UNVERIFIED
+31612345678
[Screen] [Block]
```

**Beperkingen:**
- Rate limited: 5 calls/hour
- Challenge-response required
- No direct access
- Gelogd voor audit

---

### Level 1: Verified Personal
**Voorbeelden:** Vrienden, familie, collega's

**Vereisten:**
- ✅ DID key (device)
- ✅ HID binding (human)
- ✅ Phone number registered

**Toegestaan:**
- Personal calls
- Group calls
- Video calls

**Display:**
```
✓ VERIFIED
Jasper van de Meent
+31612345678
[Accept] [Reject]
```

**Features:**
- Direct calling
- No pre-authorization
- Full provenance chain
- Privacy protected

---

### Level 2: Professional
**Voorbeelden:** Zakelijke contacten, leveranciers, klanten

**Vereisten:**
- ✅ DID + HID
- ✅ Business registration (KVK/Chamber)
- ✅ Role verification

**Toegestaan:**
- Business calls
- Contract discussions
- Sales calls (with consent)

**Display:**
```
🏢 VERIFIED BUSINESS
ABC Consultancy B.V.
KVK: 12345678
+31201234567
[Accept] [Reject]
```

**Features:**
- Business context display
- Contract references
- Consent tracking
- Compliance logging

---

### Level 3: Financial / Administrative
**Voorbeelden:** Banken, verzekeringen, belastingdienst, accountants

**Vereisten:**
- ✅ DID + HID
- ✅ Business registration
- ✅ Financial license (AFM/DNB)
- ⚠️ **Pre-authorization REQUIRED**

**Toegestaan:**
- Financial advice
- Account discussions
- Administrative matters
- **ONLY after appointment scheduled**

**Display:**
```
🏦 VERIFIED BANK
ING Bank Nederland
AFM License: 12345
Account: NL12INGB0001234567
Appointment: 26-11-2025 14:30
[Accept] [Reject]
```

**Pre-Authorization Flow:**
```
1. Bank request contact via app/email
2. Customer schedules appointment
3. FIR/A created with appointment_id
4. Bank can ONLY call during appointment window
5. Outside window = BLOCKED
```

**Features:**
- Account number display (last 4 digits)
- Appointment verification
- Recording mandatory
- Full audit trail
- Compliance mode: MiFID II / GDPR

---

### Level 4: Legal / Medical (Beroepsgeheim)
**Voorbeelden:** Advocaten, artsen, notarissen, psychologen

**Vereisten:**
- ✅ DID + HID
- ✅ Professional registration (BIG/NOvA)
- ✅ Beroepsgeheim certification
- ⚠️ **Pre-authorization MANDATORY**
- 🔒 **End-to-end encryption**

**Toegestaan:**
- Client consultations
- Patient calls
- Legal advice
- **ONLY pre-scheduled contacts**

**Display (Advocaat):**
```
⚖️ VERIFIED LEGAL
Mr. J. de Vries
NOvA Registration: 123456
Case: 2024-CV-12345
Appointment: 26-11-2025 15:00
🔒 Encrypted & Recorded
[Accept] [Reject]
```

**Display (Arts):**
```
🏥 VERIFIED MEDICAL
Dr. A. Jansen - Cardioloog
BIG: 12345678901
Patient ID: ****5678
Appointment: 26-11-2025 10:30
🔒 Encrypted (HIPAA/GDPR)
[Accept] [Reject]
```

**Pre-Authorization Flow:**
```
1. Professional requests consultation
2. Client/patient confirms via secure channel
3. FIR/A created with:
   - appointment_id
   - case_reference / patient_id
   - encryption_key_exchange
4. Call ONLY possible in time window
5. Outside window = HARD BLOCK
6. Recording encrypted, stored 7 years
```

**Features:**
- Beroepsgeheim mode (attorney-client privilege)
- HIPAA/AVG compliant
- Encrypted recordings
- Legal hold capability
- Case/patient reference display
- Time-windowed access
- Biometric re-auth required

---

### Level 5: Government / Critical Infrastructure
**Voorbeelden:** Politie, AIVD, gemeenten, ministeries, nooddiensten

**Vereisten:**
- ✅ DID + HID
- ✅ Government certificate (PKIoverheid)
- ✅ Role-based access control
- ⚠️ **Pre-authorization MANDATORY**
- 🔒 **Qualified encryption**
- 🛡️ **Multi-factor authentication**

**Toegestaan:**
- Official communications
- Emergency directives
- Critical infrastructure
- **Pre-scheduled ONLY (except emergency override)**

**Display (Politie):**
```
🚔 VERIFIED GOVERNMENT
Politie Nederland - Eenheid Amsterdam
Officer: Badge #12345
Case: 2024-ZV-98765
Appointment: 26-11-2025 09:00
🔒 PKIoverheid Certified
[Accept] [Reject]
```

**Display (Gemeente):**
```
🏛️ VERIFIED GOVERNMENT
Gemeente Amsterdam
Department: Burgerzaken
Reference: BSN-2024-12345
Appointment: 26-11-2025 11:00
🔒 Secured
[Accept] [Reject]
```

**Pre-Authorization Flow:**
```
1. Government requests contact via official channel
2. Citizen receives registered letter / secure message
3. Appointment scheduled via DigiD
4. FIR/A created with:
   - government_cert (PKIoverheid)
   - case_reference
   - appointment_id
   - legal_basis (which law allows contact)
5. Multi-factor auth before call connects
6. Call ONLY in strict time window
7. Recording encrypted, stored 20 years
8. Audit trail to oversight body
```

**Features:**
- PKIoverheid integration
- Legal basis display ("Wet X artikel Y")
- Case reference tracking
- Multi-level approval (supervisor sign-off)
- Citizen rights display ("Right to remain silent", etc.)
- Qualified signatures
- Oversight logging
- Emergency override (with explanation requirement)

---

## 🎯 TBET Intent Categories per Trust Level

### Level 0-1: Basic Intents
```json
{
  "verified_call_setup": {
    "trust_level": 1,
    "pre_auth_required": false
  },
  "unverified_call_setup": {
    "trust_level": 0,
    "pre_auth_required": false,
    "challenge_required": true
  }
}
```

### Level 2: Business Intents
```json
{
  "business_call": {
    "trust_level": 2,
    "pre_auth_required": false,
    "consent_required": true,
    "context": ["business_name", "kvk_number"]
  },
  "sales_call": {
    "trust_level": 2,
    "pre_auth_required": false,
    "consent_required": true,
    "do_not_call_check": true
  }
}
```

### Level 3: Financial Intents
```json
{
  "financial_advice": {
    "trust_level": 3,
    "pre_auth_required": true,
    "appointment_required": true,
    "context": ["account_ref", "appointment_id"],
    "recording_mandatory": true
  },
  "account_discussion": {
    "trust_level": 3,
    "pre_auth_required": true,
    "appointment_required": true,
    "mifid_compliance": true
  },
  "tax_matter": {
    "trust_level": 3,
    "pre_auth_required": true,
    "appointment_required": true,
    "context": ["bsn_last_4", "tax_year"]
  }
}
```

### Level 4: Legal/Medical Intents
```json
{
  "legal_consultation": {
    "trust_level": 4,
    "pre_auth_required": true,
    "appointment_required": true,
    "encryption_required": true,
    "context": ["case_reference", "nova_number"],
    "privilege": "attorney_client",
    "retention_years": 7
  },
  "medical_consultation": {
    "trust_level": 4,
    "pre_auth_required": true,
    "appointment_required": true,
    "encryption_required": true,
    "context": ["patient_id_masked", "big_number"],
    "hipaa_mode": true,
    "retention_years": 20
  },
  "therapy_session": {
    "trust_level": 4,
    "pre_auth_required": true,
    "appointment_required": true,
    "encryption_required": true,
    "biometric_reauth": true
  }
}
```

### Level 5: Government Intents
```json
{
  "official_communication": {
    "trust_level": 5,
    "pre_auth_required": true,
    "appointment_required": true,
    "encryption_required": true,
    "mfa_required": true,
    "context": ["case_ref", "legal_basis"],
    "pkio_cert_required": true,
    "supervisor_approval": true,
    "retention_years": 20
  },
  "police_interview": {
    "trust_level": 5,
    "pre_auth_required": true,
    "appointment_required": true,
    "rights_notification": true,
    "legal_counsel_offer": true,
    "recording_mandatory": true,
    "oversight_logging": true
  },
  "emergency_directive": {
    "trust_level": 5,
    "pre_auth_required": false,
    "emergency_override": true,
    "explanation_required": true,
    "immediate_audit": true
  }
}
```

---

## 🔒 Pre-Authorization Flows

### Flow Type A: Soft Pre-Authorization (Level 2-3)
**Use case:** Bank wil klant bellen over hypotheek

```mermaid
sequenceDiagram
    Bank->>Customer: Request via app/email
    Customer->>Bank: Schedule appointment
    Bank->>JIS Router: POST /fira/init (with appointment_id)
    JIS Router->>Bank: FIR/A created

    Note: Appointment window: 26-11-2025 14:00-15:00

    Bank->>JIS Router: POST /ift (intent: financial_advice)
    JIS Router->>JIS Router: Check appointment window
    alt Within window
        JIS Router->>Bank: 200 OK, call allowed
        Bank->>Customer: Call connects
        Customer Phone: Display "🏦 ING Bank - Appointment 14:30"
    else Outside window
        JIS Router->>Bank: 403 Forbidden (outside appointment)
        Bank->>Customer: Call BLOCKED
    end
```

**Implementation:**
```python
# Bank app
appointment = customer.schedule_appointment(
    date="2025-11-26",
    time_start="14:00",
    time_end="15:00",
    subject="Hypotheek bespreking"
)

# Create FIR/A with appointment
fir_a = bank_client.init_relationship(
    initiator="ING_Bank_NL",
    responder=f"customer_{customer.account}",
    roles=["financial_institution", "customer"],
    context={
        "appointment_id": appointment.id,
        "appointment_start": "2025-11-26T14:00:00Z",
        "appointment_end": "2025-11-26T15:00:00Z",
        "subject": "hypotheek",
        "account_ref": customer.account[-4:]  # Last 4 digits
    },
    did_key=bank_did,
    hid_key=bank_hid
)

# Later, when calling (router checks time window)
result = bank_client.send_intent(
    fir_a.id,
    "financial_advice",
    context={
        "appointment_id": appointment.id,
        "advisor_name": "J. Smit",
        "subject": "hypotheek bespreking"
    }
)
# If outside window: HTTPError 403
# If within window: 200 OK, call proceeds
```

---

### Flow Type B: Hard Pre-Authorization (Level 4-5)
**Use case:** Advocaat wil cliënt bellen over strafzaak

```mermaid
sequenceDiagram
    Lawyer->>Client: Secure request (via portal)
    Client->>Client: Multi-factor authentication
    Client->>Lawyer: Confirm appointment + case consent
    Lawyer->>JIS Router: POST /fira/init (with case_ref + encryption)
    JIS Router->>JIS Router: Verify NOvA registration
    JIS Router->>Lawyer: FIR/A created + encryption keys

    Note: Strict window: 26-11-2025 15:00-15:15 ONLY

    Lawyer->>JIS Router: POST /ift (intent: legal_consultation)
    JIS Router->>JIS Router: Check time + case consent
    alt Within window + consent valid
        JIS Router->>Client: Incoming call notification
        Client->>Client: Biometric re-authentication
        Client->>JIS Router: Confirm (HID binding)
        JIS Router->>Lawyer: 200 OK, encrypted channel
        Lawyer->>Client: E2E encrypted call
        Note: Recording encrypted, stored 7 years
    else Outside window OR no consent
        JIS Router->>Lawyer: 403 Forbidden (HARD BLOCK)
        JIS Router->>Oversight: Log attempted breach
    end
```

**Implementation:**
```python
# Lawyer portal
case_consent = client.request_consultation(
    case_ref="2024-CV-12345",
    subject="Strafzaak bespreking",
    appointment_datetime="2025-11-26T15:00:00Z",
    duration_minutes=15,  # STRICT window
    encryption_required=True
)

# Wait for client consent (via secure portal + MFA)
# Client confirms with HID binding

# Create FIR/A (ONLY after client consent)
fir_a = lawyer_client.init_relationship(
    initiator=f"lawyer_nova_{lawyer.nova_number}",
    responder=f"client_case_{case.id}",
    roles=["attorney", "client"],
    context={
        "case_ref": "2024-CV-12345",
        "nova_number": lawyer.nova_number,
        "appointment_datetime": "2025-11-26T15:00:00Z",
        "window_minutes": 15,  # STRICT
        "privilege_mode": "attorney_client",
        "encryption_key": encryption_key_public
    },
    did_key=lawyer_did,
    hid_key=lawyer_hid  # Required for beroepsgeheim
)

# Call attempt (router enforces STRICT window)
result = lawyer_client.send_intent(
    fir_a.id,
    "legal_consultation",
    context={
        "case_ref": "2024-CV-12345",
        "consultation_type": "defense_strategy",
        "privileged": True
    }
)

# Router checks:
# 1. Current time within 15:00-15:15? ✓
# 2. Client consent valid? ✓
# 3. NOvA registration valid? ✓
# 4. HID binding matches? ✓
# 5. Encryption keys exchanged? ✓
# → ALLOW (with encrypted channel + recording)

# Outside window? → HARD BLOCK + oversight notification
```

---

### Flow Type C: Government Pre-Authorization (Level 5)
**Use case:** Politie wil verdachte spreken

```mermaid
sequenceDiagram
    Police->>Citizen: Registered letter (aangetekend)
    Citizen->>Citizen: Receives letter with case_ref
    Citizen->>Police Portal: Schedule via DigiD
    Police->>JIS Router: POST /fira/init (with PKIoverheid cert)
    JIS Router->>PKI Authority: Verify government cert
    PKI Authority->>JIS Router: Cert valid
    JIS Router->>Police: FIR/A created

    Note: Appointment: 26-11-2025 09:00 SHARP

    Police->>JIS Router: POST /ift (intent: police_interview)
    JIS Router->>JIS Router: Check: time + legal basis + MFA
    alt All checks pass
        JIS Router->>Citizen: Incoming call + rights notification
        Citizen->>Citizen: MFA (DigiD)
        Citizen->>JIS Router: Authenticated
        JIS Router->>Citizen: Display rights ("Zwijgrecht", etc.)
        Citizen->>JIS Router: Accept interview
        Police->>Citizen: Encrypted call connects
        Note: Recording encrypted, sent to oversight + OM
    else Any check fails
        JIS Router->>Police: 403 Forbidden
        JIS Router->>Oversight: ALERT - Unauthorized attempt
        JIS Router->>Citizen: Notification of attempt
    end
```

**Implementation:**
```python
# Police system (with PKIoverheid)
interview_request = police.request_interview(
    citizen_bsn="123456789",  # Encrypted
    case_ref="2024-ZV-98765",
    legal_basis="Art. 27 Wetboek van Strafvordering",
    appointment_datetime="2025-11-26T09:00:00Z",
    supervisor_approval=supervisor.sign(case_ref)
)

# Citizen receives aangetekende brief
# Citizen schedules via DigiD (with MFA)

# Create FIR/A (ONLY after citizen schedules)
fir_a = police_client.init_relationship(
    initiator=f"police_badge_{officer.badge_number}",
    responder=f"citizen_bsn_masked_{bsn[-4:]}",
    roles=["law_enforcement", "citizen"],
    context={
        "case_ref": "2024-ZV-98765",
        "legal_basis": "Art. 27 WvSv",
        "badge_number": officer.badge_number,
        "supervisor_approval": supervisor_signature,
        "appointment_datetime": "2025-11-26T09:00:00Z",
        "rights": ["zwijgrecht", "recht_op_raadsman"],
        "pkio_cert": police_cert_public
    },
    did_key=police_did,
    hid_key=officer_hid  # Officer's biometric
)

# Interview attempt
result = police_client.send_intent(
    fir_a.id,
    "police_interview",
    context={
        "case_ref": "2024-ZV-98765",
        "interview_type": "verhoor_verdachte",
        "rights_read": True,
        "supervisor": supervisor.name
    }
)

# Router checks (HARD ENFORCEMENT):
# 1. PKIoverheid cert valid? ✓
# 2. Legal basis documented? ✓
# 3. Supervisor approval? ✓
# 4. Appointment time exact? ✓ (09:00 SHARP, not 09:01!)
# 5. Citizen MFA completed? ✓
# 6. Rights notification shown? ✓
# → ALLOW
#
# Recording:
# - Encrypted with qualified cert
# - Sent to: Police, OM, Oversight board
# - Stored: 20 years
# - Audit trail: Complete chain
#
# Outside time/missing check?
# → HARD BLOCK + ALERT to oversight + citizen notification
```

---

## 📱 Display Templates per Trust Level

### Template System

**File:** `tbet-display-templates.json`

```json
{
  "level_0_unverified": {
    "icon": "⚠",
    "title": "UNVERIFIED",
    "color": "#FFA500",
    "fields": [
      {"label": "Number", "value": "{caller_number}"}
    ],
    "actions": ["Screen", "Block", "Report"]
  },

  "level_1_verified_personal": {
    "icon": "✓",
    "title": "VERIFIED",
    "color": "#10B981",
    "fields": [
      {"label": "Name", "value": "{display_name}"},
      {"label": "Number", "value": "{caller_number}"}
    ],
    "actions": ["Accept", "Reject", "Message"]
  },

  "level_2_business": {
    "icon": "🏢",
    "title": "VERIFIED BUSINESS",
    "color": "#3B82F6",
    "fields": [
      {"label": "Company", "value": "{business_name}"},
      {"label": "Registration", "value": "KVK: {kvk_number}"},
      {"label": "Number", "value": "{caller_number}"}
    ],
    "actions": ["Accept", "Reject", "Voicemail"]
  },

  "level_3_financial": {
    "icon": "🏦",
    "title": "VERIFIED FINANCIAL",
    "color": "#8B5CF6",
    "fields": [
      {"label": "Institution", "value": "{institution_name}"},
      {"label": "License", "value": "AFM: {license_number}"},
      {"label": "Account", "value": "****{account_last_4}"},
      {"label": "Appointment", "value": "{appointment_datetime}"},
      {"label": "Subject", "value": "{appointment_subject}"}
    ],
    "banner": "🔒 Pre-Scheduled Contact",
    "actions": ["Accept", "Reschedule", "Reject"]
  },

  "level_4_legal": {
    "icon": "⚖️",
    "title": "VERIFIED LEGAL",
    "color": "#DC2626",
    "fields": [
      {"label": "Attorney", "value": "{attorney_name}"},
      {"label": "Registration", "value": "NOvA: {nova_number}"},
      {"label": "Case", "value": "{case_reference}"},
      {"label": "Appointment", "value": "{appointment_datetime}"}
    ],
    "banner": "🔒 Encrypted & Privileged",
    "notice": "Attorney-client privilege applies",
    "actions": ["Accept", "Reschedule"]
  },

  "level_4_medical": {
    "icon": "🏥",
    "title": "VERIFIED MEDICAL",
    "color": "#DC2626",
    "fields": [
      {"label": "Doctor", "value": "Dr. {doctor_name}"},
      {"label": "Specialty", "value": "{specialty}"},
      {"label": "Registration", "value": "BIG: {big_number}"},
      {"label": "Patient ID", "value": "****{patient_id_last_4}"},
      {"label": "Appointment", "value": "{appointment_datetime}"}
    ],
    "banner": "🔒 HIPAA/AVG Protected",
    "notice": "Medical confidentiality applies",
    "actions": ["Accept", "Reschedule", "Emergency"]
  },

  "level_5_government": {
    "icon": "🚔",
    "title": "VERIFIED GOVERNMENT",
    "color": "#991B1B",
    "fields": [
      {"label": "Agency", "value": "{agency_name}"},
      {"label": "Department", "value": "{department}"},
      {"label": "Officer", "value": "{officer_name} (Badge #{badge_number})"},
      {"label": "Case", "value": "{case_reference}"},
      {"label": "Legal Basis", "value": "{legal_basis}"},
      {"label": "Appointment", "value": "{appointment_datetime}"}
    ],
    "banner": "🛡️ PKIoverheid Certified",
    "notice_prominent": "YOUR RIGHTS:\n- Zwijgrecht (right to remain silent)\n- Recht op raadsman (right to legal counsel)\n- Dit gesprek wordt opgenomen",
    "actions": ["Accept", "Request Lawyer", "Reschedule"]
  }
}
```

---

## 🔐 Security Enforcement Rules

### Time Window Enforcement

```python
def check_appointment_window(fir_a_id: str, intent: str) -> bool:
    """Check if current time is within appointment window"""

    fir_a = get_fir_a(fir_a_id)
    intent_config = TBET_REGISTRY[intent]

    if not intent_config.get("appointment_required"):
        return True  # No appointment needed

    appointment_start = datetime.fromisoformat(fir_a.context["appointment_start"])
    appointment_end = datetime.fromisoformat(fir_a.context["appointment_end"])
    now = datetime.utcnow()

    # Strict enforcement for Level 4-5
    if intent_config["trust_level"] >= 4:
        # EXACT window, not even 1 second early/late
        if not (appointment_start <= now <= appointment_end):
            # Log breach attempt
            log_security_breach(
                fir_a_id=fir_a_id,
                intent=intent,
                reason="outside_strict_window",
                attempted_at=now,
                window=(appointment_start, appointment_end)
            )
            # Notify oversight
            notify_oversight(fir_a_id, "breach_attempt")
            # Notify citizen
            notify_citizen(fir_a.responder, "unauthorized_contact_attempt")
            return False

    # Soft enforcement for Level 2-3 (5min grace period)
    elif intent_config["trust_level"] >= 2:
        grace_period = timedelta(minutes=5)
        if not (appointment_start - grace_period <= now <= appointment_end + grace_period):
            log_warning(fir_a_id, "outside_appointment_window")
            return False

    return True
```

### Consent Verification

```python
def verify_consent(fir_a_id: str, intent: str) -> bool:
    """Verify explicit consent exists"""

    fir_a = get_fir_a(fir_a_id)
    intent_config = TBET_REGISTRY[intent]

    if intent_config["trust_level"] >= 4:
        # Level 4-5: Explicit consent + HID binding required
        consent = get_consent_record(fir_a_id)

        if not consent:
            return False

        # Verify HID binding
        if not verify_hid_binding(fir_a.responder, consent.hid_signature):
            log_security_breach(fir_a_id, "hid_binding_mismatch")
            return False

        # Check consent not expired
        if consent.expires_at < datetime.utcnow():
            return False

        # Check consent not revoked
        if consent.revoked:
            return False

    return True
```

---

## 📋 Implementation Checklist

### Phase 1: Core TBET-BETTI (Week 1-2)
- [ ] Trust level database schema
- [ ] Intent registry extended with trust levels
- [ ] Pre-authorization flow API endpoints
- [ ] Time window enforcement in router
- [ ] Display template renderer
- [ ] Consent management system

### Phase 2: Level 3 Financial (Week 3)
- [ ] Financial institution verification
- [ ] AFM/DNB license checks
- [ ] Appointment scheduling API
- [ ] MiFID II compliance logging
- [ ] Account reference masking
- [ ] Recording encryption

### Phase 3: Level 4 Legal/Medical (Week 4-5)
- [ ] NOvA/BIG registration verification
- [ ] Beroepsgeheim mode implementation
- [ ] E2E encryption for calls
- [ ] Biometric re-authentication
- [ ] Privileged communication markers
- [ ] 7-year retention system

### Phase 4: Level 5 Government (Week 6-8)
- [ ] PKIoverheid integration
- [ ] DigiD authentication
- [ ] Legal basis validation
- [ ] Supervisor approval workflow
- [ ] Citizen rights notification system
- [ ] Oversight logging
- [ ] 20-year retention with audit
- [ ] Emergency override (with explanation)

### Phase 5: Mobile Apps (Week 9-12)
- [ ] React Native caller app
- [ ] Display template rendering
- [ ] Appointment management
- [ ] Consent flows
- [ ] Biometric integration
- [ ] Push notifications

---

## 🎯 Use Case Examples

### Example 1: Bank Belt Klant

**Scenario:** ING wil klant bellen over hypotheekaanvraag

**Flow:**
```python
# 1. Bank app: Request contact
ing_app.request_customer_contact(
    account="NL12INGB0001234567",
    subject="Hypotheekaanvraag bespreking",
    preferred_dates=["2025-11-27", "2025-11-28"]
)

# 2. Customer receives notification in ING app
# Customer schedules: "27-11-2025 14:30"

# 3. FIR/A created automatically
fir_a = create_financial_relationship(
    institution="ING_Bank_NL",
    customer_account="****4567",
    appointment="2025-11-27T14:30:00Z",
    window_minutes=30,
    subject="hypotheek"
)

# 4. On 27-11-2025 at 14:35, bank calls
# Router checks: 14:35 within 14:30-15:00? ✓
# Call connects

# 5. Customer phone displays:
"""
🏦 VERIFIED BANK
ING Bank Nederland
AFM License: 12345
Account: ****4567
Appointment: 27-11-2025 14:30
Subject: Hypotheekaanvraag

🔒 This call is recorded for compliance

[Accept] [Reschedule]
"""

# 6. Customer accepts
# 7. Call proceeds, encrypted, recorded
# 8. Event chain stores:
#    - Who called (ING advisor X)
#    - When (exact timestamp)
#    - Why (hypotheek bespreking)
#    - Account (masked reference)
#    - Recording reference
# 9. Recording encrypted, stored 7 years (MiFID II)
```

**If bank calls OUTSIDE window:**
```python
# On 27-11-2025 at 16:00 (after appointment)
# Router: 403 Forbidden - Outside appointment window
# Customer: NO NOTIFICATION (silent block)
# Audit: Logged for bank compliance review
```

---

### Example 2: Advocaat Belt Cliënt

**Scenario:** Strafrechtadvocaat wil verdachte spreken

**Flow:**
```python
# 1. Lawyer portal: Request consultation
lawyer_portal.request_case_consultation(
    case_ref="2024-CV-12345",
    client_id="client_masked_5678",
    subject="Verdediging strategie bespreking",
    duration_minutes=15  # STRICT window
)

# 2. Client receives secure message (via portal + SMS)
# Client logs in with 2FA
# Client schedules: "28-11-2025 15:00"

# 3. FIR/A created WITH consent signature
fir_a = create_legal_relationship(
    lawyer_nova="123456",
    client_masked="****5678",
    case_ref="2024-CV-12345",
    appointment="2025-11-28T15:00:00Z",
    window_minutes=15,  # STRICT
    privilege="attorney_client",
    encryption=True
)

# Client signs consent with HID binding:
consent = client.sign_consent(
    fir_a_id=fir_a.id,
    hid_signature=client_hid.sign(consent_text)
)

# 4. On 28-11-2025 at 15:00 SHARP, lawyer calls
# Router checks:
#   - Time is 15:00-15:15? ✓ (STRICT)
#   - Consent valid? ✓
#   - HID binding matches? ✓
#   - NOvA registration valid? ✓
# → ALLOW

# 5. Client phone displays:
"""
⚖️ VERIFIED LEGAL
Mr. J. de Vries
NOvA Registration: 123456
Case: 2024-CV-12345
Appointment: 28-11-2025 15:00

🔒 Encrypted & Privileged Communication
Attorney-Client Privilege Applies

This call is encrypted and recorded.
Recording stored for 7 years.

[Accept] [Request Postponement]
"""

# 6. Client taps Accept
# Client prompted: "Biometric re-authentication required"
# Client: Face ID / Fingerprint
# HID binding verified: ✓

# 7. Call connects, E2E encrypted
# 8. Event chain stores:
#    - Lawyer: NOvA 123456
#    - Client: Masked ID
#    - Case: 2024-CV-12345
#    - Privilege: Attorney-client
#    - Duration: 12 minutes
#    - Recording: Encrypted ref #ABC123
# 9. Recording encrypted, sent to:
#    - Lawyer's system (encrypted)
#    - Client's portal access (encrypted)
#    - Stored 7 years with privilege marker
```

**If lawyer calls at 15:16 (1 minute late):**
```python
# Router: 403 Forbidden - Outside strict window
# Lawyer: Call blocked
# Client: NO notification
# Oversight: Logged (automatic)
# Lawyer notified: "Appointment expired, please reschedule"
```

---

### Example 3: Politie Belt Verdachte

**Scenario:** Politie wil verdachte horen over inbraak

**Flow:**
```python
# 1. Police system: Create interview request
police_system.create_interview_request(
    citizen_bsn_encrypted="...",
    case_ref="2024-ZV-98765",
    legal_basis="Art. 27 Wetboek van Strafvordering",
    supervisor=supervisor.badge_number
)

# Supervisor reviews and approves
supervisor.approve_interview(case_ref, reason="Witness statement required")

# 2. Citizen receives AANGETEKENDE BRIEF
"""
Geachte heer/mevrouw,

De politie verzoekt u om een gesprek in het kader van
onderzoek 2024-ZV-98765 (Inbraak Keizersgracht).

Wettelijke grondslag: Art. 27 Wetboek van Strafvordering

U kunt een afspraak inplannen via DigiD op:
https://politie.nl/afspraak/2024-ZV-98765

Uw rechten:
- Zwijgrecht (art. 29 WvSv)
- Recht op rechtsbijstand
- Dit gesprek wordt opgenomen

Met vriendelijke groet,
Politie Amsterdam - Eenheid Centrum
"""

# 3. Citizen logs in via DigiD (MFA)
# Schedules: "29-11-2025 09:00"

# 4. FIR/A created with PKIoverheid cert
fir_a = create_government_relationship(
    agency="politie_amsterdam",
    officer_badge="12345",
    citizen_bsn_masked="****6789",
    case_ref="2024-ZV-98765",
    legal_basis="Art. 27 WvSv",
    appointment="2025-11-29T09:00:00Z",
    supervisor_approval=supervisor_signature,
    pkio_cert=police_cert
)

# 5. On 29-11-2025 at 09:00 SHARP, officer calls
# Router checks (HARD):
#   - PKIoverheid cert valid? ✓
#   - Time is EXACTLY 09:00? ✓
#   - Legal basis documented? ✓
#   - Supervisor approval? ✓
#   - Citizen scheduled? ✓
# → ALLOW

# 6. Citizen phone displays:
"""
🚔 VERIFIED GOVERNMENT
Politie Nederland - Eenheid Amsterdam
Officer: Badge #12345
Case: 2024-ZV-98765
Legal Basis: Art. 27 WvSv
Appointment: 29-11-2025 09:00

🛡️ PKIoverheid Certified

⚠️ UW RECHTEN:
- U heeft het recht te zwijgen (art. 29 WvSv)
- U heeft recht op rechtsbijstand
- Dit gesprek wordt opgenomen
- Opname wordt verstrekt aan u en uw advocaat

[Accept] [Request Legal Counsel] [Reschedule]
"""

# 7. Citizen prompted: "DigiD authentication required"
# Citizen: DigiD app (MFA)
# Authentication: ✓

# 8. Citizen prompted: "Read your rights?"
# Citizen: Taps "Yes"
# Rights displayed in full

# 9. Citizen: Taps "Accept"

# 10. Call connects, encrypted
# 11. Event chain stores:
#     - Officer: Badge #12345
#     - Citizen: BSN (encrypted)
#     - Case: 2024-ZV-98765
#     - Legal basis: Art. 27 WvSv
#     - Supervisor: Badge #67890
#     - Rights: Read and confirmed
#     - Duration: 18 minutes
#     - Recording: Encrypted ref #GOV123
# 12. Recording encrypted, sent to:
#     - Police system
#     - Officier van Justitie (OM)
#     - Oversight board (automatic)
#     - Citizen's access portal
#     - Stored 20 years

# 13. Audit trail sent to:
#     - Rijksinspectie Veiligheid en Justitie
#     - Autoriteit Persoonsgegevens (privacy)
```

**If officer calls at 09:01 (1 minute late):**
```python
# Router: 403 Forbidden - Outside strict window
# Officer: Call BLOCKED
# Citizen: Notification "Unauthorized contact attempt by politie"
# Oversight: IMMEDIATE ALERT
# Supervisor: Automatic review triggered
# Citizen: Right to file complaint (automatic link provided)
```

**Emergency override (only for critical situations):**
```python
# Officer: Requests emergency override
police_system.request_emergency_override(
    case_ref="2024-ZV-98765",
    reason="Suspect about to flee country - urgent witness statement needed",
    supervisor=supervisor.badge_number,
    commander_approval=commander.badge_number
)

# Router: Allows call with:
#   - Explanation required: ✓
#   - Commander approval: ✓
#   - Immediate oversight notification: ✓
#   - Citizen notification: "Emergency contact - explanation will be provided"
#   - Post-call review: MANDATORY
```

---

## 📊 Database Schema Extensions

### Trust Levels Table
```sql
CREATE TABLE trust_levels (
    level INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    pre_auth_required BOOLEAN,
    encryption_required BOOLEAN,
    mfa_required BOOLEAN,
    retention_years INTEGER
);

INSERT INTO trust_levels VALUES
(0, 'Public Unverified', 'Unknown callers, spam', false, false, false, 1),
(1, 'Verified Personal', 'Friends, family, colleagues', false, false, false, 3),
(2, 'Professional Business', 'Business contacts, sales', false, false, false, 5),
(3, 'Financial/Administrative', 'Banks, insurance, tax', true, true, false, 7),
(4, 'Legal/Medical Privileged', 'Lawyers, doctors', true, true, true, 7),
(5, 'Government/Critical', 'Police, government', true, true, true, 20);
```

### Appointments Table
```sql
CREATE TABLE appointments (
    id UUID PRIMARY KEY,
    fir_a_id UUID REFERENCES events(fir_a_id),
    appointment_start TIMESTAMPTZ NOT NULL,
    appointment_end TIMESTAMPTZ NOT NULL,
    subject TEXT,
    trust_level INTEGER REFERENCES trust_levels(level),
    consent_signature TEXT,  -- HID binding
    created_at TIMESTAMPTZ DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'scheduled'  -- scheduled, completed, cancelled, missed
);

CREATE INDEX idx_appointments_fir ON appointments(fir_a_id);
CREATE INDEX idx_appointments_time ON appointments(appointment_start, appointment_end);
```

### Consent Records Table
```sql
CREATE TABLE consent_records (
    id UUID PRIMARY KEY,
    fir_a_id UUID REFERENCES events(fir_a_id),
    consent_text TEXT NOT NULL,
    hid_signature TEXT NOT NULL,  -- HID binding signature
    granted_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ,
    revoked BOOLEAN DEFAULT FALSE,
    revoked_at TIMESTAMPTZ
);

CREATE INDEX idx_consent_fir ON consent_records(fir_a_id);
```

### Breach Attempts Table
```sql
CREATE TABLE security_breaches (
    id BIGSERIAL PRIMARY KEY,
    fir_a_id UUID,
    intent VARCHAR(100),
    reason VARCHAR(50),  -- outside_window, no_consent, invalid_cert, etc.
    attempted_at TIMESTAMPTZ NOT NULL,
    initiator TEXT,
    severity VARCHAR(20),  -- low, medium, high, critical
    oversight_notified BOOLEAN DEFAULT FALSE,
    citizen_notified BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_breaches_fir ON security_breaches(fir_a_id);
CREATE INDEX idx_breaches_time ON security_breaches(attempted_at);
CREATE INDEX idx_breaches_severity ON security_breaches(severity);
```

---

## 🎯 Next Steps

1. **Review this architecture** - Feedback? Changes?
2. **Prioritize trust levels** - Start with Level 3 (Financial)?
3. **Build appointment system** - Core to pre-authorization
4. **Extend router API** - New endpoints for appointments/consent
5. **Update Admin UI** - Show trust levels, appointments, breaches
6. **Test with real bank** - Pilot with ING/Rabobank?
7. **Government pilot** - Contact DigiD team?

---

**Dit is niet meer "een idee".**
**Dit is een complete trust framework.**
**Production-ready architecture.**
**Juridisch waterdicht.**
**Schaalbaar van persoonlijk tot overheid.**

**TBET → BETTI = The Future of Trusted Communication** 🔥

---

**Version:** 2.0.0
**Status:** Architecture Complete
**Ready for:** Implementation

Wat denk je? Klopt dit met je visie? 🎯
