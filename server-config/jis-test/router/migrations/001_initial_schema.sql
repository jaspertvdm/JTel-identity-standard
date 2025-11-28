-- Migration 001: Initial schema for JIS Router
-- Creates the events table and necessary indexes

CREATE TABLE IF NOT EXISTS events (
    id BIGSERIAL PRIMARY KEY,
    fir_a_id UUID NOT NULL,
    seq INTEGER NOT NULL,
    continuity_hash TEXT NOT NULL,
    payload JSONB NOT NULL,
    ts TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_events_fir ON events(fir_a_id, seq DESC);
CREATE INDEX IF NOT EXISTS idx_events_ts ON events(ts DESC);

-- Migration tracking table
CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY,
    applied_at TIMESTAMPTZ DEFAULT NOW(),
    description TEXT
);

-- Record this migration
INSERT INTO schema_migrations (version, description)
VALUES (1, 'Initial schema with events table')
ON CONFLICT (version) DO NOTHING;
