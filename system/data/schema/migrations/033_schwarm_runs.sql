-- Migration 033: Schwarm-Runs Tracking (SQ016, SUGAR v3.8.0)
-- Protokolliert Schwarm-Ausfuehrungen mit Kosten und Performance

CREATE TABLE IF NOT EXISTS schwarm_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pattern TEXT NOT NULL,
    task TEXT,
    model TEXT DEFAULT 'claude-haiku-4-5-20251001',
    workers INTEGER DEFAULT 1,
    tokens_in INTEGER DEFAULT 0,
    tokens_out INTEGER DEFAULT 0,
    cost_usd REAL DEFAULT 0.0,
    duration_ms INTEGER DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'running',
    result_summary TEXT,
    error TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    completed_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_schwarm_runs_pattern ON schwarm_runs(pattern);
CREATE INDEX IF NOT EXISTS idx_schwarm_runs_created ON schwarm_runs(created_at);
