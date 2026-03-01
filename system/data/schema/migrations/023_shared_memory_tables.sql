-- Migration 023: Shared Memory Tabellen (SQ043 Stufe D)
-- Erstellt die Multi-Agent-Memory-Tabellen fuer SharedMemoryHandler
-- Referenz: BACH_Dev/BACH_Memory_Architektur_Konzept.md

-- shared_memory_facts
CREATE TABLE IF NOT EXISTS shared_memory_facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id TEXT NOT NULL DEFAULT 'system',
    namespace TEXT DEFAULT 'global',
    visibility TEXT DEFAULT 'private' CHECK(visibility IN ('private', 'shared', 'public')),
    category TEXT NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    value_type TEXT DEFAULT 'text' CHECK(value_type IN ('text', 'number', 'json', 'url', 'date')),
    confidence REAL DEFAULT 1.0 CHECK(confidence >= 0 AND confidence <= 1),
    source TEXT,
    tags TEXT,
    created_by TEXT NOT NULL,
    modified_by TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    dist_type INTEGER DEFAULT 2,
    UNIQUE(agent_id, namespace, category, key)
);

-- shared_memory_lessons
CREATE TABLE IF NOT EXISTS shared_memory_lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id TEXT NOT NULL DEFAULT 'system',
    namespace TEXT DEFAULT 'global',
    visibility TEXT DEFAULT 'private' CHECK(visibility IN ('private', 'shared', 'public')),
    parent_id INTEGER,
    category TEXT NOT NULL,
    severity TEXT DEFAULT 'medium' CHECK(severity IN ('critical', 'high', 'medium', 'low', 'info')),
    title TEXT NOT NULL,
    problem TEXT,
    solution TEXT NOT NULL,
    trigger_words TEXT,
    trigger_events TEXT,
    related_tools TEXT,
    related_files TEXT,
    is_active INTEGER DEFAULT 1,
    times_shown INTEGER DEFAULT 0,
    last_shown TIMESTAMP,
    confidence REAL DEFAULT 1.0 CHECK(confidence >= 0 AND confidence <= 1),
    source TEXT,
    created_by TEXT NOT NULL,
    modified_by TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    dist_type INTEGER DEFAULT 2,
    FOREIGN KEY (parent_id) REFERENCES shared_memory_lessons(id) ON DELETE SET NULL
);

-- shared_memory_sessions
CREATE TABLE IF NOT EXISTS shared_memory_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL UNIQUE,
    agent_id TEXT NOT NULL,
    project_id TEXT,
    started_at TIMESTAMP NOT NULL,
    ended_at TIMESTAMP,
    duration_seconds INTEGER,
    summary TEXT,
    tasks_completed INTEGER DEFAULT 0,
    tasks_created INTEGER DEFAULT 0,
    tokens_used INTEGER DEFAULT 0,
    delegation_count INTEGER DEFAULT 0,
    continuation_context TEXT,
    key_decisions TEXT,
    files_modified TEXT,
    is_compressed INTEGER DEFAULT 0,
    is_archived INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    dist_type INTEGER DEFAULT 0
);

-- shared_memory_working
CREATE TABLE IF NOT EXISTS shared_memory_working (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id TEXT NOT NULL,
    session_id TEXT,
    type TEXT NOT NULL CHECK(type IN ('note', 'task', 'reminder', 'thought', 'scratchpad', 'context', 'loop')),
    content TEXT NOT NULL,
    priority INTEGER DEFAULT 0 CHECK(priority >= 0 AND priority <= 10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    is_active INTEGER DEFAULT 1,
    tags TEXT,
    related_to TEXT,
    dist_type INTEGER DEFAULT 0
);

-- shared_memory_consolidation (Decay-Tracking)
CREATE TABLE IF NOT EXISTS shared_memory_consolidation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_table TEXT NOT NULL,
    source_id INTEGER NOT NULL,
    agent_id TEXT NOT NULL,
    times_accessed INTEGER DEFAULT 0,
    last_accessed TIMESTAMP,
    weight REAL DEFAULT 0.5 CHECK(weight >= 0 AND weight <= 1),
    decay_rate REAL DEFAULT 0.95 CHECK(decay_rate >= 0 AND decay_rate <= 1),
    threshold REAL DEFAULT 0.2 CHECK(threshold >= 0 AND threshold <= 1),
    status TEXT DEFAULT 'active' CHECK(status IN ('active', 'fading', 'archived', 'deleted')),
    consolidated_to INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    dist_type INTEGER DEFAULT 2,
    UNIQUE(source_table, source_id, agent_id)
);

-- shared_context_triggers
CREATE TABLE IF NOT EXISTS shared_context_triggers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id TEXT NOT NULL,
    namespace TEXT DEFAULT 'global',
    trigger_phrase TEXT NOT NULL,
    hint_text TEXT NOT NULL,
    source TEXT DEFAULT 'manual',
    confidence REAL DEFAULT 0.5 CHECK(confidence >= 0 AND confidence <= 1),
    is_active INTEGER DEFAULT 1,
    status TEXT DEFAULT 'unknown' CHECK(status IN ('unknown', 'approved', 'blocked')),
    usage_count INTEGER DEFAULT 0,
    last_used TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    dist_type INTEGER DEFAULT 1,
    -- TTL Support (Stufe D)
    expires_at TIMESTAMP,
    UNIQUE(agent_id, namespace, trigger_phrase)
);

-- Indizes fuer Performance
CREATE INDEX IF NOT EXISTS idx_shared_facts_agent ON shared_memory_facts(agent_id, namespace);
CREATE INDEX IF NOT EXISTS idx_shared_facts_category ON shared_memory_facts(category);
CREATE INDEX IF NOT EXISTS idx_shared_lessons_agent ON shared_memory_lessons(agent_id, namespace);
CREATE INDEX IF NOT EXISTS idx_shared_lessons_category ON shared_memory_lessons(category);
CREATE INDEX IF NOT EXISTS idx_shared_sessions_agent ON shared_memory_sessions(agent_id);
CREATE INDEX IF NOT EXISTS idx_shared_working_agent ON shared_memory_working(agent_id, is_active);
CREATE INDEX IF NOT EXISTS idx_shared_triggers_agent ON shared_context_triggers(agent_id, is_active);
CREATE INDEX IF NOT EXISTS idx_shared_consolidation_source ON shared_memory_consolidation(source_table, source_id);
