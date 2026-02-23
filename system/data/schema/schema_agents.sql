-- ===========================================================================
-- BACH v1.1 - AGENTS & EXPERTS SCHEMA
-- Erweitert bach.db um Agenten-Hierarchie und User-Daten
-- Erstellt: 2026-01-20
-- ===========================================================================

-- ---------------------------------------------------------------------------
-- AGENTEN (Boss-Agenten)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS bach_agents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    display_name TEXT NOT NULL,
    type TEXT DEFAULT 'boss' CHECK(type IN ('boss', 'helper', 'system')),
    category TEXT,                        -- 'privat', 'beruflich', 'system'
    description TEXT,
    skill_path TEXT,                      -- Pfad zu agents/xxx.txt
    user_data_folder TEXT,                -- Ordner unter user/ fuer Nutzerdaten
    parent_agent_id INTEGER REFERENCES bach_agents(id),

    -- Konfiguration
    is_active INTEGER DEFAULT 1,
    priority INTEGER DEFAULT 50,
    requires_setup INTEGER DEFAULT 0,
    setup_completed INTEGER DEFAULT 0,

    -- Statistiken
    usage_count INTEGER DEFAULT 0,
    last_used TIMESTAMP,

    -- Metadaten
    version TEXT DEFAULT '1.0.0',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_bach_agents_type ON bach_agents(type);
CREATE INDEX IF NOT EXISTS idx_bach_agents_category ON bach_agents(category);
CREATE INDEX IF NOT EXISTS idx_bach_agents_parent ON bach_agents(parent_agent_id);

-- ---------------------------------------------------------------------------
-- EXPERTEN (untergeordnete Spezialisten)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS bach_experts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    display_name TEXT NOT NULL,
    agent_id INTEGER NOT NULL REFERENCES bach_agents(id),  -- Zugehoeriger Boss-Agent
    description TEXT,
    skill_path TEXT,                      -- Pfad zu agents/_experts/xxx/
    user_data_folder TEXT,                -- Sub-Ordner unter Agent-Ordner

    -- Spezialisierung
    domain TEXT,                          -- 'finanzen', 'gesundheit', 'haushalt', etc.
    capabilities TEXT,                    -- JSON array

    -- Konfiguration
    is_active INTEGER DEFAULT 1,
    requires_db INTEGER DEFAULT 0,        -- Benoetigt DB-Tabellen
    requires_files INTEGER DEFAULT 0,     -- Benoetigt lokale Dateien

    -- Statistiken
    usage_count INTEGER DEFAULT 0,
    last_used TIMESTAMP,

    -- Metadaten
    version TEXT DEFAULT '1.0.0',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_bach_experts_agent ON bach_experts(agent_id);
CREATE INDEX IF NOT EXISTS idx_bach_experts_domain ON bach_experts(domain);

-- ---------------------------------------------------------------------------
-- AGENT-EXPERTEN ZUORDNUNG (m:n fuer geteilte Experten)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS agent_expert_mapping (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INTEGER NOT NULL REFERENCES bach_agents(id),
    expert_id INTEGER NOT NULL REFERENCES bach_experts(id),
    is_primary INTEGER DEFAULT 0,         -- Haupt-Agent fuer diesen Experten
    UNIQUE(agent_id, expert_id)
);

-- ---------------------------------------------------------------------------
-- USER-DATA FOLDERS (automatisch erstellte Ordner)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS user_data_folders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INTEGER REFERENCES bach_agents(id),
    expert_id INTEGER REFERENCES bach_experts(id),
    folder_path TEXT NOT NULL,            -- Relativer Pfad unter user/
    folder_type TEXT DEFAULT 'data' CHECK(folder_type IN ('data', 'archive', 'export', 'temp')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP
);

-- ---------------------------------------------------------------------------
-- GESUNDHEITSDATEN (fuer Gesundheitsassistent)
-- ---------------------------------------------------------------------------

-- Aerzte und Institutionen
CREATE TABLE IF NOT EXISTS health_contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    institution TEXT,
    specialty TEXT,                       -- 'Hausarzt', 'Kardiologe', etc.
    phone TEXT,
    email TEXT,
    address TEXT,
    notes TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Diagnosen
