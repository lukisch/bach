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
Aktualisiert directory_truth.json mit neuer Struktur (Docs-Refactoring v2.6)
"""
import json
from pathlib import Path
from datetime import datetime

SYSTEM_ROOT = Path(__file__).parent.parent
TRUTH_FILE = SYSTEM_ROOT / "data" / "directory_truth.json"

def scan_directory_structure():
    """Scannt system/ und erstellt neue Directory Truth."""
    directories = {}
    files = {}

    # Wichtige Top-Level Verzeichnisse
    important_dirs = [
        "hub", "tools", "skills", "data", "gui", "core",
        "docs", "wiki", "agents", "connectors", "partners"
    ]

    for dir_name in important_dirs:
        dir_path = SYSTEM_ROOT / dir_name
        if dir_path.exists():
            directories[dir_name] = {
                "exists": True,
                "path": str(dir_path.relative_to(SYSTEM_ROOT)),
                "count": len(list(dir_path.rglob("*")))
            }

    # Spezielle Subdirs
    if (SYSTEM_ROOT / "docs").exists():
        directories["docs/help"] = {
            "exists": True,
            "path": "docs/help",
            "count": len(list((SYSTEM_ROOT / "docs" / "help").rglob("*")))
        }
        directories["docs/guides"] = {
            "exists": True,
            "path": "docs/guides",
            "count": len(list((SYSTEM_ROOT / "docs" / "guides").rglob("*")))
        }
        directories["docs/reference"] = {
            "exists": True,
            "path": "docs/reference",
            "count": len(list((SYSTEM_ROOT / "docs" / "reference").rglob("*")))
        }

    return {
        "timestamp": datetime.now().isoformat(),
        "version": "2.6",
        "refactoring": "docs-refactoring-2026-02-14",
        "directories": directories,
        "files": files,
        "changes": [
            "docs/docs/docs/help/ -> docs/docs/docs/docs/help/",
            "wiki/ -> wiki/",
            "docs/guides/ created",
            "docs/reference/ created"
        ]
    }

if __name__ == "__main__":
    # Alte Truth laden
    if TRUTH_FILE.exists():
        with open(TRUTH_FILE, 'r', encoding='utf-8') as f:
            old_truth = json.load(f)
        print(f"Alte Truth: {len(old_truth.get('directories', {}))} Verzeichnisse")

    # Neue Truth erstellen
    new_truth = scan_directory_structure()
    print(f"Neue Truth: {len(new_truth['directories'])} Verzeichnisse")

    # Backup erstellen
    backup_file = TRUTH_FILE.with_suffix('.json.backup')
    if TRUTH_FILE.exists():
        import shutil
        shutil.copy(TRUTH_FILE, backup_file)
        print(f"Backup: {backup_file}")

    # Neue Truth speichern (kompakt, nicht riesig)
    with open(TRUTH_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_truth, f, indent=2, ensure_ascii=False)

    print(f"✅ Directory Truth aktualisiert: {TRUTH_FILE}")
    print("\nÄnderungen:")
    for change in new_truth["changes"]:
        print(f"  - {change}")
