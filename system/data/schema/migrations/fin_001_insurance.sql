-- ============================================================
-- BACH VERSICHERUNGS-MODUL
-- ============================================================
-- Erstellt: 2026-01-28 by Gemini
-- Task: #537 (Finanz-Modul Erweiterung)
-- Ziel: user.db

CREATE TABLE IF NOT EXISTS fin_insurances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    anbieter TEXT NOT NULL,                -- Allianz, HUK, etc.
    tarif_name TEXT,                       -- "Komfort Plus"
    police_nr TEXT UNIQUE,
    sparte TEXT NOT NULL,                  -- Haftpflicht, BU, KFZ, Hausrat, etc.
    status TEXT DEFAULT 'aktiv',           -- aktiv, gekuendigt, beitragsfrei
    
    -- Termine
    beginn_datum DATE,
    ablauf_datum DATE,
    kuendigungsfrist_monate INTEGER DEFAULT 3,
    verlaengerung_monate INTEGER DEFAULT 12,
    naechste_kuendigung DATE,              -- Berechnet oder manuell
    
    -- Finanzen
    beitrag REAL,
    zahlweise TEXT,                       -- monatlich, quartalsweise, jaehrlich
    steuer_relevant_typ TEXT,             -- Vorsorgeaufwendungen, etc.
    
    -- Verknüpfungen
    ordner_pfad TEXT,                      -- Pfad zu Scans
    notizen TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS fin_insurance_claims (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    insurance_id INTEGER REFERENCES fin_insurances(id),
    schadensdatum DATE,
    beschreibung TEXT,
    status TEXT DEFAULT 'offen',           -- offen, reguliert, abgelehnt
    betrag_gefordert REAL,
    betrag_gezahlt REAL,
    aktenzeichen_versicherung TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_fin_insurances_sparte ON fin_insurances(sparte);
CREATE INDEX IF NOT EXISTS idx_fin_insurances_status ON fin_insurances(status);
