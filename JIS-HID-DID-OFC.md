# HID/DID/OFC Model — Human-Origin Assurance Layer

Status: Draft  
Scope: Uitbreiding op JIS/FIR-A/ContinuityChain voor menselijke herkomst + privacy

## Kernprincipes
- HID-KEY is uitsluitend menselijk: nooit door device/AI/robot te genereren of uit te zenden.
- DID-KEY is de device-afgeleide voor transmissies en content.
- OFC/INFC geeft de flaggable staat van content; HID wordt nooit mee verzonden.
- FIR/A-root + ContinuityChain verankeren HID/DID zonder biometrie te lekken.

## Scheiding HID vs DID
- HID-KEY: lokaal in de JTel-brein van mens + device-combo; niet exporteerbaar, dupliceerbaar of verplaatsbaar.
- DID-KEY: afgeleide voor sessies/content; deelbaar als “public” equivalent zonder biometrie.
- Content bevat alleen DID-afgeleiden + context, nooit HID zelf.

## Flow (mens → device → content)
1) NIR-Rectify + IO=OK → HID verankerd aan FIR/A-root en ContinuityChain.
2) Verzenden: pre-flight check (IO/DO/OD/context) → geen flags → DID-afgeleide + OFC-metadata toegevoegd.
3) Ontvangende kant ziet: mens gestuurd (trusted_content/human_origin) maar krijgt geen biometrie/HID.

## ContinuityChain koppeling
- Elke event in de chain krijgt een incremental continuity_hash (prev_hash + event).
- HID blijft privé; DID/OFC-informatie refereert aan de chain zonder HID bloot te leggen.
- OFC/INFC-status + tijd/context worden opgeslagen bij de chain (events-table) voor audit.

## Anti-misuse impact
- Deepfake/phishing/AI-imitatie faalt omdat:
  - Geen HID-root, geen NIR-capaciteit, geen valide IO=OK.
  - DID-structuur + chain niet matchen met menselijk gedrag.
  - OFC markeert verdacht materiaal als onvertrouwd.

## Richtlijnen voor implementatie
- HID nooit serialiseren, loggen of verzenden; alleen DID/OFC-metavelden over de lijn.
- Whitelist intents/rollen per agent; enforce continuity_hash_prev op alle calls.
- Rate limiting + sterke auth (JWT/mTLS) op router/agents; audit-trail in Postgres.
- Voor media: INFC → IFT → OFC (met DID-afgeleide), maar zonder HID.

## Volgende stap
- Integreren in Unified Draft 2025 + Brein Architecture Overview.
- Koppeling expliciet maken met FIR/A-sectie en ContinuityChain in de hoofdstandaard.
