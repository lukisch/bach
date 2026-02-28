-- Migration 017: context_triggers Qualitaetssystem (SQ066/ENT-39)
-- Erstellt: 2026-02-19
-- Zweck: 3-Zustands-Status-Spalte + automatische Block-Regeln
--
-- Status-Werte:
--   'unknown'  (default) -- Nicht bewertet, funktioniert weiterhin
--   'blocked'            -- Wird bei Kontext-Injektion uebersprungen
--   'approved'           -- Explizit genehmigt
--
-- Auto-Block-Regeln (beim ersten Run):
--   1. Woerter < 4 Zeichen (Rauschen, Stop-Woerter)
--   2. Encoding-Defekte (Sonderzeichen ausserhalb ASCII+Umlaute)

-- Schritt 1: status-Spalte hinzufuegen (falls nicht vorhanden)
ALTER TABLE context_triggers ADD COLUMN status TEXT NOT NULL DEFAULT 'unknown'
    CHECK (status IN ('unknown', 'blocked', 'approved'));

-- Schritt 2: Auto-Block -- Trigger-Phrasen < 4 Zeichen
UPDATE context_triggers
SET status = 'blocked'
WHERE status = 'unknown'
  AND is_protected = 0
  AND length(trim(trigger_phrase)) < 4;

-- Schritt 3: Auto-Block -- Encoding-Defekte erkennen
-- Defekte Zeichen: Kontrollzeichen (ASCII < 32 ausser Tab/Newline),
-- Replacement-Character (U+FFFD als UTF-8: 0xEFBFBD),
-- Typische Windows-1252->UTF-8 Defekte (z.B. Â, Ã, Ã¼, â€)
UPDATE context_triggers
SET status = 'blocked'
WHERE status = 'unknown'
  AND is_protected = 0
  AND (
    -- Kontrollzeichen (ASCII 0-8, 11-12, 14-31)
    trigger_phrase GLOB '*' || char(0) || '*'
    OR trigger_phrase GLOB '*' || char(1) || '*'
    OR trigger_phrase GLOB '*' || char(2) || '*'
    OR trigger_phrase GLOB '*' || char(3) || '*'
    OR trigger_phrase GLOB '*' || char(4) || '*'
    OR trigger_phrase GLOB '*' || char(5) || '*'
    OR trigger_phrase GLOB '*' || char(6) || '*'
    OR trigger_phrase GLOB '*' || char(7) || '*'
    OR trigger_phrase GLOB '*' || char(8) || '*'
    OR trigger_phrase GLOB '*' || char(11) || '*'
    OR trigger_phrase GLOB '*' || char(12) || '*'
    OR trigger_phrase GLOB '*' || char(14) || '*'
    OR trigger_phrase GLOB '*' || char(15) || '*'
    OR trigger_phrase GLOB '*' || char(16) || '*'
    OR trigger_phrase GLOB '*' || char(17) || '*'
    OR trigger_phrase GLOB '*' || char(18) || '*'
    OR trigger_phrase GLOB '*' || char(19) || '*'
    OR trigger_phrase GLOB '*' || char(20) || '*'
    OR trigger_phrase GLOB '*' || char(21) || '*'
    OR trigger_phrase GLOB '*' || char(22) || '*'
    OR trigger_phrase GLOB '*' || char(23) || '*'
    OR trigger_phrase GLOB '*' || char(24) || '*'
    OR trigger_phrase GLOB '*' || char(25) || '*'
    OR trigger_phrase GLOB '*' || char(26) || '*'
    OR trigger_phrase GLOB '*' || char(27) || '*'
    OR trigger_phrase GLOB '*' || char(28) || '*'
    OR trigger_phrase GLOB '*' || char(29) || '*'
    OR trigger_phrase GLOB '*' || char(30) || '*'
    OR trigger_phrase GLOB '*' || char(31) || '*'
    -- Haeufige Windows-1252->UTF-8 Mojibake-Muster
    OR trigger_phrase LIKE '%Ã¼%'
    OR trigger_phrase LIKE '%Ã¶%'
    OR trigger_phrase LIKE '%Ã¤%'
    OR trigger_phrase LIKE '%Ã%'
    OR trigger_phrase LIKE '%â€%'
    OR trigger_phrase LIKE '%Â%'
  );

-- Schritt 4: Index auf status-Spalte fuer schnelle Filterung
CREATE INDEX IF NOT EXISTS idx_context_triggers_status
    ON context_triggers(status);

-- Ergebnis-Uebersicht (Kommentar -- kein SELECT in Migration-Scripts)
-- SELECT status, COUNT(*) FROM context_triggers GROUP BY status;
