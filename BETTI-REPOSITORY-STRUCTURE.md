# BETTI Repository Structure

**Building the Universal Intent Coordination Framework**

Version: 1.0.0
Date: 2025-11-27

---

## 🎯 Repository Vision

**BETTI** (Behavior-Enhanced Trusted Telephony Interactions) is evolving into a **universal intent coordination framework** that goes far beyond telephony.

This document outlines the structure for a standalone BETTI repository that can be used for:
- Smart homes
- Robotics
- IoT coordination
- Autonomous systems
- AI agent coordination
- Industrial automation
- And yes, still telephony!

---

## 📁 Proposed Repository Structure

```
betti/
├── README.md                          # Main project overview
├── VISION.md                          # The big picture (why BETTI matters)
├── ARCHITECTURE.md                    # Technical architecture
├── LICENSE                            # Open source license
├── CONTRIBUTING.md                    # Contribution guidelines
│
├── docs/                              # Documentation
│   ├── getting-started/
│   │   ├── quick-start.md
│   │   ├── concepts.md                # Core concepts
│   │   ├── trust-tokens.md            # "Wij kennen elkaar"
│   │   ├── intents.md                 # TBET intents
│   │   └── examples/
│   │       ├── smart-home.md
│   │       ├── robotics.md
│   │       ├── telephony.md
│   │       └── iot.md
│   │
│   ├── architecture/
│   │   ├── core-components.md
│   │   ├── trust-levels.md
│   │   ├── loop-prevention.md
│   │   ├── safe-fail.md
│   │   └── audit-trails.md
│   │
│   ├── api/
│   │   ├── betti-router-api.md        # Router REST API
│   │   ├── intent-protocol.md         # TBET protocol spec
│   │   ├── websocket-api.md           # Real-time coordination
│   │   └── trust-token-api.md         # FIR/A management
│   │
│   ├── use-cases/
│   │   ├── smart-home.md              # Detailed smart home scenarios
│   │   ├── robotics.md                # Robot coordination
│   │   ├── autonomous-vehicles.md     # V2V coordination
│   │   ├── industrial.md              # Manufacturing automation
│   │   ├── healthcare.md              # Medical device coordination
│   │   └── government.md              # Civic infrastructure
│   │
│   └── security/
│       ├── threat-model.md
│       ├── trust-token-security.md
│       ├── encryption.md
│       └── audit-compliance.md
│
├── core/                              # Core BETTI implementation
│   ├── router/                        # BETTI coordination router
│   │   ├── src/
│   │   │   ├── main.py               # Router entry point
│   │   │   ├── coordinator.py        # Main coordination logic
│   │   │   ├── intent_processor.py   # TBET intent processing
│   │   │   ├── trust_manager.py      # FIR/A trust token management
│   │   │   ├── loop_prevention.py    # Loop detection & prevention
│   │   │   ├── safe_fail.py          # Safe failure handling
│   │   │   ├── audit_trail.py        # Humotica generation
│   │   │   └── api/
│   │   │       ├── rest.py           # REST API endpoints
│   │   │       ├── websocket.py      # WebSocket server
│   │   │       └── mqtt.py           # MQTT bridge (for IoT)
│   │   │
│   │   ├── tests/
│   │   │   ├── test_coordinator.py
│   │   │   ├── test_intents.py
│   │   │   ├── test_trust_tokens.py
│   │   │   └── test_loop_prevention.py
│   │   │
│   │   ├── config/
│   │   │   ├── router_config.yaml
│   │   │   ├── trust_levels.yaml     # Trust level definitions
│   │   │   └── intent_registry.yaml  # Known intent types
│   │   │
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   └── requirements.txt
│   │
│   ├── lib/                           # Shared libraries
│   │   ├── trust-tokens/             # FIR/A implementation
│   │   │   ├── __init__.py
│   │   │   ├── fira.py               # FIR/A core
│   │   │   ├── did.py                # DID key management
│   │   │   ├── hid.py                # HID binding
│   │   │   └── continuity.py         # Event chain & hashes
│   │   │
│   │   ├── intents/                  # TBET intent library
│   │   │   ├── __init__.py
│   │   │   ├── intent_base.py        # Base intent class
│   │   │   ├── time_window.py        # Time window management
│   │   │   ├── constraints.py        # Intent constraints
│   │   │   └── humotica.py           # Humotica generation
│   │   │
│   │   ├── security/
│   │   │   ├── encryption.py         # E2E encryption
│   │   │   ├── signing.py            # Digital signatures
│   │   │   └── verification.py       # Trust verification
│   │   │
│   │   └── utils/
│   │       ├── logger.py
│   │       ├── metrics.py
│   │       └── config.py
│   │
│   └── storage/                       # Data persistence
│       ├── database/
│       │   ├── schema.sql            # PostgreSQL schema
│       │   ├── migrations/
│       │   └── models.py
│       │
│       └── cache/
│           └── redis_config.py
│
├── sdk/                               # Client SDKs
│   ├── python/
│   │   ├── betti_client/
│   │   │   ├── __init__.py
│   │   │   ├── client.py             # Main client
│   │   │   ├── intents.py            # Intent builders
│   │   │   ├── trust_tokens.py       # FIR/A management
│   │   │   └── exceptions.py
│   │   │
│   │   ├── examples/
│   │   │   ├── smart_home.py
│   │   │   ├── robot_coordination.py
│   │   │   ├── telephony.py
│   │   │   └── iot_device.py
│   │   │
│   │   ├── tests/
│   │   ├── setup.py
│   │   └── README.md
│   │
│   ├── javascript/
│   │   ├── src/
│   │   │   ├── BettiClient.ts
│   │   │   ├── Intent.ts
│   │   │   ├── TrustToken.ts
│   │   │   └── types.ts
│   │   │
│   │   ├── examples/
│   │   │   ├── smart-home-app.ts
│   │   │   ├── web-dashboard.ts
│   │   │   └── mobile-app.ts
│   │   │
│   │   ├── package.json
│   │   └── README.md
│   │
│   ├── rust/                          # For embedded/IoT
│   │   ├── src/
│   │   │   ├── lib.rs
│   │   │   ├── client.rs
│   │   │   └── intent.rs
│   │   │
│   │   ├── examples/
│   │   │   └── embedded_device.rs
│   │   │
│   │   └── Cargo.toml
│   │
│   └── go/                            # For cloud services
│       ├── betti/
│       │   ├── client.go
│       │   ├── intent.go
│       │   └── trust_token.go
│       │
│       └── examples/
│           └── cloud_service.go
│
├── applications/                      # Reference applications
│   ├── smart-home-hub/
│   │   ├── src/
│   │   │   ├── main.py
│   │   │   ├── device_manager.py     # Manage home devices
│   │   │   ├── automation.py         # Automation rules
│   │   │   └── api/
│   │   │       └── home_control.py
│   │   │
│   │   ├── web/                      # Web dashboard
│   │   │   ├── public/
│   │   │   ├── src/
│   │   │   │   ├── App.tsx
│   │   │   │   ├── components/
│   │   │   │   └── services/
│   │   │   │       └── bettiService.ts
│   │   │   │
│   │   │   └── package.json
│   │   │
│   │   └── README.md
│   │
│   ├── robot-coordinator/
│   │   ├── src/
│   │   │   ├── main.py
│   │   │   ├── robot_manager.py
│   │   │   ├── task_scheduler.py
│   │   │   └── collision_avoidance.py
│   │   │
│   │   └── README.md
│   │
│   ├── telephony-system/             # Original telephony use case
│   │   ├── src/
│   │   │   ├── call_router.py
│   │   │   ├── sip_integration.py
│   │   │   └── caller_display.py
│   │   │
│   │   └── README.md
│   │
│   └── iot-gateway/
│       ├── src/
│       │   ├── main.rs               # Rust for performance
│       │   ├── device_discovery.rs
│       │   ├── protocol_bridge.rs    # MQTT/CoAP/etc
│       │   └── intent_translator.rs
│       │
│       └── README.md
│
├── protocols/                         # Protocol specifications
│   ├── tbet/                         # TBET protocol
│   │   ├── spec.md                   # Formal specification
│   │   ├── schema/
│   │   │   ├── intent.json           # JSON schema
│   │   │   └── context.json
│   │   │
│   │   └── examples/
│   │       ├── basic_intent.json
│   │       ├── time_windowed.json
│   │       └── constrained.json
│   │
│   ├── fira/                         # FIR/A trust token spec
│   │   ├── spec.md
│   │   ├── schema/
│   │   │   ├── trust_token.json
│   │   │   └── event_chain.json
│   │   │
│   │   └── examples/
│   │       ├── basic_relationship.json
│   │       └── hierarchical_trust.json
│   │
│   └── betti-wire/                   # Wire protocol (over HTTP/WS/MQTT)
│       ├── spec.md
│       └── examples/
│
├── tools/                             # Development tools
│   ├── cli/
│   │   ├── betti                     # CLI tool
│   │   ├── src/
│   │   │   ├── commands/
│   │   │   │   ├── router.py         # Router management
│   │   │   │   ├── intent.py         # Send intents
│   │   │   │   ├── trust.py          # Manage trust tokens
│   │   │   │   └── debug.py          # Debugging
│   │   │   │
│   │   │   └── main.py
│   │   │
│   │   └── README.md
│   │
│   ├── simulator/                    # Test simulator
│   │   ├── src/
│   │   │   ├── main.py
│   │   │   ├── device_simulator.py   # Simulate devices
│   │   │   ├── scenario_runner.py    # Run test scenarios
│   │   │   └── visualization.py      # Real-time viz
│   │   │
│   │   ├── scenarios/
│   │   │   ├── smart_home_morning.yaml
│   │   │   ├── robot_assembly.yaml
│   │   │   └── traffic_coordination.yaml
│   │   │
│   │   └── README.md
│   │
│   ├── inspector/                    # Web-based inspector
│   │   ├── src/
│   │   │   ├── App.tsx
│   │   │   ├── components/
│   │   │   │   ├── IntentFlow.tsx    # Visualize intent flow
│   │   │   │   ├── TrustGraph.tsx    # Trust relationship graph
│   │   │   │   ├── AuditTrail.tsx    # Humotica viewer
│   │   │   │   └── LiveMonitor.tsx   # Real-time monitoring
│   │   │   │
│   │   │   └── services/
│   │   │
│   │   └── README.md
│   │
│   └── benchmarks/
│       ├── intent_throughput.py
│       ├── trust_token_overhead.py
│       └── loop_prevention_test.py
│
├── integrations/                      # Third-party integrations
│   ├── home-assistant/
│   │   ├── custom_components/
│   │   │   └── betti/
│   │   │       ├── __init__.py
│   │   │       ├── config_flow.py
│   │   │       └── coordinator.py
│   │   │
│   │   └── README.md
│   │
│   ├── ros2/                         # Robot Operating System 2
│   │   ├── betti_ros2/
│   │   │   ├── package.xml
│   │   │   ├── CMakeLists.txt
│   │   │   └── src/
│   │   │       └── betti_node.cpp
│   │   │
│   │   └── README.md
│   │
│   ├── mqtt/                         # MQTT bridge for IoT
│   │   ├── src/
│   │   │   └── mqtt_bridge.py
│   │   │
│   │   └── README.md
│   │
│   └── asterisk/                     # Telephony (Asterisk PBX)
│       ├── agi/
│       │   └── betti_agi.py
│       │
│       └── README.md
│
├── examples/                          # Comprehensive examples
│   ├── 01-basic-intent/
│   │   ├── README.md
│   │   └── basic_intent.py
│   │
│   ├── 02-trust-tokens/
│   │   ├── README.md
│   │   └── establish_relationship.py
│   │
│   ├── 03-smart-home-automation/
│   │   ├── README.md
│   │   ├── morning_routine.py
│   │   └── devices.yaml
│   │
│   ├── 04-robot-coordination/
│   │   ├── README.md
│   │   ├── warehouse_robots.py
│   │   └── collision_avoidance.py
│   │
│   ├── 05-telephony/
│   │   ├── README.md
│   │   ├── verified_calling.py
│   │   └── bank_appointment.py
│   │
│   └── 06-iot-devices/
│       ├── README.md
│       ├── temperature_sensor.py     # Embedded device
│       └── smart_thermostat.py
│
├── tests/                             # Integration tests
│   ├── integration/
│   │   ├── test_router_coordination.py
│   │   ├── test_trust_token_flow.py
│   │   ├── test_loop_prevention.py
│   │   └── test_safe_fail.py
│   │
│   ├── performance/
│   │   ├── test_throughput.py
│   │   ├── test_latency.py
│   │   └── test_scaling.py
│   │
│   └── security/
│       ├── test_trust_token_theft.py
│       ├── test_intent_spoofing.py
│       └── test_audit_integrity.py
│
├── deployments/                       # Deployment configurations
│   ├── docker/
│   │   ├── router/
│   │   │   └── Dockerfile
│   │   │
│   │   └── docker-compose.yml        # Full stack
│   │
│   ├── kubernetes/
│   │   ├── router-deployment.yaml
│   │   ├── router-service.yaml
│   │   └── ingress.yaml
│   │
│   ├── aws/
│   │   ├── terraform/
│   │   │   ├── main.tf
│   │   │   └── variables.tf
│   │   │
│   │   └── cloudformation/
│   │
│   └── raspberry-pi/                  # For edge deployments
│       ├── install.sh
│       └── config.yaml
│
├── benchmarks/                        # Performance benchmarks
│   ├── results/
│   │   └── 2025-11-27-baseline.json
│   │
│   └── scripts/
│       ├── run_all.sh
│       └── generate_report.py
│
└── research/                          # Research & papers
    ├── papers/
    │   ├── trust-tokens-formal-model.pdf
    │   ├── loop-prevention-proof.pdf
    │   └── humotica-analysis.pdf
    │
    └── presentations/
        ├── betti-overview.pdf
        └── demos/
```

