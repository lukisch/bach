#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TOWER_OF_BABEL: Translate 273 tool descriptions from DE to EN
and insert as new rows with language='en' into bach.db tools table.

Prerequisite: UNIQUE constraint must be (name, language) not just (name).
This script handles the schema migration if needed.
"""

import sqlite3
import json
import sys
from pathlib import Path
from datetime import datetime

BACH_ROOT = Path(__file__).parent.parent.parent
DB = BACH_ROOT / "data" / "bach.db"
JSON_FILE = Path("/tmp/tower_tools_de.json")


def translate_desc(desc):
    """Translate description to English. Keep technical terms as-is."""
    if desc is None:
        return None

    translations = {
        "Registriert alle Skills aus skills/ in bach.db":
            "Registers all skills from skills/ into bach.db",
        "Generiert nutzerfreundlichen Skills-Report in user/SKILLS_REPORT.md":
            "Generates user-friendly skills report in user/SKILLS_REPORT.md",
        "Auto-Logger - Protokolliert automatisch alle Aktionen":
            "Auto-Logger - Automatically logs all actions",
        "Injector System - Automatische Hilfe und Kontext":
            "Injector System - Automatic help and context",
        "F\u00fcgen Sie das Hauptverzeichnis zum Pfad hinzu, um Module zu importieren":
            "Add main directory to path for module imports",
        "Problems First - Automatische Fehler-Erkennung":
            "Problems First - Automatic error detection",
        "boot_checks Tabelle erstellen - KRITISCH f\u00fcr Pre-Prompt Checks":
            "Create boot_checks table - CRITICAL for pre-prompt checks",
        "OllamaClient - REST-API Wrapper fuer lokale Ollama-Instanz":
            "OllamaClient - REST API wrapper for local Ollama instance",
        "Boot Integration f\u00fcr Tool Registry":
            "Boot integration for Tool Registry",
        "BACH_STREAM Selbsterfahrungsprotokoll - Test Runner & Query Tool":
            "BACH_STREAM Self-Experience Protocol - Test Runner & Query Tool",
        "Time System - Unified Zeit-Funktionen fuer BACH":
            "Time System - Unified time functions for BACH",
        "encoding_fix.py - Zentraler Encoding-Sanitizer fuer BACH =========================================================":
            "encoding_fix.py - Central encoding sanitizer for BACH",
        "Generiert Keywords aus Titel und trigger_words JSON.":
            "Generates keywords from title and trigger_words JSON.",
        "Extrahiert Beschreibung und Usage aus einem Python Script.":
            "Extracts description and usage from a Python script.",
        "Extrahiert Titel und Ziel aus einer Workflow-Datei.":
            "Extracts title and goal from a workflow file.",
        "AI-kompatible Software Analyse":
            "AI-compatible software analysis",
        "Analyse echter AI-kompatibler Tools (nur EXE/CMD/BAT)":
            "Analysis of real AI-compatible tools (EXE/CMD/BAT only)",
        "Extrahiert Metadaten aus SKILL.md oder manifest.json.":
            "Extracts metadata from SKILL.md or manifest.json.",
        "Pfade setzen": "Set paths",
        "Pfad zu BACH root (parent von tools)":
            "Path to BACH root (parent of tools)",
        "Pfade Setup": "Path setup",
        "Pfade": "Paths",
        "llmauto.core.config -- Konfigurationsmanagement":
            "llmauto.core.config -- Configuration management",
        "llmauto.core.state -- State-Management":
            "llmauto.core.state -- State management",
        "llmauto.modes.chain -- Ketten-Modus (Marble-Run)":
            "llmauto.modes.chain -- Chain mode (Marble-Run)",
    }

    if desc in translations:
        return translations[desc]

    # Already English or code snippets -- keep as-is
    return desc


def check_and_migrate_schema(conn):
    """Ensure UNIQUE constraint is (name, language), not just (name)."""
    cur = conn.cursor()
    cur.execute("PRAGMA index_list(tools)")
    indexes = cur.fetchall()

    for idx in indexes:
        idx_name = idx[1]
        cur.execute(f"PRAGMA index_info({idx_name})")
        cols = [r[2] for r in cur.fetchall()]
        if cols == ['name'] and idx[3] == 'u':  # unique on name only
            print("Migrating schema: UNIQUE(name) -> UNIQUE(name, language)...")
            cur.executescript("""
                BEGIN;
                CREATE TABLE tools_new (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    category TEXT,
                    path TEXT,
                    endpoint TEXT,
                    command TEXT,
                    description TEXT,
                    version TEXT,
                    capabilities TEXT,
                    use_for TEXT,
                    is_available INTEGER DEFAULT 1,
                    last_check TEXT,
                    error_count INTEGER DEFAULT 0,
                    tokens_saved_percent INTEGER,
                    speed TEXT,
                    created_at TEXT,
                    updated_at TEXT,
                    dist_type INTEGER DEFAULT 2,
                    template_content TEXT,
                    content TEXT,
                    content_hash TEXT,
                    language TEXT DEFAULT 'de',
                    UNIQUE(name, language)
                );
                INSERT INTO tools_new SELECT * FROM tools;
                DROP TABLE tools;
                ALTER TABLE tools_new RENAME TO tools;
                COMMIT;
            """)
            print("Schema migration complete.")
            return True
    return False


def main():
    if not JSON_FILE.exists():
        print(f"ERROR: {JSON_FILE} not found")
        sys.exit(1)

    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        tools = json.load(f)
    print(f"Loaded {len(tools)} tools from {JSON_FILE}")

    conn = sqlite3.connect(str(DB))
    cur = conn.cursor()

    # Check current state
    cur.execute("SELECT language, COUNT(*) FROM tools GROUP BY language")
    print(f"Before: {cur.fetchall()}")

    # Check if EN already exist
    cur.execute("SELECT COUNT(*) FROM tools WHERE language='en'")
    en_count = cur.fetchone()[0]
    if en_count > 0:
        print(f"Already {en_count} EN tools in DB. Aborting to prevent duplicates.")
        conn.close()
        return

    # Migrate schema if needed
    check_and_migrate_schema(conn)

    # Insert EN translations
    inserted = 0
    skipped = 0
    errors = 0
    now = datetime.now().isoformat()

    for tool in tools:
        tid = tool['id']
        en_desc = translate_desc(tool['desc'])

        try:
            cur.execute("""
                INSERT INTO tools (name, type, category, path, endpoint, command,
                    description, version, capabilities, use_for, is_available,
                    last_check, error_count, tokens_saved_percent, speed,
                    created_at, updated_at, dist_type, template_content,
                    content, content_hash, language)
                SELECT name, type, category, path, endpoint, command,
                    ?, version, capabilities, use_for, is_available,
                    last_check, error_count, tokens_saved_percent, speed,
                    created_at, ?, dist_type, template_content,
                    content, content_hash, 'en'
                FROM tools WHERE id = ? AND language = 'de'
            """, (en_desc, now, tid))

            if cur.rowcount > 0:
                inserted += 1
            else:
                skipped += 1
                print(f"  SKIP: id={tid} name={tool['name']} - no DE row with that id")
        except Exception as e:
            errors += 1
            print(f"  ERROR: id={tid} name={tool['name']} - {e}")

    conn.commit()

    # Final count
    cur.execute("SELECT language, COUNT(*) FROM tools GROUP BY language")
    final = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM tools")
    total = cur.fetchone()[0]

    print(f"\nResult: inserted={inserted}, skipped={skipped}, errors={errors}")
    print(f"Final counts by language: {final}")
    print(f"Total rows in tools: {total}")

    conn.close()


if __name__ == "__main__":
    main()
