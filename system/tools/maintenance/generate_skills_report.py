#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
generate_skills_report.py - Generiert nutzerfreundlichen Skills-Bericht

Erstellt: user/SKILLS_REPORT.md
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from collections import defaultdict

BACH_ROOT = Path(__file__).parent.parent
DB_PATH = BACH_ROOT / "data" / "bach.db"
OUTPUT_PATH = BACH_ROOT / "user" / "SKILLS_REPORT.md"

def generate_report():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Alle Skills laden
    c.execute("""
        SELECT name, type, category, path, description, is_active, version
        FROM skills
        ORDER BY category, name
    """)
    skills = c.fetchall()
    conn.close()
    
    # Nach Kategorie gruppieren
    by_category = defaultdict(list)
    for skill in skills:
        by_category[skill['category'] or 'uncategorized'].append(skill)
    
    # Bericht generieren
    lines = [
        f"# BACH Skills Report",
        f"",
        f"*Generiert: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        f"",
        f"## Übersicht",
        f"",
        f"| Kategorie | Anzahl |",
        f"|-----------|--------|",
    ]
    
    for cat in sorted(by_category.keys()):
        lines.append(f"| {cat} | {len(by_category[cat])} |")
    
    lines.append(f"| **GESAMT** | **{len(skills)}** |")
    lines.append("")
    
    # Details pro Kategorie
    for cat in sorted(by_category.keys()):
        lines.append(f"## {cat.upper()}")
        lines.append("")
        lines.append(f"| Name | Typ | Status | Pfad |")
        lines.append(f"|------|-----|--------|------|")
        
        for s in by_category[cat]:
            status = "✓" if s['is_active'] else "✗"
            lines.append(f"| {s['name']} | {s['type']} | {status} | `{s['path']}` |")
        
        lines.append("")
    
    # Speichern
    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Report erstellt: {OUTPUT_PATH}")
    print(f"     {len(skills)} Skills in {len(by_category)} Kategorien")

if __name__ == "__main__":
    generate_report()
