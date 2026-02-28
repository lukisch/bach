-- Migration 019: Denkarium (SQ045, Runde 34)
-- Zwei Modi: Logbuch (Sternzeit) + Denkarium (Gedanken-Sammler)

CREATE TABLE IF NOT EXISTS denkarium_entries (
    id INTEGER PRIMARY KEY,

    -- Typ: logbuch (Tagebuch/Sternzeit) oder denkarium (Gedanken-Sammler)
    entry_type TEXT NOT NULL DEFAULT 'denkarium',

    -- Titel (kurz, optional)
    title TEXT,

    -- Inhalt (Markdown)
    content TEXT NOT NULL,

    -- Kategorie (frei waehlbar: idee, frage, erkenntnis, plan, reflexion)
    category TEXT DEFAULT 'notiz',

    -- Tags (komma-getrennt)
    tags TEXT,

    -- Quelle (wer hat geschrieben: user, claude, gemini, system)
    source TEXT DEFAULT 'user',

    -- Stimmung/Energie (optional, 1-5)
    mood INTEGER,

    -- Verknuepfung zu Task oder Wiki
    linked_task_id INTEGER,
    linked_wiki_id INTEGER,

    -- Promote-Status (kann zu Task oder Wiki-Artikel werden)
    promoted_to TEXT,  -- 'task', 'wiki', NULL
    promoted_id INTEGER,

    -- dist_type (0=USER, persoenlich)
    dist_type INTEGER DEFAULT 0,

    -- Timestamps
    created_at TEXT DEFAULT (datetime('now', 'localtime')),
    updated_at TEXT
);

-- Index fuer schnelle Suche
CREATE INDEX IF NOT EXISTS idx_denkarium_type ON denkarium_entries(entry_type);
CREATE INDEX IF NOT EXISTS idx_denkarium_category ON denkarium_entries(category);
CREATE INDEX IF NOT EXISTS idx_denkarium_created ON denkarium_entries(created_at);
