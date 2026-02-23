#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (c) 2026 Lukas Geiger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
Migration 009: Agent Instances - Python Handler
================================================

SQLite unterstützt kein ALTER TABLE ... ADD COLUMN IF NOT EXISTS.
Daher müssen wir die Spalten dynamisch hinzufügen.

Wird automatisch von db.run_migrations() aufgerufen.
"""

import sqlite3
from pathlib import Path


def migrate(db_path: Path) -> bool:
    """
    Führt Migration 009 aus.

    Args:
        db_path: Pfad zur bach.db

    Returns:
        True wenn erfolgreich
    """
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    try:
        # Prüfe welche Spalten bereits existieren
        cursor.execute("PRAGMA table_info(tasks)")
        existing_columns = {row[1] for row in cursor.fetchall()}

        # Füge fehlende Spalten hinzu
        if 'source' not in existing_columns:
            cursor.execute("ALTER TABLE tasks ADD COLUMN source TEXT")
            print("[Migration 009] Spalte 'source' zu tasks hinzugefügt")

        if 'assigned_agent' not in existing_columns:
            cursor.execute("ALTER TABLE tasks ADD COLUMN assigned_agent TEXT")
            print("[Migration 009] Spalte 'assigned_agent' zu tasks hinzugefügt")

        conn.commit()
        return True

    except Exception as e:
        print(f"[Migration 009] Fehler: {e}")
        conn.rollback()
        return False

    finally:
        conn.close()


if __name__ == "__main__":
    # Test-Modus: Direkt ausführen
    import sys
    if len(sys.argv) > 1:
        db_path = Path(sys.argv[1])
        success = migrate(db_path)
        sys.exit(0 if success else 1)
    else:
        print("Usage: python 009_agent_instances.py <path_to_bach.db>")
        sys.exit(1)
