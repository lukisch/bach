-- Migration 020: document_vectors Tabelle (SQ064 - Semantische Suche mit sqlite-vec)
-- Datum: 2026-02-21
-- Zweck: Vektorspeicher für Embeddings (paraphrase-multilingual-mpnet-base-v2, 768 Dimensionen)

CREATE TABLE IF NOT EXISTS document_vectors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chunk_id TEXT NOT NULL,
    vector BLOB NOT NULL,  -- 768 float32 = 3072 bytes (mpnet-base-v2) oder 384 float32 = 1536 bytes (MiniLM)
    model_name TEXT DEFAULT 'paraphrase-multilingual-mpnet-base-v2',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chunk_id) REFERENCES document_chunks(id) ON DELETE CASCADE
);

-- Index für schnelle chunk_id Lookups
CREATE INDEX IF NOT EXISTS idx_document_vectors_chunk_id ON document_vectors(chunk_id);

-- Index für Modell-Lookups (falls mehrere Modelle parallel genutzt werden)
CREATE INDEX IF NOT EXISTS idx_document_vectors_model ON document_vectors(model_name);

-- Kommentar: vector-Spalte wird von sqlite-vec für Kosinus-Suche genutzt
-- Hybrid-Suche: FTS5 (BM25) 30% + Embedding (Kosinus) 70%
