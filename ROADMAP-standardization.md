# JTel Semantic Safety – Roadmap naar (Inter)nationale Standaard

## Fase 0 — Basis opschonen (nu)
- Waarschuwingen/compose version verwijderen; poorten/documentatie consistent houden.
- Eén canonical repo met tags/releases en changelog.

## Fase 1 — Spec & RFC-stijl
- Opstellen RFC-achtige specificatie: terminologie (HID/DID/IO/DO/OD/NIR/IFT/INFC/OFC), message formats (HTTP/WS/MQTT headers/payloads), foutcodes, conformance-eisen.
- Registries: intents, roles, context keys, header-namen; versiebeleid.
- Threat model + mitigaties (auth, rate-limit, replay, downgrade, privacy).
- Privacy/PIA: HID nooit op de lijn; logging-richtlijnen.

## Fase 2 — Referentie-implementaties
- Router: harden (mTLS/JWT, whitelists, ratelimits, Postgres/Redis).
- Bridges: HTTP, WebSocket, MQTT, SMTP-milter/proxy, SIP/ARI-AGI, WebRTC signaling hook.
- Client-SDK skeletons: HTTP/WS/MQTT (Python/Node/Go) met fir_a_id + continuity_hash_prev patroon.
- Testvectors: vaste fir_a_id/intents/hash-chains voor conformance.

## Fase 3 — Conformance & Interop
- Conformance suite: tests die goede/ foute continuity_hash_prev en intents simuleren; verwacht 200/409/401.
- Interop events: matrix van bridges/protocols onderling (HTTP↔MQTT↔WS).
- Benchmarks: latency/throughput-impact van checks.

## Fase 4 — Pilots & Security Review
- Pilots per domein: SIP/VoIP, WebRTC signaling, mail (milter), IoT/MQTT.
- Externe security review/pen-test op router/bridges.
- Operational playbooks: key-rotatie, incident/NIR/flag-handling, logging/retentie.

## Fase 5 — Governance & Publicatie
- Governance: registries-beheer, wijzigingsproces, versiebeleid (semver).
- Licentie/Legal: open standaard + referentie-implementatie licentie.
- Publicatie: RFC-stijl document, whitepaper, referentiesite.

## Directe acties (korte termijn)
- Draft RFC-stijl spec starten in repo (JIS-RFC.md) met message formats + error codes.
- Integratie-uitwerkingen toevoegen voor SMTP (milter) en SIP (ARI/AGI) als werkende voorbeelden.
- Conformance testvectors schrijven voor continuity_hash (good/bad chain) en intent-whitelist.
- Compose waarschuwingsregel (`version`) verwijderen en poortmappingen definitief vastleggen.
