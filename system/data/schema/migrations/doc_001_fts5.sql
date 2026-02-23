-- ============================================================
-- MIGRATION: DOC_001 - Document Index mit FTS5 Volltextsuche
-- ============================================================
-- Datum: 2026-02-06
-- Beschreibung: Erstellt document_index Tabelle und FTS5 virtuellen Index
--               fuer schnelle Volltextsuche ueber alle Dokumente.
-- ============================================================

CREATE TABLE IF NOT EXISTS document_index (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path TEXT UNIQUE NOT NULL,
    file_name TEXT,
    file_ext TEXT,
    file_size INTEGER,
    file_hash TEXT,
    file_category TEXT,
    content_text TEXT,
    word_count INTEGER,
    indexed_at TEXT DEFAULT (datetime('now')),
    modified_at TEXT
);

CREATE VIRTUAL TABLE IF NOT EXISTS document_fts
USING fts5(file_name, content_text, content=document_index, content_rowid=id);

-- Trigger um FTS-Index bei INSERT/UPDATE/DELETE synchron zu halten
CREATE TRIGGER IF NOT EXISTS document_index_ai AFTER INSERT ON document_index BEGIN
    INSERT INTO document_fts(rowid, file_name, content_text)
    VALUES (new.id, new.file_name, new.content_text);
END;

CREATE TRIGGER IF NOT EXISTS document_index_ad AFTER DELETE ON document_index BEGIN
    INSERT INTO document_fts(document_fts, rowid, file_name, content_text)
    VALUES('delete', old.id, old.file_name, old.content_text);
END;

CREATE TRIGGER IF NOT EXISTS document_index_au AFTER UPDATE ON document_index BEGIN
    INSERT INTO document_fts(document_fts, rowid, file_name, content_text)
    VALUES('delete', old.id, old.file_name, old.content_text);
    INSERT INTO document_fts(rowid, file_name, content_text)
    VALUES (new.id, new.file_name, new.content_text);
END;

-- Index fuer schnelle Pfad-Lookups
CREATE INDEX IF NOT EXISTS idx_document_index_path ON document_index(file_path);
CREATE INDEX IF NOT EXISTS idx_document_index_category ON document_index(file_category);

-- ============================================================
-- MIGRATION ENDE
-- ============================================================
