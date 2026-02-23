-- ═══════════════════════════════════════════════════════════════════════════
-- BACH_STREAM Test Library Database
-- Schema v1.0 | 2026-01-11
-- ═══════════════════════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════════════════════
-- TESTAUFGABEN (Bibliothek)
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS test_tasks (
    id TEXT PRIMARY KEY,                 -- z.B. "A001"
    name TEXT NOT NULL,                  -- z.B. "Task erstellen"
    category TEXT NOT NULL,              -- z.B. "Task-Management"
    difficulty TEXT,                     -- "basis", "mittel", "fortgeschritten"
    expected_time_sec INTEGER,           -- Erwartete Zeit in Sekunden
    feature_tests TEXT,                  -- JSON-Array von getesteten Features
    file_path TEXT,                      -- Pfad zur .md Datei
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════════════════════════════════════════════════════════════════════
-- TESTPROFILE
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS test_profiles (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,           -- z.B. "STANDARD"
    description TEXT,
    estimated_time_min INTEGER,
    test_ids TEXT,                       -- JSON-Array von Test-IDs
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════════════════════════════════════════════════════════════════════
-- TESTLAEUFE (Durchfuehrungen)
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS test_runs (
    id INTEGER PRIMARY KEY,
    system_name TEXT NOT NULL,           -- Getestetes System
    profile_name TEXT,                   -- Verwendetes Profil
    started_at DATETIME NOT NULL,
    completed_at DATETIME,
    tester TEXT,                         -- "Claude", "User", etc.
    notes TEXT,
    FOREIGN KEY (profile_name) REFERENCES test_profiles(name)
);

-- ═══════════════════════════════════════════════════════════════════════════
-- EINZELERGEBNISSE
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS test_results (
    id INTEGER PRIMARY KEY,
    run_id INTEGER NOT NULL,
    task_id TEXT NOT NULL,
    
    -- Zeitmessungen (in Sekunden)
    t_start DATETIME,
    t_end DATETIME,
    t_total_sec REAL,
    
    -- Erfolg
    success INTEGER,                     -- 0 = failed, 1 = partial, 2 = success
    
    -- Metriken
    n_files_touched INTEGER,
    n_steps INTEGER,
    
    -- Subjektive Bewertungen (1-5)
    rating_clarity INTEGER,
    rating_simplicity INTEGER,
    rating_documentation INTEGER,
    
    -- Freitext
    observations TEXT,
    difficulties TEXT,
    
    FOREIGN KEY (run_id) REFERENCES test_runs(id),
    FOREIGN KEY (task_id) REFERENCES test_tasks(id)
);

-- ═══════════════════════════════════════════════════════════════════════════
-- DIMENSIONSBEWERTUNGEN (Gesamtbewertung pro Dimension)
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS dimension_ratings (
    id INTEGER PRIMARY KEY,
    run_id INTEGER NOT NULL,
    
    -- Dimensionen (1-5)
    d1_onboarding INTEGER,
    d2_navigation INTEGER,
    d3_memory INTEGER,
    d4_task_management INTEGER,
    d5_communication INTEGER,
    d6_tools INTEGER,
    d7_error_tolerance INTEGER,
    
    -- Gesamtnote
    overall_rating REAL,
    
    -- Freitext
    strengths TEXT,                      -- Top 3 Staerken
    weaknesses TEXT,                     -- Top 3 Schwaechen
    recommendations TEXT,
    
    FOREIGN KEY (run_id) REFERENCES test_runs(id)
);

-- ═══════════════════════════════════════════════════════════════════════════
-- VIEWS
-- ═══════════════════════════════════════════════════════════════════════════

-- Durchschnittswerte pro System
CREATE VIEW IF NOT EXISTS system_averages AS
SELECT 
    tr.system_name,
    COUNT(DISTINCT tr.id) as n_runs,
    AVG(dr.d1_onboarding) as avg_onboarding,
    AVG(dr.d2_navigation) as avg_navigation,
    AVG(dr.d3_memory) as avg_memory,
    AVG(dr.d4_task_management) as avg_task,
    AVG(dr.d5_communication) as avg_comm,
    AVG(dr.d6_tools) as avg_tools,
    AVG(dr.d7_error_tolerance) as avg_error,
    AVG(dr.overall_rating) as avg_overall
FROM test_runs tr
LEFT JOIN dimension_ratings dr ON tr.id = dr.run_id
GROUP BY tr.system_name;

-- Zeitmessungen pro Task und System
CREATE VIEW IF NOT EXISTS task_times AS
SELECT 
    tr.system_name,
    tt.id as task_id,
    tt.name as task_name,
    AVG(res.t_total_sec) as avg_time_sec,
    MIN(res.t_total_sec) as min_time_sec,
    MAX(res.t_total_sec) as max_time_sec,
    tt.expected_time_sec
FROM test_results res
JOIN test_runs tr ON res.run_id = tr.id
JOIN test_tasks tt ON res.task_id = tt.id
GROUP BY tr.system_name, tt.id;

-- Erfolgsraten pro System
CREATE VIEW IF NOT EXISTS success_rates AS
SELECT 
    tr.system_name,
    tt.id as task_id,
    tt.name as task_name,
    COUNT(*) as n_attempts,
    SUM(CASE WHEN res.success = 2 THEN 1 ELSE 0 END) as n_success,
    ROUND(100.0 * SUM(CASE WHEN res.success = 2 THEN 1 ELSE 0 END) / COUNT(*), 1) as success_rate
FROM test_results res
JOIN test_runs tr ON res.run_id = tr.id
JOIN test_tasks tt ON res.task_id = tt.id
GROUP BY tr.system_name, tt.id;

-- ═══════════════════════════════════════════════════════════════════════════
-- INDIZES
-- ═══════════════════════════════════════════════════════════════════════════
CREATE INDEX IF NOT EXISTS idx_results_run ON test_results(run_id);
CREATE INDEX IF NOT EXISTS idx_results_task ON test_results(task_id);
CREATE INDEX IF NOT EXISTS idx_runs_system ON test_runs(system_name);
