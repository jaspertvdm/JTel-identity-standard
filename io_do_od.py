"""
IO/DO/OD - Continuous Identity & Device Verification
=====================================================

The heartbeat of the JTel trust system.

IO  = Identity OK        - Is the human still who they claim to be?
DO  = Device OK          - Is the device still trustworthy?
OD  = Operation Device   - Is this operation allowed on this device?

This module provides:
- Continuous verification (not just login)
- Behavioral analysis
- Biometric spot-checks
- Anomaly detection
- Flag generation for suspicious patterns

The system doesn't just check once - it KEEPS checking.
Any deviation can trigger a flag, requiring re-verification
or session termination.

Author: Jasper van de Meent / JTel
"""

import asyncio
import json
import hashlib
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any, Callable, Tuple
from enum import Enum
from collections import deque
import statistics


# =============================================================================
# Enums
# =============================================================================

class VerificationStatus(Enum):
    """Status of a verification check"""
    OK = "ok"
    WARNING = "warning"
    FLAGGED = "flagged"
    BLOCKED = "blocked"
    PENDING = "pending"


class FlagSeverity(Enum):
    """Severity of a flag"""
    LOW = "low"           # Log only
    MEDIUM = "medium"     # Require soft verification
    HIGH = "high"         # Require hard verification
    CRITICAL = "critical" # Immediate session termination


class FlagCategory(Enum):
    """Category of flags"""
    IDENTITY = "identity"       # IO flags
    DEVICE = "device"           # DO flags
    OPERATION = "operation"     # OD flags
    BEHAVIOR = "behavior"       # Behavioral anomaly
    NETWORK = "network"         # Network anomaly
    BIOMETRIC = "biometric"     # Biometric mismatch
    TEMPORAL = "temporal"       # Time-based anomaly
    LOCATION = "location"       # Location anomaly


class VerificationType(Enum):
    """Types of verification that can be requested"""
    NONE = "none"
    FACE_CHECK = "face_check"
    FINGERPRINT = "fingerprint"
    VOICE_CHECK = "voice_check"
    PIN = "pin"
    PASSPHRASE = "passphrase"
    DEVICE_CONFIRM = "device_confirm"
    LOCATION_CONFIRM = "location_confirm"
    FULL_REAUTH = "full_reauth"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class IODOODState:
    """Current state of IO/DO/OD verification"""
    io_status: VerificationStatus = VerificationStatus.OK
    do_status: VerificationStatus = VerificationStatus.OK
    od_status: VerificationStatus = VerificationStatus.OK
    
    io_confidence: float = 1.0  # 0.0 - 1.0
    do_confidence: float = 1.0
    od_confidence: float = 1.0
    
    last_io_check: Optional[str] = None
    last_do_check: Optional[str] = None
    last_od_check: Optional[str] = None
    
    active_flags: List[str] = field(default_factory=list)
    pending_verification: Optional[VerificationType] = None
    
    def overall_status(self) -> VerificationStatus:
        """Get overall verification status"""
        statuses = [self.io_status, self.do_status, self.od_status]
        
        if VerificationStatus.BLOCKED in statuses:
            return VerificationStatus.BLOCKED
        if VerificationStatus.FLAGGED in statuses:
            return VerificationStatus.FLAGGED
        if VerificationStatus.WARNING in statuses:
            return VerificationStatus.WARNING
        if VerificationStatus.PENDING in statuses:
            return VerificationStatus.PENDING
        return VerificationStatus.OK
    
    def overall_confidence(self) -> float:
        """Get overall confidence (product of all three)"""
        return self.io_confidence * self.do_confidence * self.od_confidence


@dataclass
class Flag:
    """A verification flag"""
    flag_id: str
    category: FlagCategory
    severity: FlagSeverity
    reason: str
    details: Dict[str, Any]
    timestamp: str
    resolved: bool = False
    resolved_at: Optional[str] = None
    resolution: Optional[str] = None
    required_verification: VerificationType = VerificationType.NONE


