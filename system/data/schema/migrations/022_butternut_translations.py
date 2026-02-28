#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Migration 022: BUTTERNUT Uebersetzungen einfuegen."""

import sqlite3
import sys
import os

def migrate(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    translations = [
        # === Handler-Namen (namespace: handler) ===
        ("agent", "handler", "en", "Agent Launcher"),
        ("agent", "handler", "de", "Agent-Starter"),
        ("prompt", "handler", "en", "Prompt Manager"),
        ("prompt", "handler", "de", "Prompt-Verwaltung"),
        ("scheduler", "handler", "en", "Scheduler"),
        ("scheduler", "handler", "de", "Zeitplaner"),
        ("chain", "handler", "en", "Chain Manager"),
        ("chain", "handler", "de", "Ketten-Verwaltung"),
        ("shared_memory", "handler", "en", "Shared Memory"),
        ("shared_memory", "handler", "de", "Gemeinsamer Speicher"),
        ("memory", "handler", "en", "Memory"),
        ("memory", "handler", "de", "Gedaechtnis"),
        ("task", "handler", "en", "Task Manager"),
        ("task", "handler", "de", "Aufgabenverwaltung"),
        ("backup", "handler", "en", "Backup Manager"),
        ("backup", "handler", "de", "Datensicherung"),
        ("status", "handler", "en", "System Status"),
        ("status", "handler", "de", "Systemstatus"),
        ("help", "handler", "en", "Help"),
        ("help", "handler", "de", "Hilfe"),
        ("lesson", "handler", "en", "Lessons Learned"),
        ("lesson", "handler", "de", "Erkenntnisse"),
        ("calendar", "handler", "en", "Calendar"),
        ("calendar", "handler", "de", "Kalender"),
        ("contact", "handler", "en", "Contacts"),
        ("contact", "handler", "de", "Kontakte"),
        ("email", "handler", "en", "Email"),
        ("email", "handler", "de", "E-Mail"),
        ("steuer", "handler", "en", "Tax Manager"),
        ("steuer", "handler", "de", "Steuerverwaltung"),
        ("abo", "handler", "en", "Subscriptions"),
        ("abo", "handler", "de", "Abonnements"),
        ("wiki", "handler", "en", "Wiki"),
        ("wiki", "handler", "de", "Wiki"),
        ("scan", "handler", "en", "Scanner"),
        ("scan", "handler", "de", "Scanner"),
        ("session", "handler", "en", "Session Manager"),
        ("session", "handler", "de", "Sitzungsverwaltung"),
        ("consolidate", "handler", "en", "Consolidation"),
        ("consolidate", "handler", "de", "Konsolidierung"),
        ("tools", "handler", "en", "Tools"),
        ("tools", "handler", "de", "Werkzeuge"),
        ("plugins", "handler", "en", "Plugins"),
        ("plugins", "handler", "de", "Erweiterungen"),
        ("hooks", "handler", "en", "Hooks"),
        ("hooks", "handler", "de", "Hooks"),
        ("gesundheit", "handler", "en", "Health Manager"),
        ("gesundheit", "handler", "de", "Gesundheitsverwaltung"),
        ("haushalt", "handler", "en", "Household Manager"),
        ("haushalt", "handler", "de", "Haushaltsverwaltung"),
        ("versicherung", "handler", "en", "Insurance Manager"),
        ("versicherung", "handler", "de", "Versicherungsverwaltung"),
        ("lang", "handler", "en", "Language Settings"),
        ("lang", "handler", "de", "Spracheinstellungen"),
        ("doc", "handler", "en", "Documentation"),
        ("doc", "handler", "de", "Dokumentation"),
        ("bericht", "handler", "en", "Reports"),
        ("bericht", "handler", "de", "Berichte"),
        ("inbox", "handler", "en", "Inbox"),
        ("inbox", "handler", "de", "Posteingang"),
        ("secrets", "handler", "en", "Secrets Manager"),
        ("secrets", "handler", "de", "Geheimnisse"),
        ("api_prober", "handler", "en", "API Prober"),
        ("api_prober", "handler", "de", "API-Pruefung"),
        ("n8n_manager", "handler", "en", "n8n Workflow Manager"),
        ("n8n_manager", "handler", "de", "n8n Workflow-Verwaltung"),
        ("user_sync", "handler", "en", "User Sync"),
        ("user_sync", "handler", "de", "Benutzer-Synchronisation"),
        ("routine", "handler", "en", "Routines"),
        ("routine", "handler", "de", "Routinen"),
        ("partner", "handler", "en", "Partners"),
        ("partner", "handler", "de", "Partner"),
        ("messages", "handler", "en", "Messages"),
        ("messages", "handler", "de", "Nachrichten"),
        ("data_analysis", "handler", "en", "Data Analysis"),
        ("data_analysis", "handler", "de", "Datenanalyse"),
        ("curriculum", "handler", "en", "Curriculum Vitae"),
        ("curriculum", "handler", "de", "Lebenslauf"),
        ("skills", "handler", "en", "Skills"),
        ("skills", "handler", "de", "Faehigkeiten"),
        ("extensions", "handler", "en", "Extensions"),
        ("extensions", "handler", "de", "Erweiterungen"),
        ("mount", "handler", "en", "Mount Points"),
        ("mount", "handler", "de", "Einhängepunkte"),

        # === Operationen (namespace: operation) ===
        ("list", "operation", "en", "List"),
        ("list", "operation", "de", "Auflisten"),
        ("add", "operation", "en", "Add"),
        ("add", "operation", "de", "Hinzufuegen"),
        ("get", "operation", "en", "Get details"),
        ("get", "operation", "de", "Details anzeigen"),
        ("update", "operation", "en", "Update"),
        ("update", "operation", "de", "Aktualisieren"),
        ("delete", "operation", "en", "Delete"),
        ("delete", "operation", "de", "Loeschen"),
        ("search", "operation", "en", "Search"),
        ("search", "operation", "de", "Suchen"),
        ("status", "operation", "en", "Show status"),
        ("status", "operation", "de", "Status anzeigen"),
        ("start", "operation", "en", "Start"),
        ("start", "operation", "de", "Starten"),
        ("stop", "operation", "en", "Stop"),
        ("stop", "operation", "de", "Stoppen"),
        ("create", "operation", "en", "Create"),
        ("create", "operation", "de", "Erstellen"),
        ("boards", "operation", "en", "Show boards"),
        ("boards", "operation", "de", "Boards anzeigen"),
        ("board", "operation", "en", "Show board"),
        ("board", "operation", "de", "Board anzeigen"),
        ("help", "operation", "en", "Show help"),
        ("help", "operation", "de", "Hilfe anzeigen"),
        ("week", "operation", "en", "Weekly view"),
        ("week", "operation", "de", "Wochenansicht"),
        ("drafts", "operation", "en", "Show drafts"),
        ("drafts", "operation", "de", "Entwuerfe anzeigen"),
        ("info", "operation", "en", "Show info"),
        ("info", "operation", "de", "Info anzeigen"),

        # === SharedMemory (namespace: shared_memory) ===
        ("current_task", "shared_memory", "en", "Current task"),
        ("current_task", "shared_memory", "de", "Aktuelle Aufgabe"),
        ("generate_context", "shared_memory", "en", "Generate context"),
        ("generate_context", "shared_memory", "de", "Kontext generieren"),
        ("decay", "shared_memory", "en", "Memory decay"),
        ("decay", "shared_memory", "de", "Gedaechtnis-Verfall"),
        ("changes_since", "shared_memory", "en", "Changes since timestamp"),
        ("changes_since", "shared_memory", "de", "Aenderungen seit Zeitpunkt"),
        ("conflict_resolution", "shared_memory", "en", "Confidence-based conflict resolution"),
        ("conflict_resolution", "shared_memory", "de", "Konfidenz-basierte Konfliktloesung"),
        ("facts", "shared_memory", "en", "Facts (persistent knowledge)"),
        ("facts", "shared_memory", "de", "Fakten (persistentes Wissen)"),
        ("lessons", "shared_memory", "en", "Lessons learned"),
        ("lessons", "shared_memory", "de", "Gelerntes"),
        ("working", "shared_memory", "en", "Working memory (session notes)"),
        ("working", "shared_memory", "de", "Arbeitsspeicher (Sitzungsnotizen)"),

        # === Scheduler (namespace: scheduler) ===
        ("scheduler_jobs", "scheduler", "en", "Scheduled jobs"),
        ("scheduler_jobs", "scheduler", "de", "Geplante Auftraege"),
        ("scheduler_runs", "scheduler", "en", "Job execution history"),
        ("scheduler_runs", "scheduler", "de", "Ausfuehrungshistorie"),
        ("job_type_chain", "scheduler", "en", "Chain job type"),
        ("job_type_chain", "scheduler", "de", "Ketten-Auftragstyp"),
        ("job_type_handler", "scheduler", "en", "Handler job type"),
        ("job_type_handler", "scheduler", "de", "Handler-Auftragstyp"),
        ("job_type_shell", "scheduler", "en", "Shell job type"),
        ("job_type_shell", "scheduler", "de", "Shell-Auftragstyp"),

        # === Prompt-System (namespace: prompt) ===
        ("template", "prompt", "en", "Prompt template"),
        ("template", "prompt", "de", "Prompt-Vorlage"),
        ("version", "prompt", "en", "Template version"),
        ("version", "prompt", "de", "Vorlagen-Version"),
        ("board", "prompt", "en", "Prompt board (collection)"),
        ("board", "prompt", "de", "Prompt-Board (Sammlung)"),
        ("bach_url", "prompt", "en", "bach:// URL reference"),
        ("bach_url", "prompt", "de", "bach:// URL-Referenz"),

        # === USMC (namespace: usmc) ===
        ("bridge", "usmc", "en", "USMC Bridge (cross-agent sync)"),
        ("bridge", "usmc", "de", "USMC-Bruecke (Cross-Agent-Sync)"),
        ("sync_to", "usmc", "en", "Sync BACH to USMC"),
        ("sync_to", "usmc", "de", "BACH nach USMC synchronisieren"),
        ("sync_from", "usmc", "en", "Sync USMC to BACH"),
        ("sync_from", "usmc", "de", "USMC nach BACH synchronisieren"),

        # === System-Meldungen (namespace: system) ===
        ("startup", "system", "en", "System startup"),
        ("startup", "system", "de", "Systemstart"),
        ("shutdown", "system", "en", "System shutdown"),
        ("shutdown", "system", "de", "Systemabschaltung"),
        ("no_results", "system", "en", "No results found"),
        ("no_results", "system", "de", "Keine Ergebnisse gefunden"),
        ("success", "system", "en", "Operation successful"),
        ("success", "system", "de", "Vorgang erfolgreich"),
        ("error", "system", "en", "An error occurred"),
        ("error", "system", "de", "Ein Fehler ist aufgetreten"),
        ("not_found", "system", "en", "Not found"),
        ("not_found", "system", "de", "Nicht gefunden"),
        ("saved", "system", "en", "Saved successfully"),
        ("saved", "system", "de", "Erfolgreich gespeichert"),
        ("deleted", "system", "en", "Deleted successfully"),
        ("deleted", "system", "de", "Erfolgreich geloescht"),
        ("updated", "system", "en", "Updated successfully"),
        ("updated", "system", "de", "Erfolgreich aktualisiert"),

        # === Agent-Launcher (namespace: agent) ===
        ("boss_agents", "agent", "en", "Boss agents"),
        ("boss_agents", "agent", "de", "Boss-Agenten"),
        ("expert_agents", "agent", "en", "Expert agents"),
        ("expert_agents", "agent", "de", "Experten-Agenten"),
        ("agent_started", "agent", "en", "Agent started"),
        ("agent_started", "agent", "de", "Agent gestartet"),
        ("agent_stopped", "agent", "en", "Agent stopped"),
        ("agent_stopped", "agent", "de", "Agent gestoppt"),
        ("pid_tracking", "agent", "en", "Process ID tracking"),
        ("pid_tracking", "agent", "de", "Prozess-ID-Tracking"),

        # === Chain (namespace: chain) ===
        ("toolchain", "chain", "en", "Toolchain (DB-based)"),
        ("toolchain", "chain", "de", "Toolchain (DB-basiert)"),
        ("llmauto_chain", "chain", "en", "LLMauto chain (file-based)"),
        ("llmauto_chain", "chain", "de", "LLMauto-Kette (dateibasiert)"),
        ("chain_created", "chain", "en", "Chain created"),
        ("chain_created", "chain", "de", "Kette erstellt"),
        ("chain_started", "chain", "en", "Chain started"),
        ("chain_started", "chain", "de", "Kette gestartet"),
        ("chain_stopped", "chain", "en", "Chain stopped"),
        ("chain_stopped", "chain", "de", "Kette gestoppt"),
    ]

    for key, ns, lang, val in translations:
        cur.execute(
            "INSERT OR REPLACE INTO languages_translations "
            "(key, namespace, language, value, is_verified, source) "
            "VALUES (?, ?, ?, ?, 1, 'butternut')",
            (key, ns, lang, val)
        )

    conn.commit()
    count = cur.execute("SELECT COUNT(*) FROM languages_translations").fetchone()[0]
    print(f"{len(translations)} Uebersetzungen eingefuegt (Gesamt: {count})")
    conn.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        db_path = sys.argv[1]
    else:
        db_path = os.path.join(os.path.dirname(__file__), "..", "..", "bach.db")
    migrate(db_path)
