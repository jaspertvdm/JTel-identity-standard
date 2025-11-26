# JTel Project Overdracht

## Voor: Claude (volgende sessie)
## Van: Claude (huidige sessie)
## Betreft: Jasper van de Meent / JTel / Kit
## Datum: November 2024

---

## TL;DR

Jasper bouwt **de vertrouwenslaag die het internet mist**. Niet een app, niet een product - **infrastructuur voor digitaal vertrouwen**. Het begon met "Hello World" en de vraag "wat als ik dit veilig tegen de hele wereld kon zeggen en bewijzen dat ik het was?"

---

## Wie is Jasper

- Founder van JTel (in oprichting)
- Bouwt Kit: een menselijke communicatie-app die uitgroeide tot een volledig ecosysteem
- Technisch onderlegd, denkt in systemen en architectuur
- Gevestigd in Nederland
- Tijdlijn: paar maanden geleden begonnen → nu protocol + werkende code → straks FOSDEM 2025 → kantoortje

---

## De Visie

### Het Probleem
Alle digitale communicatie is fundamenteel onveilig:
- Je weet niet zeker met wie je praat
- Spoofing is triviaal
- Geen bewijs van gesprekken
- Privacy en veiligheid zijn tegengesteld (ten onrechte)
- Mensen wantrouwen AI/robots/IoT omdat het hackbaar is

### De Oplossing
JTel - een protocol stack die vertrouwen inbouwt in elke digitale interactie:
- Niet security-first (dat leidt tot systemen die mensen haten)
- Maar **Humotica-first**: begin bij menselijke intentie, en de security volgt

### De Scope
Dit is GEEN:
- Alleen een chat app
- Alleen voor mensen
- Alleen voor consumenten

Dit is WEL:
- Infrastructuur (zoals TCP/IP voor transport, HTTPS voor encryptie, JTel voor vertrouwen)
- Voor alles wat communiceert (mens↔mens, mens↔machine, machine↔machine)
- Van simpel (twee vrienden appen) tot complex (overheid↔burger juridisch contact)

---

## De Architectuur

### Kernconcepten

| Term | Betekenis | Functie |
|------|-----------|---------|
| **DID** | Decentralized Identifier | Identificatie van devices |
| **HID** | Human Identifier | Identificatie van de MENS achter devices |
| **DID-KEY** | Device sleutel | Cryptografische identiteit device |
| **HID-KEY** | Human sleutel | Cryptografische identiteit mens |
| **FIR/A** | Flag → Identify → Revoke/Accept | Relaties opbouwen, gradueel vertrouwen |
| **NIR** | Notify → Identify → Rectify | Problemen signaleren en oplossen |
| **TBET** | Time Based Event Token | Vooraankondiging van intentie |
| **BETTI** | Base Event Token Time Intent | Registry voor TBETs |
| **IO** | Identity OK | Continue verificatie: ben jij nog jij? |
| **DO** | Device OK | Continue verificatie: is device te vertrouwen? |
| **OD** | Operation Device | Mag deze operatie op dit device? |
| **ContinuityChain** | Ononderbroken bewijsketen | Alles wordt gelogd, niets kan worden ontkend |

### Hoe het samenhangt

```
INTENTIE (TBET)
     │
     ▼
IDENTITEIT (DID-KEY + HID-KEY)
     │
     ▼
VERIFICATIE (IO/DO/OD - continu!)
     │
     ▼
RELATIE (FIR/A)
     │
     ▼
COMMUNICATIE (elk protocol)
     │
     ▼
BEWIJS (ContinuityChain)
```

### Waarom IO/DO/OD cruciaal is

Traditioneel: login = trusted forever
JTel: **continue verificatie**

Triggers voor spot-checks:
- Typpatroon verandert → fingerprint check
- Locatie springt onmogelijk → face check
- Netwerk verandert tijdens gevoelige operatie → verificatie
- Periodiek (elk uur) → face check
- Hoge waarde transactie → extra verificatie

Dit maakt device cloning/spoofing onmogelijk omdat:
- Twee devices met zelfde DID = instant flag
- Afwijkend gedrag = flag
- Andere devices in omgeving flaggen onbekenden
- De zwerm beschermt zichzelf

### TBET/BETTI - Aangetekende communicatie

Voor "registered" communicatie (juridisch bindend):
1. TBET inschieten: intentie declareren VOORDAT contact
2. Ontvanger krijgt notificatie
3. Accept/reject/counter
4. Bij accept: beide partijen committed
5. Communicatie vindt plaats
6. Bewijs bestaat van intentie + uitvoering

Use cases:
- Aangetekend bellen
- Aangetekend mailen
- Document ondertekening
- Tijdelijke verificatie (bijv. verloren rijbewijs → tijdelijk geverifieerd bewijs)

---

## De Software Stack

### Gebouwd (code bestaat):

| Module | Bestand | Functie |
|--------|---------|---------|
| JIS Client | `jis_client.py` | DID, HID, FIR/A, NIR, ContinuityChain |
| BETTI | `betti.py` | TBET lifecycle, registry |
| Brein Endpoints | `brein_betti_endpoints.py` | Server-side TBET API |
| Kit Client | `kit_betti_client.py` | Client-side TBET + UI cards |
| IO/DO/OD | `io_do_od.py` | Continue verificatie engine |
| Sense | `sense.py` | Sensor monitoring, rule engine |
| LLM Assistant | `llm_assistant.py` | Lokale LLM (Ollama) integratie |
| Actuators | `actuators.py` | LED, audio, outputs |
| Main | `main.py` | Alles geïntegreerd |