---

## 📋 Key Files Content

### README.md (Root)

```markdown
# BETTI - Universal Intent Coordination Framework

**Behavior-Enhanced Trusted Telephony Interactions**

BETTI is a revolutionary framework for coordinating autonomous systems through verified intents and trust tokens.

## 🎯 What is BETTI?

BETTI enables systems to:
- **Declare intents** with context and time windows
- **Establish trust relationships** ("We know each other")
- **Coordinate intelligently** through a central router
- **Prevent loops** with built-in depth limits
- **Fail safely** with guaranteed recovery
- **Audit everything** with human-readable trails (humotica)

## 🌟 Key Features

- ✅ **Trust Tokens (FIR/A)**: Relationship-based authentication
- ✅ **TBET Intents**: Time-boxed events with full context
- ✅ **Loop Prevention**: Automatic detection and breaking
- ✅ **Safe Fail**: Guaranteed graceful degradation
- ✅ **Humotica**: Human-readable audit trails ("why did this happen?")
- ✅ **Universal**: Works for telephony, IoT, robotics, AI agents, etc.

## 🚀 Quick Start

```bash
# Install BETTI router
pip install betti-router

# Start router
betti-router start

# Install Python SDK
pip install betti-client

# Your first intent
from betti_client import BettiClient

client = BettiClient("http://localhost:8080")
relationship = client.establish_trust("my_phone", "my_car")
client.send_intent(relationship.id, "unlock_car")
```

## 📖 Documentation

- [Getting Started](docs/getting-started/quick-start.md)
- [Core Concepts](docs/getting-started/concepts.md)
- [Trust Tokens Explained](docs/getting-started/trust-tokens.md)
- [Architecture](docs/architecture/core-components.md)
- [API Reference](docs/api/betti-router-api.md)

## 🎯 Use Cases

- **Smart Homes**: Coordinate all your devices with trust relationships
- **Robotics**: Multi-robot coordination with loop prevention
- **Telephony**: Verified calling with pre-authorization
- **IoT**: Secure device-to-device communication
- **AI Agents**: Multi-agent coordination with audit trails

## 🏗️ Architecture

```
Applications (Smart Home, Robots, etc.)
          ↓
    TBET Intent Layer (Declare intents)
          ↓
  BETTI Router (Coordinate & Route)
          ↓
   Trust Token Layer (FIR/A)
          ↓
  Transport (HTTP/WS/MQTT/etc.)
