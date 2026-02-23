-- =============================================================================
-- HOUSEHOLD SERVICE - SQLite Schema
-- Version: 1.0.0
-- Erstellt: 2026-01-25
-- Basiert auf: household/stubs/models.py, inventory.py, health.py
-- Kombiniert: HausLagerist (Inventory) + MediPlaner (Health)
-- =============================================================================

-- =============================================================================
-- INVENTORY MODULE (HausLagerist)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- PRODUCTS - Produkte im Haushalt
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS household_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT DEFAULT 'general',        -- 'food', 'cleaning', 'hygiene', 'general'
    barcode TEXT UNIQUE,
    
    -- Bestand
    stock REAL DEFAULT 0,
    unit TEXT DEFAULT 'Stück',              -- 'Stück', 'kg', 'l', 'ml', 'g'
    min_stock REAL DEFAULT 1,               -- Warnschwelle
    
    -- Bestellung
    preferred_shop TEXT,
    price_estimate REAL,
    order_size REAL DEFAULT 1,              -- Standard-Bestellmenge
    
    -- Meta
    location TEXT,                          -- 'Küche', 'Keller', 'Bad'
    notes TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- SCAN_LOG - Barcode-Scan Protokoll
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS household_scan_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    scan_type TEXT NOT NULL,                -- 'consume', 'add', 'inventory'
    quantity REAL DEFAULT 1,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (product_id) REFERENCES household_products(id)
);

-- -----------------------------------------------------------------------------
-- SHOPPING_LIST - Einkaufsliste
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS household_shopping_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    priority INTEGER DEFAULT 2,             -- 1=hoch, 2=normal, 3=niedrig
    pull_factor REAL DEFAULT 1.0,           -- Berechneter Dringlichkeitsfaktor
    is_purchased INTEGER DEFAULT 0,
    purchased_at TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (product_id) REFERENCES household_products(id)
);

-- =============================================================================
-- HEALTH MODULE (MediPlaner)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- CLIENTS - Personen/Klienten
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS household_clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    birth_date TEXT,
    notes TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- MEDICATIONS - Medikamente (Stammdaten)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS household_medications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    active_ingredient TEXT,                 -- Wirkstoff
    dose TEXT,                              -- z.B. '100mg', '5ml'
    unit TEXT DEFAULT 'Tabletten',          -- 'Tabletten', 'ml', 'Tropfen'
    manufacturer TEXT,
    pzn TEXT,                               -- Pharmazentralnummer
    
    -- Bestand
    stock REAL DEFAULT 0,
    min_stock REAL DEFAULT 7,               -- Tage-Vorrat Warnschwelle
    
    -- Bestellung
    prescription_required INTEGER DEFAULT 0,
    pharmacy TEXT,
    price_estimate REAL,
    
    -- Meta
    notes TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- MEDICATION_ENTRIES - Medikamentenplan (wer nimmt was wann)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS household_medication_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    medication_id INTEGER NOT NULL,
    
    -- Dosierung
    dose_amount REAL NOT NULL,              -- z.B. 1.0 (Tablette), 2.5 (ml)
    dose_unit TEXT DEFAULT 'Stück',
    
    -- Einnahmezeiten
    time_morning INTEGER DEFAULT 0,
    time_noon INTEGER DEFAULT 0,
    time_evening INTEGER DEFAULT 0,
    time_night INTEGER DEFAULT 0,
    specific_time TEXT,                     -- Genaue Uhrzeit wenn nötig
    
    -- Zeitraum
    start_date TEXT,
    end_date TEXT,                          -- NULL = unbefristet
    
    -- Status
    is_active INTEGER DEFAULT 1,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (client_id) REFERENCES household_clients(id),
    FOREIGN KEY (medication_id) REFERENCES household_medications(id)
);