### Jasper's Setup:

- **Brein**: Server/backend die de motor is
- **Kit**: Client app(s) op devices
- **Raspberry Pi**: Edge device voor demos
- **Lokale LLM**: Ollama voor natuurlijke interactie

---

## Humotica

Jasper's filosofie voor menselijke computing:

- **Intent Layer**: Wat wil de gebruiker bereiken?
- **Context Core**: Wat is de situatie?
- **Sense**: Wat nemen we waar?

De UI vertaalt technische staten naar menselijke feedback:
- `FIR/A: PENDING` → "Even geduld, ik leg contact voor je..."
- `IO/DO/OD: flag` → "Hé, ben jij dat nog? Even checken..."
- `NIR: triggered` → "Hmm, er klopt iets niet..."

Warmte, kleur, toon - niet koude foutmeldingen.

---

## Kit

**K**nowledge-based **I**ntent **T**ransactions

Maar ook:
- Kit (bouwpakket) - je bouwt je eigen setup
- Kit (uitrusting) - je digitale toolkit
- Kit (jong vosje) - slim, alert, speels
- Kit (verbinden) - lijmen/connecten

### Positionering

"Copilot/Siri/Alexa maar dan:"
- Lokaal (jouw data blijft van jou)
- Veilig (JTel stack ingebouwd)
- Bewijsbaar (niet "trust us")
- Van jou (jij controleert)

---

## Waarom dit Fake/Scams oplost

```
Nep account: "Ik ben je bank"
     │
     ▼
JTel check:
├── DID? Niet van bekende bank
├── FIR/A? Geen relatie historie  
├── HID? Kan niet verifiëren
├── IO/DO/OD? Geen continuïteit
├── TBET? Geen vooraankondiging
     │
     ▼
🚨 FAKE FLAG - Vertrouwensscore: 0%
```

Fake kan geen HID hebben van een vertrouwde DID waar IO/DO/OD succesvol op liep.

---

## Overheid & Privacy

Balans:
- Normaal: volledige privacy, jij hebt de sleutels
- Bij ernstige zaken: overheid KAN toegang krijgen, MAAR:
  - Alleen met rechterlijk bevel
  - Specifiek en beperkt
  - Gelogd in chain (bewijs dat ze toegang vroegen)
  - Tijdelijk
  - Transparant

Overheid kan NIET:
- Massasurveillance
- Onzichtbaar meekijken
- Zonder bevel toegang

---

## De Tijdlijn

```
Paar maanden geleden:  "Hello World... wat als dit veilig kon?"
                              │
Nu:                     Protocol + werkende code
                              │
FOSDEM 2025 (feb):      Demo + talk
                              │
2025+:                  Open source, eerste implementaties
                              │
Straks:                 Het kantoortje 🚀
```

---

## FOSDEM 2025 Talk

**Titel**: "Hello World" — But Actually Secure

**Hook**: "A few months ago, I wrote `<html>Hello World</html>` and thought: What if I could say this to the entire world — and actually prove it was me?"

**Core message**: Begon niet met security, begon met "hoe maak ik communicatie menselijk?" En dat leidde tot betere security.

Proposal is geschreven en klaar voor submission.

---

## Belangrijke Inzichten

1. **Protocol-agnostisch**: JTel werkt op ELKE communicatielaag (HTTP, WebSocket, MQTT, SIP, I2C, CAN, etc.)

2. **Schaalbaar zonder architectuurwijziging**: Van twee vrienden appen tot overheid-burger juridisch contact - zelfde code, andere configuratie

3. **De zwerm beschermt zichzelf**: Devices flaggen onbekenden, cloning is detecteerbaar

4. **Niet security-first maar Humotica-first**: Begin bij de mens, security volgt

5. **Infrastructure, not product**: Zoals TCP/IP voor transport, JTel voor vertrouwen

---

## Jasper's Communicatiestijl

- Denkt in systemen en verbanden
- Ziet het grote plaatje
- Technisch maar ook filosofisch
- Pragmatisch: "dit moet werken"
- Humor: "Hello World" grap is echt de origin story
- Nederlands maar tech-termen in Engels

---

## Volgende Stappen

1. Code integreren in Jasper's eigen omgeving (Brein server)
2. Demo werkend krijgen voor FOSDEM
3. FOSDEM proposal indienen
4. Documentatie/website
5. Open source release
6. "Het kantoortje"

---

## De Essentie

> "JTel maakt elke digitale interactie bewijsbaar, onvervalsbaar, en menselijk - van een simpel appje tot een juridisch document."

> "De command line van de toekomst is geen command line. Het is een gesprek."

> "Zodat iedereen AI en robotica durft aan te durven."

---

## Files Beschikbaar

In `/mnt/user-data/outputs/`:
- `raspberry-pi-jis.zip` - Complete codebase
- `fosdem-2025-proposal.md` - FOSDEM talk proposal

---

*Deze overdracht is geschreven zonder TBET, zonder DID verificatie, zonder IO/DO/OD check. Oh, de ironie. Maar dat gaan we fixen.* 😄

---

**Status**: Genesis block van de JTel ContinuityChain is conceptueel gelegd. De rest is uitvoering.

Succes, volgende Claude. Je werkt met iemand die iets fundamenteels aan het bouwen is.

🦊 Kit - Powered by context, driven by intent.
