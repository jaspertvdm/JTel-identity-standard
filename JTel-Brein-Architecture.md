# JTel Brein Architecture — Overview (Draft)

Doel: kerncomponenten, lagen en hoofdflows van het JTel-brein, met verankering in FIR/A + ContinuityChain en HID/DID/OFC.

## Lagen
- **Humotica Layer**: taal/ritme/affect → intent + context hints.
- **Intent Core**: normaliseert intent, doel, targets.
- **Context Core**: tijd/locatie/rol/kanaal; matcht tegen policy en continuïteit.
- **Sense Layer**: device/omgeving-signalen, gedragspatronen, afwijkingsdetectie.
- **Safety Core (fail2flag4intent)**: IO/DO/OD/NIR beslislogica, flags, timeboxes.
- **Continuity Engine**: FIR/A-root + ContinuityChain (incremental hash, events).
- **Content Semantics**: INFC → IFT → OFC, SCS-koppeling, DID-afgeleiden.
- **Identity Boundary**: HID (mens, nooit gedeeld) ↔ DID (device-afgeleide).

## Hoofdflows
1) **Onboarding (FIR/A)**: Flag → Identify → Accept/Revoke; creëert FIR/A-root + eerste hash; rollen/context geregistreerd.
2) **Intent/Operatie**: IFT ontvangen → IO/DO/OD check → append event → continuity_hash updaten → OFC/INFC verrijken.
3) **NIR**: Notify bij twijfel → Identify → Rectify of Revoke; chain krijgt NIR-events.
4) **Content**: INFC + IFT → OFC + SCS; HID blijft privé, DID-afgeleide wordt meegestuurd.

## Datapaden
- **Events**: canonieke JSON, seq-nr, incremental hash; opslag in log (Postgres).
- **Caches/Timers**: Redis voor NIR-timeboxes en rate limits.
- **Auth**: mTLS of JWT per agent; intent/role whitelists per service.

## Veiligheidsregels
- HID blijft binnen brein/device; nooit serialiseren of verzenden.
- continuity_hash_prev verplicht per call; mismatch → 409/flag/NIR.
- Whitelist intents/rollen; rate-limit per IP/agent; audit alle events.
- TLS/mTLS op transport; gescheiden secrets/keys per agent.

## Componenten in deployment
- **Router/API**: FastAPI/HTTP endpoint laag; valideert auth, rate-limit, schema’s; schrijft events naar log.
- **Brein Core**: Intent/Context/Safety/Continuity modules; kan als service of library draaien.
- **Agents**: SIP/WebRTC/Chat/IoT hooks; vertalen ruwe signalen naar JIS-events.
- **Stores**: Postgres (events/log); Redis (counters/timeboxes).

## Koppeling aan standaarden
- FIR/A + ContinuityChain: basisanker voor relaties en hashes.
- HID/DID/OFC: menselijke herkomstlaag zonder biometrie te delen.
- IO/DO/OD/NIR: beslis- en herstelmechaniek bovenop transportprotocollen.
