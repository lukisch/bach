-- =============================================================================
-- SCHEDULING SERVICE - SQLite Schema
-- Version: 1.0.0
-- Erstellt: 2026-01-25
-- Basiert auf: scheduling/stubs/models.py (UpToday Routines Engine)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- ITEMS - Haupttabelle für Routinen, Tasks und Termine
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS scheduling_items (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'task',  -- 'routine', 'task', 'appointment'
    description TEXT,
    
    -- Zeit
    has_time INTEGER DEFAULT 0,
    start_time TEXT,                        -- HH:MM Format
    end_time TEXT,
    location TEXT,
    
    -- Wiederholung
    has_recurrence INTEGER DEFAULT 0,
    interval_type TEXT,                     -- 'daily', 'weekly', 'monthly', 'yearly'
    interval_value INTEGER DEFAULT 1,
    weekdays TEXT,                          -- JSON Array [0-6], Mo=0
    
    -- Status
    is_active INTEGER DEFAULT 0,
    is_template INTEGER DEFAULT 0,
    template_id TEXT,
    
    -- Darstellung
    color_code TEXT DEFAULT 'blue',
    icon TEXT,
    sort_order INTEGER DEFAULT 0,
    
    -- Meta
    person_id INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (template_id) REFERENCES scheduling_items(id)
);

-- -----------------------------------------------------------------------------
-- STEPS - Schritte innerhalb von Routinen
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS scheduling_steps (
    id TEXT PRIMARY KEY,
    item_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    image_path TEXT,
    position INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,                -- Verschachtelungstiefe
    duration_minutes INTEGER,
    parent_step_id TEXT,
    
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (item_id) REFERENCES scheduling_items(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_step_id) REFERENCES scheduling_steps(id)
);

-- -----------------------------------------------------------------------------
-- ITEM_INSTANCES - Tägliche Instanzen von Items
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS scheduling_instances (
    id TEXT PRIMARY KEY,
    item_id TEXT NOT NULL,
    due_date TEXT NOT NULL,                 -- YYYY-MM-DD
    instance_number INTEGER DEFAULT 1,      -- Bei mehrfachen Instanzen pro Tag
    is_completed INTEGER DEFAULT 0,
    completed_at TEXT,
    notes TEXT,
    
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (item_id) REFERENCES scheduling_items(id) ON DELETE CASCADE,
    UNIQUE(item_id, due_date, instance_number)
);

-- -----------------------------------------------------------------------------
-- STEP_COMPLETIONS - Fortschritt pro Step pro Instance
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS scheduling_step_completions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    instance_id TEXT NOT NULL,
    step_id TEXT NOT NULL,
    is_completed INTEGER DEFAULT 0,
    completed_at TEXT,
    
    FOREIGN KEY (instance_id) REFERENCES scheduling_instances(id) ON DELETE CASCADE,
    FOREIGN KEY (step_id) REFERENCES scheduling_steps(id) ON DELETE CASCADE,
    UNIQUE(instance_id, step_id)
);

-- -----------------------------------------------------------------------------
-- TODAY_BOARD - Heute-Board Konfiguration
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS scheduling_today_board (
    id TEXT PRIMARY KEY,
    instance_id TEXT NOT NULL,
    sort_order INTEGER DEFAULT 0,
    time_slot TEXT,                         -- 'morning', 'noon', 'evening', 'night'
    pinned INTEGER DEFAULT 0,
    
    FOREIGN KEY (instance_id) REFERENCES scheduling_instances(id) ON DELETE CASCADE
);

-- =============================================================================
-- INDICES
-- =============================================================================
CREATE INDEX IF NOT EXISTS idx_items_category ON scheduling_items(category);
CREATE INDEX IF NOT EXISTS idx_items_active ON scheduling_items(is_active);
CREATE INDEX IF NOT EXISTS idx_items_person ON scheduling_items(person_id);

CREATE INDEX IF NOT EXISTS idx_steps_item ON scheduling_steps(item_id);
CREATE INDEX IF NOT EXISTS idx_steps_parent ON scheduling_steps(parent_step_id);

CREATE INDEX IF NOT EXISTS idx_instances_date ON scheduling_instances(due_date);
CREATE INDEX IF NOT EXISTS idx_instances_item ON scheduling_instances(item_id);
CREATE INDEX IF NOT EXISTS idx_instances_completed ON scheduling_instances(is_completed);

-- =============================================================================
-- VIEWS
-- =============================================================================

-- Today View: Alle Items für heute mit Progress
CREATE VIEW IF NOT EXISTS v_scheduling_today AS
SELECT 
    i.id as instance_id,
    i.due_date,
    i.is_completed,
    i.completed_at,
    it.id as item_id,
    it.title,
    it.category,
    it.start_time,
    it.end_time,
    it.color_code,
    it.icon,
    tb.sort_order,
    tb.time_slot,
    tb.pinned,
    (SELECT COUNT(*) FROM scheduling_steps s WHERE s.item_id = it.id) as total_steps,
    (SELECT COUNT(*) FROM scheduling_step_completions sc 
     WHERE sc.instance_id = i.id AND sc.is_completed = 1) as completed_steps
FROM scheduling_instances i
JOIN scheduling_items it ON i.item_id = it.id
LEFT JOIN scheduling_today_board tb ON tb.instance_id = i.id
WHERE i.due_date = date('now');

-- =============================================================================
-- MIGRATION NOTES
-- =============================================================================
-- Prefix 'scheduling_' für alle Tabellen um Konflikte mit bach.db zu vermeiden
-- Kann später in bach.db integriert werden mit:
--   .read skills/_services/scheduling/schema_scheduling.sql
