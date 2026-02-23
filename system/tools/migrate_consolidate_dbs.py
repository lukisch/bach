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
DB-Konsolidierung: archive.db + registry.db → bach.db
=====================================================
Task 980: Drei DBs zu einer zusammenführen.

Schritte:
1. archive.db Tabellen in bach.db anlegen + Daten migrieren
2. registry.db Tabellen mit dist_ Prefix in bach.db anlegen + Daten migrieren
3. Code-Referenzen aktualisieren (manuell nach Script)

Backup: Wurde VOR Ausführung erstellt (userdata_2026-02-16_163216.zip)
"""
import sqlite3
import sys
import os
from pathlib import Path

# BACH base path
BASE = Path(__file__).resolve().parent.parent
BACH_DB = BASE / "data" / "bach.db"
ARCHIVE_DB = BASE / "data" / "archive.db"
REGISTRY_DB = BASE / "tools" / "data" / "registry.db"


def migrate_archive():
    """Migriert archive.db Tabellen nach bach.db."""
    print("=== SCHRITT 1: archive.db → bach.db ===")

    if not ARCHIVE_DB.exists():
        print("  [SKIP] archive.db nicht gefunden")
        return

    conn = sqlite3.connect(str(BACH_DB))
    archive_conn = sqlite3.connect(str(ARCHIVE_DB))

    cursor = conn.cursor()
    archive_cursor = archive_conn.cursor()

    schemas = archive_cursor.execute(
        "SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    ).fetchall()

    for name, sql in schemas:
        if not sql:
            continue
        exists = cursor.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?", (name,)
        ).fetchone()[0]

        if exists:
            print(f"  [SKIP] {name} existiert bereits in bach.db")
        else:
            try:
                cursor.execute(sql)
                print(f"  [OK] {name} erstellt")
            except Exception as e:
                print(f"  [ERR] {name}: {e}")

        # Daten migrieren
        count = archive_cursor.execute(f'SELECT COUNT(*) FROM [{name}]').fetchone()[0]
        if count > 0:
            rows = archive_cursor.execute(f'SELECT * FROM [{name}]').fetchall()
            cols = [d[0] for d in archive_cursor.description]
            placeholders = ','.join(['?' for _ in cols])
            col_names = ','.join([f'[{c}]' for c in cols])
            migrated = 0
            for row in rows:
                try:
                    cursor.execute(
                        f'INSERT OR IGNORE INTO [{name}] ({col_names}) VALUES ({placeholders})', row
                    )
                    migrated += 1
                except Exception as e:
                    print(f"  [WARN] {name} row: {e}")
            print(f"  [DATA] {name}: {migrated}/{count} Eintraege migriert")

    conn.commit()
    archive_conn.close()
    conn.close()


def migrate_registry():
    """Migriert registry.db Tabellen nach bach.db mit dist_ Prefix."""
    print("\n=== SCHRITT 2: registry.db → bach.db (dist_ Prefix) ===")

    if not REGISTRY_DB.exists():
        print("  [SKIP] registry.db nicht gefunden")
        return

    conn = sqlite3.connect(str(BACH_DB))
    reg_conn = sqlite3.connect(str(REGISTRY_DB))

    cursor = conn.cursor()
    reg_cursor = reg_conn.cursor()

    schemas = reg_cursor.execute(
        "SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    ).fetchall()

    for name, sql in schemas:
        if not sql:
            continue
        new_name = f"dist_{name}"

        exists = cursor.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?", (new_name,)
        ).fetchone()[0]

        if exists:
            print(f"  [SKIP] {new_name} existiert bereits")
        else:
            # Tabellenname im CREATE Statement ersetzen
            new_sql = sql.replace(f"CREATE TABLE {name}", f"CREATE TABLE {new_name}", 1)
            new_sql = new_sql.replace(f'CREATE TABLE "{name}"', f'CREATE TABLE "{new_name}"', 1)
            try:
                cursor.execute(new_sql)
                print(f"  [OK] {new_name} erstellt (aus {name})")
            except Exception as e:
                print(f"  [ERR] {new_name}: {e}")

        # Daten migrieren
        count = reg_cursor.execute(f'SELECT COUNT(*) FROM [{name}]').fetchone()[0]
        if count > 0:
            rows = reg_cursor.execute(f'SELECT * FROM [{name}]').fetchall()
            cols = [d[0] for d in reg_cursor.description]
            placeholders = ','.join(['?' for _ in cols])
            col_names = ','.join([f'[{c}]' for c in cols])
            migrated = 0
            for row in rows:
                try:
                    cursor.execute(
                        f'INSERT OR IGNORE INTO [{new_name}] ({col_names}) VALUES ({placeholders})', row
                    )
                    migrated += 1
                except Exception as e:
                    pass
            print(f"  [DATA] {new_name}: {migrated}/{count} Eintraege migriert")

    conn.commit()
    reg_conn.close()
    conn.close()


def verify():
    """Verifiziert die Migration."""
    print("\n=== VERIFIZIERUNG ===")
    conn = sqlite3.connect(str(BACH_DB))
    cursor = conn.cursor()

    # Archive-Tabellen pruefen
    for t in ['archive_meta', 'archived_tasks', 'archived_sessions', 'archived_memory', 'archived_files', 'restore_log']:
        exists = cursor.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?", (t,)
        ).fetchone()[0]
        count = cursor.execute(f"SELECT COUNT(*) FROM [{t}]").fetchone()[0] if exists else -1
        status = "OK" if exists else "FEHLT"
        print(f"  [{status}] {t}: {count} Eintraege")

    # Registry-Tabellen pruefen
    for t in ['dist_tiers', 'dist_tier_patterns', 'dist_filesystem_entries', 'dist_file_versions',
              'dist_instance_identity', 'dist_mode_transitions', 'dist_snapshots', 'dist_snapshot_files', 'dist_releases']:
        exists = cursor.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?", (t,)
        ).fetchone()[0]
        count = cursor.execute(f"SELECT COUNT(*) FROM [{t}]").fetchone()[0] if exists else -1
        status = "OK" if exists else "FEHLT"
        print(f"  [{status}] {t}: {count} Eintraege")

    total = cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
    print(f"\n  bach.db Tabellen gesamt: {total}")
    conn.close()


if __name__ == "__main__":
    # UTF-8 fix for Windows
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

    print("DB-Konsolidierung: archive.db + registry.db -> bach.db")
    print("=" * 55)

    if not BACH_DB.exists():
        print("FEHLER: bach.db nicht gefunden!")
        sys.exit(1)

    migrate_archive()
    migrate_registry()
    verify()

    print("\n=== FERTIG ===")
    print("Naechste Schritte (manuell):")
    print("  1. bach_paths.py: ARCHIVE_DB Referenz auf bach.db aendern")
    print("  2. distribution_system.py: DB_FILE auf bach.db aendern (dist_ Prefix)")
    print("  3. archive.db + registry.db loeschen")
