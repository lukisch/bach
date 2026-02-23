-- Fackelträger-Lock für 24h-Bridge-Session
CREATE TABLE IF NOT EXISTS bridge_session_lock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pc_name TEXT NOT NULL,              -- Hostname des PC
    user_id TEXT NOT NULL,              -- User-ID (System-Benutzername)
    session_id TEXT UNIQUE,             -- Claude-Session-ID
    session_type TEXT DEFAULT 'bridge', -- 'bridge' oder 'gui'
    acquired_at TEXT NOT NULL,          -- ISO-Timestamp
    heartbeat_at TEXT NOT NULL,         -- Letzter Heartbeat
    is_active INTEGER DEFAULT 1,
    UNIQUE(session_type)                -- Nur eine Bridge-Session aktiv
);

-- Index für schnelle Heartbeat-Checks
CREATE INDEX IF NOT EXISTS idx_session_lock_active
ON bridge_session_lock(session_type, is_active, heartbeat_at);
