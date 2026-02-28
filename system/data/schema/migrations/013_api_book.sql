-- Migration 013: API-Buch
-- Erstellt: 2026-02-19

CREATE TABLE IF NOT EXISTS api_book (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    provider TEXT,
    base_url TEXT NOT NULL,
    auth_type TEXT DEFAULT 'none',
    description TEXT,
    endpoints_json TEXT DEFAULT '[]',
    examples_json TEXT DEFAULT '[]',
    tags TEXT,
    last_verified TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    dist_type INTEGER DEFAULT 0
);
