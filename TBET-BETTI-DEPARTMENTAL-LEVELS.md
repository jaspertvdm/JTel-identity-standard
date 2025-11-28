# TBET-BETTI Departmental & Role-Based Levels

**Hiërarchische differentiatie binnen organisaties**

Version: 1.0.0
Date: 2025-11-27

---

## 🎯 Kernprincipe

**Niet elke afdeling binnen een organisatie heeft hetzelfde trust level nodig.**

Voorbeelden:
- **Bank:** Administratie ≠ Wealth Management ≠ Compliance
- **Overheid:** Burgerzaken ≠ Belastingdienst ≠ AIVD
- **Ziekenhuis:** Receptie ≠ Huisarts ≠ Psychiatrie

**TBET payload grootte varieert:**
- Kleine TBET = basis info (administratie)
- Grote TBET = volledige trail + humotica (sensitieve afdelingen)

**BETTI enforcement varieert:**
- Lage requirements = simpele pre-auth
- Hoge requirements = encryption + audit + oversight

---

## 📊 Departmental Trust Levels

### Level Schema

```
Organization Level (0-5)
  └─> Department Level (A-D)
       └─> Role Level (1-9)
```

**Voorbeeld: ING Bank (Organization Level 3)**
```
ING Bank (Level 3: Financial)
  ├─> Klantenservice (3-A)
  │    ├─> Medewerker Algemeen (3-A-1) → Lage TBET
  │    └─> Teamleider (3-A-2) → Medium TBET
  │
  ├─> Hypotheken (3-B)
  │    ├─> Adviseur (3-B-3) → Medium TBET + recording
  │    └─> Senior Adviseur (3-B-4) → Medium TBET + full trail
  │
  ├─> Wealth Management (3-C)
  │    ├─> Adviseur (3-C-5) → Hoge TBET + encryption
  │    └─> Private Banker (3-C-6) → Hoge TBET + full audit
  │
  └─> Compliance (3-D)
       ├─> Analist (3-D-7) → Maximum TBET + oversight
       └─> Compliance Officer (3-D-8) → Maximum TBET + legal hold
```

**Voorbeeld: Overheid (Organization Level 5)**
```
Gemeente Amsterdam (Level 5: Government)
  ├─> Burgerzaken (5-A)
  │    ├─> Baliemedewerker (5-A-1) → Lage TBET (basis info)
  │    └─> Coördinator (5-A-2) → Medium TBET
  │
  ├─> Belastingen (5-B)
  │    ├─> Medewerker (5-B-3) → Medium TBET + BSN encryption
  │    └─> Inspecteur (5-B-4) → Hoge TBET + financial data
  │
  └─> Bijzondere Zaken (5-C)
       └─> Specialist (5-C-5) → Maximum TBET + full trail

Politie Nederland (Level 5: Law Enforcement)
  ├─> Wijkagent (5-A-1) → Medium TBET
  ├─> Recherchebureau (5-B-3) → Hoge TBET + case trail
  └─> Zware Criminaliteit (5-C-5) → Maximum TBET + classified
```

---

## 📦 TBET Payload Sizes

### Payload Structure

Elke afdeling/rol krijgt een **TBET template** met verschillende velden:

```python
class TBETPayload:
    # ALTIJD aanwezig (Minimal)
    required_fields = [
        "fir_a_id",
        "intent",
        "timestamp",
        "initiator",
        "responder"
    ]

    # Departmental fields (per level)
    department_fields = {
        "A": ["department_name", "role"],  # Basic
        "B": ["department_name", "role", "license_number", "appointment_id"],  # Medium
        "C": ["department_name", "role", "license_number", "appointment_id",
              "case_reference", "supervisor_approval"],  # High
        "D": ["department_name", "role", "license_number", "appointment_id",
              "case_reference", "supervisor_approval", "legal_basis",
              "encryption_keys", "audit_trail_id"]  # Maximum
    }

    # Humotica (human intent trace)
    humotica_levels = {
        1: "basic",      # "Klantenservice belt over vraag"
        2: "detailed",   # "Hypotheekadviseur belt over aanvraag #12345"
        3: "full",       # "Compliance officer belt over transactie review"
        4: "classified"  # "Recherche belt over zaak 2024-ZV-12345 (confidential)"
    }
```

