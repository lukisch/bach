-- Migration 030: Injector Tables (SQ040 + SQ042)
-- Reminder Injector + Meta-Feedback Injector

-- SQ040: Reminder Injector
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trigger_condition TEXT NOT NULL DEFAULT 'always',
    trigger_value TEXT,
    message TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1,
    priority INTEGER NOT NULL DEFAULT 5,
    last_triggered TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- SQ042: Meta-Feedback Injector
CREATE TABLE IF NOT EXISTS meta_feedback_patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pattern TEXT NOT NULL,
    pattern_type TEXT NOT NULL DEFAULT 'substring',
    correction TEXT NOT NULL,
    frequency INTEGER NOT NULL DEFAULT 0,
    max_inactive_count INTEGER NOT NULL DEFAULT 10,
    inactive_count INTEGER NOT NULL DEFAULT 0,
    active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_reminders_active ON reminders(active);
CREATE INDEX IF NOT EXISTS idx_reminders_trigger ON reminders(trigger_condition);
CREATE INDEX IF NOT EXISTS idx_meta_feedback_active ON meta_feedback_patterns(active);
