-- Migration 025: HausLagerist V4 Integration (INT02, PEANUT v3.3.0)
-- Pull-basiertes Vorratsmanagement mit automatischer Einkaufslisten-Generierung
--
-- Erweitert household_inventory um Pull-Felder
-- Erstellt: household_suppliers, household_orders, household_stock_transactions

-- ============================================================
-- 1. household_inventory erweitern (ALTER TABLE)
-- ============================================================

-- Einheiten-Erweiterung
ALTER TABLE household_inventory ADD COLUMN pack_unit TEXT DEFAULT 'Packung';
ALTER TABLE household_inventory ADD COLUMN pack_size REAL DEFAULT 1;

-- Produktdetails
ALTER TABLE household_inventory ADD COLUMN brand TEXT;
ALTER TABLE household_inventory ADD COLUMN barcode TEXT;

-- Pull-Einstellungen (V4 Kern)
ALTER TABLE household_inventory ADD COLUMN priority INTEGER DEFAULT 2;
ALTER TABLE household_inventory ADD COLUMN pull_threshold REAL DEFAULT 1.0;
ALTER TABLE household_inventory ADD COLUMN learning_alpha REAL DEFAULT 0.3;

-- Lieferant-Verknuepfung
ALTER TABLE household_inventory ADD COLUMN preferred_supplier_id INTEGER;

-- Archiv-Flag
ALTER TABLE household_inventory ADD COLUMN archived INTEGER DEFAULT 0;


-- ============================================================
-- 2. Neue Tabellen
-- ============================================================

CREATE TABLE IF NOT EXISTS household_suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    supplier_type TEXT DEFAULT 'other',   -- supermarket, drugstore, online, other
    address TEXT,
    phone TEXT,
    email TEXT,
    website TEXT,
    notes TEXT,
    archived INTEGER DEFAULT 0,
    dist_type INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS household_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER NOT NULL,
    order_type TEXT NOT NULL DEFAULT 'routine',  -- routine|period|oneshot|project
    start_date TEXT,                             -- ISO-Format YYYY-MM-DD
    end_date TEXT,                               -- Fuer period/project
    target_date TEXT,                            -- Fuer oneshot
    quantity_value REAL NOT NULL,                -- Menge pro Zyklus/Zeitraum
    cycle_interval_days INTEGER,                 -- Fuer routine: alle X Tage
    status TEXT DEFAULT 'active',                -- active|fulfilled|cancelled|expired
    fulfilled_date TEXT,
    reason TEXT,
    priority INTEGER DEFAULT 2,                  -- 1=optional, 2=wichtig, 3=kritisch
    notes TEXT,
    dist_type INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (article_id) REFERENCES household_inventory(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS household_stock_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER NOT NULL,
    transaction_type TEXT NOT NULL,               -- purchase|consumption|remove|manual
    amount REAL NOT NULL,                         -- Positive = Eingang, Negative = Ausgang
    stock_before REAL,
    stock_after REAL,
    supplier_id INTEGER,
    price_per_unit REAL,
    note TEXT,
    dist_type INTEGER DEFAULT 0,
    timestamp TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (article_id) REFERENCES household_inventory(id) ON DELETE CASCADE,
    FOREIGN KEY (supplier_id) REFERENCES household_suppliers(id) ON DELETE SET NULL
);


-- ============================================================
-- 3. Indizes
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_ho_article_status ON household_orders(article_id, status);
CREATE INDEX IF NOT EXISTS idx_hst_article ON household_stock_transactions(article_id);
CREATE INDEX IF NOT EXISTS idx_hst_timestamp ON household_stock_transactions(timestamp);
CREATE INDEX IF NOT EXISTS idx_hi_category ON household_inventory(category);
CREATE INDEX IF NOT EXISTS idx_hi_archived ON household_inventory(archived);
