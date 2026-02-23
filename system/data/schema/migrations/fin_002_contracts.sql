-- ============================================================
-- BACH VERTRAGS- & ABO-MODUL
-- ============================================================
-- Erstellt: 2026-01-28 by Gemini
-- Task: #538 (Finanz-Modul Erweiterung)
-- Ziel: user.db

CREATE TABLE IF NOT EXISTS fin_contracts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Grunddaten
    name TEXT NOT NULL,                    -- z.B. "Netflix", "Vodafone"
    kategorie TEXT,                        -- Streaming, Wohnen, Sport, Internet, Mobilfunk
    anbieter TEXT,                         -- Vertragspartner
    kundennummer TEXT,
    vertragsnummer TEXT,
    
    -- Kosten
    betrag REAL,
    waehrung TEXT DEFAULT 'EUR',
    intervall TEXT,                        -- monatlich, jaehrlich, quartalsweise
    naechste_zahlung DATE,
    
    -- Laufzeiten & Kündigung
    beginn_datum DATE,
    mindestlaufzeit_monate INTEGER,
    kuendigungsfrist_tage INTEGER, 
    verlaengerung_monate INTEGER,          
    ablauf_datum DATE,                     
    kuendigungs_status TEXT DEFAULT 'aktiv', -- aktiv, gekuendigt, pausiert
    
    -- Verknüpfungen
    dokument_pfad TEXT,
    web_login_url TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_fin_contracts_status ON fin_contracts(kuendigungs_status);
CREATE INDEX IF NOT EXISTS idx_fin_contracts_cat ON fin_contracts(kategorie);
