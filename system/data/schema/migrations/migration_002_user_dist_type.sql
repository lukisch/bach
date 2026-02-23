-- ============================================================
-- BACH v1.1 - MIGRATION 002: dist_type fuer alle user.db Tabellen
-- ============================================================
-- Erstellt: 2026-01-28
-- Zweck: Alle user.db Tabellen mit dist_type versehen
--         damit User-Daten bei Distribution nicht mitgeliefert werden
-- Ref: docs/WICHTIG_SYSTEMISCH_FIRST.md
-- ============================================================
--
-- dist_type Werte:
--   0 = USER_DATA   (nicht mitverpacken, bleibt beim User)
--   1 = TEMPLATE    (mitverpacken, zuruecksetzbar)
--   2 = CORE        (mitverpacken, unveraenderlich)
--
-- Regel: Alle Tabellen mit Nutzer-generierten Daten -> DEFAULT 0
--        System-Definitionen (agents, experts) -> DEFAULT 2
-- ============================================================

-- USER_DATA (dist_type = 0): Nutzer-spezifische Daten
ALTER TABLE abo_payments ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE abo_subscriptions ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE assistant_briefings ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE assistant_calendar ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE assistant_contacts ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE assistant_user_profile ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE fin_contracts ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE fin_insurance_claims ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE fin_insurances ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE financial_emails ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE financial_subscriptions ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE financial_summary ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE health_appointments ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE health_contacts ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE health_diagnoses ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE health_documents ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE health_lab_values ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE health_medications ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE household_finances ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE household_inventory ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE household_routines ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE household_shopping_items ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE household_shopping_lists ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE mail_accounts ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE mail_sync_runs ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE psycho_observations ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE psycho_sessions ADD COLUMN dist_type INTEGER DEFAULT 0;
ALTER TABLE user_data_folders ADD COLUMN dist_type INTEGER DEFAULT 0;

-- CORE (dist_type = 2): System-Definitionen
ALTER TABLE bach_agents ADD COLUMN dist_type INTEGER DEFAULT 2;
ALTER TABLE bach_experts ADD COLUMN dist_type INTEGER DEFAULT 2;
ALTER TABLE agent_expert_mapping ADD COLUMN dist_type INTEGER DEFAULT 2;

-- ============================================================
-- BACKUP-VIEW: Alle User-Daten fuer Backup
-- ============================================================
CREATE VIEW IF NOT EXISTS v_user_backup_tables AS
SELECT 'assistant_contacts' as tbl, COUNT(*) as cnt FROM assistant_contacts WHERE dist_type = 0
UNION ALL SELECT 'assistant_calendar', COUNT(*) FROM assistant_calendar WHERE dist_type = 0
UNION ALL SELECT 'fin_insurances', COUNT(*) FROM fin_insurances WHERE dist_type = 0
UNION ALL SELECT 'fin_contracts', COUNT(*) FROM fin_contracts WHERE dist_type = 0
UNION ALL SELECT 'health_contacts', COUNT(*) FROM health_contacts WHERE dist_type = 0
UNION ALL SELECT 'health_diagnoses', COUNT(*) FROM health_diagnoses WHERE dist_type = 0
UNION ALL SELECT 'health_medications', COUNT(*) FROM health_medications WHERE dist_type = 0
UNION ALL SELECT 'health_lab_values', COUNT(*) FROM health_lab_values WHERE dist_type = 0
UNION ALL SELECT 'health_documents', COUNT(*) FROM health_documents WHERE dist_type = 0
UNION ALL SELECT 'health_appointments', COUNT(*) FROM health_appointments WHERE dist_type = 0
UNION ALL SELECT 'household_routines', COUNT(*) FROM household_routines WHERE dist_type = 0
UNION ALL SELECT 'financial_emails', COUNT(*) FROM financial_emails WHERE dist_type = 0;
