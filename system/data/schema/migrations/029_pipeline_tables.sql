-- Pipeline-Framework Tabellen (SQ011)
-- Upgrade bestehender Tabellen + fehlende Spalten nachruesten

-- Tabellen anlegen falls sie noch nicht existieren (Erstinstallation)
CREATE TABLE IF NOT EXISTS pipeline_configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pipeline_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    version TEXT DEFAULT '1.0.0',
    type TEXT DEFAULT 'scanner',
    schedule TEXT,
    config_json TEXT DEFAULT '{}',
    is_active INTEGER DEFAULT 1,
    installed_at TEXT DEFAULT (datetime('now')),
    last_run TEXT,
    status TEXT DEFAULT 'installed',
    dist_type INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS pipeline_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pipeline_id TEXT NOT NULL,
    started_at TEXT DEFAULT (datetime('now')),
    finished_at TEXT,
    status TEXT DEFAULT 'running',
    items_processed INTEGER DEFAULT 0,
    errors_count INTEGER DEFAULT 0,
    log TEXT,
    dist_type INTEGER DEFAULT 0,
    FOREIGN KEY (pipeline_id) REFERENCES pipeline_configs(pipeline_id) ON DELETE CASCADE
);

-- Fehlende Spalten nachruesten (ALTER TABLE ignoriert Fehler nicht,
-- daher wird das per Python-Migration ausgefuehrt — siehe 029_pipeline_tables.py)

-- Indizes anlegen
CREATE INDEX IF NOT EXISTS idx_pr_pipeline ON pipeline_runs(pipeline_id);
CREATE INDEX IF NOT EXISTS idx_pr_started ON pipeline_runs(started_at DESC);