---

## 🏦 Voorbeeld: ING Bank Afdelingen

### Department A: Klantenservice (Level 3-A)

**Role:** Algemene vragen, saldo checks

**TBET Intent: `customer_service_call`**
```json
{
  "fir_a_id": "fira-12345",
  "intent": "customer_service_call",
  "timestamp": "2025-11-27T14:30:00Z",

  "initiator": "ing_klantenservice",
  "responder": "customer_phone_+31612345678",

  "department": {
    "level": "3-A",
    "name": "Klantenservice",
    "role": "Medewerker Algemeen"
  },

  "context": {
    "employee_id": "KS-001234",
    "account_last_4": "4567",
    "reason": "Saldo check vraag"
  },

  "humotica": "Klantenservice belt over saldo vraag",

  "pre_auth": {
    "required": false  // Level A = no appointment needed
  },

  "security": {
    "recording": "optional",
    "encryption": false,
    "retention_years": 1
  }
}
```

**Payload grootte: ~250 bytes** (klein)

**BETTI Response:**
- ✅ DID/HID check
- ✅ Business registration (KVK)
- ❌ Geen appointment vereist
- ❌ Geen encryption
- 📞 Direct doorverbinden na consent

---

### Department B: Hypotheken (Level 3-B)

**Role:** Hypotheekadvies, complexe producten

**TBET Intent: `mortgage_advice_call`**
```json
{
  "fir_a_id": "fira-67890",
  "intent": "mortgage_advice_call",
  "timestamp": "2025-11-27T15:00:00Z",

  "initiator": "ing_hypotheken",
  "responder": "customer_phone_+31612345678",

  "department": {
    "level": "3-B",
    "name": "Hypotheken",
    "role": "Adviseur",
    "employee_id": "HYP-005678",
    "license": "AFM-HYP-2024-12345"
  },

  "context": {
    "account_last_4": "4567",
    "mortgage_application_id": "MORT-2024-98765",
    "appointment_id": "appt_20251127_1500",
    "subject": "Hypotheek offerte bespreking",
    "loan_amount_range": "€200k-€300k"  // Masked
  },

  "appointment": {
    "appointment_id": "appt_20251127_1500",
    "appointment_start": "2025-11-27T15:00:00Z",
    "appointment_end": "2025-11-27T15:30:00Z",
    "scheduled_by": "customer",
    "confirmed": true
  },

  "humotica": "Hypotheekadviseur belt over offerte bespreking voor aanvraag MORT-2024-98765",

  "pre_auth": {
    "required": true,
    "appointment_required": true
  },

  "security": {
    "recording": "mandatory",
    "encryption": true,  // Basic encryption
    "retention_years": 7,  // MiFID II
    "compliance": ["MiFID II", "GDPR"]
  },

  "provenance": {
    "advisor_name": "J. Smit",
    "supervisor": "Team Lead Hypotheken",
    "internal_approval": true
  }
}
```

**Payload grootte: ~600 bytes** (medium)

**BETTI Response:**
- ✅ DID/HID check
- ✅ AFM license verification
- ✅ **Appointment window check** (REQUIRED)
- ✅ Basic encryption
- ✅ Recording mandatory
- 📞 Connect alleen binnen appointment window

---

### Department C: Wealth Management (Level 3-C)

**Role:** Private banking, grote vermogens (>€500k)

