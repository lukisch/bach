-- ============================================================
-- BACH v1.1 - SCHEMA-ERWEITERUNG: DISTRIBUTION SYSTEM
-- ============================================================
-- Erstellt: 2026-01-14
-- Zweck: Installer-fähige Datenbank mit 3-Stufen-System
-- ============================================================

-- ============================================================
-- KONZEPT: dist_type (Distribution Type)
-- ============================================================
--
--   dist_type = 2  → CORE (Systemdatei, unverändert mitverpacken)
--   dist_type = 1  → TEMPLATE (Systemdatei, auf Urzustand zurücksetzen)
--   dist_type = 0  → USER_DATA (nicht mitverpacken)
--
-- INSTALLER-WORKFLOW:
--   1. SELECT * FROM <table> WHERE dist_type >= 1
--   2. Bei dist_type = 1: template_content statt content verwenden
--   3. Bei dist_type = 0: Zeile nicht exportieren
--   4. Ergebnis → JSON/SQL → ZIP → Installation = Entpacken
--
-- ============================================================

-- ============================================================
-- NEUE SPALTEN FÜR ALLE RELEVANTEN TABELLEN
-- ============================================================

-- SKILLS: Welche Skills sind System vs. User?
ALTER TABLE skills ADD COLUMN dist_type INTEGER DEFAULT 2;
-- 2 = CORE: brainstorm.md, think.md (immer dabei)
-- 1 = TEMPLATE: entwickler.txt (Basis-Version)
-- 0 = USER: assist-beruflich-kunden-und-projekte-kontakte.txt (dein Projekt)

ALTER TABLE skills ADD COLUMN template_content TEXT;
-- Original-Inhalt für Reset bei dist_type = 1


-- TOOLS: Welche Tools sind System vs. User?
ALTER TABLE tools ADD COLUMN dist_type INTEGER DEFAULT 2;
-- 2 = CORE: autolog.py, dirscan.py (immer dabei)
-- 1 = TEMPLATE: code_generator.py (konfigurierbar)
-- 0 = USER: förderplaner_cli.py (dein spezifisches Tool)


-- TASKS: Alle Tasks sind User-Daten!
ALTER TABLE tasks ADD COLUMN dist_type INTEGER DEFAULT 0;
-- 0 = USER: Alle Tasks sind nutzerspezifisch
-- (Installer startet mit leerer Task-Liste)


-- MEMORY: Sessions sind User-Daten, Lessons können TEMPLATE sein
ALTER TABLE memory_sessions ADD COLUMN dist_type INTEGER DEFAULT 0;
-- 0 = USER: Alle Sessions

ALTER TABLE memory_lessons ADD COLUMN dist_type INTEGER DEFAULT 1;
-- 1 = TEMPLATE: Basis-Lessons (zurücksetzen)
-- 0 = USER: Eigene Lessons

ALTER TABLE memory_lessons ADD COLUMN template_content TEXT;


-- SYSTEM_CONFIG: Manche Configs sind CORE, manche TEMPLATE
ALTER TABLE system_config ADD COLUMN dist_type INTEGER DEFAULT 2;
-- 2 = CORE: token_thresholds (nicht änderbar)
-- 1 = TEMPLATE: user_preferences (zurücksetzen)


-- FILES (Directory Truth): Pfade sind TEMPLATE
ALTER TABLE files_directory_truth ADD COLUMN dist_type INTEGER DEFAULT 1;
-- 1 = TEMPLATE: Soll-Struktur (zurücksetzen auf Basis)
-- 0 = USER: User-spezifische Pfade


-- AUTOMATION: Triggers können CORE oder USER sein
ALTER TABLE automation_triggers ADD COLUMN dist_type INTEGER DEFAULT 2;
-- 2 = CORE: System-Triggers
-- 1 = TEMPLATE: Konfigurierbare Triggers
-- 0 = USER: Eigene Triggers


-- ============================================================
-- INSTALLER-VIEWS (für einfachen Export)
-- ============================================================