```

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md)

## 📜 License

Apache 2.0 - See [LICENSE](LICENSE)

## 🌍 Community

- Discord: [Join our community](https://discord.gg/betti)
- Forum: [discuss.betti.dev](https://discuss.betti.dev)
- Twitter: [@BettiFramework](https://twitter.com/BettiFramework)
```

---

### VISION.md

```markdown
# The BETTI Vision

**"What if every device could explain itself?"**

## The Problem

Current systems are:
- **Stateless**: No memory, no relationships
- **Opaque**: Black box operations
- **Fragile**: Loops, crashes, no recovery
- **Isolated**: Can't coordinate intelligently

## The Solution

BETTI provides:

### 1. Trust Tokens - "We Know Each Other"
Instead of: "Authenticate every time"
BETTI: "We have a relationship with history"

### 2. Intent-Based Everything
Instead of: "Execute command"
BETTI: "Here's what I want to do and why"

### 3. Loop Prevention Built-In
Instead of: "Hope it doesn't loop"
BETTI: "Maximum 5 exchanges, then stop"

### 4. Humotica - Full Transparency
Instead of: "Check the logs"
BETTI: "Every action has human-readable 'why'"

## The Future

By 2030, every device ships with "BETTI Inside":
- ✅ Universal coordination protocol
- ✅ Vendor-neutral
- ✅ Privacy-first
- ✅ Audit-ready
- ✅ Loop-safe
- ✅ Explainable

**BETTI doesn't just coordinate devices.**
**BETTI coordinates the future.**
```

