#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration 011: dist_type Spalten nachtragen (HQ1-A)
====================================================

Traegt die fehlende dist_type Spalte in drei Tabellen nach,
fuer die schema_distribution.sql das Schema definiert hat
(ALTER TABLE wurde nie angewandt):

  - system_config:       dist_type DEFAULT 2 (CORE)
  - files_truth:         dist_type DEFAULT 1 (TEMPLATE)
  - automation_triggers: dist_type DEFAULT 2 (CORE)

Hinweis: Das Schema-SQL referenziert 'files_directory_truth',
die echte Tabelle heisst aber 'files_truth'.

Wird automatisch von db.run_migrations() aufgerufen.
"""

import sqlite3
from pathlib import Path


def migrate(db_path: Path) -> bool:
    """
    Fuehrt Migration 011 aus.

    Args:
        db_path: Pfad zur bach.db

    Returns:
        True wenn erfolgreich
    """
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    try:
        # system_config: CORE (DEFAULT 2)
        cursor.execute("PRAGMA table_info(system_config)")
        existing = {row[1] for row in cursor.fetchall()}
        if 'dist_type' not in existing:
            cursor.execute(
                "ALTER TABLE system_config ADD COLUMN dist_type INTEGER DEFAULT 2"
            )
            print("[Migration 011] dist_type zu system_config hinzugefuegt (DEFAULT 2=CORE)")
        else:
            print("[Migration 011] system_config: dist_type bereits vorhanden")

        # files_truth: TEMPLATE (DEFAULT 1)
        cursor.execute("PRAGMA table_info(files_truth)")
        existing = {row[1] for row in cursor.fetchall()}
        if 'dist_type' not in existing:
            cursor.execute(
                "ALTER TABLE files_truth ADD COLUMN dist_type INTEGER DEFAULT 1"
            )
            print("[Migration 011] dist_type zu files_truth hinzugefuegt (DEFAULT 1=TEMPLATE)")
        else:
            print("[Migration 011] files_truth: dist_type bereits vorhanden")

        # automation_triggers: CORE (DEFAULT 2)
        cursor.execute("PRAGMA table_info(automation_triggers)")
        existing = {row[1] for row in cursor.fetchall()}
        if 'dist_type' not in existing:
            cursor.execute(
                "ALTER TABLE automation_triggers ADD COLUMN dist_type INTEGER DEFAULT 2"
            )
            print("[Migration 011] dist_type zu automation_triggers hinzugefuegt (DEFAULT 2=CORE)")
        else:
            print("[Migration 011] automation_triggers: dist_type bereits vorhanden")

        conn.commit()
        print("[Migration 011] Erfolgreich abgeschlossen.")
        return True

    except Exception as e:
        print(f"[Migration 011] Fehler: {e}")
        conn.rollback()
        return False

    finally:
        conn.close()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        db_path = Path(sys.argv[1])
        success = migrate(db_path)
        sys.exit(0 if success else 1)
    else:
        print("Usage: python 011_dist_type_columns.py <path_to_bach.db>")
        sys.exit(1)
