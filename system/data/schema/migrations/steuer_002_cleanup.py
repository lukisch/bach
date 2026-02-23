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
Tool: steuer_002_cleanup
Version: 1.0.0
Author: Claude
Created: 2026-02-06
Updated: 2026-02-06
Anthropic-Compatible: True

Description:
    Migration script to clean up steuer DB redundancies.

    Removes:
    - steuer_dokumente.belegnr (100% identical to id)
    - steuer_posten.belegnr (duplicate of dokument_id, after backfill)
    - steuer_posten.posten_id_str (computed from dokument_id + postennr)

    Keeps:
    - steuer_posten.dateiname (deferred - too many JOINs needed)

    Makes:
    - steuer_posten.dokument_id NOT NULL (after backfilling from belegnr)

    Usage:
        python steuer_002_cleanup.py              # Execute migration
        python steuer_002_cleanup.py --dry-run     # Show what would happen
        python steuer_002_cleanup.py --info         # Show current state
"""
__version__ = "1.0.0"

import sys
import os
import shutil
import sqlite3
from pathlib import Path
from datetime import datetime


# === PFADE ===
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent  # system/data/
DB_PATH = DATA_DIR / "bach.db"


def get_sqlite_version():
    """Returns SQLite version as tuple, e.g. (3, 45, 0)."""
    conn = sqlite3.connect(":memory:")
    ver = conn.execute("SELECT sqlite_version()").fetchone()[0]
    conn.close()
    parts = ver.split(".")
    return tuple(int(p) for p in parts), ver


def supports_drop_column():
    """SQLite >= 3.35.0 supports ALTER TABLE DROP COLUMN."""
    ver_tuple, _ = get_sqlite_version()
    return ver_tuple >= (3, 35, 0)


def get_table_columns(conn, table_name):
    """Returns list of column names for a table."""
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return [r[1] for r in rows]


def get_row_count(conn, table_name):
    """Returns row count for a table."""
    return conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]


def check_current_state(conn):
    """Analyzes current DB state and returns info dict."""
    info = {}

    # Check if tables exist
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'steuer_%'"
    ).fetchall()
    info["tables"] = [t[0] for t in tables]

    if "steuer_dokumente" not in info["tables"]:
        info["error"] = "steuer_dokumente table not found"
        return info
    if "steuer_posten" not in info["tables"]:
        info["error"] = "steuer_posten table not found"
        return info

    # Column info
    info["dok_columns"] = get_table_columns(conn, "steuer_dokumente")
    info["posten_columns"] = get_table_columns(conn, "steuer_posten")

    # Row counts
    info["dok_count"] = get_row_count(conn, "steuer_dokumente")
    info["posten_count"] = get_row_count(conn, "steuer_posten")

    # Check belegnr == id in steuer_dokumente
    if "belegnr" in info["dok_columns"]:
        mismatches = conn.execute("""
            SELECT COUNT(*) FROM steuer_dokumente WHERE belegnr != id
        """).fetchone()[0]
        info["dok_belegnr_mismatches"] = mismatches
    else:
        info["dok_belegnr_already_removed"] = True

    # Check steuer_posten.dokument_id NULLs
    if "dokument_id" in info["posten_columns"]:
        null_count = conn.execute("""
            SELECT COUNT(*) FROM steuer_posten WHERE dokument_id IS NULL
        """).fetchone()[0]
        info["posten_dokument_id_nulls"] = null_count

    # Check steuer_posten.belegnr exists
    if "belegnr" in info["posten_columns"]:
        info["posten_has_belegnr"] = True
        # Check if belegnr can fill dokument_id NULLs
        if "dokument_id" in info["posten_columns"]:
            fillable = conn.execute("""
                SELECT COUNT(*) FROM steuer_posten
                WHERE dokument_id IS NULL AND belegnr IS NOT NULL
            """).fetchone()[0]
            info["posten_fillable_from_belegnr"] = fillable
    else:
        info["posten_has_belegnr"] = False

    # Check posten_id_str exists
    info["posten_has_posten_id_str"] = "posten_id_str" in info["posten_columns"]

    return info


def print_info(info):
    """Prints current DB state."""
    print("\n" + "=" * 60)
    print("STEUER DB - CURRENT STATE")
    print("=" * 60)

    if "error" in info:
        print(f"\n  [ERROR] {info['error']}")
        return

    print(f"\n  steuer_dokumente: {info['dok_count']} rows")
    print(f"    Columns: {', '.join(info['dok_columns'])}")
    if info.get("dok_belegnr_already_removed"):
        print("    belegnr: ALREADY REMOVED")
    else:
        mismatches = info.get("dok_belegnr_mismatches", "?")
        print(f"    belegnr != id mismatches: {mismatches}")

    print(f"\n  steuer_posten: {info['posten_count']} rows")
    print(f"    Columns: {', '.join(info['posten_columns'])}")
    print(f"    dokument_id NULLs: {info.get('posten_dokument_id_nulls', '?')}")
    print(f"    has belegnr: {info.get('posten_has_belegnr', False)}")
    print(f"    has posten_id_str: {info.get('posten_has_posten_id_str', False)}")
    if info.get("posten_fillable_from_belegnr"):
        print(f"    fillable from belegnr: {info['posten_fillable_from_belegnr']}")


def backup_db(db_path, dry_run=False):
    """Creates a backup of the database file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak_path = db_path.with_suffix(f".bak_steuer002_{timestamp}")

    if dry_run:
        print(f"\n  [DRY-RUN] Would backup: {db_path.name} -> {bak_path.name}")
        return bak_path

    print(f"\n  Backing up: {db_path.name} -> {bak_path.name}")
    shutil.copy2(db_path, bak_path)

    # Verify backup
    bak_size = bak_path.stat().st_size
    orig_size = db_path.stat().st_size
    if bak_size != orig_size:
        raise RuntimeError(f"Backup size mismatch: {bak_size} != {orig_size}")

    print(f"  Backup OK ({bak_size:,} bytes)")
    return bak_path