**TBET Intent: `wealth_management_call`**
```json
{
  "fir_a_id": "fira-11111",
  "intent": "wealth_management_call",
  "timestamp": "2025-11-27T16:00:00Z",

  "initiator": "ing_wealth_management",
  "responder": "client_phone_+31612345678",

  "department": {
    "level": "3-C",
    "name": "Wealth Management",
    "role": "Private Banker",
    "employee_id": "WM-002345",
    "license": "AFM-WM-2024-PREMIUM-5678",
    "certifications": ["CFA", "RBA"]
  },

  "context": {
    "client_id_masked": "****5678",
    "portfolio_value_range": "€1M-€5M",  // Masked range
    "investment_proposal_id": "INV-2024-PROP-12345",
    "appointment_id": "appt_20251127_1600",
    "subject": "Portfolio rebalancing strategy",
    "classification": "high_net_worth"
  },

  "appointment": {
    "appointment_id": "appt_20251127_1600",
    "appointment_start": "2025-11-27T16:00:00Z",
    "appointment_end": "2025-11-27T17:00:00Z",
    "scheduled_by": "client",
    "confirmed": true,
    "strict_window": true  // No grace period
  },

  "humotica": "Private Banker belt over portfolio rebalancing voorstel INV-2024-PROP-12345 voor high net worth client (€1M-€5M portfolio)",

  "pre_auth": {
    "required": true,
    "appointment_required": true,
    "client_consent_signature": "hid_signature_abc123...",
    "biometric_reauth_required": true
  },

  "security": {
    "recording": "mandatory",
    "encryption": "e2e",  // End-to-end
    "retention_years": 10,
    "compliance": ["MiFID II", "GDPR", "AML"],
    "qualified_signature": true
  },

  "provenance": {
    "banker_name": "A. van der Berg",
    "supervisor": "Head of Wealth Management",
    "compliance_approval": "COMP-2024-WM-567",
    "risk_assessment": "completed",
    "internal_approval_chain": [
      {"role": "Banker", "approved": true},
      {"role": "Team Lead", "approved": true},
      {"role": "Compliance", "approved": true}
    ]
  },

  "audit_trail": {
    "trail_id": "audit_wm_20251127_001",
    "linked_events": ["portfolio_review", "risk_analysis", "proposal_created"],
    "oversight_copy": true  // AFM oversight gets copy
  }
}
```

**Payload grootte: ~1.2 KB** (large)

**BETTI Response:**
- ✅ DID/HID check
- ✅ AFM premium license
- ✅ **STRICT appointment window** (no grace period)
- ✅ Client consent with HID signature
- ✅ **Biometric re-auth required**
- ✅ E2E encryption
- ✅ Recording + qualified signature
- ✅ Compliance chain verified
- 📞 Maximum security mode

---

### Department D: Compliance (Level 3-D)

**Role:** AML, fraud detection, regulatory

**TBET Intent: `compliance_investigation_call`**
```json
{
  "fir_a_id": "fira-99999",
  "intent": "compliance_investigation_call",
  "timestamp": "2025-11-27T10:00:00Z",

  "initiator": "ing_compliance",
  "responder": "customer_phone_+31612345678",

  "department": {
    "level": "3-D",
    "name": "Compliance & AML",
    "role": "Compliance Officer",
    "employee_id": "COMP-001234",
    "license": "AFM-COMP-2024-9999",
    "clearance_level": "confidential"
  },

  "context": {
    "investigation_id": "INV-AML-2024-5678",
    "case_type": "unusual_transaction_pattern",
    "transaction_refs": ["TRX-2024-A", "TRX-2024-B", "TRX-2024-C"],
    "flagged_amount_range": "€50k-€100k",
    "appointment_id": "appt_20251127_1000",
    "subject": "Transaction verification required",
    "urgency": "high",
    "regulatory_deadline": "2025-12-01"
  },

  "appointment": {
    "appointment_id": "appt_20251127_1000",
    "appointment_start": "2025-11-27T10:00:00Z",
    "appointment_end": "2025-11-27T10:30:00Z",
    "scheduled_by": "compliance",
    "customer_confirmed": true,
    "strict_window": true,
    "mandatory": true  // Customer MUST respond
  },

  "humotica": "Compliance officer belt over ongebruikelijke transactiepatroon (INV-AML-2024-5678) - TRX refs: 2024-A/B/C - totaal €50k-€100k - verificatie vereist voor regulatory deadline 01-12-2025",

  "legal_basis": {
    "law": "Wet ter voorkoming van witwassen en financieren van terrorisme (Wwft)",
    "article": "Art. 3.1 - Customer due diligence",
    "justification": "Unusual transaction pattern detected requiring verification",
    "regulatory_authority": "AFM / De Nederlandsche Bank"
  },

  "pre_auth": {
    "required": true,
    "appointment_required": true,
    "customer_consent": "mandatory_compliance",
    "legal_obligation": true,
    "biometric_reauth_required": true,
    "supervisor_approval_required": true
  },

  "security": {
    "recording": "mandatory",
    "encryption": "qualified_e2e",  // Qualified encryption
    "retention_years": 10,  // Wwft requirement
    "compliance": ["Wwft", "MiFID II", "GDPR", "AML"],
    "qualified_signature": true,
    "legal_hold": true  // Can't be deleted
  },

  "provenance": {
    "officer_name": "Dr. M. Jansen",
    "supervisor": "Head of Compliance",
    "supervisor_approval": "SUP-2024-COMP-567",
    "compliance_approval_chain": [
      {"role": "AML Analyst", "approved": true, "timestamp": "2025-11-26T14:00:00Z"},
      {"role": "Senior Compliance Officer", "approved": true, "timestamp": "2025-11-26T15:30:00Z"},
      {"role": "Head of Compliance", "approved": true, "timestamp": "2025-11-26T16:00:00Z"},
      {"role": "Legal Department", "reviewed": true, "timestamp": "2025-11-26T16:30:00Z"}
    ],
    "risk_level": "high"
  },

  "audit_trail": {
    "trail_id": "audit_comp_20251127_001",
    "investigation_timeline": [
      {"event": "pattern_detected", "timestamp": "2025-11-20T10:00:00Z"},
      {"event": "case_opened", "timestamp": "2025-11-20T11:00:00Z"},
      {"event": "supervisor_notified", "timestamp": "2025-11-20T12:00:00Z"},
      {"event": "appointment_requested", "timestamp": "2025-11-25T09:00:00Z"},
      {"event": "customer_confirmed", "timestamp": "2025-11-26T14:00:00Z"},
      {"event": "call_initiated", "timestamp": "2025-11-27T10:00:00Z"}
    ],
    "linked_investigations": ["INV-2024-1234", "INV-2024-5677"],
    "regulatory_copy": true,  // AFM + DNB get copies
    "oversight_notification": true,
    "legal_review_required": true
  },

  "oversight": {
    "afm_notification": true,
    "dnb_notification": true,
    "fiu_netherlands_copy": true,  // Financial Intelligence Unit
    "immediate_escalation": false,
    "post_call_report_required": true,
    "deadline": "2025-11-28T17:00:00Z"
  }
}
```

