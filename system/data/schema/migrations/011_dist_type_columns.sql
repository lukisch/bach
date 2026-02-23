-- Migration 011: dist_type Spalten nachtragen (HQ1-A)
-- Datum: 2026-02-17
-- Beschreibung: Traegt die fehlende dist_type Spalte in drei Tabellen nach,
--   fuer die schema_distribution.sql das Schema definiert hat.
--
-- Hinweis: Das Schema-SQL referenziert 'files_directory_truth',
--   die echte Tabelle heisst aber 'files_truth'.
--
-- ACHTUNG: SQLite unterstuetzt kein "ADD COLUMN IF NOT EXISTS".
--   Bei erneutem Ausfuehren auf einer DB wo die Spalten bereits existieren,
--   wird SQLite einen Fehler werfen. Die begleitende .py-Datei bietet
--   eine idempotente Alternative fuer manuelle Ausfuehrung.

-- system_config: dist_type = 2 (CORE)
ALTER TABLE system_config ADD COLUMN dist_type INTEGER DEFAULT 2;

-- files_truth: dist_type = 1 (TEMPLATE)
ALTER TABLE files_truth ADD COLUMN dist_type INTEGER DEFAULT 1;

-- automation_triggers: dist_type = 2 (CORE)
ALTER TABLE automation_triggers ADD COLUMN dist_type INTEGER DEFAULT 2;
