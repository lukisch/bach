-- Migration 031: Session Context / 24h-Agent (SQ048)
-- Tagesbasierte Session-Persistenz mit Arbeitsmodi

CREATE TABLE IF NOT EXISTS session_context (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    context_json TEXT NOT NULL DEFAULT '{}',
    summary TEXT,
    handover_notes TEXT,
    work_mode TEXT NOT NULL DEFAULT 'assistant',
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(date)
);
