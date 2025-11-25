# JTel Identity Standard — Semantic Keying Extension (2025)

## FIR/A‑Rooted Key Continuity & Semantic Relationship Anchoring

**Status:** Draft Extension
**Auteur:** Jasper van de Meent (JTel)
**Onderdeel van:** JIS Unified Draft 2025

---

# 1. Inleiding

Dit document beschrijft de uitbreiding op de JTel Identity Standard (JIS) waarbij **semantische sleutels** worden gevormd uit een onveranderlijke eerste kennismaking (FIR/A) en een groeiende continuïteitsketen. Dit model elimineert sleutelhergebruik, spoofing, imitatie en contextloze verbindingen door veiligheid niet te baseren op cryptografische bits, maar op **context + intentie + continuïteit + rol**.

---

# 2. FIR/A — Het Genesis‑Moment

Elke relatie tussen twee entiteiten (mens ↔ device, device ↔ device, server ↔ server, object ↔ gebruiker) begint met één uniek proces:

**FIR/A = Flag → Identify → Revoke/Accept**

Dit is het "genesis‑moment" van de relatie.

* De eerste flag creëert bewustzijn.
* Identify legt rol, gedrag, intent en context vast.
* Accept creëert een relatie.
* Revoke beëindigt deze onmiddellijk.

**FIR/A is onveranderlijk, uniek en niet reproduceerbaar.**

---

# 3. De Semantische Sleutel

Elke relatie heeft een sleutel die bestaat uit twee delen:

```
SemanticKey = FIR/A_root + ContinuityChain(n)
```

## 3.1 FIR/A_root

* Unieke eerste identificatie
* Rol, context, intentie
* Niet vervalsbaar
* Niet kopieerbaar
* Niet vervangbaar
* Ontstaat maar één keer per relatie

## 3.2 ContinuityChain(n)

Een groeiende keten van gebeurtenissen:

* IO‑states (menselijke continuïteit)
* DO‑states (apparaatcontinuïteit)
* OD‑states (operatievalidatie)
* Contextwijzigingen
* Intentieontwikkelingen
* Objecttransformaties (INFC → OFC)

De chain is veranderlijk, maar altijd verankerd aan dezelfde **FIR/A_root**.

---

# 4. ContinuityHash

De totale sleutel kan worden gevalideerd via een hash‑mechanisme:

```
ContinuityHash = Hash(FIR/A_root + ContinuityChain(n))
```

Een mismatch in ContinuityHash betekent:

* De relatie klopt niet meer.
* De chain hoort niet bij de FIR/A_root.
* Spoofing of contextverlies.

In dat geval wordt een **nieuwe FIR/A** opgestart en wordt de oude relatie geïsoleerd.

---

# 5. Onmogelijkheid van Sleutelhergebruik

Cryptografische sleutels kunnen worden gekloond of gestolen.
**Semantische sleutels kunnen dat niet.**

Waarom niet?

* Je kunt geen FIR/A kopiëren.
* Je kunt geen intentie nabootsen.
* Je kunt geen context dupliceren.
* Je kunt geen tijdlijn reconstrueren.
* Je kunt geen DO/OD/IO‑historie vervalsen.

Elke poging tot sleutelhergebruik resulteert automatisch in:

1. ContinuityHash mismatch
2. Nieuwe FIR/A (genesis van nieuwe relatie)
3. Isolatie of rejection van de oude relatie

---

# 6. Relatiebeheer

Elke relatie krijgt:

* een **FIR/A-root**
* een groeiende **ContinuityChain**
* een **ContinuityHash** (controleerbaar)

Relaties kunnen niet worden vermengd.
Relaties kunnen niet worden gedupliceerd.
Relaties kunnen niet worden verplaatst zonder semantische breuk.

Dit maakt impersonatie onmogelijk.

---

# 7. Universele Regel voor Onboarding

Bij een eerste contact geldt altijd:

* Een device of server móét flaggen.
* FIR/A bepaalt de legitimacy.
* Zonder rol, context, intent → niet flaggable → automatische reject.

Dit voorkomt dat onbekende entiteiten zelfs maar kunnen deelnemen aan de mesh.

---

# 8. INFC → OFC en de Rol in de Sleutel

Wanneer een object (foto, document, NFC‑payload) wordt verzonden:

* Het object zelf is **INFC** (betekenisloos).
* De intentie wordt eerst verzonden (IFT).
* Na IFT + context ontstaat **OFC**.

OFC‑operaties worden toegevoegd aan de ContinuityChain.

Een deepfake mist FIR/A_root en kan geen geldige ContinuityChain opbouwen.

---

# 9. Spoofing‑Preventie

De FIR/A‑root maakt spoofing onmogelijk:

* Een kloner kan cryptografische sleutels stelen.
* Maar nooit dezelfde FIR/A‑root creëren.
* Een nieuw apparaat genereert per definitie een nieuwe FIR/A.

Daarom is elke poging tot imitatie automatisch zichtbaar.

---

# 10. Conclusie

De Semantische Sleutel is:

* onvervalsbaar
* niet kopieerbaar
* altijd uniek
* gebaseerd op context + intentie in plaats van bits
* onlosmakelijk verbonden met het FIR/A‑genesis‑moment

Dit model biedt een vorm van veiligheid die cryptografische systemen nooit kunnen bereiken:
**veiligheid door betekenis, tijdlijn en continuïteit.**