**Payload grootte: ~2.5 KB** (maximum)

**BETTI Response:**
- ✅ DID/HID check
- ✅ AFM + DNB license verification
- ✅ **Legal basis verification** (Wwft compliance)
- ✅ **Supervisor approval chain check** (4 levels)
- ✅ STRICT appointment window
- ✅ Customer mandatory response
- ✅ **Biometric + legal acknowledgment**
- ✅ **Qualified E2E encryption**
- ✅ Recording with legal hold
- ✅ **Oversight copies** → AFM, DNB, FIU
- ✅ Complete audit trail
- 📞 Maximum compliance mode + oversight logging

---

## 🏛️ Voorbeeld: Overheid Afdelingen

### Gemeente Amsterdam - Burgerzaken (Level 5-A)

**TBET Intent: `citizen_services_call`**
```json
{
  "intent": "citizen_services_call",
  "department": {
    "level": "5-A",
    "name": "Burgerzaken",
    "role": "Baliemedewerker"
  },
  "context": {
    "bsn_last_4": "5678",
    "subject": "Paspoort aanvraag status",
    "appointment_id": "appt_burgers_123"
  },
  "humotica": "Burgerzaken belt over status paspoort aanvraag",
  "security": {
    "recording": "optional",
    "encryption": "basic",
    "retention_years": 3
  }
}
```

**Payload: ~400 bytes** (klein)

---

### Belastingdienst - Particulieren (Level 5-B)

**TBET Intent: `tax_inquiry_call`**
```json
{
  "intent": "tax_inquiry_call",
  "department": {
    "level": "5-B",
    "name": "Belastingdienst Particulieren",
    "role": "Inspecteur",
    "employee_id": "BD-123456"
  },
  "context": {
    "bsn_encrypted": "encrypted_bsn_data...",
    "tax_year": "2024",
    "case_ref": "BD-2024-P-98765",
    "subject": "Aanvullende informatie aangifte",
    "appointment_id": "appt_bd_456"
  },
  "legal_basis": {
    "law": "Algemene wet inzake rijksbelastingen",
    "article": "Art. 47 - Informatieplicht"
  },
  "humotica": "Belastinginspecteur belt over aanvullende info bij aangifte 2024 (zaak BD-2024-P-98765)",
  "security": {
    "recording": "mandatory",
    "encryption": "e2e",
    "retention_years": 7,
    "bsn_encryption": true
  },
  "audit_trail": {
    "trail_id": "audit_bd_001",
    "supervisor_approval": true
  }
}
```

