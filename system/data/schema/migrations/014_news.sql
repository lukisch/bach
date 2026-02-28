-- Migration 014: News-Aggregation
-- Erstellt: 2026-02-19

CREATE TABLE IF NOT EXISTS news_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('rss','web','youtube','social')),
    url TEXT UNIQUE NOT NULL,
    category TEXT DEFAULT 'allgemein',
    schedule TEXT DEFAULT 'daily',
    is_active INTEGER DEFAULT 1,
    last_fetched TEXT,
    fetch_count INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0,
    last_error TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    dist_type INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS news_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER NOT NULL REFERENCES news_sources(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    content TEXT,
    summary TEXT,
    url TEXT,
    author TEXT,
    published_at TEXT,
    fetched_at TEXT DEFAULT CURRENT_TIMESTAMP,
    is_read INTEGER DEFAULT 0,
    category TEXT,
    UNIQUE(source_id, url)
);
