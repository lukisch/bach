-- Migration 026: LitZentrum Integration (INT01, PEANUT v3.3.0)
-- Literaturverwaltung mit Quellen, Zitaten, Aufgaben, Zusammenfassungen
-- Portiert aus LitZentrum Standalone (ordner-basiert → SQLite)

-- ============================================================
-- 1. Haupttabelle: Quellen
-- ============================================================

CREATE TABLE IF NOT EXISTS lit_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    authors TEXT,                         -- JSON-Array: ["Smith, John", "Doe, Jane"]
    year INTEGER,
    source_type TEXT DEFAULT 'article',   -- article|book|chapter|thesis|conference|website|other
    -- Publikationsdetails
    journal TEXT,
    publisher TEXT,
    volume TEXT,
    issue TEXT,
    pages TEXT,
    edition TEXT,
    -- Identifikatoren
    doi TEXT,
    isbn TEXT,
    url TEXT,
    -- Inhalt
    abstract TEXT,
    tags TEXT,                            -- JSON-Array: ["AI", "Machine Learning"]
    language TEXT DEFAULT 'de',
    -- Dateireferenz
    pdf_path TEXT,                        -- Relativer Pfad zur PDF-Datei
    -- Status
    read_status TEXT DEFAULT 'unread',    -- unread|reading|read|archived
    rating INTEGER,                       -- 1-5 Sterne
    -- Meta
    notes TEXT,                           -- Allgemeine Notizen zur Quelle
    metadata_source TEXT DEFAULT 'manual', -- manual|doi_lookup|isbn_lookup|bibtex_import
    dist_type INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- ============================================================
-- 2. Zitate aus Quellen
-- ============================================================

CREATE TABLE IF NOT EXISTS lit_quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER NOT NULL,
    quote_type TEXT DEFAULT 'direct',     -- direct|indirect|paraphrase
    text TEXT NOT NULL,
    page INTEGER,
    page_end INTEGER,
    comment TEXT,                         -- Kommentar/Einordnung
    tags TEXT,                            -- JSON-Array
    used_in TEXT,                         -- JSON-Array: In welchen Arbeiten verwendet
    dist_type INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (source_id) REFERENCES lit_sources(id) ON DELETE CASCADE
);

-- ============================================================
-- 3. Aufgaben pro Quelle
-- ============================================================

CREATE TABLE IF NOT EXISTS lit_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER,                   -- NULL = projektweite Aufgabe
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'open',          -- open|in_progress|done
    priority TEXT DEFAULT 'normal',      -- low|normal|high|urgent
    due_date TEXT,
    page INTEGER,                        -- Seitenreferenz
    dist_type INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    completed_at TEXT,
    FOREIGN KEY (source_id) REFERENCES lit_sources(id) ON DELETE CASCADE
);

-- ============================================================
-- 4. Zusammenfassungen
-- ============================================================

CREATE TABLE IF NOT EXISTS lit_summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER NOT NULL,
    title TEXT,
    content TEXT NOT NULL,
    summary_type TEXT DEFAULT 'full',    -- full|chapter|section|abstract
    source_method TEXT DEFAULT 'manual', -- manual|ai_generated
    ai_model TEXT,                       -- z.B. "claude-3-opus"
    pages TEXT,                          -- Seitenbereich: "23-45"
    tags TEXT,                           -- JSON-Array
    dist_type INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT,
    FOREIGN KEY (source_id) REFERENCES lit_sources(id) ON DELETE CASCADE
);

-- ============================================================
-- 5. Indizes
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_ls_title ON lit_sources(title);
CREATE INDEX IF NOT EXISTS idx_ls_year ON lit_sources(year);
CREATE INDEX IF NOT EXISTS idx_ls_type ON lit_sources(source_type);
CREATE INDEX IF NOT EXISTS idx_ls_status ON lit_sources(read_status);
CREATE INDEX IF NOT EXISTS idx_lq_source ON lit_quotes(source_id);
CREATE INDEX IF NOT EXISTS idx_lt_source ON lit_tasks(source_id);
CREATE INDEX IF NOT EXISTS idx_lt_status ON lit_tasks(status);
CREATE INDEX IF NOT EXISTS idx_lsum_source ON lit_summaries(source_id);