**Payload: ~800 bytes** (medium)

---

### AIVD - Classified Operations (Level 5-C)

**TBET Intent: `classified_intelligence_call`**
```json
{
  "intent": "classified_intelligence_call",
  "department": {
    "level": "5-C",
    "name": "AIVD Operations",
    "role": "Intelligence Officer",
    "clearance": "TOP_SECRET",
    "employee_id": "AIVD-CLASSIFIED"
  },
  "context": {
    "operation_code": "OP-2024-CLASSIFIED",
    "subject": "[CLASSIFIED]",
    "bsn_encrypted": "quantum_encrypted_bsn...",
    "appointment_id": "appt_classified_999",
    "urgency": "critical"
  },
  "legal_basis": {
    "law": "Wet op de inlichtingen- en veiligheidsdiensten 2017 (Wiv 2017)",
    "article": "Art. 28 - Specifieke bevoegdheden",
    "minister_approval": true,
    "toetsingscommissie_approval": "TIB-2024-567",
    "judicial_oversight": true
  },
  "humotica": "[CLASSIFIED] - Intelligence operation OP-2024-CLASSIFIED - ministerial approval TIB-2024-567 - judicial oversight active",
  "pre_auth": {
    "required": true,
    "minister_approval": true,
    "judicial_review": true,
    "multi_level_clearance": ["minister", "aivd_director", "judicial_oversight"]
  },
  "security": {
    "recording": "mandatory",
    "encryption": "quantum_resistant",
    "retention_years": 20,
    "classification": "TOP_SECRET",
    "compartmentalized": true,
    "need_to_know": true
  },
  "audit_trail": {
    "trail_id": "audit_aivd_classified_001",
    "approval_chain": [
      {"role": "Officer", "clearance": "TOP_SECRET", "approved": true},
      {"role": "Team Lead", "clearance": "TOP_SECRET", "approved": true},
      {"role": "AIVD Director", "approved": true},
      {"role": "Minister BZK", "approved": true},
      {"role": "Toetsingscommissie Inzet Bevoegdheden", "reviewed": true}
    ],
    "oversight": [
      "Commissie van Toezicht betreffende de Inlichtingen- en Veiligheidsdiensten (CTIVD)",
      "Toetsingscommissie Inzet Bevoegdheden (TIB)"
    ],
    "parliamentary_notification": "classified_timeline"
  },
  "oversight": {
    "ctivd_realtime_monitoring": true,
    "tib_pre_approval": true,
    "judicial_warrant": "WARRANT-2024-AIVD-567",
    "ministerial_accountability": true,
    "parliamentary_oversight": "delayed_notification"
  }
}
```

**Payload: ~2 KB** (maximum government)

**BETTI Response:**
- ✅ PKIoverheid + quantum-resistant encryption
- ✅ **Ministerial approval verification**
- ✅ **Judicial warrant check**
- ✅ **CTIVD realtime monitoring** (oversight)
- ✅ **TIB pre-approval** verified
- ✅ Compartmentalized access (need-to-know)
- ✅ Parliamentary accountability trail
- 📞 Maximum classification + judicial oversight

---

## 🔓 Overheid Ontsleuteling & Trail Viewing

### Decryption Levels

**Verschillende niveaus van toegang tot encrypted trails:**