def rebuild_table_without_columns(conn, table_name, drop_columns,
                                  column_overrides=None, dry_run=False):
    """
    Rebuilds a table without specified columns (for SQLite < 3.35).
    Also supports changing column definitions via column_overrides.

    Args:
        conn: SQLite connection
        table_name: Name of the table to rebuild
        drop_columns: List of column names to remove
        column_overrides: Dict of {col_name: new_definition} for altering columns
        dry_run: If True, only print what would happen
    """
    column_overrides = column_overrides or {}

    # Get current table schema
    create_sql = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,)
    ).fetchone()[0]

    # Get current columns
    pragma = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    all_columns = [(r[1], r[2], r[3], r[4], r[5]) for r in pragma]
    # (name, type, notnull, default, pk)

    # Filter out dropped columns
    keep_columns = [c for c in all_columns if c[0] not in drop_columns]
    keep_names = [c[0] for c in keep_columns]

    if dry_run:
        removed = [c[0] for c in all_columns if c[0] in drop_columns]
        print(f"    [DRY-RUN] Would rebuild {table_name}:")
        print(f"      Remove columns: {', '.join(removed)}")
        if column_overrides:
            print(f"      Override columns: {', '.join(column_overrides.keys())}")
        print(f"      Keep columns: {', '.join(keep_names)}")
        return

    # Build new CREATE TABLE statement
    col_defs = []
    for name, typ, notnull, default, pk in keep_columns:
        if name in column_overrides:
            col_defs.append(column_overrides[name])
        else:
            parts = [name, typ]
            if pk:
                parts.append("PRIMARY KEY")
            if notnull and not pk:
                parts.append("NOT NULL")
            if default is not None:
                # Wrap in parens if it's an expression (contains function calls etc.)
                if "(" in str(default):
                    parts.append(f"DEFAULT ({default})")
                else:
                    parts.append(f"DEFAULT {default}")
            col_defs.append(" ".join(parts))

    temp_name = f"_temp_{table_name}"

    # Get indexes to recreate later
    indexes = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name=? AND sql IS NOT NULL",
        (table_name,)
    ).fetchall()

    cols_str = ", ".join(keep_names)
    col_defs_str = ",\n        ".join(col_defs)

    # Save and drop all views (they can block DDL operations)
    views = conn.execute(
        "SELECT name, sql FROM sqlite_master WHERE type='view'"
    ).fetchall()
    for vname, vsql in views:
        try:
            conn.execute(f"DROP VIEW IF EXISTS {vname}")
        except Exception:
            pass

    # Execute the rebuild
    try:
        # Create temp table with new schema
        conn.execute(f"""
            CREATE TABLE {temp_name} (
        {col_defs_str}
            )
        """)

        # Copy data
        conn.execute(f"""
            INSERT INTO {temp_name} ({cols_str})
            SELECT {cols_str} FROM {table_name}
        """)

        # Drop old table
        conn.execute(f"DROP TABLE {table_name}")

        # Rename temp to original
        conn.execute(f"ALTER TABLE {temp_name} RENAME TO {table_name}")

        # Recreate indexes (filtering out those referencing dropped columns)
        for idx_row in indexes:
            idx_sql = idx_row[0]
            # Check if index references any dropped column
            skip = False
            for dc in drop_columns:
                if dc in idx_sql:
                    print(f"    Skipping index (references dropped column): {idx_sql[:60]}...")
                    skip = True
                    break
            if not skip:
                try:
                    conn.execute(idx_sql)
                except sqlite3.OperationalError as e:
                    print(f"    Warning: Could not recreate index: {e}")

    except Exception as e:
        raise RuntimeError(f"Table rebuild failed for {table_name}: {e}")
    finally:
        # Recreate all views
        for vname, vsql in views:
            if vsql:
                try:
                    conn.execute(vsql)
                except Exception as e:
                    print(f"    Warning: Could not recreate view {vname}: {e}")