@dataclass
class BehaviorSample:
    """A sample of user behavior for analysis"""
    timestamp: float
    sample_type: str  # "keystroke", "mouse", "touch", "voice", "face"
    data: Dict[str, Any]


@dataclass
class DeviceFingerprint:
    """Device fingerprint for DO verification"""
    device_id: str
    hardware_hash: str
    software_hash: str
    network_signature: str
    location_hash: Optional[str] = None
    last_seen: Optional[str] = None
    trust_score: float = 1.0


# =============================================================================
# Behavior Analyzers
# =============================================================================

class KeystrokeAnalyzer:
    """Analyzes typing patterns for identity verification"""
    
    def __init__(self):
        self.baseline: Dict[str, float] = {}  # Baseline timing patterns
        self.samples: deque = deque(maxlen=1000)
        self.min_samples_for_baseline = 100
    
    def record_keystroke(self, key: str, timestamp: float, duration: float):
        """Record a keystroke event"""
        self.samples.append({
            "key": key,
            "timestamp": timestamp,
            "duration": duration,
            "interval": None  # Set below
        })
        
        # Calculate interval from previous
        if len(self.samples) > 1:
            prev = self.samples[-2]
            self.samples[-1]["interval"] = timestamp - prev["timestamp"]
    
    def calculate_baseline(self):
        """Calculate baseline typing pattern"""
        if len(self.samples) < self.min_samples_for_baseline:
            return
        
        intervals = [s["interval"] for s in self.samples if s["interval"]]
        durations = [s["duration"] for s in self.samples]
        
        self.baseline = {
            "avg_interval": statistics.mean(intervals),
            "std_interval": statistics.stdev(intervals) if len(intervals) > 1 else 0,
            "avg_duration": statistics.mean(durations),
            "std_duration": statistics.stdev(durations) if len(durations) > 1 else 0
        }
    
    def analyze_current(self, window: int = 50) -> Tuple[float, Optional[str]]:
        """
        Analyze recent typing against baseline.
        Returns (confidence, reason) where confidence is 0.0-1.0
        """
        if not self.baseline or len(self.samples) < window:
            return 1.0, None
        
        recent = list(self.samples)[-window:]
        intervals = [s["interval"] for s in recent if s["interval"]]
        durations = [s["duration"] for s in recent]
        
        if not intervals:
            return 1.0, None
        
        # Calculate deviation from baseline
        interval_diff = abs(statistics.mean(intervals) - self.baseline["avg_interval"])
        duration_diff = abs(statistics.mean(durations) - self.baseline["avg_duration"])
        
        # Normalize by standard deviation
        interval_z = interval_diff / max(self.baseline["std_interval"], 0.01)
        duration_z = duration_diff / max(self.baseline["std_duration"], 0.01)
        
        # Convert to confidence (higher z-score = lower confidence)
        confidence = max(0.0, 1.0 - (interval_z + duration_z) / 10)
        
        reason = None
        if confidence < 0.7:
            reason = f"Typing pattern deviation: interval={interval_z:.1f}σ, duration={duration_z:.1f}σ"
        
        return confidence, reason


class VoiceAnalyzer:
    """Analyzes voice patterns for identity verification"""
    
    def __init__(self):
        self.baseline_features: Optional[Dict] = None
        self.samples: deque = deque(maxlen=100)
    
    def record_voice_sample(self, features: Dict[str, float]):
        """
        Record voice features.
        Features might include: pitch_mean, pitch_std, energy, mfcc_coefficients, etc.
        """
        self.samples.append({
            "timestamp": time.time(),
            "features": features
        })
    
    def set_baseline(self, features: Dict[str, float]):
        """Set baseline voice features"""
        self.baseline_features = features
    
    def analyze_current(self, current_features: Dict[str, float]) -> Tuple[float, Optional[str]]:
        """Analyze current voice against baseline"""
        if not self.baseline_features:
            return 1.0, None
        
        # Calculate similarity (simplified cosine similarity on common features)
        common_keys = set(current_features.keys()) & set(self.baseline_features.keys())
        
        if not common_keys:
            return 1.0, None
        
        dot_product = sum(
            current_features[k] * self.baseline_features[k]
            for k in common_keys
        )
        
        magnitude_current = sum(current_features[k] ** 2 for k in common_keys) ** 0.5
        magnitude_baseline = sum(self.baseline_features[k] ** 2 for k in common_keys) ** 0.5
        
        if magnitude_current == 0 or magnitude_baseline == 0:
            return 1.0, None
        
        similarity = dot_product / (magnitude_current * magnitude_baseline)
        confidence = max(0.0, min(1.0, similarity))
        
        reason = None
        if confidence < 0.7:
            reason = f"Voice pattern mismatch: similarity={confidence:.2f}"
        
        return confidence, reason