-- View: Alles was in Distribution gehört (dist_type >= 1)
CREATE VIEW IF NOT EXISTS v_distribution_skills AS
SELECT id, name, type, category, path, version, description, 
       is_active, priority, trigger_phrases,
       CASE WHEN dist_type = 1 THEN template_content ELSE NULL END as reset_content
FROM skills 
WHERE dist_type >= 1;

CREATE VIEW IF NOT EXISTS v_distribution_tools AS
SELECT id, name, type, category, path, endpoint, command,
       version, description, is_active
FROM tools 
WHERE dist_type >= 1;

CREATE VIEW IF NOT EXISTS v_distribution_config AS
SELECT key, value, type, category, description
FROM system_config 
WHERE dist_type >= 1;


-- ============================================================
-- HELPER-TABELLE: DATEI-MANIFEST
-- ============================================================
-- Für Dateien die nicht in DB sind (SKILL.md, hub.py, etc.)

CREATE TABLE IF NOT EXISTS distribution_manifest (
    id INTEGER PRIMARY KEY,
    
    -- Pfad relativ zu BACH/
    path TEXT UNIQUE NOT NULL,
    
    -- Distribution Type
    dist_type INTEGER DEFAULT 2,     -- 2=CORE, 1=TEMPLATE, 0=USER
    
    -- Für Templates: Original-Hash zur Erkennung von Änderungen
    template_hash TEXT,
    
    -- Beschreibung
    description TEXT,
    
    -- Timestamps
    created_at TEXT,
    updated_at TEXT
);

-- Basis-Einträge für das Manifest
INSERT OR IGNORE INTO distribution_manifest (path, dist_type, description) VALUES
-- CORE (dist_type = 2) - Immer dabei, unverändert
('SKILL.md', 2, 'Haupteinstiegspunkt'),
('bach.py', 2, 'CLI-Zentrale'),
('schema.sql', 2, 'Datenbank-Schema'),
('setup_db.py', 2, 'DB-Setup'),
('hub/hub.py', 2, 'Hub-Logik'),
('hub/handlers/base.py', 2, 'Basis-Handler'),
('hub/handlers/startup.py', 2, 'Startup-Handler'),
('hub/handlers/shutdown.py', 2, 'Shutdown-Handler'),
('hub/handlers/help.py', 2, 'Help-Handler'),
('hub/handlers/status.py', 2, 'Status-Handler'),
('hub/handlers/memory.py', 2, 'Memory-Handler'),
('hub/handlers/context.py', 2, 'Context-Handler'),
('hub/handlers/inject.py', 2, 'Inject-Handler'),

-- TEMPLATE (dist_type = 1) - Dabei, aber zurücksetzbar
('memory/archive/.gitkeep', 1, 'Leerer Archive-Ordner'),
('logs/sessions/.gitkeep', 1, 'Leerer Sessions-Ordner'),
('user/IDENTITY.md', 1, 'Identity-Template'),
('bach.db', 1, 'Datenbank (leere User-Daten)'),

-- USER (dist_type = 0) - Nicht mitverpacken
('memory/archive/*.md', 0, 'Session-Archive'),
('logs/sessions/*.log', 0, 'Session-Logs'),
('tools/TRANSFER/*', 0, 'Transfer-Dateien');


-- ============================================================
-- EXPORT-FUNKTION (Pseudo-Code als Kommentar)
-- ============================================================
--
-- def create_distribution():
--     # 1. DB exportieren (nur dist_type >= 1)
--     for table in ['skills', 'tools', 'config', ...]:
--         SELECT * WHERE dist_type >= 1
--         Bei dist_type = 1: template_content verwenden
--     
--     # 2. Dateien kopieren (aus distribution_manifest)
--     for file in SELECT path FROM distribution_manifest WHERE dist_type >= 1:
--         if dist_type = 1:
--             reset_to_template(file)
--         copy_to_dist(file)
--     
--     # 3. ZIP erstellen
--     zip('BACH_v1.0_distribution.zip', dist_folder)
--
-- ============================================================


-- ============================================================
-- SYSTEM-IDENTITAET & SIEGEL
-- ============================================================

