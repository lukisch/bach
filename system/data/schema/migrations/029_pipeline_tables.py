#!/usr/bin/env python3
"""Migration 029: Pipeline-Tabellen upgraden (SQ011).

Fuegt fehlende Spalten zu bestehenden pipeline_configs/pipeline_runs hinzu
und erstellt Indizes.
"""

import sqlite3
import sys
from pathlib import Path


def _column_exists(conn, table, column):
    """Prueft ob eine Spalte in der Tabelle existiert."""
    cols = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return any(c[1] == column for c in cols)


def _add_column_if_missing(conn, table, column, definition):
    """Fuegt Spalte hinzu falls sie noch nicht existiert."""
    if not _column_exists(conn, table, column):
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")
        print(f"  + {table}.{column}")
        return True
    return False


def migrate(db_path=None):
    """Hauptmigration."""
    if db_path is None:
        db_path = str(Path(__file__).parent.parent.parent / "bach.db")

    conn = sqlite3.connect(db_path)
    print("Migration 029: Pipeline-Tabellen (SQ011)")

    # 1. SQL-Teil ausfuehren (CREATE TABLE IF NOT EXISTS + Indizes)
    sql_file = Path(__file__).with_suffix(".sql")
    if sql_file.exists():
        sql = sql_file.read_text(encoding="utf-8")
        conn.executescript(sql)
        print("  SQL-Schema angewendet")

    # 2. Fehlende Spalten in pipeline_configs nachruesten
    added = 0
    added += _add_column_if_missing(conn, "pipeline_configs", "is_active", "INTEGER DEFAULT 1")
    added += _add_column_if_missing(conn, "pipeline_configs", "dist_type", "INTEGER DEFAULT 0")
    # SQLite erlaubt kein ALTER TABLE ADD COLUMN mit nicht-konstantem Default
    added += _add_column_if_missing(conn, "pipeline_configs", "created_at", "TEXT")

    # 3. Fehlende Spalten in pipeline_runs nachruesten
    added += _add_column_if_missing(conn, "pipeline_runs", "dist_type", "INTEGER DEFAULT 0")

    # 4. Index auf is_active (jetzt sicher vorhanden)
    try:
        conn.execute("CREATE INDEX IF NOT EXISTS idx_pc_active ON pipeline_configs(is_active)")
    except sqlite3.OperationalError:
        pass  # Index existiert bereits

    conn.commit()

    if added:
        print(f"  {added} Spalte(n) hinzugefuegt")
    else:
        print("  Alle Spalten bereits vorhanden")

    # Verifizierung
    tables = conn.execute("SELECT name FROM sqlite_master WHERE name LIKE 'pipeline%' AND type='table'").fetchall()
    print(f"  Tabellen: {[t[0] for t in tables]}")

    conn.close()
    print("  OK")


if __name__ == "__main__":
    db = sys.argv[1] if len(sys.argv) > 1 else None
    migrate(db)
