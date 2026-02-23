-- Migration 001: Connector Queue Upgrade
-- Zuverlaessige Nachrichtenzustellung mit Retry, Backoff und Circuit Breaker
-- Datum: 2026-02-08

-- ── connector_messages: Retry-Tracking ──────────────────────────────

ALTER TABLE connector_messages ADD COLUMN retry_count INTEGER DEFAULT 0;
ALTER TABLE connector_messages ADD COLUMN max_retries INTEGER DEFAULT 5;
ALTER TABLE connector_messages ADD COLUMN next_retry_at TEXT;
ALTER TABLE connector_messages ADD COLUMN status TEXT DEFAULT 'pending';
ALTER TABLE connector_messages ADD COLUMN updated_at TEXT;

-- Backfill: Bestehende Zeilen basierend auf processed/error migrieren
UPDATE connector_messages SET status = 'sent'    WHERE processed = 1 AND error IS NULL;
UPDATE connector_messages SET status = 'sent'    WHERE processed = 1 AND error IS NOT NULL;
UPDATE connector_messages SET status = 'failed'  WHERE processed = 0 AND error IS NOT NULL;
UPDATE connector_messages SET status = 'pending' WHERE processed = 0 AND error IS NULL;

-- Index fuer Retry-Scheduling (naechster Versuch faellig?)
CREATE INDEX IF NOT EXISTS idx_cm_retry
    ON connector_messages(status, next_retry_at);

-- Index fuer Outbound-Dispatch (pro Connector)
CREATE INDEX IF NOT EXISTS idx_cm_outbound
    ON connector_messages(connector_name, direction, status);

-- ── connections: Circuit Breaker ────────────────────────────────────

ALTER TABLE connections ADD COLUMN consecutive_failures INTEGER DEFAULT 0;
ALTER TABLE connections ADD COLUMN disabled_until TEXT;