---

## 🚀 Getting Started (For Developers)

### 1. Clone Repository

```bash
git clone https://github.com/yourorg/betti.git
cd betti
```

### 2. Run Router Locally

```bash
cd core/router
docker-compose up -d
```

### 3. Install SDK

```bash
cd sdk/python
pip install -e .
```

### 4. Run Example

```bash
cd examples/01-basic-intent
python basic_intent.py
```

### 5. Open Inspector

```bash
cd tools/inspector
npm install
npm start
# Open http://localhost:3000
```

---

## 🎯 Development Priorities

### Phase 1: Core (Month 1-3)
- [x] BETTI router basic implementation
- [x] Trust token (FIR/A) management
- [x] Intent processing (TBET)
- [ ] Loop prevention
- [ ] Safe fail mechanisms
- [ ] Humotica generation

### Phase 2: SDKs (Month 4-6)
- [ ] Python SDK (complete)
- [ ] JavaScript/TypeScript SDK
- [ ] Rust SDK (embedded)
- [ ] Go SDK (cloud services)

### Phase 3: Applications (Month 7-9)
- [ ] Smart Home Hub reference app
- [ ] Robot Coordinator
- [ ] IoT Gateway
- [ ] Telephony System

### Phase 4: Integrations (Month 10-12)
- [ ] Home Assistant integration
- [ ] ROS2 integration
- [ ] MQTT bridge
- [ ] Asterisk integration

