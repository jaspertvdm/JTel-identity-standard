# JTel Identity Standard (JIS) v0.1  
## IO (Identity OK) & NIR (Notify–Identify–Rectify) on top of Humotica


# JTel Identity Standard (JIS) v0.1  
## IO (Identity OK) & NIR (Notify–Identify–Rectify) on top of Humotica

**Status:** Draft  
**Auteur:** Jasper van de Meent (JTel)  
**Doel:** Definitie van een doorlopende, context- en intentie-gedreven digitale identiteitslaag, gebouwd op humotica.

---

## 1. Inleiding

De JTel Identity Standard (JIS) beschrijft een continue, semantische identiteitslaag bovenop bestaande authenticatie- en autorisatiemechanismen.

In plaats van identiteiten te behandelen als een éénmalig “login-moment”, gaat JIS uit van:

- **IO (Identity OK):** een doorlopende inschatting of gedrag, context en intentie overeenkomen met de bekende eigenschappen van een gebruiker.
- **NIR (Notify – Identify – Rectify):** een proces voor het menselijk, veilig en frictie-arm herstellen of aanscherpen van vertrouwen.
- **fail2flag4intent:** een mechanisme om afwijkingen niet stil te laten falen, maar te vertalen naar veiligheids-signalen (flags) die context toevoegen in plaats van blokkeren.

JIS is ontworpen als semantische laag bovenop bestaande protocollen (HTTP, Matrix, SIP, ntfy, MQTT, etc.) en bestaande authenticatie-methodes (wachtwoorden, WebAuthn, MFA). Het vervangt die niet, maar voegt **intent- en contextbegrip** toe.

---

## 2. Doelen & Niet-doelen

### 2.1 Doelen

- Een **continue identiteitstoestand** definiëren: “Identity OK” (IO).
- Een **bidirectioneel proces** definiëren voor herauthenticatie en twijfelgevallen: NIR.
- Een generiek **flag → notice → handle**-model definiëren dat boven iedere app, dienst of device kan draaien.
- Een **semantische veiligheidslaag** bieden die social engineering en misbruik moeilijker maakt, door gedrag, context en intentie te combineren.
- Compatibel zijn met zowel **bestaande** als **nieuwe** apparaten en diensten, zonder verplicht firmware- of protocol-updates.

### 2.2 Niet-doelen

- Authenticatie-methodes (wachtwoord, WebAuthn, MFA) vervangen.
- Een nieuw transportprotocol definiëren.
- Een specifiek storage- of database-model voorschrijven.
- Een vendor-locked ecosysteem creëren.

---

## 3. Terminologie

- **Actor:** een gebruiker, dienst of proces waarvoor identiteit en gedrag worden beoordeeld.
- **IO (Identity OK):** toestand waarin gedrag, context en intentie overeenkomen met het bekende profiel van de actor.
- **Humotica:** de mensgerichte interactielaag die intentie en context samenbrengt en vertaalt naar acties.
- **fail2flag4intent:** veiligheidsmechanisme dat afwijkend of onvolledig gedrag omzet in flags in plaats van stille errors of brute blokkades.
- **Flag:** een geregistreerde afwijking, onzekerheid of risicosignaal; geen directe blokkade.
- **Notice:** expliciete melding of vraag naar actor of operator (“check dit even”).
- **Handle:** concrete actie als gevolg van de beoordeling (bijv. extra verificatie, lock, beperking, of juist risk-verlaging).
- **NIR:** Notify–Identify–Rectify; het proces waarmee flags worden opgelost en vertrouwen wordt hersteld.
- **RiskScore:** numerieke inschatting (bijv. 0.0–1.0) van het risico dat een actie niet overeenkomt met de echte actor-intentie.
- **Device:** elk hardware- of software-endpoint dat events kan sturen en/of acties kan ontvangen (smartphone, horloge, auto, deurslot, deurbel, etc.).
- **Kit:** de interpretatie- en interfacecomponent die humotica, JIS en de onderliggende JTel-kernen verbindt met de gebruiker.

---

## 4. Architectuur-overzicht

Logische lagen (vereenvoudigd):

```text
[ Menselijke expressie ]
        │
   Humotica Layer
        │
       KIT
        │
  fail2flag4intent
        │
 ┌──────┼─────────────────────────────┐
 │  IO State Engine (Identity OK)    │
 │  JTel Intent / Context / Sense    │
 │  JTel Safety Core (kritische cases) │
 └──────┼─────────────────────────────┘
        │
  JTel Routing Engine (multi-channel)
        │
 ┌──────┼─────────────────────────────────────────────┐
 │  Device Inputs  │  Device Outputs  │  Externe diensten │
 └───────────────────────────────────────────────────────┘
