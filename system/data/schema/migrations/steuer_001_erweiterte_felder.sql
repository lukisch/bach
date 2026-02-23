-- ============================================================
-- MIGRATION: STEUER_001 - Erweiterte DB-Felder
-- ============================================================
-- Datum: 2026-01-24
-- Beschreibung: Fuegt mwst_betrag, mwst_satz, ist_eigenbeleg etc. hinzu
-- ============================================================

-- Neue Felder zu steuer_posten hinzufuegen
ALTER TABLE steuer_posten ADD COLUMN mwst_betrag REAL;
ALTER TABLE steuer_posten ADD COLUMN mwst_satz INTEGER DEFAULT 19;
ALTER TABLE steuer_posten ADD COLUMN ist_eigenbeleg INTEGER DEFAULT 0;
ALTER TABLE steuer_posten ADD COLUMN zahlungsart TEXT;
ALTER TABLE steuer_posten ADD COLUMN bank_referenz TEXT;

-- Bestehende Daten: mwst_betrag aus brutto und netto berechnen
UPDATE steuer_posten
SET mwst_betrag = brutto - netto
WHERE mwst_betrag IS NULL AND brutto IS NOT NULL AND netto IS NOT NULL;

-- Bestehende Daten: mwst_satz ableiten (19% default)
UPDATE steuer_posten
SET mwst_satz = 19
WHERE mwst_satz IS NULL;

-- Index fuer Eigenbeleg-Suche
CREATE INDEX IF NOT EXISTS idx_steuer_posten_eigenbeleg
    ON steuer_posten(ist_eigenbeleg);

-- ============================================================
-- MIGRATION ENDE
-- ============================================================
