-- Migration 012: Neue Experten + Notizblock-Service registrieren
-- Datum: 2026-02-18
-- Beschreibung: Transkriptions-Service und Decision-Briefing als Experten
--               unter persoenlicher-assistent; Notizblock als Service

-- ═══════════════════════════════════════════════════════════════
-- bach_experts: Neue Experten eintragen
-- ═══════════════════════════════════════════════════════════════

INSERT OR IGNORE INTO bach_experts
    (name, display_name, agent_id, description, skill_path, domain, requires_files)
VALUES
    (
        'transkriptions-service',
        'Transkriptions-Service',
        (SELECT id FROM bach_agents WHERE name = 'persoenlicher-assistent'),
        'Audiodateien und Gespraeche wörtlich transkribieren, Sprecher erkennen, bereinigen, exportieren',
        'agents/_experts/transkriptions-service/',
        'medien',
        1
    ),
    (
        'decision-briefing',
        'Decision-Briefing',
        (SELECT id FROM bach_agents WHERE name = 'persoenlicher-assistent'),
        'Offene Entscheidungen und User-Aufgaben systemweit sammeln, bündeln, vorlegen und zurückverteilen',
        'agents/_experts/decision-briefing/',
        'organisation',
        1
    );

-- ═══════════════════════════════════════════════════════════════
-- agent_expert_mapping: Zuordnungen eintragen
-- ═══════════════════════════════════════════════════════════════

INSERT OR IGNORE INTO agent_expert_mapping (agent_id, expert_id, is_primary)
SELECT
    (SELECT id FROM bach_agents WHERE name = 'persoenlicher-assistent'),
    id,
    1
FROM bach_experts
WHERE name IN ('transkriptions-service', 'decision-briefing');

-- ═══════════════════════════════════════════════════════════════
-- agent_instances: Neue Experten als Instanzen registrieren
-- ═══════════════════════════════════════════════════════════════

INSERT OR IGNORE INTO agent_instances (name, agent_type, capabilities, config, is_active, created_at)
VALUES (
    'transkriptions-service',
    'expert',
    '["transkription", "sprecher-erkennung", "bereinigung", "export-pdf", "export-md"]',
    '{"notation": "standard", "export_formats": ["txt", "md", "pdf"], "notizblock_transfer": true}',
    1,
    datetime('now')
);

INSERT OR IGNORE INTO agent_instances (name, agent_type, capabilities, config, is_active, created_at)
VALUES (
    'decision-briefing',
    'expert',
    '["scan", "briefing", "entscheidungs-session", "rueckverteilung", "aufgaben-tracking"]',
    '{"sources_file": "user/decision_briefing/sources.json", "auto_scan": false}',
    1,
    datetime('now')
);

-- ═══════════════════════════════════════════════════════════════
-- HINWEIS: Notizblock-Service
-- Kein DB-Eintrag nötig — reiner dateibasierter Service.
-- Dateistruktur: user/notizen/ (siehe skills/_services/notizblock.md)
-- ═══════════════════════════════════════════════════════════════
