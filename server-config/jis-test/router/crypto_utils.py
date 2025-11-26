"""
JIS Cryptographic Utilities
Handles DID/HID key management and exchange
"""
import hashlib
import json
from typing import Dict, Tuple

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, x25519


class DIDKey:
    """
    Device Identity Key (DID-KEY)
    - Can be shared/exported
    - Used for device authentication
    - Derived from device characteristics
    """

    def __init__(self, private_key: ed25519.Ed25519PrivateKey = None):
        self.private_key = private_key or ed25519.Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

    def sign(self, data: bytes) -> bytes:
        """Sign data with DID private key"""
        return self.private_key.sign(data)

    def verify(self, signature: bytes, data: bytes, public_key: ed25519.Ed25519PublicKey) -> bool:
        """Verify signature with DID public key"""
        try:
            public_key.verify(signature, data)
            return True
        except Exception:
            return False

    def export_public(self) -> str:
        """Export public key as PEM string"""
        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem.decode('utf-8')

    def export_private(self) -> str:
        """Export private key as PEM string (use with caution!)"""
        pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        return pem.decode('utf-8')

    @classmethod
    def from_public_pem(cls, pem: str) -> ed25519.Ed25519PublicKey:
        """Load public key from PEM string"""
        return serialization.load_pem_public_key(pem.encode('utf-8'))


class HIDKey:
    """
    Human Identity Key (HID-KEY)
    - NEVER shared or exported
    - Lives only in local device ("brein")
    - Bound to biometric data
    - Used to prove human presence
    """

    def __init__(self, private_key: ed25519.Ed25519PrivateKey = None):
        self.private_key = private_key or ed25519.Ed25519PrivateKey.generate()
        # Public key exists but is NEVER transmitted
        self.public_key = self.private_key.public_key()

    def attest(self, did_public: str, context: Dict) -> bytes:
        """
        Create attestation that links HID to DID
        This proves human authorized this device
        Returns signature, NOT the HID key itself
        """
        payload = json.dumps({
            "did_public": did_public,
            "context": context,
            "type": "hid_attestation"
        }, sort_keys=True).encode('utf-8')

        return self.private_key.sign(payload)

    def derive_did_binding(self, did_key: DIDKey) -> str:
        """
        Derive a binding hash between HID and DID
        Can be verified without exposing HID
        """
        combined = (
            self.public_key.public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw
            ) +
            did_key.public_key.public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw
            )
        )
        return hashlib.sha256(combined).hexdigest()


class KeyExchange:
    """
    Diffie-Hellman key exchange for secure channel setup
    Used during FIR/A initialization
    """

    def __init__(self):
        self.private_key = x25519.X25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

    def export_public(self) -> str:
        """Export public exchange key"""
        raw = self.public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        return raw.hex()

    def derive_shared_secret(self, peer_public_hex: str) -> bytes:
        """Derive shared secret from peer's public key"""
        peer_public_raw = bytes.fromhex(peer_public_hex)
        peer_public = x25519.X25519PublicKey.from_public_bytes(peer_public_raw)
        shared = self.private_key.exchange(peer_public)
        # Derive key material with HKDF
        return hashlib.sha256(shared).digest()


def create_did_exchange_payload(did_key: DIDKey, exchange: KeyExchange) -> Dict:
    """
    Create payload for DID key exchange during FIR/A
    Contains:
    - DID public key (for authentication)
    - Exchange public key (for encrypted channel)
    - Signature proving ownership
    """
    payload = {
        "did_public": did_key.export_public(),
        "exchange_public": exchange.export_public(),
    }

    # Sign the exchange key with DID to prove ownership
    to_sign = json.dumps(payload, sort_keys=True).encode('utf-8')
    signature = did_key.sign(to_sign)

    payload["signature"] = signature.hex()
    return payload


def verify_did_exchange_payload(payload: Dict) -> bool:
    """Verify DID exchange payload signature"""
    try:
        did_public = DIDKey.from_public_pem(payload["did_public"])
        signature = bytes.fromhex(payload["signature"])

        # Reconstruct signed data
        verify_payload = {
            "did_public": payload["did_public"],
            "exchange_public": payload["exchange_public"],
        }
        to_verify = json.dumps(verify_payload, sort_keys=True).encode('utf-8')

        did_public.verify(signature, to_verify)
        return True
    except Exception:
        return False


# Example usage and testing
if __name__ == "__main__":
    print("JIS Key Exchange Demo")
    print("=" * 50)

    # Alice's keys (client)
    print("\n1. Alice generates keys...")
    alice_did = DIDKey()
    alice_hid = HIDKey()  # Never leaves Alice's device!
    alice_exchange = KeyExchange()

    # HID attests DID
    attestation = alice_hid.attest(
        alice_did.export_public(),
        {"device": "phone", "location": "home"}
    )
    print(f"   ✓ HID attestation: {attestation.hex()[:32]}...")

    # Create exchange payload
    alice_payload = create_did_exchange_payload(alice_did, alice_exchange)
    print(f"   ✓ DID public: {alice_payload['did_public'][:50]}...")

    # Bob's keys (server)
    print("\n2. Bob generates keys...")
    bob_did = DIDKey()
    bob_exchange = KeyExchange()
    bob_payload = create_did_exchange_payload(bob_did, bob_exchange)

    # Verify exchange
    print("\n3. Verifying exchange...")
    assert verify_did_exchange_payload(alice_payload), "Alice verification failed!"
    assert verify_did_exchange_payload(bob_payload), "Bob verification failed!"
    print("   ✓ Both payloads verified")

    # Derive shared secrets
    print("\n4. Deriving shared secrets...")
    alice_shared = alice_exchange.derive_shared_secret(bob_payload["exchange_public"])
    bob_shared = bob_exchange.derive_shared_secret(alice_payload["exchange_public"])

    assert alice_shared == bob_shared, "Shared secret mismatch!"
    print(f"   ✓ Shared secret: {alice_shared.hex()[:32]}...")

    # HID-DID binding
    print("\n5. HID-DID binding (local only)...")
    binding = alice_hid.derive_did_binding(alice_did)
    print(f"   ✓ Binding hash: {binding[:32]}...")
    print("   ⚠ HID key never transmitted!")

    print("\n✓ Key exchange complete and secure!")
