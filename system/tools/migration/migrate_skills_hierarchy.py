#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
BACH Skills Hierarchy Migration
================================
Migriert data/skills_hierarchy.json nach bach.db

Tabellen:
- hierarchy_types: Typ-Definitionen
- hierarchy_items: Alle Entities (agents, experts, skills, services, workflows)
- hierarchy_assignments: Zuweisungen zwischen Entities

Usage:
    python tools/migration/migrate_skills_hierarchy.py [--dry-run]

Stand: 2026-01-29
"""

import json
import sqlite3
import sys
from pathlib import Path
from datetime import datetime

# BACH Root
BACH_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BACH_ROOT / "data"
DB_PATH = DATA_DIR / "bach.db"
JSON_PATH = DATA_DIR / "skills_hierarchy.json"


def create_tables(conn: sqlite3.Connection, dry_run: bool = False) -> None:
    """Erstellt die benoetigten Tabellen."""
    schema = """
    -- Typ-Definitionen
    CREATE TABLE IF NOT EXISTS hierarchy_types (
        id TEXT PRIMARY KEY,
        label TEXT NOT NULL,
        color TEXT,
        icon TEXT,
        display_order INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    -- Alle Entities
    CREATE TABLE IF NOT EXISTS hierarchy_items (
        id TEXT PRIMARY KEY,
        type TEXT NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        dashboard_url TEXT,
        status TEXT DEFAULT 'active',
        is_active INTEGER DEFAULT 1,
        priority INTEGER DEFAULT 50,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT,
        FOREIGN KEY (type) REFERENCES hierarchy_types(id)
    );

    -- Zuweisungen
    CREATE TABLE IF NOT EXISTS hierarchy_assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        parent_id TEXT NOT NULL,
        parent_type TEXT NOT NULL,
        child_id TEXT NOT NULL,
        child_type TEXT NOT NULL,
        assignment_order INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(parent_id, child_id)
    );

    -- Indizes
    CREATE INDEX IF NOT EXISTS idx_hierarchy_items_type ON hierarchy_items(type);
    CREATE INDEX IF NOT EXISTS idx_hierarchy_items_status ON hierarchy_items(status);
    CREATE INDEX IF NOT EXISTS idx_hierarchy_assignments_parent ON hierarchy_assignments(parent_id);
    CREATE INDEX IF NOT EXISTS idx_hierarchy_assignments_child ON hierarchy_assignments(child_id);
    """

    if dry_run:
        print("[DRY-RUN] Wuerde Tabellen erstellen:")
        print("  - hierarchy_types")
        print("  - hierarchy_items")
        print("  - hierarchy_assignments")
        return

    conn.executescript(schema)
    conn.commit()
    print("[OK] Tabellen erstellt/geprueft")


def migrate_types(conn: sqlite3.Connection, data: dict, dry_run: bool = False) -> int:
    """Migriert hierarchy_types."""
    types = data.get("hierarchy_types", {})
    count = 0

    for type_id, type_data in types.items():
        if dry_run:
            print(f"[DRY-RUN] Typ: {type_id} -> {type_data.get('label')}")
            count += 1
            continue

        conn.execute("""
            INSERT OR REPLACE INTO hierarchy_types (id, label, color, icon, display_order)
            VALUES (?, ?, ?, ?, ?)
        """, (
            type_id,
            type_data.get("label", type_id),
            type_data.get("color"),
            type_data.get("icon"),
            type_data.get("order", 0)
        ))
        count += 1

    if not dry_run:
        conn.commit()

    return count


def migrate_items(conn: sqlite3.Connection, data: dict, dry_run: bool = False) -> int:
    """Migriert alle Items (agents, experts, skills, services, workflows)."""
    items = data.get("items", {})
    count = 0
    now = datetime.now().isoformat()

    type_mapping = {
        "agents": "agent",
        "experts": "expert",
        "skills": "skill",
        "services": "service",
        "workflows": "workflow"
    }

    for category, item_type in type_mapping.items():
        category_items = items.get(category, [])

        for item in category_items:
            item_id = item.get("id")
            if not item_id:
                continue

            if dry_run:
                print(f"[DRY-RUN] Item: {item_type}/{item_id} -> {item.get('name')}")
                count += 1
                continue

            conn.execute("""
                INSERT OR REPLACE INTO hierarchy_items
                (id, type, name, description, dashboard_url, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                item_id,
                item_type,
                item.get("name", item_id),
                item.get("description"),
                item.get("dashboard"),
                item.get("status", "active"),
                now
            ))
            count += 1

    if not dry_run:
        conn.commit()

    return count