CREATE TABLE IF NOT EXISTS health_diagnoses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    diagnosis_name TEXT NOT NULL,
    icd_code TEXT,                        -- ICD-10 Code
    diagnosis_date DATE,
    status TEXT DEFAULT 'aktiv' CHECK(status IN ('aktiv', 'in_abklaerung', 'hypothese', 'widerlegt', 'geheilt')),
    severity TEXT CHECK(severity IN ('leicht', 'mittel', 'schwer')),
    doctor_id INTEGER REFERENCES health_contacts(id),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Medikamente
CREATE TABLE IF NOT EXISTS health_medications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    active_ingredient TEXT,               -- Wirkstoff
    dosage TEXT,                          -- z.B. "100mg"
    schedule TEXT,                        -- JSON: {"morning": 1, "evening": 1}
    diagnosis_id INTEGER REFERENCES health_diagnoses(id),
    start_date DATE,
    end_date DATE,
    status TEXT DEFAULT 'aktiv' CHECK(status IN ('aktiv', 'pausiert', 'beendet')),
    notes TEXT,
    side_effects TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Laborwerte
CREATE TABLE IF NOT EXISTS health_lab_values (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_name TEXT NOT NULL,
    value REAL,
    unit TEXT,
    reference_min REAL,
    reference_max REAL,
    test_date DATE NOT NULL,
    is_abnormal INTEGER DEFAULT 0,
    doctor_id INTEGER REFERENCES health_contacts(id),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dokumente (Befunde, Berichte)
CREATE TABLE IF NOT EXISTS health_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    doc_type TEXT CHECK(doc_type IN ('befund', 'arztbrief', 'labor', 'rezept', 'studie', 'sonstiges')),
    file_path TEXT,
    content_summary TEXT,
    document_date DATE,
    doctor_id INTEGER REFERENCES health_contacts(id),
    diagnosis_id INTEGER REFERENCES health_diagnoses(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Termine
CREATE TABLE IF NOT EXISTS health_appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    doctor_id INTEGER REFERENCES health_contacts(id),
    appointment_date DATETIME NOT NULL,
    duration_minutes INTEGER DEFAULT 30,
    appointment_type TEXT,                -- 'Vorsorge', 'Kontrolle', 'Akut'
    status TEXT DEFAULT 'geplant' CHECK(status IN ('geplant', 'bestaetigt', 'abgesagt', 'verschoben', 'erledigt')),
    notes TEXT,
    reminder_sent INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------------------
-- HAUSHALTSDATEN (fuer Haushaltsmanagement)
-- ---------------------------------------------------------------------------

-- Lagerbestaende
CREATE TABLE IF NOT EXISTS household_inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT,                        -- 'Medikamente', 'Hygiene', 'Lebensmittel', etc.
    quantity INTEGER DEFAULT 0,
    unit TEXT DEFAULT 'Stueck',
    min_quantity INTEGER DEFAULT 1,       -- Mindestbestand fuer Warnung
    location TEXT,                        -- Lagerort
    expiry_date DATE,
    last_restocked DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Einkaufslisten
CREATE TABLE IF NOT EXISTS household_shopping_lists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT DEFAULT 'Einkaufsliste',
    status TEXT DEFAULT 'aktiv' CHECK(status IN ('aktiv', 'erledigt', 'archiviert')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS household_shopping_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    list_id INTEGER NOT NULL REFERENCES household_shopping_lists(id),
    item_name TEXT NOT NULL,
    quantity INTEGER DEFAULT 1,
    unit TEXT,
    category TEXT,
    is_checked INTEGER DEFAULT 0,
    priority INTEGER DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Haushaltsbuch (Einnahmen/Ausgaben)
CREATE TABLE IF NOT EXISTS household_finances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_date DATE NOT NULL,
    entry_type TEXT NOT NULL CHECK(entry_type IN ('einnahme', 'ausgabe')),
    category TEXT,
    description TEXT,
    amount DECIMAL(10,2) NOT NULL,
    payment_method TEXT,                  -- 'Bar', 'Karte', 'Ueberweisung'
    is_recurring INTEGER DEFAULT 0,
    recurrence_interval TEXT,             -- 'monthly', 'yearly'
    tags TEXT,                            -- JSON array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_household_finances_date ON household_finances(entry_date);
CREATE INDEX IF NOT EXISTS idx_household_finances_category ON household_finances(category);

-- Routinen und Haushaltsplaene
CREATE TABLE IF NOT EXISTS household_routines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    frequency TEXT NOT NULL,              -- 'daily', 'weekly', 'monthly'
    schedule TEXT,                        -- JSON: {"days": [1,3,5], "time": "09:00"}
    category TEXT,                        -- 'Putzen', 'Waschen', etc.
    duration_minutes INTEGER,
    last_done TIMESTAMP,
    next_due TIMESTAMP,
    is_active INTEGER DEFAULT 1,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------------------
-- PSYCHO-BERATER DATEN
-- ---------------------------------------------------------------------------

-- Gespraechsprotokolle
CREATE TABLE IF NOT EXISTS psycho_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_date DATETIME NOT NULL,
    duration_minutes INTEGER,
    main_topics TEXT,                     -- JSON array
    key_insights TEXT,
    mood_before TEXT,
    mood_after TEXT,
    interventions_used TEXT,              -- JSON array
    homework TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Hypothesen und Beobachtungen
CREATE TABLE IF NOT EXISTS psycho_observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER REFERENCES psycho_sessions(id),
    observation_type TEXT CHECK(observation_type IN ('hypothese', 'beobachtung', 'muster', 'ressource')),
    content TEXT NOT NULL,
    confidence TEXT CHECK(confidence IN ('niedrig', 'mittel', 'hoch')),
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------------------
-- PERSOENLICHER ASSISTENT DATEN
-- ---------------------------------------------------------------------------

-- Kontakte
CREATE TABLE IF NOT EXISTS assistant_contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    context TEXT,                         -- 'privat', 'beruflich'
    email TEXT,
    phone TEXT,
    mobile TEXT,
    address TEXT,
    birthday DATE,
    notes TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Kalender-Eintraege
CREATE TABLE IF NOT EXISTS assistant_calendar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    event_type TEXT,                      -- 'termin', 'aufgabe', 'erinnerung'
    start_datetime DATETIME,
    end_datetime DATETIME,
    location TEXT,
    description TEXT,
    attendees TEXT,                       -- JSON array of contact_ids
    status TEXT DEFAULT 'geplant' CHECK(status IN ('geplant', 'bestaetigt', 'abgesagt', 'erledigt')),
    reminder_minutes INTEGER,
    is_recurring INTEGER DEFAULT 0,
    recurrence_rule TEXT,                 -- iCal RRULE format
    external_id TEXT,                     -- Google Calendar ID
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_assistant_calendar_date ON assistant_calendar(start_datetime);

-- Briefings und Dossiers
CREATE TABLE IF NOT EXISTS assistant_briefings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    briefing_type TEXT CHECK(briefing_type IN ('sachverhalt', 'person', 'location', 'reise')),
    content TEXT,
    file_path TEXT,
    related_event_id INTEGER REFERENCES assistant_calendar(id),
    sources TEXT,                         -- JSON array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Charaktersheet (gelerntes ueber Nutzer)
CREATE TABLE IF NOT EXISTS assistant_user_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,               -- 'praeferenz', 'gewohnheit', 'eigenheit'
    key TEXT NOT NULL,
    value TEXT,
    confidence TEXT DEFAULT 'mittel' CHECK(confidence IN ('niedrig', 'mittel', 'hoch')),
    learned_from TEXT,                    -- Quelle der Information
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(category, key)
);

-- ---------------------------------------------------------------------------
-- INITIAL DATA - AGENTEN
-- ---------------------------------------------------------------------------

INSERT OR IGNORE INTO bach_agents (name, display_name, type, category, description, skill_path, user_data_folder) VALUES
    ('persoenlicher-assistent', 'Persoenlicher Assistent', 'boss', 'privat',
     'Terminverwaltung, Recherche, Kommunikation und Organisation',
     'agents/persoenlicher-assistent.txt', 'persoenlicher_assistent'),

    ('gesundheitsassistent', 'Gesundheitsassistent', 'boss', 'privat',
     'Verwaltung medizinischer Dokumente, Befunde, Diagnosen und Medikamente',
     'agents/gesundheitsassistent.txt', 'gesundheit'),

    ('bueroassistent', 'Bueroassistent', 'boss', 'beruflich',
     'Berufliche Unterstuetzung: Steuern, Foerderplanung, Dokumentation',
     'agents/bueroassistent.txt', 'buero');

-- ---------------------------------------------------------------------------
-- INITIAL DATA - EXPERTEN
-- ---------------------------------------------------------------------------

-- Experten unter Persoenlicher Assistent
INSERT OR IGNORE INTO bach_experts (name, display_name, agent_id, description, skill_path, domain) VALUES
    ('haushaltsmanagement', 'Haushaltsmanagement',
     (SELECT id FROM bach_agents WHERE name='persoenlicher-assistent'),
     'Haushaltsbuch, Lagerbestaende, Einkaufslisten, Routinen',
     'agents/_experts/haushaltsmanagement/', 'haushalt');

-- Experten unter Gesundheitsassistent
INSERT OR IGNORE INTO bach_experts (name, display_name, agent_id, description, skill_path, domain) VALUES
    ('gesundheitsverwalter', 'Gesundheitsverwalter',
     (SELECT id FROM bach_agents WHERE name='gesundheitsassistent'),
     'Arztberichte, Blutwerte, Medikamente, Aerzte-Kontakte',
     'agents/_experts/gesundheitsverwalter/', 'gesundheit'),

    ('psycho-berater', 'Psycho-Berater',
     (SELECT id FROM bach_agents WHERE name='gesundheitsassistent'),
     'Therapeutische Gespraechsfuehrung und Dokumentation',
     'agents/_experts/psycho-berater/', 'psychologie');

-- Experten unter Bueroassistent
INSERT OR IGNORE INTO bach_experts (name, display_name, agent_id, description, skill_path, domain) VALUES
    ('steuer-agent', 'Steuer-Agent',
     (SELECT id FROM bach_agents WHERE name='bueroassistent'),
     'Steuererklarung und Belegerfassung',
     'agents/_experts/steuer/', 'finanzen'),

    ('foerderplaner', 'Foerderplaner',
     (SELECT id FROM bach_agents WHERE name='bueroassistent'),
     'ICF-basierte Foerderplanung und Materialrecherche',
     'agents/_experts/foerderplaner/', 'paedagogik');

-- ---------------------------------------------------------------------------
-- VIEWS
-- ---------------------------------------------------------------------------

-- Agenten mit Experten-Anzahl
CREATE VIEW IF NOT EXISTS v_agents_overview AS
SELECT
    a.id,
    a.name,
    a.display_name,
    a.type,
    a.category,
    a.is_active,
    a.usage_count,
    a.last_used,
    COUNT(e.id) as expert_count
FROM bach_agents a
LEFT JOIN bach_experts e ON e.agent_id = a.id
GROUP BY a.id;

-- Experten mit Agent-Namen
CREATE VIEW IF NOT EXISTS v_experts_overview AS
SELECT
    e.id,
    e.name,
    e.display_name,
    e.domain,
    e.is_active,
    a.name as agent_name,
    a.display_name as agent_display_name
FROM bach_experts e
JOIN bach_agents a ON a.id = e.agent_id;

-- Gesundheits-Dashboard View
CREATE VIEW IF NOT EXISTS v_health_dashboard AS
SELECT
    (SELECT COUNT(*) FROM health_diagnoses WHERE status = 'aktiv') as active_diagnoses,
    (SELECT COUNT(*) FROM health_medications WHERE status = 'aktiv') as active_medications,
    (SELECT COUNT(*) FROM health_appointments WHERE status IN ('geplant', 'bestaetigt') AND appointment_date >= date('now')) as upcoming_appointments,
    (SELECT COUNT(*) FROM health_lab_values WHERE is_abnormal = 1 AND test_date >= date('now', '-90 days')) as recent_abnormal_values;

-- Haushalts-Dashboard View
CREATE VIEW IF NOT EXISTS v_household_dashboard AS
SELECT
    (SELECT COUNT(*) FROM household_inventory WHERE quantity <= min_quantity) as low_stock_items,
    (SELECT COUNT(*) FROM household_shopping_items WHERE is_checked = 0 AND list_id IN (SELECT id FROM household_shopping_lists WHERE status = 'aktiv')) as open_shopping_items,
    (SELECT SUM(amount) FROM household_finances WHERE entry_type = 'ausgabe' AND entry_date >= date('now', 'start of month')) as monthly_expenses,
    (SELECT COUNT(*) FROM household_routines WHERE is_active = 1 AND next_due <= datetime('now')) as overdue_routines;