```python
class AuditTrailDecryption:
    """Overheid audit trail decryption systeem"""

    decryption_levels = {
        # Level 1: Basic oversight (AFM, DNB)
        "regulatory_oversight": {
            "can_decrypt": ["metadata", "timestamps", "participants"],
            "cannot_decrypt": ["content", "humotica_details"],
            "use_case": "Toezicht op naleving procedures"
        },

        # Level 2: Investigation (FIOD, Police with warrant)
        "investigation": {
            "can_decrypt": ["metadata", "timestamps", "participants", "content_summary"],
            "cannot_decrypt": ["full_content", "privileged_communications"],
            "requires": ["judicial_warrant", "case_reference"],
            "use_case": "Strafrechtelijk onderzoek"
        },

        # Level 3: Judicial (Rechter, OM)
        "judicial": {
            "can_decrypt": ["metadata", "timestamps", "participants", "full_content"],
            "cannot_decrypt": ["privileged_attorney_client"],
            "requires": ["judicial_order", "case_number"],
            "use_case": "Gerechtelijk onderzoek, bewijsvoering"
        },

        # Level 4: Oversight maximum (CTIVD, TIB)
        "oversight_maximum": {
            "can_decrypt": ["everything"],
            "requires": ["oversight_mandate", "parliamentary_authorization"],
            "use_case": "AIVD/MIVD oversight, grondwettelijke checks",
            "time_delayed": True  # Real-time for active ops, delayed for historical
        }
    }
```

### Decryption Request Flow

```mermaid
sequenceDiagram
    participant AFM as AFM Inspector
    participant Router as JIS Router
    participant HSM as Hardware Security Module
    participant Oversight as Oversight Board

    AFM->>Router: Request audit trail (case_ref)
    Router->>Router: Check requester authorization
    Router->>Router: Verify legal basis

    alt Authorized (regulatory oversight)
        Router->>HSM: Request decryption (level: regulatory_oversight)
        HSM->>HSM: Decrypt metadata only
        HSM->>Router: Decrypted metadata
        Router->>AFM: Audit trail (metadata + timestamps)

        Note: AFM ziet WIE, WANNEER, WAAROM<br/>maar NIET de volledige inhoud
    else Unauthorized
        Router->>AFM: 403 Forbidden
        Router->>Oversight: Log unauthorized access attempt
    end
```

### Practical Example: AFM Compliance Check

**AFM wil checken of ING compliance case correct afgehandeld is:**

```python
# AFM request
afm_request = {
    "requester": "AFM_Inspector_ID_12345",
    "authorization": "afm_oversight_mandate",
    "case_ref": "INV-AML-2024-5678",
    "audit_trail_id": "audit_comp_20251127_001",
    "decryption_level": "regulatory_oversight",
    "purpose": "Compliance verification - Wwft procedures"
}

# Router response (decrypted metadata)
response = {
    "audit_trail_id": "audit_comp_20251127_001",
    "decryption_level": "regulatory_oversight",

    # ✅ AFM KAN ZIEN:
    "metadata": {
        "case_ref": "INV-AML-2024-5678",
        "department": "ING Compliance & AML",
        "officer": "COMP-001234",
        "customer_id_masked": "****5678",
        "investigation_opened": "2025-11-20T10:00:00Z",
        "call_timestamp": "2025-11-27T10:00:00Z",
        "duration_seconds": 1200
    },

    "timeline": [
        {"event": "pattern_detected", "timestamp": "2025-11-20T10:00:00Z"},
        {"event": "case_opened", "timestamp": "2025-11-20T11:00:00Z"},
        {"event": "supervisor_notified", "timestamp": "2025-11-20T12:00:00Z"},
        {"event": "call_completed", "timestamp": "2025-11-27T10:20:00Z"},
        {"event": "report_filed", "timestamp": "2025-11-27T11:00:00Z"}
    ],

    "approval_chain": [
        {"role": "AML Analyst", "approved": true},
        {"role": "Senior Compliance Officer", "approved": true},
        {"role": "Head of Compliance", "approved": true},
        {"role": "Legal Department", "reviewed": true}
    ],

    "legal_basis": "Wwft Art. 3.1",
    "procedures_followed": true,
    "deadline_met": true,

    # ❌ AFM ZIET NIET:
    # - Volledige gesprekscontent (encrypted)
    # - Exacte transactiebedragen (masked)
    # - Klant persoonlijke details (encrypted)
    # - Humotica full text (encrypted)

    "encrypted_content": "[ENCRYPTED - Requires judicial_warrant]",
    "humotica_summary": "Compliance case regarding unusual transaction pattern",
    "humotica_full": "[ENCRYPTED]"
}
```

**AFM conclusie:**
```
✅ Procedures correct gevolgd
✅ Timeline binnen wettelijke termijnen
✅ Approval chain compleet
✅ Legal basis gedocumenteerd

→ Compliance check: PASSED
→ Geen verdere actie nodig
```

