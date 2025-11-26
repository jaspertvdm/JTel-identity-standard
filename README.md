# JTel Kit - Raspberry Pi Demo

**Powered by context, driven by intent**

Dit is de edge device implementatie van het JTel ecosystem. Het demonstreert:

- **JIS Protocol**: Device identity, FIR/A relaties, ContinuityChain
- **Sense Engine**: Sensor monitoring en rule-based triggers
- **LLM Assistant**: Natuurlijke taal interactie via lokale Ollama
- **Actuators**: LED strips, audio, en andere outputs

## Architectuur

```
┌─────────────────────────────────────────────────────────┐
│                    Raspberry Pi                         │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ JIS Client  │  │   Sense     │  │     LLM     │     │
│  │             │  │   Engine    │  │  Assistant  │     │
│  │ - DID       │  │ - Sensors   │  │ - Ollama    │     │
│  │ - FIR/A     │  │ - Rules     │  │ - Intent    │     │
│  │ - Chain     │  │ - Triggers  │  │ - Response  │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │             │
│         └────────────────┼────────────────┘             │
│                          │                              │
│                  ┌───────┴───────┐                      │
│                  │   Actuators   │                      │
│                  │ - LED Strip   │                      │
│                  │ - Audio       │                      │
│                  │ - Relays      │                      │
│                  └───────────────┘                      │
├─────────────────────────────────────────────────────────┤
│                    WebSocket / MQTT                     │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │   JTel Brein    │
                   │    (Server)     │
                   └─────────────────┘
```

## Hardware Vereisten

### Minimum
- Raspberry Pi 4 (2GB+) of Pi 5
- MicroSD kaart (16GB+)
- Voeding
- Netwerk (WiFi of Ethernet)

### Optioneel voor demo
- WS2812B LED strip (NeoPixel compatible)
- DHT22 temperatuur/vochtigheid sensor
- PIR bewegingssensor
- Speaker (3.5mm of USB)
- Microfoon (voor voice input)

## Software Setup

### 1. Raspberry Pi OS installeren

```bash
# Download Raspberry Pi Imager en installeer Raspberry Pi OS Lite (64-bit)
# Enable SSH in de imager settings
```

### 2. Basis setup

```bash
# Update systeem
sudo apt update && sudo apt upgrade -y

# Installeer Python en dependencies
sudo apt install -y python3-pip python3-venv git

# Maak project directory
mkdir -p ~/jtel
cd ~/jtel

# Clone of kopieer de bestanden
# (kopieer jis_client.py, sense.py, llm_assistant.py, actuators.py, main.py)

# Maak virtual environment
python3 -m venv venv
source venv/bin/activate

# Installeer Python packages
pip install aiohttp aiofiles
```

### 3. Ollama installeren (voor LLM)

```bash
# Installeer Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
sudo systemctl enable ollama
sudo systemctl start ollama

# Download een klein model
ollama pull phi
# Of voor meer capability:
# ollama pull mistral:7b-instruct-q4_0
```

### 4. Hardware libraries (optioneel)

```bash
# Voor GPIO
sudo apt install -y python3-rpi.gpio

# Voor NeoPixel LED strip
pip install adafruit-circuitpython-neopixel

# Voor DHT sensor
pip install adafruit-circuitpython-dht
sudo apt install -y libgpiod2

# Voor audio
sudo apt install -y python3-pygame
pip install pyttsx3
```

### 5. Configuratie aanpassen

Edit `main.py` en pas de configuratie aan:

```python
class AppConfig:
    DEVICE_NAME = "Jouw-Pi-Naam"
    DEVICE_LOCATION = "Woonkamer"
    
    # Hardware pins (pas aan voor jouw setup)
    LED_STRIP_PIN = 18
    LED_COUNT = 30
    # etc...
```

Edit `jis_client.py` voor de Brein server:

```python
class Config:
    BREIN_URL = "http://192.168.1.100:8081"  # Jouw Brein server
    BREIN_WS_URL = "ws://192.168.1.100:9000"
```

### 6. Starten

```bash
cd ~/jtel
source venv/bin/activate
python main.py
```

## Demo Commands

In de interactive console:

| Command | Beschrijving |
|---------|-------------|
| `/status` | Toon device status |
| `/mood relaxed` | Zet sfeerverlichting |
| `/light 80` | Zet helderheid op 80% |
| `/emergency` | Trigger noodgeval demo |
| `/smoke` | Trigger rookmelder demo |
| `/identify` | Flash LEDs om device te identificeren |
| `/quit` | Afsluiten |

Of typ gewoon in natuurlijke taal:
- "Zet de lichten aan"
- "Maak het wat gezelliger"
- "Wat is de temperatuur?"

## Bestanden

| Bestand | Beschrijving |
|---------|-------------|
| `main.py` | Hoofdapplicatie die alles integreert |
| `jis_client.py` | JIS protocol implementatie |
| `sense.py` | Sensor engine en rules |
| `llm_assistant.py` | LLM integratie via Ollama |
| `actuators.py` | LED, audio, relay controllers |

## Autostart bij boot

```bash
# Maak systemd service
sudo nano /etc/systemd/system/jtel-kit.service
```

```ini
[Unit]
Description=JTel Kit
After=network.target ollama.service

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/jtel
ExecStart=/home/pi/jtel/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable jtel-kit
sudo systemctl start jtel-kit
```

## Troubleshooting

### Ollama niet beschikbaar
```bash
# Check of Ollama draait
systemctl status ollama

# Check model
ollama list
```

### GPIO permission errors
```bash
# Voeg user toe aan gpio groep
sudo usermod -a -G gpio $USER
# Reboot nodig
```

### LED strip werkt niet
- Check of pin 18 correct is
- Zorg dat de LED strip genoeg stroom krijgt (externe voeding voor >30 LEDs)
- Check of je `sudo` gebruikt voor de eerste keer (voor /dev/mem access)

### WebSocket verbinding faalt
- Check of Brein server draait
- Check firewall settings
- Controleer IP adres in config

## Licentie

Proprietary - JTel / Jasper van de Meent

---

**Powered by context, driven by intent**

JTel - De command line van de toekomst is geen command line. Het is een gesprek.
