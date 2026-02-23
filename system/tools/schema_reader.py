#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Tool: schema_reader
Version: 1.0.0
Author: BACH Team
Created: 2026-02-04
Updated: 2026-02-04
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version schema_reader

Description:
    [Beschreibung hinzufügen]

Usage:
    python schema_reader.py [args]
"""

__version__ = "1.0.0"
__author__ = "BACH Team"

import sys
import sqlite3
from pathlib import Path

# Pfad-Setup für Standalone-Ausführung
script_dir = Path(__file__).resolve().parent
system_dir = script_dir.parent
if str(system_dir) not in sys.path:
    sys.path.insert(0, str(system_dir))

# DB-Pfad aus zentraler Konfiguration
try:
    from hub.bach_paths import BACH_DB
    DB_PATH = BACH_DB
except ImportError:
    # Fallback für ältere Setups
    DB_PATH = system_dir / "data" / "bach.db"

def get_schema(table_name="tasks"):
    db_path = DB_PATH
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(f"SELECT sql FROM sqlite_master WHERE name='{table_name}'")
    row = cur.fetchone()
    if row:
        print(row[0])
    else:
        print(f"Tabelle {table_name} nicht gefunden.")
    conn.close()

if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else "tasks"
    get_schema(t)