def drop_column_modern(conn, table_name, column_name, dry_run=False):
    """Uses ALTER TABLE DROP COLUMN (SQLite >= 3.35).
    Temporarily drops and recreates views that may block the operation."""
    if dry_run:
        print(f"    [DRY-RUN] Would drop {table_name}.{column_name}")
        return

    # Save and drop all views (they can block ALTER TABLE DROP COLUMN)
    views = conn.execute(
        "SELECT name, sql FROM sqlite_master WHERE type='view'"
    ).fetchall()
    for vname, vsql in views:
        try:
            conn.execute(f"DROP VIEW IF EXISTS {vname}")
        except Exception:
            pass

    try:
        conn.execute(f"ALTER TABLE {table_name} DROP COLUMN {column_name}")
    finally:
        # Recreate all views
        for vname, vsql in views:
            if vsql:
                try:
                    conn.execute(vsql)
                except Exception as e:
                    print(f"    Warning: Could not recreate view {vname}: {e}")


def phase1_backfill(conn, dry_run=False):
    """Phase 1: Backfill NULL dokument_id from belegnr in steuer_posten."""
    print("\n--- Phase 1: Backfill dokument_id NULLs from belegnr ---")

    null_count = conn.execute("""
        SELECT COUNT(*) FROM steuer_posten WHERE dokument_id IS NULL
    """).fetchone()[0]

    fillable = conn.execute("""
        SELECT COUNT(*) FROM steuer_posten
        WHERE dokument_id IS NULL AND belegnr IS NOT NULL
    """).fetchone()[0]

    unfillable = null_count - fillable

    print(f"  dokument_id NULLs: {null_count}")
    print(f"  Fillable from belegnr: {fillable}")
    if unfillable > 0:
        print(f"  WARNING: {unfillable} rows with NULL dokument_id AND NULL belegnr!")

    if null_count == 0:
        print("  Nothing to backfill.")
        return True

    if dry_run:
        print(f"  [DRY-RUN] Would UPDATE {fillable} rows: SET dokument_id = belegnr")
        return True

    conn.execute("""
        UPDATE steuer_posten
        SET dokument_id = belegnr
        WHERE dokument_id IS NULL AND belegnr IS NOT NULL
    """)
    conn.commit()

    # Verify
    remaining = conn.execute("""
        SELECT COUNT(*) FROM steuer_posten WHERE dokument_id IS NULL
    """).fetchone()[0]

    print(f"  Backfilled: {fillable} rows")
    if remaining > 0:
        print(f"  WARNING: {remaining} rows still have NULL dokument_id!")
        return False
    else:
        print(f"  All dokument_id values are now populated.")
        return True


def phase2_drop_dok_belegnr(conn, use_drop, dry_run=False):
    """Phase 2: Drop steuer_dokumente.belegnr."""
    print("\n--- Phase 2: Drop steuer_dokumente.belegnr ---")

    columns = get_table_columns(conn, "steuer_dokumente")
    if "belegnr" not in columns:
        print("  belegnr already removed. Skipping.")
        return

    # Verify id == belegnr
    mismatches = conn.execute("""
        SELECT COUNT(*) FROM steuer_dokumente WHERE belegnr != id
    """).fetchone()[0]

    if mismatches > 0:
        print(f"  ERROR: {mismatches} rows where belegnr != id. Aborting phase 2!")
        return

    print(f"  Verified: belegnr == id for all rows.")

    if use_drop:
        drop_column_modern(conn, "steuer_dokumente", "belegnr", dry_run)
    else:
        rebuild_table_without_columns(conn, "steuer_dokumente", ["belegnr"], dry_run=dry_run)

    if not dry_run:
        conn.commit()
        new_cols = get_table_columns(conn, "steuer_dokumente")
        if "belegnr" not in new_cols:
            print("  OK: steuer_dokumente.belegnr removed.")
        else:
            print("  ERROR: belegnr still present!")
    else:
        print("  [DRY-RUN] Would remove steuer_dokumente.belegnr")


