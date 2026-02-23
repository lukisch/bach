-- ═══════════════════════════════════════════════════════════════════════════
-- BACH_STREAM Feature-Mapping Database
-- Schema v1.0 | 2026-01-11
-- ═══════════════════════════════════════════════════════════════════════════

-- Grundidee:
-- 1. Features sind der Kern (semantische Ebene)
-- 2. Implementierungen sind konkret (Dateien, Ordner)
-- 3. Bewertungen sind mehrdimensional
-- 4. Aliase verbinden verschiedene Namen zum gleichen Feature

-- ═══════════════════════════════════════════════════════════════════════════
-- SYSTEME
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS systems (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,           -- z.B. "_CHIAH", "_BATCH", "recludOS"
    type TEXT,                           -- "system", "utility", "meta"
    version TEXT,
    entry_point TEXT,
    base_path TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════════════════════════════════════════════════════════════════════
-- FEATURE-KATEGORIEN (Hierarchie)
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS feature_categories (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,           -- z.B. "Memory", "Task-Management"
    parent_id INTEGER,                   -- Für Sub-Kategorien
    description TEXT,
    FOREIGN KEY (parent_id) REFERENCES feature_categories(id)
);

-- ═══════════════════════════════════════════════════════════════════════════
-- FEATURES (Semantische Ebene)
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS features (
    id INTEGER PRIMARY KEY,
    canonical_name TEXT UNIQUE NOT NULL, -- z.B. "memory_short_term"
    display_name TEXT,                   -- z.B. "Kurzzeit-Memory"
    category_id INTEGER,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES feature_categories(id)
);

-- ═══════════════════════════════════════════════════════════════════════════
-- FEATURE-ALIASE (Verschiedene Namen → gleiches Feature)
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS feature_aliases (
    id INTEGER PRIMARY KEY,
    feature_id INTEGER NOT NULL,
    alias TEXT NOT NULL,                 -- z.B. "CONNI", "tasks.json", "Task-DB"
    alias_type TEXT,                     -- "filename", "foldername", "concept"
    system_id INTEGER,                   -- Optional: System-spezifischer Alias
    FOREIGN KEY (feature_id) REFERENCES features(id),
    FOREIGN KEY (system_id) REFERENCES systems(id)
);

-- ═══════════════════════════════════════════════════════════════════════════
-- IMPLEMENTIERUNGEN (Konkrete Umsetzung pro System)
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS implementations (
    id INTEGER PRIMARY KEY,
    feature_id INTEGER NOT NULL,
    system_id INTEGER NOT NULL,
    
    -- Lokalisierung
    path TEXT,                           -- Relativer Pfad im System
    files TEXT,                          -- JSON-Array von Dateien
    
    -- Technische Umsetzung
    technology TEXT,                     -- "sqlite", "json", "txt", "python"
    loc_estimate INTEGER,                -- Lines of Code (geschätzt)
    
    -- Status
    status TEXT DEFAULT 'implemented',   -- "implemented", "partial", "planned", "missing"
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (feature_id) REFERENCES features(id),
    FOREIGN KEY (system_id) REFERENCES systems(id),
    UNIQUE(feature_id, system_id)
);

-- ═══════════════════════════════════════════════════════════════════════════
-- BEWERTUNGEN (Mehrdimensional)
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS ratings (
    id INTEGER PRIMARY KEY,
    implementation_id INTEGER NOT NULL,
    
    -- Dimensionen (1-5 Skala)
    completeness INTEGER,                -- Vollständigkeit
    sophistication INTEGER,              -- Ausgereiftheit/Komplexität
    documentation INTEGER,               -- Dokumentation
    usability INTEGER,                   -- Benutzerfreundlichkeit
    innovation INTEGER,                  -- Innovationsgrad
    
    -- Freitext
    strengths TEXT,                      -- Stärken
    weaknesses TEXT,                     -- Schwächen
    notes TEXT,                          -- Notizen
    
    rated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    rated_by TEXT,                       -- "Claude", "User"
    
    FOREIGN KEY (implementation_id) REFERENCES implementations(id)
);

-- ═══════════════════════════════════════════════════════════════════════════
-- DATEI-FINGERPRINTS (Für Duplikat-Erkennung)
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS file_fingerprints (
    id INTEGER PRIMARY KEY,
    system_id INTEGER NOT NULL,
    path TEXT NOT NULL,
    filename TEXT NOT NULL,
    
    -- Fingerprints
    size_bytes INTEGER,
    line_count INTEGER,
    content_hash TEXT,                   -- MD5/SHA für Duplikat-Erkennung
    
    -- Metadaten
    file_type TEXT,                      -- "python", "json", "markdown", etc.
    
    scanned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (system_id) REFERENCES systems(id)
);

-- ═══════════════════════════════════════════════════════════════════════════
-- SYNOPSEN (Vorberechnete Vergleiche)
-- ═══════════════════════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS synopses (
    id INTEGER PRIMARY KEY,
    feature_id INTEGER NOT NULL,
    
    -- Vergleichs-Daten
    systems_compared TEXT,               -- JSON-Array der System-IDs
    comparison_text TEXT,                -- Generierte Synopse
    winner_system_id INTEGER,            -- Bestes System für dieses Feature
    
    generated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (feature_id) REFERENCES features(id),
    FOREIGN KEY (winner_system_id) REFERENCES systems(id)
);

-- ═══════════════════════════════════════════════════════════════════════════
-- VIEWS für einfache Abfragen
-- ═══════════════════════════════════════════════════════════════════════════

-- Feature-Matrix (welches System hat welches Feature)
CREATE VIEW IF NOT EXISTS feature_matrix AS
SELECT 
    f.canonical_name,
    f.display_name,
    fc.name as category,
    s.name as system_name,
    i.status,
    i.technology,
    r.completeness,
    r.sophistication
FROM features f
LEFT JOIN feature_categories fc ON f.category_id = fc.id
LEFT JOIN implementations i ON f.id = i.feature_id
LEFT JOIN systems s ON i.system_id = s.id
LEFT JOIN ratings r ON i.id = r.implementation_id;

-- Duplikat-Kandidaten (gleicher Hash, verschiedene Namen)
CREATE VIEW IF NOT EXISTS duplicate_candidates AS
SELECT 
    f1.filename as file1,
    f2.filename as file2,
    s1.name as system1,
    s2.name as system2,
    f1.content_hash
FROM file_fingerprints f1
JOIN file_fingerprints f2 ON f1.content_hash = f2.content_hash 
    AND f1.id < f2.id
JOIN systems s1 ON f1.system_id = s1.id
JOIN systems s2 ON f2.system_id = s2.id;

-- Feature-Lücken (Features die ein System nicht hat)
CREATE VIEW IF NOT EXISTS feature_gaps AS
SELECT 
    s.name as system_name,
    f.display_name as missing_feature,
    fc.name as category
FROM systems s
CROSS JOIN features f
LEFT JOIN feature_categories fc ON f.category_id = fc.id
LEFT JOIN implementations i ON f.id = i.feature_id AND i.system_id = s.id
WHERE i.id IS NULL;

-- ═══════════════════════════════════════════════════════════════════════════
-- INDIZES für Performance
-- ═══════════════════════════════════════════════════════════════════════════
CREATE INDEX IF NOT EXISTS idx_implementations_feature ON implementations(feature_id);
CREATE INDEX IF NOT EXISTS idx_implementations_system ON implementations(system_id);
CREATE INDEX IF NOT EXISTS idx_fingerprints_hash ON file_fingerprints(content_hash);
CREATE INDEX IF NOT EXISTS idx_aliases_feature ON feature_aliases(feature_id);