def migrate_assignments(conn: sqlite3.Connection, data: dict, dry_run: bool = False) -> int:
    """Migriert Zuweisungen (Agent -> Expert, Agent -> Service, etc.)."""
    assignments = data.get("assignments", {})
    count = 0
    now = datetime.now().isoformat()

    child_type_mapping = {
        "experts": "expert",
        "skills": "skill",
        "services": "service",
        "workflows": "workflow"
    }

    for parent_id, assignment_data in assignments.items():
        # Parent ist immer ein Agent (in aktueller JSON-Struktur)
        parent_type = "agent"

        for child_category, child_type in child_type_mapping.items():
            child_ids = assignment_data.get(child_category, [])

            for order, child_id in enumerate(child_ids):
                if dry_run:
                    print(f"[DRY-RUN] Assignment: {parent_id} -> {child_id} ({child_type})")
                    count += 1
                    continue

                try:
                    conn.execute("""
                        INSERT OR IGNORE INTO hierarchy_assignments
                        (parent_id, parent_type, child_id, child_type, assignment_order, created_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        parent_id,
                        parent_type,
                        child_id,
                        child_type,
                        order,
                        now
                    ))
                    count += 1
                except sqlite3.IntegrityError:
                    pass  # Duplikat ignorieren

    if not dry_run:
        conn.commit()

    return count


def main():
    dry_run = "--dry-run" in sys.argv

    print("=" * 60)
    print("BACH Skills Hierarchy Migration")
    print("=" * 60)

    if dry_run:
        print("[MODE] Dry-Run - keine Aenderungen werden gespeichert\n")

    # JSON laden
    if not JSON_PATH.exists():
        print(f"[ERROR] JSON nicht gefunden: {JSON_PATH}")
        sys.exit(1)

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"[OK] JSON geladen: {JSON_PATH}")
    print(f"     Version: {data.get('_meta', {}).get('version', 'unbekannt')}")
    print()

    # DB-Verbindung
    if dry_run:
        conn = sqlite3.connect(":memory:")
    else:
        conn = sqlite3.connect(DB_PATH)

    try:
        # Migration
        create_tables(conn, dry_run)

        print("\n[1/3] Typen migrieren...")
        type_count = migrate_types(conn, data, dry_run)
        print(f"      {type_count} Typen")

        print("\n[2/3] Items migrieren...")
        item_count = migrate_items(conn, data, dry_run)
        print(f"      {item_count} Items")

        print("\n[3/3] Zuweisungen migrieren...")
        assign_count = migrate_assignments(conn, data, dry_run)
        print(f"      {assign_count} Zuweisungen")

        print("\n" + "=" * 60)
        print(f"ZUSAMMENFASSUNG")
        print("=" * 60)
        print(f"Typen:       {type_count}")
        print(f"Items:       {item_count}")
        print(f"Zuweisungen: {assign_count}")
        print(f"TOTAL:       {type_count + item_count + assign_count}")

        if dry_run:
            print("\n[DRY-RUN] Keine Aenderungen gespeichert.")
            print("          Fuehre ohne --dry-run aus fuer echte Migration.")
        else:
            print(f"\n[OK] Migration nach {DB_PATH} abgeschlossen!")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
