-- Migration 002: Add DID key storage
-- Stores public DID keys for each FIR/A relationship

CREATE TABLE IF NOT EXISTS did_keys (
    id BIGSERIAL PRIMARY KEY,
    fir_a_id UUID NOT NULL,
    entity_name TEXT NOT NULL,  -- 'initiator' or 'responder'
    did_public_key TEXT NOT NULL,  -- PEM format
    exchange_public_key TEXT,  -- hex format, optional for key exchange
    hid_did_binding TEXT,  -- Hash binding HID to DID (for verification, not the HID itself!)
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(fir_a_id, entity_name)
);

CREATE INDEX IF NOT EXISTS idx_did_keys_fir ON did_keys(fir_a_id);

-- Record this migration
INSERT INTO schema_migrations (version, description)
VALUES (2, 'Add DID key storage table')
ON CONFLICT (version) DO NOTHING;