def phase3_drop_posten_columns(conn, use_drop, dry_run=False):
    """Phase 3: Drop steuer_posten.belegnr and steuer_posten.posten_id_str.
    Also make dokument_id NOT NULL."""
    print("\n--- Phase 3: Drop steuer_posten.belegnr + posten_id_str, make dokument_id NOT NULL ---")

    columns = get_table_columns(conn, "steuer_posten")

    drop_cols = []
    if "belegnr" in columns:
        drop_cols.append("belegnr")
    if "posten_id_str" in columns:
        drop_cols.append("posten_id_str")

    if not drop_cols and "dokument_id" in columns:
        # Check if already NOT NULL
        pragma = conn.execute("PRAGMA table_info(steuer_posten)").fetchall()
        for row in pragma:
            if row[1] == "dokument_id" and row[3]:  # notnull flag
                print("  All changes already applied. Skipping.")
                return

    if not drop_cols:
        print("  Columns already removed.")
    else:
        print(f"  Columns to remove: {', '.join(drop_cols)}")

    # For the NOT NULL change, we always need rebuild regardless of SQLite version
    # (ALTER TABLE cannot change column constraints in SQLite)
    # So we always use rebuild for this phase

    column_overrides = {
        "dokument_id": "dokument_id INTEGER NOT NULL"
    }

    if dry_run:
        rebuild_table_without_columns(
            conn, "steuer_posten", drop_cols,
            column_overrides=column_overrides, dry_run=True
        )
        return

    # Verify no NULL dokument_id before making NOT NULL
    null_check = conn.execute("""
        SELECT COUNT(*) FROM steuer_posten WHERE dokument_id IS NULL
    """).fetchone()[0]

    if null_check > 0:
        print(f"  ERROR: {null_check} rows still have NULL dokument_id. Cannot make NOT NULL!")
        print("  Run Phase 1 first, or fix manually.")
        return

    rebuild_table_without_columns(
        conn, "steuer_posten", drop_cols,
        column_overrides=column_overrides
    )

    # Verify
    new_cols = get_table_columns(conn, "steuer_posten")
    removed = [c for c in drop_cols if c not in new_cols]
    still_there = [c for c in drop_cols if c in new_cols]

    if removed:
        print(f"  OK: Removed: {', '.join(removed)}")
    if still_there:
        print(f"  ERROR: Still present: {', '.join(still_there)}")

    # Verify NOT NULL
    pragma = conn.execute("PRAGMA table_info(steuer_posten)").fetchall()
    for row in pragma:
        if row[1] == "dokument_id":
            if row[3]:  # notnull
                print("  OK: dokument_id is now NOT NULL")
            else:
                print("  WARNING: dokument_id NOT NULL constraint may not have applied")


def verify_migration(conn, pre_counts):
    """Verify row counts match before/after."""
    print("\n--- Verification ---")

    dok_count = get_row_count(conn, "steuer_dokumente")
    posten_count = get_row_count(conn, "steuer_posten")

    dok_ok = dok_count == pre_counts["dok"]
    posten_ok = posten_count == pre_counts["posten"]

    print(f"  steuer_dokumente: {pre_counts['dok']} -> {dok_count} {'OK' if dok_ok else 'MISMATCH!'}")
    print(f"  steuer_posten:    {pre_counts['posten']} -> {posten_count} {'OK' if posten_ok else 'MISMATCH!'}")

    if not dok_ok or not posten_ok:
        print("\n  *** ROW COUNT MISMATCH - MIGRATION MAY HAVE LOST DATA ***")
        print("  *** Restore from backup! ***")
        return False

    return True


