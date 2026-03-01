-- Migration 028: Memory-Daten von legacy-Tabellen in shared_* kopieren
-- SQ043 Stufe D: Datenmigration

-- Sessions migrieren
INSERT OR IGNORE INTO shared_memory_sessions
    (session_id, agent_id, started_at, ended_at, summary,
     tasks_completed, tasks_created, tokens_used, delegation_count,
     continuation_context, is_compressed, dist_type)
SELECT
    session_id,
    COALESCE(partner_id, 'legacy'),  -- agent_id aus partner_id
    started_at, ended_at, summary,
    tasks_completed, tasks_created, tokens_used, delegation_count,
    continuation_context, is_compressed, dist_type
FROM memory_sessions
WHERE session_id NOT IN (SELECT session_id FROM shared_memory_sessions);

-- Context-Triggers migrieren
INSERT OR IGNORE INTO shared_context_triggers
    (agent_id, trigger_phrase, hint_text, source, confidence,
     usage_count, last_used, is_active, created_at, updated_at, status, dist_type)
SELECT
    'legacy',  -- agent_id
    trigger_phrase, hint_text, source, confidence,
    usage_count, last_used, is_active, created_at, updated_at, status, 0
FROM context_triggers
WHERE trigger_phrase NOT IN (SELECT trigger_phrase FROM shared_context_triggers);
