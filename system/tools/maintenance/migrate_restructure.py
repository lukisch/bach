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
migrate_restructure.py - BACH Directory Restructuring Migration
================================================================

Einmaliges Script fuer die Standards-konforme Verzeichnis-Umstrukturierung.

Verschiebungen:
  agents/*      -> agents/*
  agents/_experts/*     -> agents/_experts/*
  skills/_workflows/*   -> skills/workflows/*
  partners/*    -> partners/*
  connectors/*  -> connectors/*
  hub/_services/*.md    -> skills/_services/*.md  (nur Top-Level .md Dateien)

Usage:
  python migrate_restructure.py --dry-run    # Nur anzeigen
  python migrate_restructure.py              # Ausfuehren
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# BACH Root ermitteln
SCRIPT_DIR = Path(__file__).parent
SYSTEM_ROOT = SCRIPT_DIR.parent.parent

def log(msg):
    print(f"  {msg}")

def migrate(dry_run=False):
    print("=" * 60)
    print("BACH DIRECTORY RESTRUCTURING MIGRATION")
    print(f"System Root: {SYSTEM_ROOT}")
    print(f"Mode: {'DRY-RUN' if dry_run else 'LIVE'}")
    print("=" * 60)

    skills_dir = SYSTEM_ROOT / "skills"
    moved_count = 0
    errors = []

    # ================================================================
    # 1. Neue Ziel-Verzeichnisse erstellen
    # ================================================================
    print("\n[1/6] Erstelle Ziel-Verzeichnisse...")
    new_dirs = [
        SYSTEM_ROOT / "agents",
        SYSTEM_ROOT / "agents" / "_experts",
        SYSTEM_ROOT / "connectors",
        SYSTEM_ROOT / "partners",
        skills_dir / "workflows",
    ]

    for d in new_dirs:
        if d.exists():
            log(f"[EXISTS] {d.relative_to(SYSTEM_ROOT)}")
        else:
            log(f"[CREATE] {d.relative_to(SYSTEM_ROOT)}")
            if not dry_run:
                d.mkdir(parents=True, exist_ok=True)

    # ================================================================
    # 2. agents/* -> agents/*
    # ================================================================
    print("\n[2/6] Verschiebe agents/* -> agents/*...")
    src_agents = skills_dir / "_agents"
    dst_agents = SYSTEM_ROOT / "agents"

    if src_agents.exists():
        for item in sorted(src_agents.iterdir()):
            if item.name == "_archive":
                # Archive mitnehmen
                dst = dst_agents / "_archive"
            else:
                dst = dst_agents / item.name

            if dst.exists():
                log(f"[SKIP] {item.name} existiert bereits in agents/")
                continue

            log(f"[MOVE] {item.name} -> agents/{item.name}")
            if not dry_run:
                shutil.move(str(item), str(dst))
            moved_count += 1
    else:
        log("[SKIP] agents/ existiert nicht")

    # ================================================================
    # 3. agents/_experts/* -> agents/_experts/*
    # ================================================================
    print("\n[3/6] Verschiebe agents/_experts/* -> agents/_experts/*...")
    src_experts = skills_dir / "_experts"
    dst_experts = SYSTEM_ROOT / "agents" / "_experts"

    if src_experts.exists():
        for item in sorted(src_experts.iterdir()):
            dst = dst_experts / item.name

            if dst.exists():
                log(f"[SKIP] {item.name} existiert bereits in agents/_experts/")
                continue

            log(f"[MOVE] {item.name} -> agents/_experts/{item.name}")
            if not dry_run:
                shutil.move(str(item), str(dst))
            moved_count += 1
    else:
        log("[SKIP] agents/_experts/ existiert nicht")

    # ================================================================
    # 4. skills/_workflows/* -> skills/workflows/*
    # ================================================================
    print("\n[4/6] Verschiebe skills/_workflows/* -> skills/workflows/*...")
    src_workflows = skills_dir / "_workflows"
    dst_workflows = skills_dir / "workflows"

    if src_workflows.exists():
        for item in sorted(src_workflows.iterdir()):
            dst = dst_workflows / item.name

            if dst.exists():
                log(f"[SKIP] {item.name} existiert bereits in skills/workflows/")
                continue

            log(f"[MOVE] {item.name} -> skills/workflows/{item.name}")
            if not dry_run:
                shutil.move(str(item), str(dst))
            moved_count += 1
    else:
        log("[SKIP] skills/workflows/ existiert nicht")

    # ================================================================
    # 5. connectors/* -> connectors/*
    #    partners/* -> partners/*
    # ================================================================
    print("\n[5/6] Verschiebe _connectors und _partners...")

    moves = [
        (skills_dir / "_connectors", SYSTEM_ROOT / "connectors", "connectors"),
        (skills_dir / "_partners", SYSTEM_ROOT / "partners", "partners"),
    ]

    for src, dst_base, label in moves:
        if src.exists():
            for item in sorted(src.iterdir()):
                dst = dst_base / item.name

                if dst.exists():
                    log(f"[SKIP] {item.name} existiert bereits in {label}/")
                    continue

                log(f"[MOVE] {item.name} -> {label}/{item.name}")
                if not dry_run:
                    shutil.move(str(item), str(dst))
                moved_count += 1
        else:
            log(f"[SKIP] skills/_{label}/ existiert nicht")

    # ================================================================
    # 6. hub/_services/*.md -> skills/_services/*.md (nur Top-Level)
    # ================================================================
    print("\n[6/6] Kopiere hub/_services/*.md -> skills/_services/*.md...")
    src_services = SYSTEM_ROOT / "hub" / "_services"
    dst_services = skills_dir / "_services"

    if src_services.exists():
        # Nur Top-Level .md Dateien (keine Unterordner-Dateien)
        md_files = [f for f in src_services.iterdir()
                    if f.is_file() and f.suffix == '.md']

        for md_file in sorted(md_files):
            dst = dst_services / md_file.name

            if dst.exists():
                log(f"[SKIP] {md_file.name} existiert bereits in skills/_services/")
                continue

            log(f"[COPY] {md_file.name} -> skills/_services/{md_file.name}")
            if not dry_run:
                dst_services.mkdir(parents=True, exist_ok=True)
                shutil.copy2(str(md_file), str(dst))
            moved_count += 1

        # Nach erfolgreichem Kopieren: Originale loeschen
        if not dry_run:
            for md_file in md_files:
                dst = dst_services / md_file.name
                if dst.exists():
                    md_file.unlink()
                    log(f"[DEL]  hub/_services/{md_file.name} (Original entfernt)")
    else:
        log("[SKIP] hub/_services/ existiert nicht")

    # ================================================================
    # Aufraumen: Leere Alt-Verzeichnisse entfernen
    # ================================================================
    print("\n[CLEANUP] Leere Alt-Verzeichnisse pruefen...")
    cleanup_dirs = [
        skills_dir / "_agents",
        skills_dir / "_experts",
        skills_dir / "_workflows",
        skills_dir / "_connectors",
        skills_dir / "_partners",
    ]

    for d in cleanup_dirs:
        if d.exists():
            remaining = list(d.iterdir())
            if not remaining:
                log(f"[REMOVE] {d.relative_to(SYSTEM_ROOT)} (leer)")
                if not dry_run:
                    d.rmdir()
            else:
                log(f"[KEEP]   {d.relative_to(SYSTEM_ROOT)} ({len(remaining)} Items verbleibend)")

    # ================================================================
    # Report
    # ================================================================
    print("\n" + "=" * 60)
    print(f"{'DRY-RUN' if dry_run else 'MIGRATION'} ABGESCHLOSSEN")
    print(f"  Verschoben/Kopiert: {moved_count} Items")
    print(f"  Fehler: {len(errors)}")
    if errors:
        for err in errors:
            print(f"  [ERR] {err}")
    print("=" * 60)

    return moved_count, errors


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    moved, errors = migrate(dry_run)
    sys.exit(0 if not errors else 1)
