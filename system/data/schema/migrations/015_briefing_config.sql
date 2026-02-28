-- Migration 015: Briefing-Konfiguration
-- Erstellt: 2026-02-19

CREATE TABLE IF NOT EXISTS briefing_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_name TEXT UNIQUE NOT NULL,
    is_active INTEGER DEFAULT 1,
    priority INTEGER DEFAULT 50,
    settings_json TEXT DEFAULT '{}',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    dist_type INTEGER DEFAULT 0
);

INSERT OR IGNORE INTO briefing_config (module_name, is_active, priority) VALUES
    ('task_briefing', 1, 10),
    ('message_briefing', 1, 20),
    ('news_briefing', 1, 30),
    ('session_briefing', 1, 40),
    ('weather_briefing', 0, 50),
    ('calendar_briefing', 0, 70);