def print_summary(conn, bak_path, dry_run=False):
    """Prints final summary."""
    print("\n" + "=" * 60)
    if dry_run:
        print("DRY-RUN SUMMARY (no changes made)")
    else:
        print("MIGRATION SUMMARY")
    print("=" * 60)

    dok_cols = get_table_columns(conn, "steuer_dokumente")
    posten_cols = get_table_columns(conn, "steuer_posten")

    print(f"\n  steuer_dokumente columns: {len(dok_cols)}")
    for c in dok_cols:
        print(f"    - {c}")

    print(f"\n  steuer_posten columns: {len(posten_cols)}")
    for c in posten_cols:
        print(f"    - {c}")

    removed = []
    if "belegnr" not in dok_cols:
        removed.append("steuer_dokumente.belegnr")
    if "belegnr" not in posten_cols:
        removed.append("steuer_posten.belegnr")
    if "posten_id_str" not in posten_cols:
        removed.append("steuer_posten.posten_id_str")

    if removed:
        print(f"\n  Columns removed: {', '.join(removed)}")

    if bak_path:
        print(f"\n  Backup: {bak_path}")

    print(f"\n  IMPORTANT: Update Python code to match new schema!")
    print(f"  See FILES_TO_UPDATE section in this script's docstring.")
    print()


def run_migration(dry_run=False):
    """Main migration logic."""
    print("\n" + "=" * 60)
    print(f"STEUER DB MIGRATION 002 - Cleanup Redundancies")
    print(f"{'DRY RUN' if dry_run else 'LIVE RUN'}")
    print("=" * 60)

    # Check SQLite version
    ver_tuple, ver_str = get_sqlite_version()
    use_drop = supports_drop_column()
    print(f"\n  SQLite version: {ver_str}")
    print(f"  DROP COLUMN support: {'Yes' if use_drop else 'No (will rebuild tables)'}")

    # Check DB exists
    if not DB_PATH.exists():
        print(f"\n  ERROR: Database not found: {DB_PATH}")
        return 1

    print(f"  Database: {DB_PATH}")
    print(f"  Size: {DB_PATH.stat().st_size:,} bytes")

    # Step 1: Backup
    bak_path = backup_db(DB_PATH, dry_run=dry_run)

    # Connect
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        # Check current state
        info = check_current_state(conn)
        print_info(info)

        if "error" in info:
            print(f"\n  Cannot proceed: {info['error']}")
            return 1

        # Pre-migration counts
        pre_counts = {
            "dok": info["dok_count"],
            "posten": info["posten_count"]
        }

        # Check if already migrated
        already_done = (
            info.get("dok_belegnr_already_removed", False)
            and not info.get("posten_has_belegnr", True)
            and not info.get("posten_has_posten_id_str", True)
        )
        if already_done:
            print("\n  Migration already applied. Nothing to do.")
            return 0

        # Phase 1: Backfill
        if info.get("posten_has_belegnr") and info.get("posten_dokument_id_nulls", 0) > 0:
            ok = phase1_backfill(conn, dry_run=dry_run)
            if not ok and not dry_run:
                print("\n  Phase 1 failed. Aborting.")
                return 1
        else:
            print("\n--- Phase 1: Backfill ---")
            if info.get("posten_dokument_id_nulls", 0) == 0:
                print("  No NULLs in dokument_id. Skipping.")
            else:
                print("  belegnr not available for backfill.")

        # Phase 2: Drop steuer_dokumente.belegnr
        if not info.get("dok_belegnr_already_removed"):
            phase2_drop_dok_belegnr(conn, use_drop, dry_run=dry_run)
        else:
            print("\n--- Phase 2: Already done ---")

        # Phase 3: Drop steuer_posten.belegnr + posten_id_str, make dokument_id NOT NULL
        if info.get("posten_has_belegnr") or info.get("posten_has_posten_id_str"):
            phase3_drop_posten_columns(conn, use_drop, dry_run=dry_run)
        else:
            print("\n--- Phase 3: Already done ---")

        # Phase 4: dateiname - DEFERRED
        print("\n--- Phase 4: steuer_posten.dateiname ---")
        print("  DEFERRED: Keeping dateiname for now (too many JOINs needed).")
        print("  Will be addressed in a future migration.")

        # Verify
        if not dry_run:
            verify_migration(conn, pre_counts)

        # Summary
        print_summary(conn, bak_path, dry_run=dry_run)

        return 0

    finally:
        conn.close()


def main():
    """Entry point."""
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(__doc__)
        return 0

    if "--info" in args:
        if not DB_PATH.exists():
            print(f"  ERROR: Database not found: {DB_PATH}")
            return 1
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        info = check_current_state(conn)
        print_info(info)
        conn.close()
        return 0

    dry_run = "--dry-run" in args

    return run_migration(dry_run=dry_run)


if __name__ == "__main__":
    sys.exit(main())