CREATE TABLE IF NOT EXISTS instance_identity (
    instance_id TEXT PRIMARY KEY,
    instance_name TEXT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    forked_from TEXT,
    seal_status TEXT DEFAULT 'intact',    -- 'intact', 'broken'
    seal_broken_at TIMESTAMP,
    seal_broken_by TEXT,
    seal_broken_reason TEXT,
    kernel_hash TEXT,                     -- SHA256 ueber CORE-Dateien
    kernel_version TEXT,
    seal_last_verified TIMESTAMP,
    base_release TEXT,
    base_release_date TIMESTAMP
);


-- ============================================================
-- SNAPSHOTS (Point-in-Time Backups)
-- ============================================================

CREATE TABLE IF NOT EXISTS distribution_snapshots (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    snapshot_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    snapshot_type TEXT DEFAULT 'manual',  -- manual/daily/release/pre-update
    file_count INTEGER DEFAULT 0,
    total_size INTEGER DEFAULT 0,
    is_valid INTEGER DEFAULT 1
);


-- ============================================================
-- SNAPSHOT-INHALT (referenziert distribution_manifest)
-- ============================================================

CREATE TABLE IF NOT EXISTS distribution_snapshot_files (
    id INTEGER PRIMARY KEY,
    snapshot_id INTEGER NOT NULL REFERENCES distribution_snapshots(id) ON DELETE CASCADE,
    manifest_id INTEGER NOT NULL REFERENCES distribution_manifest(id),
    file_checksum TEXT,
    file_size INTEGER
);


-- ============================================================
-- RELEASES (offizielle Versionen)
-- ============================================================

CREATE TABLE IF NOT EXISTS distribution_releases (
    id INTEGER PRIMARY KEY,
    version TEXT UNIQUE NOT NULL,
    release_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    changelog TEXT,
    kernel_hash TEXT,
    snapshot_id INTEGER REFERENCES distribution_snapshots(id),
    status TEXT DEFAULT 'draft',         -- draft/final/deprecated
    is_stable INTEGER DEFAULT 0,
    dist_zip_path TEXT
);


-- ============================================================
-- DATEI-VERSIONEN (vereinfacht)
-- ============================================================

CREATE TABLE IF NOT EXISTS distribution_file_versions (
    id INTEGER PRIMARY KEY,
    manifest_id INTEGER NOT NULL REFERENCES distribution_manifest(id),
    checksum TEXT,
    size INTEGER,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT DEFAULT 'system',
    change_type TEXT,                    -- create/update/delete
    change_description TEXT
);


-- ============================================================
-- STATISTIK-VIEW
-- ============================================================

CREATE VIEW IF NOT EXISTS v_distribution_stats AS
SELECT
    'skills' as table_name,
    COUNT(*) as total,
    SUM(CASE WHEN dist_type = 2 THEN 1 ELSE 0 END) as core,
    SUM(CASE WHEN dist_type = 1 THEN 1 ELSE 0 END) as template,
    SUM(CASE WHEN dist_type = 0 THEN 1 ELSE 0 END) as user_data
FROM skills
UNION ALL
SELECT
    'tools' as table_name,
    COUNT(*) as total,
    SUM(CASE WHEN dist_type = 2 THEN 1 ELSE 0 END) as core,
    SUM(CASE WHEN dist_type = 1 THEN 1 ELSE 0 END) as template,
    SUM(CASE WHEN dist_type = 0 THEN 1 ELSE 0 END) as user_data
FROM tools
UNION ALL
SELECT
    'tasks' as table_name,
    COUNT(*) as total,
    SUM(CASE WHEN dist_type = 2 THEN 1 ELSE 0 END) as core,
    SUM(CASE WHEN dist_type = 1 THEN 1 ELSE 0 END) as template,
    SUM(CASE WHEN dist_type = 0 THEN 1 ELSE 0 END) as user_data
FROM tasks
UNION ALL
SELECT
    'manifest' as table_name,
    COUNT(*) as total,
    SUM(CASE WHEN dist_type = 2 THEN 1 ELSE 0 END) as core,
    SUM(CASE WHEN dist_type = 1 THEN 1 ELSE 0 END) as template,
    SUM(CASE WHEN dist_type = 0 THEN 1 ELSE 0 END) as user_data
FROM distribution_manifest;