---

### Judicial Decryption: Rechter Needs Full Content

**Rechter in strafzaak heeft volledige content nodig:**

```python
# Judicial request (with warrant)
judicial_request = {
    "requester": "Rechtbank_Amsterdam_Judge_567",
    "authorization": "judicial_order",
    "warrant_number": "WARRANT-2024-RB-AMS-9876",
    "case_number": "STRAF-2024-12345",
    "audit_trail_id": "audit_comp_20251127_001",
    "decryption_level": "judicial",
    "legal_basis": "Art. 126nd Sv - Vordering gegevens",
    "purpose": "Bewijsvoering in strafzaak"
}

# Router verifies warrant with judicial system
warrant_valid = verify_warrant_with_rechtspraak_nl(
    warrant_number="WARRANT-2024-RB-AMS-9876"
)

if warrant_valid:
    # HSM decrypts full content
    response = {
        # ✅ RECHTER KRIJGT ALLES (behalve attorney-client privilege):

        "metadata": { ... },  # Volledig
        "timeline": [ ... ],  # Volledig
        "approval_chain": [ ... ],  # Volledig

        "call_transcript": {
            "participants": ["COMP-001234 (ING)", "Customer ****5678"],
            "duration": "20 minutes",
            "transcript": [
                {"speaker": "Compliance Officer", "timestamp": "10:00:05", "text": "Goedemorgen, u spreekt met Dr. M. Jansen van ING Compliance..."},
                {"speaker": "Customer", "timestamp": "10:00:15", "text": "Ja goedemorgen..."},
                # ... volledige transcript
            ]
        },

        "transaction_details": {
            "transactions": [
                {"ref": "TRX-2024-A", "amount": "€45,000", "date": "2024-11-15", "counterparty": "Unknown"},
                {"ref": "TRX-2024-B", "amount": "€30,000", "date": "2024-11-18", "counterparty": "Unknown"},
                {"ref": "TRX-2024-C", "amount": "€25,000", "date": "2024-11-22", "counterparty": "Unknown"}
            ],
            "total": "€100,000",
            "pattern": "Unusual - rapid large transfers to new accounts"
        },

        "humotica_full": "Compliance officer Dr. M. Jansen contacted customer regarding unusual transaction pattern detected on account NL12INGB****5678. Three large transfers totaling €100k to previously unknown accounts within one week triggered AML alert. Customer explained transfers were for legitimate business purchases but could not immediately provide supporting documentation. Follow-up appointment scheduled for documentation review. Case remains open pending documentation.",

        "customer_explanation": "[Full customer statement during call...]",

        "compliance_assessment": "Medium risk - await documentation",

        "encrypted_sections": {
            "attorney_client_privileged": "[STILL ENCRYPTED - Requires separate privilege waiver]"
        }
    }
```

**Rechter kan nu:**
- ✅ Volledige transcript lezen
- ✅ Transactiedetails zien
- ✅ Humotica begrijpen (menselijke intentie trace)
- ✅ Compliance assessment review
- ❌ Attorney-client privileged sections blijven encrypted (constitutionele bescherming)

---

## 📊 Humotica Visibility Matrix

**Wie ziet welk deel van de Humotica (human intent trace)?**

| Rol | Summary | Basic | Detailed | Full | Privileged |
|-----|---------|-------|----------|------|------------|
| **AFM Inspector** | ✅ | ✅ | ❌ | ❌ | ❌ |
| **DNB Auditor** | ✅ | ✅ | ❌ | ❌ | ❌ |
| **Police (no warrant)** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Police (with warrant)** | ✅ | ✅ | ✅ | ❌ | ❌ |
| **FIOD** | ✅ | ✅ | ✅ | ✅ | ❌ |
| **Rechter** | ✅ | ✅ | ✅ | ✅ | ❌* |
| **OM (Officier van Justitie)** | ✅ | ✅ | ✅ | ✅ | ❌* |
| **CTIVD** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Advocaat (own client)** | ✅ | ✅ | ✅ | ✅ | ✅ |

*= Unless privilege waived by client

---

## 🎯 Implementation Recommendations

### 1. TBET Payload Templates

Maak templates per department level:

