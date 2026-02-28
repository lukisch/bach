#!/usr/bin/env python3
"""Migrate bestehende Prompt-Dateien in prompt_templates DB-Tabelle.

Quellen:
  1. hub/_services/prompt_generator/templates/{agents,system,custom}/*.txt
  2. tools/llmauto/prompts/*.txt
  3. agents/*/prompt_templates/*.txt (z.B. agents/ati/prompt_templates/)
"""
import sqlite3
import json
import sys
from pathlib import Path
from datetime import datetime

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS prompt_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    purpose TEXT,
    text TEXT NOT NULL,
    tags TEXT,
    category TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    dist_type INTEGER DEFAULT 1
);
"""


def migrate(db_path: Path, system_root: Path, dry_run: bool = False):
    """Migriert alle Prompt-Dateien in die DB.

    Returns:
        tuple: (inserted, skipped) counts
    """
    conn = sqlite3.connect(str(db_path))
    conn.execute(CREATE_TABLE_SQL)
    now = datetime.now().isoformat()
    inserted = 0
    skipped = 0

    def _insert(name: str, purpose: str, text: str, category: str, tags: list):
        nonlocal inserted, skipped
        if dry_run:
            print(f"  [DRY] {name} ({category})")
            inserted += 1
            return
        try:
            conn.execute(
                """INSERT OR IGNORE INTO prompt_templates
                   (name, purpose, text, category, tags, dist_type, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, 1, ?, ?)""",
                (name, purpose, text, category, json.dumps(tags), now, now),
            )
            if conn.total_changes:
                inserted += 1
            else:
                skipped += 1
        except sqlite3.IntegrityError:
            skipped += 1
            print(f"  [SKIP] {name} (existiert bereits)")

    # --- System 1: prompt_generator templates ---
    print("\n[1] prompt_generator/templates/")
    templates_dir = system_root / "hub" / "_services" / "prompt_generator" / "templates"
    pg_count_before = inserted
    for category_dir in ["agents", "system", "custom"]:
        cat_path = templates_dir / category_dir
        if not cat_path.exists():
            continue
        for txt_file in sorted(cat_path.glob("*.txt")):
            name = f"pg_{txt_file.stem}"
            text = txt_file.read_text(encoding="utf-8")
            purpose = f"Prompt Generator: {category_dir}/{txt_file.stem}"
            tags = ["prompt_generator", category_dir]
            _insert(name, purpose, text, category_dir, tags)
            print(f"  + {name}")
    print(f"  Subtotal: {inserted - pg_count_before} Dateien")

    # --- System 2: llmauto prompts ---
    print("\n[2] tools/llmauto/prompts/")
    llmauto_dir = system_root / "tools" / "llmauto" / "prompts"
    ll_count_before = inserted
    if llmauto_dir.exists():
        for txt_file in sorted(llmauto_dir.glob("*.txt")):
            name = txt_file.stem
            text = txt_file.read_text(encoding="utf-8")
            purpose = f"llmauto Prompt: {name}"
            tags = ["llmauto"]
            _insert(name, purpose, text, "llmauto", tags)
            print(f"  + {name}")
    else:
        print("  (Verzeichnis nicht gefunden)")
    print(f"  Subtotal: {inserted - ll_count_before} Dateien")

    # --- System 3: Agent-spezifische templates ---
    print("\n[3] agents/*/prompt_templates/")
    agents_dir = system_root / "agents"
    ag_count_before = inserted
    if agents_dir.exists():
        for prompt_dir in sorted(agents_dir.rglob("prompt_templates")):
            if not prompt_dir.is_dir():
                continue
            agent_name = prompt_dir.parent.name
            for txt_file in sorted(prompt_dir.glob("*.txt")):
                name = f"{agent_name}_{txt_file.stem}"
                text = txt_file.read_text(encoding="utf-8")
                purpose = f"Agent {agent_name}: {txt_file.stem}"
                tags = ["agent", agent_name]
                _insert(name, purpose, text, "agent", tags)
                print(f"  + {name}")
    else:
        print("  (Verzeichnis nicht gefunden)")
    print(f"  Subtotal: {inserted - ag_count_before} Dateien")

    if not dry_run:
        conn.commit()
    conn.close()
    return inserted, skipped


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv

    # system_root = data/schema/migrations/../../.. = system/
    system_root = Path(__file__).resolve().parent.parent.parent.parent
    db_path = system_root / "data" / "bach.db"

    print("=" * 50)
    print("BACH Prompt Migration")
    print("=" * 50)
    print(f"System Root: {system_root}")
    print(f"DB:          {db_path}")
    if dry_run:
        print("Modus:       DRY-RUN (keine DB-Aenderungen)")

    if not db_path.exists():
        print(f"\nERROR: DB nicht gefunden: {db_path}")
        sys.exit(1)

    inserted, skipped = migrate(db_path, system_root, dry_run=dry_run)

    print("\n" + "=" * 50)
    print(f"Ergebnis: {inserted} eingefuegt, {skipped} uebersprungen")
    print("=" * 50)
