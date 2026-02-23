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
Phase 2: dist_ Tabellen -> unpraefixierte Tabellen in bach.db
Damit distribution_system.py direkt bach.db nutzen kann.
"""
import sqlite3
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
BACH_DB = BASE / "data" / "bach.db"

DIST_TABLES = [
    'dist_tiers', 'dist_tier_patterns', 'dist_filesystem_entries',
    'dist_file_versions', 'dist_instance_identity', 'dist_mode_transitions',
    'dist_snapshots', 'dist_snapshot_files', 'dist_releases'
]

def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    conn = sqlite3.connect(str(BACH_DB))
    cursor = conn.cursor()

    print("Phase 2: dist_ -> unpraefixiert")
    print("=" * 40)

    for dist_name in DIST_TABLES:
        clean_name = dist_name.replace('dist_', '', 1)

        # Pruefen ob dist_-Tabelle existiert
        exists_dist = cursor.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?", (dist_name,)
        ).fetchone()[0]
        if not exists_dist:
            print(f"  [SKIP] {dist_name} existiert nicht")
            continue

        # Pruefen ob Ziel schon existiert
        exists_clean = cursor.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?", (clean_name,)
        ).fetchone()[0]

        if exists_clean:
            # Daten ruebermergen falls dist_ Daten hat
            count_dist = cursor.execute(f"SELECT COUNT(*) FROM [{dist_name}]").fetchone()[0]
            count_clean = cursor.execute(f"SELECT COUNT(*) FROM [{clean_name}]").fetchone()[0]
            if count_dist > 0 and count_clean == 0:
                cols = [row[1] for row in cursor.execute(f"PRAGMA table_info([{dist_name}])").fetchall()]
                col_str = ','.join([f'[{c}]' for c in cols])
                cursor.execute(f"INSERT OR IGNORE INTO [{clean_name}] ({col_str}) SELECT {col_str} FROM [{dist_name}]")
                print(f"  [MERGE] {dist_name} -> {clean_name}: {count_dist} Eintraege")
            else:
                print(f"  [SKIP] {clean_name} existiert mit {count_clean} Eintraegen")
        else:
            # Tabelle umbenennen
            cursor.execute(f"ALTER TABLE [{dist_name}] RENAME TO [{clean_name}]")
            count = cursor.execute(f"SELECT COUNT(*) FROM [{clean_name}]").fetchone()[0]
            print(f"  [RENAME] {dist_name} -> {clean_name} ({count} Eintraege)")
            continue

        # dist_-Tabelle droppen
        cursor.execute(f"DROP TABLE IF EXISTS [{dist_name}]")
        print(f"  [DROP] {dist_name}")

    conn.commit()

    # Verifizierung
    print("\nVerifizierung:")
    for dist_name in DIST_TABLES:
        clean_name = dist_name.replace('dist_', '', 1)
        exists = cursor.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?", (clean_name,)
        ).fetchone()[0]
        if exists:
            count = cursor.execute(f"SELECT COUNT(*) FROM [{clean_name}]").fetchone()[0]
            print(f"  [OK] {clean_name}: {count}")

    total = cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
    print(f"\nbach.db Tabellen: {total}")
    conn.close()


if __name__ == "__main__":
    main()
