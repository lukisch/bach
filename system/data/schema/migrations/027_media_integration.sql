-- Migration 027: MediaBrain Integration (INT03, PEANUT v3.3.0)
-- Medienverwaltung mit Provider-Support, Favoriten, Blacklist
-- Portiert aus MediaBrain Standalone (PyQt6 → SQLite CLI)

-- ============================================================
-- 1. Haupttabelle: Media Items
-- ============================================================

CREATE TABLE IF NOT EXISTS media_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    media_type TEXT NOT NULL DEFAULT 'movie',   -- movie|series|music|clip|podcast|audiobook|document
    source TEXT NOT NULL DEFAULT 'local',       -- netflix|youtube|spotify|disney|prime|appletv|twitch|local
    provider_id TEXT,                           -- Eindeutige ID beim Provider
    url TEXT,                                   -- URL zum Oeffnen
    -- Metadaten
    description TEXT,
    artist TEXT,                                -- Musik: Kuenstler
    album TEXT,                                 -- Musik: Album
    channel TEXT,                               -- YouTube/Twitch: Channel
    season INTEGER,                             -- Serie: Staffel
    episode INTEGER,                            -- Serie: Episode
    length_seconds INTEGER,                     -- Dauer in Sekunden
    -- Lokale Dateien
    local_path TEXT,                            -- Pfad zur lokalen Datei
    -- Status
    is_favorite INTEGER DEFAULT 0,
    blacklist_flag INTEGER DEFAULT 0,
    blacklisted_at TEXT,
    -- Rating
    rating INTEGER,                             -- 1-5 Sterne
    -- Tags
    tags TEXT,                                  -- JSON-Array
    notes TEXT,
    -- Meta
    dist_type INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    last_opened_at TEXT,
    UNIQUE(provider_id, source)
);

-- ============================================================
-- 2. Wiedergabe-Historie
-- ============================================================

CREATE TABLE IF NOT EXISTS media_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    media_id INTEGER NOT NULL,
    opened_at TEXT DEFAULT (datetime('now')),
    open_method TEXT DEFAULT 'manual',           -- manual|browser|app|auto
    dist_type INTEGER DEFAULT 0,
    FOREIGN KEY (media_id) REFERENCES media_items(id) ON DELETE CASCADE
);

-- ============================================================
-- 3. Listen (Watchlist, Playlist, etc.)
-- ============================================================

CREATE TABLE IF NOT EXISTS media_lists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    list_type TEXT DEFAULT 'watchlist',          -- watchlist|playlist|collection
    description TEXT,
    dist_type INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS media_list_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    list_id INTEGER NOT NULL,
    media_id INTEGER NOT NULL,
    position INTEGER DEFAULT 0,
    added_at TEXT DEFAULT (datetime('now')),
    dist_type INTEGER DEFAULT 0,
    FOREIGN KEY (list_id) REFERENCES media_lists(id) ON DELETE CASCADE,
    FOREIGN KEY (media_id) REFERENCES media_items(id) ON DELETE CASCADE,
    UNIQUE(list_id, media_id)
);

-- ============================================================
-- 4. Indizes
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_mi_type ON media_items(media_type);
CREATE INDEX IF NOT EXISTS idx_mi_source ON media_items(source);
CREATE INDEX IF NOT EXISTS idx_mi_favorite ON media_items(is_favorite);
CREATE INDEX IF NOT EXISTS idx_mi_blacklist ON media_items(blacklist_flag);
CREATE INDEX IF NOT EXISTS idx_mi_last_opened ON media_items(last_opened_at);
CREATE INDEX IF NOT EXISTS idx_mi_title ON media_items(title);
CREATE INDEX IF NOT EXISTS idx_mh_media ON media_history(media_id);
CREATE INDEX IF NOT EXISTS idx_mh_opened ON media_history(opened_at);
CREATE INDEX IF NOT EXISTS idx_mli_list ON media_list_items(list_id);