-- -----------------------------------------------------------------------------
-- MEDICATION_LOG - Einnahme-Protokoll
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS household_medication_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id INTEGER NOT NULL,
    taken_at TEXT DEFAULT CURRENT_TIMESTAMP,
    taken_dose REAL,
    skipped INTEGER DEFAULT 0,
    notes TEXT,
    
    FOREIGN KEY (entry_id) REFERENCES household_medication_entries(id)
);

-- =============================================================================
-- INDICES
-- =============================================================================
CREATE INDEX IF NOT EXISTS idx_products_barcode ON household_products(barcode);
CREATE INDEX IF NOT EXISTS idx_products_category ON household_products(category);
CREATE INDEX IF NOT EXISTS idx_products_active ON household_products(is_active);

CREATE INDEX IF NOT EXISTS idx_scan_product ON household_scan_log(product_id);
CREATE INDEX IF NOT EXISTS idx_scan_timestamp ON household_scan_log(timestamp);

CREATE INDEX IF NOT EXISTS idx_shopping_purchased ON household_shopping_list(is_purchased);
CREATE INDEX IF NOT EXISTS idx_shopping_product ON household_shopping_list(product_id);

CREATE INDEX IF NOT EXISTS idx_clients_active ON household_clients(is_active);

CREATE INDEX IF NOT EXISTS idx_medications_active ON household_medications(is_active);
CREATE INDEX IF NOT EXISTS idx_medications_pzn ON household_medications(pzn);

CREATE INDEX IF NOT EXISTS idx_entries_client ON household_medication_entries(client_id);
CREATE INDEX IF NOT EXISTS idx_entries_medication ON household_medication_entries(medication_id);
CREATE INDEX IF NOT EXISTS idx_entries_active ON household_medication_entries(is_active);

-- =============================================================================
-- VIEWS
-- =============================================================================

-- Low Stock Alert: Produkte unter Mindestbestand
CREATE VIEW IF NOT EXISTS v_household_low_stock AS
SELECT 
    p.id,
    p.name,
    p.category,
    p.stock,
    p.min_stock,
    p.unit,
    (p.stock / p.min_stock) as stock_ratio,
    CASE 
        WHEN p.stock <= 0 THEN 'critical'
        WHEN p.stock < p.min_stock THEN 'warning'
        ELSE 'ok'
    END as status
FROM household_products p
WHERE p.is_active = 1 AND p.stock < p.min_stock;

-- Medication Overview: Medikamente mit Verbrauch und Status
CREATE VIEW IF NOT EXISTS v_household_medication_status AS
SELECT 
    m.id,
    m.name,
    m.stock,
    m.min_stock,
    m.unit,
    (SELECT SUM(
        e.dose_amount * (e.time_morning + e.time_noon + e.time_evening + e.time_night)
    ) FROM household_medication_entries e 
    WHERE e.medication_id = m.id AND e.is_active = 1) as daily_consumption,
    CASE
        WHEN m.stock <= 0 THEN 'red'
        WHEN m.stock < m.min_stock THEN 'yellow'
        ELSE 'green'
    END as ampel_status
FROM household_medications m
WHERE m.is_active = 1;

-- Client Medication Plan: Vollständiger Plan pro Klient
CREATE VIEW IF NOT EXISTS v_household_client_plan AS
SELECT 
    c.id as client_id,
    c.name as client_name,
    m.name as medication_name,
    e.dose_amount,
    e.dose_unit,
    e.time_morning,
    e.time_noon,
    e.time_evening,
    e.time_night,
    e.specific_time,
    e.notes
FROM household_clients c
JOIN household_medication_entries e ON e.client_id = c.id
JOIN household_medications m ON e.medication_id = m.id
WHERE c.is_active = 1 AND e.is_active = 1;

-- =============================================================================
-- MIGRATION NOTES
-- =============================================================================
-- Prefix 'household_' für alle Tabellen um Konflikte mit bach.db zu vermeiden
-- Kann später in bach.db integriert werden mit:
--   .read skills/_services/household/schema_household.sql