```python
# templates/tbet_payloads.py

def create_tbet_payload(org_level, dept_level, role_level, intent, context):
    """Generate TBET payload based on departmental level"""

    payload = {
        "fir_a_id": context["fir_a_id"],
        "intent": intent,
        "timestamp": datetime.utcnow().isoformat(),
        "initiator": context["initiator"],
        "responder": context["responder"]
    }

    # Add department info
    payload["department"] = get_department_info(org_level, dept_level, role_level)

    # Add fields based on dept level
    if dept_level == "A":
        payload["context"] = get_basic_context(context)
        payload["humotica"] = generate_basic_humotica(intent, context)
        payload["security"] = {"recording": "optional", "encryption": False}

    elif dept_level == "B":
        payload["context"] = get_medium_context(context)
        payload["appointment"] = get_appointment_info(context)
        payload["humotica"] = generate_detailed_humotica(intent, context)
        payload["security"] = {"recording": "mandatory", "encryption": "basic"}

    elif dept_level == "C":
        payload["context"] = get_high_context(context)
        payload["appointment"] = get_strict_appointment(context)
        payload["humotica"] = generate_full_humotica(intent, context)
        payload["provenance"] = get_approval_chain(context)
        payload["security"] = {"recording": "mandatory", "encryption": "e2e"}

    elif dept_level == "D":
        payload["context"] = get_maximum_context(context)
        payload["appointment"] = get_mandatory_appointment(context)
        payload["legal_basis"] = get_legal_basis(context)
        payload["humotica"] = generate_classified_humotica(intent, context)
        payload["provenance"] = get_full_approval_chain(context)
        payload["audit_trail"] = create_audit_trail(context)
        payload["security"] = {
            "recording": "mandatory",
            "encryption": "qualified_e2e",
            "legal_hold": True
        }
        payload["oversight"] = get_oversight_config(context)

    return payload
```

### 2. Decryption Access Control

```python
# security/decryption.py

def decrypt_audit_trail(trail_id, requester, authorization):
    """Decrypt audit trail based on requester authorization level"""

    # Verify authorization
    auth_level = verify_authorization(requester, authorization)

    # Get encrypted trail
    trail = get_audit_trail(trail_id)

    # Decrypt based on level
    if auth_level == "regulatory_oversight":
        return decrypt_metadata_only(trail)

    elif auth_level == "investigation":
        warrant = verify_judicial_warrant(authorization["warrant_number"])
        if warrant.valid:
            return decrypt_content_summary(trail)

    elif auth_level == "judicial":
        court_order = verify_court_order(authorization["court_order_number"])
        if court_order.valid:
            return decrypt_full_content(trail, exclude_privileged=True)

    elif auth_level == "oversight_maximum":
        oversight_mandate = verify_oversight_mandate(authorization)
        if oversight_mandate.valid:
            return decrypt_everything(trail)

    else:
        raise UnauthorizedAccessError("Insufficient authorization level")
```

---

## ✅ Summary

**Key Takeaways:**

1. **Departmental levels** (A-D) bepalen TBET payload grootte
   - A = Klein (basic info)
   - B = Medium (appointments + recording)
   - C = Groot (encryption + provenance)
   - D = Maximum (full trail + oversight)

2. **BETTI enforcement** schaalt mee
   - Level A = Soft checks
   - Level D = Maximum enforcement + oversight

3. **Humotica** wordt logisch opgebouwd per level
   - Basic: "Klantenservice belt"
   - Full: "Compliance officer belt over AML case X met transacties Y totaal €Z"

4. **Overheid decryption** is gelaagd
   - AFM: Metadata only (procedures check)
   - Rechter: Full content (bewijsvoering)
   - CTIVD: Everything (constitutional oversight)

5. **Trail blijft traceable** voor bevoegde instanties
   - Maar privacy protected voor regulier toezicht
   - Judicial warrant vereist voor volledige content
   - Attorney-client privilege blijft beschermd

**Dit systeem balanceert:**
- ✅ Privacy (encrypted by default)
- ✅ Compliance (AFM kan procedures checken)
- ✅ Judicial access (rechter krijgt bewijs)
- ✅ Oversight (CTIVD ziet alles)
- ✅ Efficiency (kleine payloads waar mogelijk)

---

**Ready voor implementatie! 🚀**
