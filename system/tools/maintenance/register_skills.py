# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Skills in bach.db registrieren
==============================
Scannt skills/ Ordner und registriert alle Skill-Dateien in der DB.
"""
import sqlite3
from pathlib import Path
from datetime import datetime

BACH_DIR = Path(__file__).parent.parent
DB_PATH = BACH_DIR / "data" / "bach.db"
SKILLS_DIR = BACH_DIR / "skills"

# Skill-Kategorien basierend auf Ordnerstruktur
SKILL_CATEGORIES = {
    "_services": "service",
    "workflows": "protocol",
    "_templates": "template",
    "_os": "os",
    "__FUTURES": "future"
}

# Agents und Experts liegen jetzt unter system/agents/ (v2.5)
AGENTS_DIR = BACH_DIR / "agents"
EXPERTS_DIR = AGENTS_DIR / "_experts"

def scan_skills():
    """Scannt skills/ Ordner und sammelt Skill-Definitionen"""
    skills = []
    
    # Root-Level Skill-Dateien
    for f in SKILLS_DIR.glob("*.md"):
        skills.append({
            "name": f.stem,
            "type": "definition",
            "category": "core",
            "path": f"skills/{f.name}",
            "description": f"Core skill definition: {f.stem}"
        })
    
    # Unterordner-Skills (skills/_services, workflows, etc.)
    for subdir in SKILLS_DIR.iterdir():
        if subdir.is_dir() and subdir.name in SKILL_CATEGORIES:
            category = SKILL_CATEGORIES[subdir.name]

            for f in subdir.glob("*"):
                if f.suffix in [".md", ".txt"]:
                    skills.append({
                        "name": f.stem,
                        "type": "skill",
                        "category": category,
                        "path": f"skills/{subdir.name}/{f.name}",
                        "description": f"{category.capitalize()} skill: {f.stem}"
                    })

    # Agents (system/agents/) - v2.5
    if AGENTS_DIR.exists():
        for f in AGENTS_DIR.glob("*"):
            if f.suffix in [".md", ".txt"] or (f.is_dir() and not f.name.startswith("_")):
                skills.append({
                    "name": f.stem if f.is_file() else f.name,
                    "type": "profile",
                    "category": "agent",
                    "path": f"agents/{f.name}",
                    "description": f"Agent: {f.stem if f.is_file() else f.name}"
                })

    # Experts (system/agents/_experts/) - v2.5
    if EXPERTS_DIR.exists():
        for f in EXPERTS_DIR.glob("*"):
            if f.suffix in [".md", ".txt"] or (f.is_dir() and not f.name.startswith("_")):
                skills.append({
                    "name": f.stem if f.is_file() else f.name,
                    "type": "skill",
                    "category": "expert",
                    "path": f"agents/_experts/{f.name}",
                    "description": f"Expert: {f.stem if f.is_file() else f.name}"
                })

    return skills

def register_skills():
    """Registriert alle Skills in bach.db"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    skills = scan_skills()
    
    registered = 0
    updated = 0
    
    for skill in skills:
        cursor.execute("SELECT id FROM skills WHERE name = ? AND category = ?",
                      (skill['name'], skill['category']))
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute("""
                UPDATE skills SET 
                    path = ?, description = ?, updated_at = ?, is_active = 1
                WHERE id = ?
            """, (skill['path'], skill['description'], now, existing[0]))
            updated += 1
        else:
            cursor.execute("""
                INSERT INTO skills (name, type, category, path, description,
                                    is_active, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, 1, ?, ?)
            """, (skill['name'], skill['type'], skill['category'], skill['path'],
                  skill['description'], now, now))
            registered += 1
    
    conn.commit()
    conn.close()
    
    print(f"Skills registriert: {registered} neu, {updated} aktualisiert")
    print(f"Gesamt: {registered + updated} Skills")
    return registered, updated

if __name__ == "__main__":
    register_skills()