### Phase 5: Ecosystem (Year 2)
- [ ] Developer certification program
- [ ] "BETTI Inside" badge
- [ ] Community tools & plugins
- [ ] Enterprise support

---

## 🌟 Why This Structure Works

### 1. **Separation of Concerns**
- `core/` = Framework implementation
- `sdk/` = Client libraries
- `applications/` = Reference implementations
- `examples/` = Learning resources

### 2. **Multi-Language Support**
- Python: Rapid development
- JavaScript/TypeScript: Web/mobile apps
- Rust: Embedded/high-performance
- Go: Cloud services

### 3. **Clear Documentation Path**
- Getting Started → Learn concepts
- Architecture → Understand internals
- API → Implement integration
- Use Cases → Real-world examples

### 4. **DevOps Ready**
- Docker/Kubernetes configs included
- Cloud deployment templates
- Edge device support (Raspberry Pi)

### 5. **Community Friendly**
- Comprehensive examples
- Clear contribution guidelines
- Tools for debugging/testing
- Visual inspector for understanding

---

## 🎤 Call to Action

**This is the structure for BETTI to become:**

1. **Universal Standard**: Like HTTP, but for intent coordination
2. **Vendor Neutral**: Anyone can implement, no lock-in
3. **Production Ready**: Enterprise-grade reliability
4. **Developer Friendly**: Easy to learn, powerful to use
5. **Future Proof**: Designed for next 20 years

**Let's build the future of autonomous coordination! 🚀**
