-- Migration 009: Agent Instances & Launcher System
-- Datum: 2026-02-14
-- Beschreibung: Neue Tabellen für Agent-Runtime und Multi-Access-Tracking

-- ═══════════════════════════════════════════════════════════════
-- Neue Tabelle: agent_instances
-- ═══════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS agent_instances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,                -- z.B. "steuer-agent", "research-agent"
    agent_type TEXT NOT NULL,                 -- 'expert', 'worker', 'boss', 'specialist'
    capabilities TEXT,                        -- JSON array: ["ocr", "skr04", "datev"]
    config TEXT,                              -- JSON config
    is_active INTEGER DEFAULT 1,
    created_at TEXT NOT NULL,
    last_used TEXT,
    success_count INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_agent_instances_name ON agent_instances(name);
CREATE INDEX IF NOT EXISTS idx_agent_instances_active ON agent_instances(is_active);

-- ═══════════════════════════════════════════════════════════════
-- Erweitern: tasks Tabelle (für Source-Tracking)
-- ═══════════════════════════════════════════════════════════════

-- Prüfe ob Spalte bereits existiert (SQLite kann kein IF NOT EXISTS für ALTER TABLE)
-- Wir nutzen PRAGMA table_info() und CASE für sichere Migration

-- Neue Spalten:
--   source: 'cli', 'telegram', 'claude'
--   assigned_agent: Agent-Name falls via Agent ausgeführt

-- Diese werden via Python-Code hinzugefügt (in db.py run_migrations())
-- da SQLite kein ALTER TABLE ... ADD COLUMN IF NOT EXISTS hat

-- COMMENT: Python migration handler will check and add:
--   ALTER TABLE tasks ADD COLUMN source TEXT;
--   ALTER TABLE tasks ADD COLUMN assigned_agent TEXT;

-- ═══════════════════════════════════════════════════════════════
-- Seed Data: Standard-Agenten registrieren
-- ═══════════════════════════════════════════════════════════════

-- Steuer-Agent
INSERT OR IGNORE INTO agent_instances (name, agent_type, capabilities, config, is_active, created_at)
VALUES (
    'steuer-agent',
    'expert',
    '["ocr", "skr04", "datev", "beleg-scan"]',
    '{"auto_scan": true, "ocr_engine": "tesseract"}',
    1,
    datetime('now')
);

-- Research-Agent
INSERT OR IGNORE INTO agent_instances (name, agent_type, capabilities, config, is_active, created_at)
VALUES (
    'research-agent',
    'worker',
    '["websearch", "analyze", "summarize"]',
    '{"max_results": 10, "sources": ["web", "papers"]}',
    1,
    datetime('now')
);

-- Entwickler-Agent
INSERT OR IGNORE INTO agent_instances (name, agent_type, capabilities, config, is_active, created_at)
VALUES (
    'entwickler-agent',
    'worker',
    '["code-analysis", "implementation", "testing"]',
    '{"language": "python", "framework": "bach"}',
    1,
    datetime('now')
);

-- Production-Agent
INSERT OR IGNORE INTO agent_instances (name, agent_type, capabilities, config, is_active, created_at)
VALUES (
    'production-agent',
    'boss',
    '["music", "video", "text", "pr"]',
    '{"tools": ["ai-music", "ai-video", "llm"]}',
    1,
    datetime('now')
);

-- ═══════════════════════════════════════════════════════════════
-- Neue Tabelle: launcher_log (optional - für Analytics)
-- ═══════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS launcher_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    source TEXT NOT NULL,              -- 'cli', 'telegram', 'claude'
    user TEXT NOT NULL,                -- User-ID
    command TEXT NOT NULL,             -- Handler-Name
    operation TEXT,
    routing TEXT,                      -- 'handler' oder 'agent:name'
    success INTEGER DEFAULT 1,
    duration_ms INTEGER,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_launcher_log_source ON launcher_log(source);
CREATE INDEX IF NOT EXISTS idx_launcher_log_command ON launcher_log(command);
CREATE INDEX IF NOT EXISTS idx_launcher_log_timestamp ON launcher_log(timestamp);