class LocationAnalyzer:
    """Analyzes location patterns for device verification"""
    
    def __init__(self):
        self.known_locations: List[Dict] = []  # lat, lon, radius, name
        self.location_history: deque = deque(maxlen=1000)
        self.max_speed_kmh = 200  # Maximum realistic travel speed
    
    def add_known_location(self, lat: float, lon: float, radius_m: float, name: str):
        """Add a known/trusted location"""
        self.known_locations.append({
            "lat": lat,
            "lon": lon,
            "radius": radius_m,
            "name": name
        })
    
    def record_location(self, lat: float, lon: float, accuracy: float):
        """Record a location update"""
        self.location_history.append({
            "timestamp": time.time(),
            "lat": lat,
            "lon": lon,
            "accuracy": accuracy
        })
    
    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in meters"""
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371000  # Earth's radius in meters
        
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c
    
    def analyze_current(self, lat: float, lon: float) -> Tuple[float, Optional[str]]:
        """Analyze current location"""
        confidence = 1.0
        reasons = []
        
        # Check if in known location
        in_known = False
        for loc in self.known_locations:
            distance = self._haversine_distance(lat, lon, loc["lat"], loc["lon"])
            if distance <= loc["radius"]:
                in_known = True
                break
        
        if not in_known and self.known_locations:
            confidence *= 0.8
            reasons.append("Location not in known areas")
        
        # Check for impossible travel (teleportation)
        if len(self.location_history) > 0:
            last = self.location_history[-1]
            distance = self._haversine_distance(lat, lon, last["lat"], last["lon"])
            time_diff = time.time() - last["timestamp"]
            
            if time_diff > 0:
                speed_kmh = (distance / 1000) / (time_diff / 3600)
                
                if speed_kmh > self.max_speed_kmh:
                    confidence *= 0.3
                    reasons.append(f"Impossible travel speed: {speed_kmh:.0f} km/h")
        
        reason = "; ".join(reasons) if reasons else None
        return confidence, reason


class NetworkAnalyzer:
    """Analyzes network patterns for device verification"""
    
    def __init__(self):
        self.known_networks: List[str] = []  # Network signatures
        self.connection_history: deque = deque(maxlen=100)
    
    def add_known_network(self, signature: str):
        """Add a known/trusted network signature"""
        self.known_networks.append(signature)
    
    def record_connection(self, signature: str, ip: str, is_vpn: bool, country: str):
        """Record a network connection"""
        self.connection_history.append({
            "timestamp": time.time(),
            "signature": signature,
            "ip": ip,
            "is_vpn": is_vpn,
            "country": country
        })
    
    def analyze_current(self, signature: str, ip: str, is_vpn: bool, country: str) -> Tuple[float, Optional[str]]:
        """Analyze current network connection"""
        confidence = 1.0
        reasons = []
        
        # Check if known network
        if self.known_networks and signature not in self.known_networks:
            confidence *= 0.9
            reasons.append("Unknown network")
        
        # Check for VPN (might be suspicious in some contexts)
        if is_vpn:
            confidence *= 0.95
            reasons.append("VPN detected")
        
        # Check for country change
        if len(self.connection_history) > 0:
            last = self.connection_history[-1]
            if last["country"] != country:
                time_diff = time.time() - last["timestamp"]
                if time_diff < 3600:  # Less than an hour
                    confidence *= 0.5
                    reasons.append(f"Rapid country change: {last['country']} → {country}")
        
        reason = "; ".join(reasons) if reasons else None
        return confidence, reason


# =============================================================================
# Main IO/DO/OD Engine
# =============================================================================

class IODOODEngine:
    """
    Main engine for continuous identity and device verification.
    
    This is the heartbeat of the trust system. It continuously monitors
    and can flag suspicious activity at any time.
    """
    
    def __init__(self):
        # Current state
        self.state = IODOODState()
        
        # Analyzers
        self.keystroke = KeystrokeAnalyzer()
        self.voice = VoiceAnalyzer()
        self.location = LocationAnalyzer()
        self.network = NetworkAnalyzer()
        
        # Device fingerprint
        self.device_fingerprint: Optional[DeviceFingerprint] = None
        self.registered_devices: Dict[str, DeviceFingerprint] = {}
        
        # Flags
        self.flags: Dict[str, Flag] = {}
        self.flag_history: List[Flag] = []
        
        # Thresholds
        self.io_warning_threshold = 0.7
        self.io_flag_threshold = 0.5
        self.do_warning_threshold = 0.8
        self.do_flag_threshold = 0.6
        self.od_warning_threshold = 0.9
        self.od_flag_threshold = 0.7
        
        # Callbacks
        self.on_flag: Optional[Callable[[Flag], None]] = None
        self.on_verification_required: Optional[Callable[[VerificationType], None]] = None
        self.on_session_terminated: Optional[Callable[[str], None]] = None
        
        # Check intervals
        self.io_check_interval = 30  # seconds
        self.do_check_interval = 60
        self.od_check_interval = 10
        
        self._running = False
    
    # -------------------------------------------------------------------------
    # Initialization
    # -------------------------------------------------------------------------
    
    async def initialize(self, device_id: str, did: str):
        """Initialize the engine"""
        self.device_id = device_id
        self.did = did
        
        print(f"[IO/DO/OD] Initializing for device {device_id}")
        
        # Load or create device fingerprint
        await self._initialize_device_fingerprint()
        
        print(f"[IO/DO/OD] Ready. Starting continuous verification.")
    
    async def _initialize_device_fingerprint(self):
        """Initialize device fingerprint"""
        # In production, this would gather actual hardware/software info
        self.device_fingerprint = DeviceFingerprint(
            device_id=self.device_id,
            hardware_hash=hashlib.sha256(self.device_id.encode()).hexdigest()[:16],
            software_hash=hashlib.sha256(b"software_info").hexdigest()[:16],
            network_signature="",
            last_seen=datetime.utcnow().isoformat(),
            trust_score=1.0
        )
    
    # -------------------------------------------------------------------------
    # Main Loop
    # -------------------------------------------------------------------------
    
    async def start(self):
        """Start the continuous verification loop"""
        self._running = True
        
        # Start check loops
        await asyncio.gather(
            self._io_check_loop(),
            self._do_check_loop(),
            self._od_check_loop()
        )
    
    def stop(self):
        """Stop the engine"""
        self._running = False
    
    async def _io_check_loop(self):
        """Identity OK check loop"""
        while self._running:
            await self._check_io()
            await asyncio.sleep(self.io_check_interval)
    
    async def _do_check_loop(self):
        """Device OK check loop"""
        while self._running:
            await self._check_do()
            await asyncio.sleep(self.do_check_interval)
    
    async def _od_check_loop(self):
        """Operation Device check loop"""
        while self._running:
            await self._check_od()
            await asyncio.sleep(self.od_check_interval)
    
    # -------------------------------------------------------------------------
    # IO - Identity OK
    # -------------------------------------------------------------------------
    
    async def _check_io(self):
        """Check Identity OK"""
        confidences = []
        reasons = []
        
        # Keystroke analysis
        keystroke_conf, keystroke_reason = self.keystroke.analyze_current()
        confidences.append(keystroke_conf)
        if keystroke_reason:
            reasons.append(keystroke_reason)
        
        # Voice analysis (if recent samples)
        if self.voice.samples:
            recent = self.voice.samples[-1]["features"] if self.voice.samples else {}
            voice_conf, voice_reason = self.voice.analyze_current(recent)
            confidences.append(voice_conf)
            if voice_reason:
                reasons.append(voice_reason)
        
        # Calculate overall IO confidence
        self.state.io_confidence = min(confidences) if confidences else 1.0
        self.state.last_io_check = datetime.utcnow().isoformat()
        
        # Update status and potentially flag
        await self._evaluate_io_status(reasons)
    
    async def _evaluate_io_status(self, reasons: List[str]):
        """Evaluate IO status and create flags if needed"""
        conf = self.state.io_confidence
        
        if conf >= self.io_warning_threshold:
            self.state.io_status = VerificationStatus.OK
        elif conf >= self.io_flag_threshold:
            self.state.io_status = VerificationStatus.WARNING
            await self._create_flag(
                FlagCategory.IDENTITY,
                FlagSeverity.MEDIUM,
                "Identity confidence decreased",
                {"confidence": conf, "reasons": reasons},
                VerificationType.FACE_CHECK
            )
        else:
            self.state.io_status = VerificationStatus.FLAGGED
            await self._create_flag(
                FlagCategory.IDENTITY,
                FlagSeverity.HIGH,
                "Identity verification required",
                {"confidence": conf, "reasons": reasons},
                VerificationType.FULL_REAUTH
            )
    
    async def record_keystroke(self, key: str, duration: float):
        """Record a keystroke for IO analysis"""
        self.keystroke.record_keystroke(key, time.time(), duration)
        
        # Recalculate baseline periodically
        if len(self.keystroke.samples) % 100 == 0:
            self.keystroke.calculate_baseline()
    
    async def record_voice(self, features: Dict[str, float]):
        """Record voice features for IO analysis"""
        self.voice.record_voice_sample(features)
    
    async def verify_face(self, face_data: bytes) -> bool:
        """Verify face against baseline"""
        # In production, this would do actual face comparison
        # For now, always pass
        return True
    
    async def verify_fingerprint(self, fingerprint_data: bytes) -> bool:
        """Verify fingerprint against baseline"""
        # In production, this would do actual fingerprint comparison
        return True
    
    # -------------------------------------------------------------------------
    # DO - Device OK
    # -------------------------------------------------------------------------
    
    async def _check_do(self):
        """Check Device OK"""
        confidences = []
        reasons = []
        
        # Location analysis
        if self.location.location_history:
            last_loc = self.location.location_history[-1]
            loc_conf, loc_reason = self.location.analyze_current(
                last_loc["lat"], last_loc["lon"]
            )
            confidences.append(loc_conf)
            if loc_reason:
                reasons.append(loc_reason)
        
        # Network analysis
        if self.network.connection_history:
            last_net = self.network.connection_history[-1]
            net_conf, net_reason = self.network.analyze_current(
                last_net["signature"],
                last_net["ip"],
                last_net["is_vpn"],
                last_net["country"]
            )
            confidences.append(net_conf)
            if net_reason:
                reasons.append(net_reason)
        
        # Device fingerprint check
        if self.device_fingerprint:
            # Check if fingerprint matches registered
            fp_conf = self.device_fingerprint.trust_score
            confidences.append(fp_conf)
        
        # Calculate overall DO confidence
        self.state.do_confidence = min(confidences) if confidences else 1.0
        self.state.last_do_check = datetime.utcnow().isoformat()
        
        # Update status
        await self._evaluate_do_status(reasons)
    
    async def _evaluate_do_status(self, reasons: List[str]):
        """Evaluate DO status and create flags if needed"""
        conf = self.state.do_confidence
        
        if conf >= self.do_warning_threshold:
            self.state.do_status = VerificationStatus.OK
        elif conf >= self.do_flag_threshold:
            self.state.do_status = VerificationStatus.WARNING
            await self._create_flag(
                FlagCategory.DEVICE,
                FlagSeverity.MEDIUM,
                "Device trust decreased",
                {"confidence": conf, "reasons": reasons},
                VerificationType.DEVICE_CONFIRM
            )
        else:
            self.state.do_status = VerificationStatus.FLAGGED
            await self._create_flag(
                FlagCategory.DEVICE,
                FlagSeverity.HIGH,
                "Device verification required",
                {"confidence": conf, "reasons": reasons},
                VerificationType.FULL_REAUTH
            )
    
    async def update_location(self, lat: float, lon: float, accuracy: float):
        """Update device location"""
        self.location.record_location(lat, lon, accuracy)
    
    async def update_network(self, signature: str, ip: str, is_vpn: bool, country: str):
        """Update network connection info"""
        self.network.record_connection(signature, ip, is_vpn, country)
    
    # -------------------------------------------------------------------------
    # OD - Operation Device
    # -------------------------------------------------------------------------
    
    async def _check_od(self):
        """Check Operation Device permissions"""
        # This is checked on-demand for each operation
        # The loop just maintains state
        self.state.last_od_check = datetime.utcnow().isoformat()
    
    async def check_operation(
        self,
        operation: str,
        classification: str,
        context: Dict = None
    ) -> Tuple[bool, Optional[VerificationType]]:
        """
        Check if an operation is allowed on this device.
        Returns (allowed, required_verification)
        """
        
        # First check overall state
        if self.state.overall_status() == VerificationStatus.BLOCKED:
            return False, VerificationType.FULL_REAUTH
        
        # High-sensitivity operations require higher confidence
        sensitivity_thresholds = {
            "casual": 0.5,
            "business": 0.6,
            "formal": 0.7,
            "legal": 0.8,
            "government": 0.85,
            "emergency": 0.3  # Lower for emergencies
        }
        
        threshold = sensitivity_thresholds.get(classification, 0.7)
        current_confidence = self.state.overall_confidence()
        
        if current_confidence >= threshold:
            self.state.od_status = VerificationStatus.OK
            self.state.od_confidence = current_confidence
            return True, None
        
        # Determine required verification based on gap
        gap = threshold - current_confidence
        
        if gap < 0.1:
            required = VerificationType.PIN
        elif gap < 0.2:
            required = VerificationType.FINGERPRINT
        elif gap < 0.3:
            required = VerificationType.FACE_CHECK
        else:
            required = VerificationType.FULL_REAUTH
        
        self.state.od_status = VerificationStatus.PENDING
        self.state.pending_verification = required
        
        return False, required
    
    async def confirm_operation(
        self,
        operation: str,
        verification_type: VerificationType,
        verification_data: Any
    ) -> bool:
        """Confirm an operation with verification"""
        
        success = False
        
        if verification_type == VerificationType.PIN:
            # Verify PIN
            success = True  # Would actually verify
        elif verification_type == VerificationType.FINGERPRINT:
            success = await self.verify_fingerprint(verification_data)
        elif verification_type == VerificationType.FACE_CHECK:
            success = await self.verify_face(verification_data)
        elif verification_type == VerificationType.FULL_REAUTH:
            # Full re-authentication
            success = True  # Would actually re-auth
        
        if success:
            # Boost confidence temporarily
            self.state.io_confidence = min(1.0, self.state.io_confidence + 0.2)
            self.state.do_confidence = min(1.0, self.state.do_confidence + 0.1)
            self.state.od_confidence = 1.0
            self.state.od_status = VerificationStatus.OK
            self.state.pending_verification = None
            
            # Resolve related flags
            await self._resolve_flags_for_verification(verification_type)
        
        return success
    
    # -------------------------------------------------------------------------
    # Flag Management
    # -------------------------------------------------------------------------
    
    async def _create_flag(
        self,
        category: FlagCategory,
        severity: FlagSeverity,
        reason: str,
        details: Dict,
        required_verification: VerificationType
    ):
        """Create a new flag"""
        import uuid
        
        flag = Flag(
            flag_id=str(uuid.uuid4()),
            category=category,
            severity=severity,
            reason=reason,
            details=details,
            timestamp=datetime.utcnow().isoformat(),
            required_verification=required_verification
        )
        
        self.flags[flag.flag_id] = flag
        self.state.active_flags.append(flag.flag_id)
        
        print(f"[IO/DO/OD] Flag created: {category.value}/{severity.value} - {reason}")
        
        # Call callback
        if self.on_flag:
            await self.on_flag(flag)
        
        # Request verification if needed
        if required_verification != VerificationType.NONE and self.on_verification_required:
            await self.on_verification_required(required_verification)
        
        # Critical flags terminate session
        if severity == FlagSeverity.CRITICAL:
            if self.on_session_terminated:
                await self.on_session_terminated(reason)
            self.state.io_status = VerificationStatus.BLOCKED
            self.state.do_status = VerificationStatus.BLOCKED
    
    async def _resolve_flags_for_verification(self, verification_type: VerificationType):
        """Resolve flags that are satisfied by a verification"""
        now = datetime.utcnow().isoformat()
        
        resolved = []
        for flag_id in self.state.active_flags:
            flag = self.flags.get(flag_id)
            if flag and flag.required_verification == verification_type:
                flag.resolved = True
                flag.resolved_at = now
                flag.resolution = f"Verified via {verification_type.value}"
                resolved.append(flag_id)
        
        for flag_id in resolved:
            self.state.active_flags.remove(flag_id)
            self.flag_history.append(self.flags[flag_id])
    
    # -------------------------------------------------------------------------
    # Spot Checks (triggered by Sense rules)
    # -------------------------------------------------------------------------
    
    async def trigger_spot_check(self, check_type: str, reason: str = None):
        """Trigger a spot check (called by Sense engine)"""
        
        print(f"[IO/DO/OD] Spot check triggered: {check_type}")
        
        if check_type == "face":
            await self._create_flag(
                FlagCategory.IDENTITY,
                FlagSeverity.MEDIUM,
                reason or "Spot check: face verification",
                {"trigger": "sense_rule"},
                VerificationType.FACE_CHECK
            )
        
        elif check_type == "fingerprint":
            await self._create_flag(
                FlagCategory.IDENTITY,
                FlagSeverity.MEDIUM,
                reason or "Spot check: fingerprint verification",
                {"trigger": "sense_rule"},
                VerificationType.FINGERPRINT
            )
        
        elif check_type == "voice":
            await self._create_flag(
                FlagCategory.IDENTITY,
                FlagSeverity.LOW,
                reason or "Spot check: voice verification",
                {"trigger": "sense_rule"},
                VerificationType.VOICE_CHECK
            )
        
        elif check_type == "location":
            await self._create_flag(
                FlagCategory.LOCATION,
                FlagSeverity.MEDIUM,
                reason or "Spot check: location verification",
                {"trigger": "sense_rule"},
                VerificationType.LOCATION_CONFIRM
            )
    
    # -------------------------------------------------------------------------
    # State Export
    # -------------------------------------------------------------------------
    
    def get_state_summary(self) -> Dict:
        """Get current state summary"""
        return {
            "overall_status": self.state.overall_status().value,
            "overall_confidence": self.state.overall_confidence(),
            "io": {
                "status": self.state.io_status.value,
                "confidence": self.state.io_confidence,
                "last_check": self.state.last_io_check
            },
            "do": {
                "status": self.state.do_status.value,
                "confidence": self.state.do_confidence,
                "last_check": self.state.last_do_check
            },
            "od": {
                "status": self.state.od_status.value,
                "confidence": self.state.od_confidence,
                "last_check": self.state.last_od_check
            },
            "active_flags": len(self.state.active_flags),
            "pending_verification": self.state.pending_verification.value if self.state.pending_verification else None
        }


# =============================================================================
# Integration with JIS/Sense
# =============================================================================

def create_sense_rules_for_iodood(engine: IODOODEngine) -> List[Dict]:
    """
    Create Sense rules that trigger IO/DO/OD spot checks.
    These would be added to the Sense engine.
    """
    
    return [
        {
            "rule_id": "typing_anomaly",
            "name": "Typing Pattern Anomaly",
            "conditions": [
                {"sensor_type": "keystroke", "operator": "deviation", "threshold": 2.0}
            ],
            "action": "iodood_check",
            "action_params": {"check_type": "fingerprint", "reason": "Typing pattern changed"}
        },
        {
            "rule_id": "location_jump",
            "name": "Impossible Location Change",
            "conditions": [
                {"sensor_type": "location", "operator": "speed_exceeds", "threshold": 200}
            ],
            "action": "iodood_check",
            "action_params": {"check_type": "face", "reason": "Impossible travel detected"}
        },
        {
            "rule_id": "network_change",
            "name": "Network Change During Sensitive Op",
            "conditions": [
                {"sensor_type": "network", "operator": "changed", "threshold": None},
                {"context": "sensitive_operation", "operator": "is_true", "threshold": None}
            ],
            "logic": "and",
            "action": "iodood_check",
            "action_params": {"check_type": "location", "reason": "Network changed during sensitive operation"}
        },
        {
            "rule_id": "periodic_face_check",
            "name": "Periodic Face Verification",
            "conditions": [
                {"sensor_type": "time", "operator": "interval", "threshold": 3600}  # Every hour
            ],
            "action": "iodood_check",
            "action_params": {"check_type": "face", "reason": "Periodic verification"}
        },
        {
            "rule_id": "high_value_operation",
            "name": "High Value Operation Check",
            "conditions": [
                {"context": "operation_value", "operator": ">", "threshold": 10000}
            ],
            "action": "iodood_check",
            "action_params": {"check_type": "fingerprint", "reason": "High value operation"}
        }
    ]


# =============================================================================
# CLI Test
# =============================================================================

async def main():
    """Test the IO/DO/OD engine"""
    
    print("=" * 60)
    print("IO/DO/OD Engine Test")
    print("=" * 60)
    
    engine = IODOODEngine()
    await engine.initialize("device-123", "did:jtel:user:jasper")
    
    # Set up callbacks
    async def on_flag(flag):
        print(f"\n🚩 FLAG: {flag.category.value}/{flag.severity.value}")
        print(f"   Reason: {flag.reason}")
        print(f"   Required: {flag.required_verification.value}")
    
    async def on_verification_required(vtype):
        print(f"\n🔐 VERIFICATION REQUIRED: {vtype.value}")
    
    engine.on_flag = on_flag
    engine.on_verification_required = on_verification_required
    
    # Simulate keystroke baseline
    print("\n[TEST] Building keystroke baseline...")
    for i in range(150):
        engine.keystroke.record_keystroke(
            chr(ord('a') + i % 26),
            time.time() + i * 0.1,
            0.08 + (i % 10) * 0.01
        )
    engine.keystroke.calculate_baseline()
    print(f"Baseline: {engine.keystroke.baseline}")
    
    # Normal state
    print("\n[TEST] Current state:")
    print(json.dumps(engine.get_state_summary(), indent=2))
    
    # Check an operation
    print("\n[TEST] Checking LEGAL operation...")
    allowed, required = await engine.check_operation("sign_document", "legal")
    print(f"Allowed: {allowed}, Required: {required}")
    
    # Simulate typing anomaly
    print("\n[TEST] Simulating typing anomaly...")
    for i in range(50):
        engine.keystroke.record_keystroke(
            chr(ord('a') + i % 26),
            time.time() + i * 0.3,  # Much slower typing
            0.2 + (i % 10) * 0.05   # Longer key presses
        )
    
    # Manual IO check
    await engine._check_io()
    
    # Check state after anomaly
    print("\n[TEST] State after anomaly:")
    print(json.dumps(engine.get_state_summary(), indent=2))
    
    # Trigger spot check
    print("\n[TEST] Triggering face spot check...")
    await engine.trigger_spot_check("face", "Manual test")
    
    # Show final state
    print("\n[TEST] Final state:")
    print(json.dumps(engine.get_state_summary(), indent=2))
    
    print("\n" + "=" * 60)
    print("Test complete!")


if __name__ == "__main__":
    asyncio.run(main())
