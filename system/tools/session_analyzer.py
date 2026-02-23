#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Tool: session_analyzer
Version: 1.0.0
Author: BACH Team
Created: 2026-02-04
Updated: 2026-02-04
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version session_analyzer

Description:
    [Beschreibung hinzufügen]

Usage:
    python session_analyzer.py [args]
"""

__version__ = "1.0.0"
__author__ = "BACH Team"

import sys
import sqlite3
from pathlib import Path
from datetime import datetime

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

def analyze_sessions():
    db_path = DB_PATH
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    cur.execute("SELECT id, summary, continuation_context FROM memory_sessions WHERE is_compressed = 0 OR is_compressed IS NULL")
    rows = cur.fetchall()
    
    total = len(rows)
    with_content = [r for r in rows if r[1] or r[2]]
    
    print(f"Total uncompressed sessions: {total}")
    print(f"Sessions with content: {len(with_content)}")
    
    if total == 0:
        print("Keine Sessions zum Komprimieren.")
        conn.close()
        return

    # 1. Zusammenfassung erstellen
    summary = f"KOMPRIMIERUNG {total} SESSIONS (Stand {datetime.now().strftime('%Y-%m-%d')})\n\n"
    summary += "Zusammenfassung der Meilensteine:\n"
    # Wichtigste Meilensteine (ersten 20 mit content)
    for r in with_content[:20]:
        title = r[1].split('.')[0] if r[1] else "Fortsetzung"
        summary += f"- {title}\n"
    
    # 2. In memory_context speichern
    now = datetime.now().isoformat()
    # Sicherstellen dass Tabelle existiert/geladen ist
    cur.execute("CREATE TABLE IF NOT EXISTS memory_context (id INTEGER PRIMARY KEY, source_name TEXT UNIQUE, weight INTEGER, injection_template TEXT, updated_at TEXT)")
    
    cur.execute("""
        INSERT OR REPLACE INTO memory_context 
        (source_name, weight, injection_template, updated_at)
        VALUES (?, ?, ?, ?)
    """, (f"CONSOL_BATCH_{datetime.now().strftime('%Y%j %H%M')}", 8, summary, now))
    
    # 3. Als komprimiert markieren
    cur.execute("UPDATE memory_sessions SET is_compressed = 1 WHERE is_compressed = 0 OR is_compressed IS NULL")
    
    conn.commit()
    print(f"[OK] {total} Sessions komprimiert und in Kontext gespeichert.")
    conn.close()

if __name__ == "__main__":
    analyze_sessions()
