-- Migration 016: Press-Dokumente
-- Erstellt: 2026-02-19

CREATE TABLE IF NOT EXISTS press_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_type TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT,
    metadata_json TEXT,
    pdf_path TEXT,
    status TEXT DEFAULT 'draft',
    sent_to TEXT,
    sent_at TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    dist_type INTEGER DEFAULT 0
);
