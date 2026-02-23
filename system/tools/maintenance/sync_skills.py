#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
sync_skills.py - Synchronisiert skills/ Dateien mit bach.db/skills Tabelle
Version: 0.1.0 (Grundgeruest)
Task: #90 [SKILL_001]

FUNKTION:
- Scannt skills/ Verzeichnisse (_agents, _experts, _services, _workflows, _templates)
- Liest Metadaten aus Dateien (YAML-Header oder Dateinamen)
- Synchronisiert mit DB-Tabelle `skills`

VERWENDUNG:
  python sync_skills.py              # Sync durchfuehren
  python sync_skills.py --dry-run    # Nur anzeigen was passiert
  python sync_skills.py --verbose    # Mit Details

STATUS (Task #90 [SKILL_001]):
  [x] SKILL_001a: Datei-Scanner implementieren (os.walk ueber skills/)
  [x] SKILL_001b: Metadaten-Parser (YAML-Header aus .md Dateien)
  [x] SKILL_001c: DB-Sync Logik (INSERT/UPDATE mit Duplikat-Check)
  [x] SKILL_001d: --dry-run Modus implementieren
  [ ] SKILL_001e: CLI-Integration in bach.py (bach --maintain sync --skills)
"""

import os
import sys
import sqlite3
import argparse
from datetime import datetime
from pathlib import Path

# BACH Basispfad
BACH_ROOT = Path(__file__).parent.parent.parent
DB_PATH = BACH_ROOT / "data" / "bach.db"
SKILLS_ROOT = BACH_ROOT / "skills"

# Skill-Typen nach Verzeichnis (v2.5 Restructuring)
# Agents und Experts liegen jetzt unter system/agents/, nicht skills/
TYPE_MAPPING = {
    "_services": "service",
    "workflows": "protocol",
    "_templates": "template",
    "_os": "os"
}

# Zusaetzliche Scan-Verzeichnisse ausserhalb von skills/
EXTRA_SCAN_DIRS = {
    "agents": "agent",           # system/agents/
    "agents/_experts": "expert", # system/agents/_experts/
}


def get_db_connection():
    """Verbindung zur BACH-Datenbank"""
    return sqlite3.connect(DB_PATH)


def scan_skill_files():
    """
    Scannt alle Skill-Dateien und gibt Liste zurueck
    
    TODO: Implementieren - os.walk ueber SKILLS_ROOT
    Returns: List[dict] mit {name, type, category, path, ...}
    """
    skills = []
    
    # Skills aus skills/ Unterverzeichnissen
    all_mappings = dict(TYPE_MAPPING)

    # Extra-Verzeichnisse (agents/, agents/_experts/) hinzufuegen
    extra_dirs = {str(BACH_ROOT / k): v for k, v in EXTRA_SCAN_DIRS.items()}

    for dir_name, skill_type in all_mappings.items():
        dir_path = SKILLS_ROOT / dir_name
        if not dir_path.exists():
            continue
            
        for root, dirs, files in os.walk(dir_path):
            # _archive ignorieren
            if "_archive" in root:
                continue
                
            for file in files:
                if file.endswith(('.md', '.txt')):
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(BACH_ROOT)
                    
                    # Basis-Metadaten
                    # Eindeutiger Name: type/pfad innerhalb Type-Ordner
                    # z.B. _agents/bueroassistent.md -> "agent/bueroassistent"
                    # z.B. _services/steuer/README.md -> "service/steuer/README"
                    rel_from_type = file_path.relative_to(dir_path)
                    name_parts = list(rel_from_type.parts[:-1])  # Unterordner
                    name_parts.append(rel_from_type.stem)  # Dateiname ohne Endung
                    local_name = '/'.join(name_parts) if name_parts else rel_from_type.stem
                    unique_name = f"{skill_type}/{local_name}"
                    
                    # Category ist der direkte Unterordner (falls vorhanden)
                    category = name_parts[0] if len(name_parts) > 1 else None
                    
                    skill = {
                        "name": unique_name,
                        "type": skill_type,
                        "category": category,
                        "path": str(rel_path),
                        "description": None,
                        "version": "1.0.0"
                    }
                    
                    # YAML-Header lesen falls vorhanden
                    yaml_meta = parse_yaml_header(file_path)
                    if yaml_meta:
                        # HINWEIS: 'name' wird NICHT übernommen - DB braucht eindeutigen Namen
                        # YAML-name könnte in 'display_name' Feld (falls DB erweitert wird)
                        if 'description' in yaml_meta:
                            skill['description'] = yaml_meta['description']
                        if 'version' in yaml_meta:
                            skill['version'] = yaml_meta['version']
                    
                    skills.append(skill)

    # Extra-Verzeichnisse scannen (agents/, agents/_experts/)
    for dir_path_str, skill_type in extra_dirs.items():
        dir_path = Path(dir_path_str)
        if not dir_path.exists():
            continue
        for root, dirs, files in os.walk(dir_path):
            if "_archive" in root:
                continue
            for file in files:
                if file.endswith(('.md', '.txt')):
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(BACH_ROOT)
                    rel_from_type = file_path.relative_to(dir_path)
                    name_parts = list(rel_from_type.parts[:-1])
                    name_parts.append(rel_from_type.stem)
                    local_name = '/'.join(name_parts) if name_parts else rel_from_type.stem
                    unique_name = f"{skill_type}/{local_name}"
                    category = name_parts[0] if len(name_parts) > 1 else None
                    skill = {
                        "name": unique_name,
                        "type": skill_type,
                        "category": category,
                        "path": str(rel_path),
                        "description": None,
                        "version": "1.0.0"
                    }
                    yaml_meta = parse_yaml_header(file_path)
                    if yaml_meta:
                        if 'description' in yaml_meta:
                            skill['description'] = yaml_meta['description']
                        if 'version' in yaml_meta:
                            skill['version'] = yaml_meta['version']
                    skills.append(skill)

    
    return skills


def parse_yaml_header(file_path):
    """
    Extrahiert YAML-Header aus Markdown-Datei
    
    Format: --- ... --- Block am Anfang der Datei
    Returns: dict mit Metadaten oder None
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read(2000)  # Nur Anfang lesen
            
        # Check ob YAML-Header vorhanden (--- am Anfang)
        if not content.startswith('---'):
            return None
            
        # Finde Ende des Headers
        end_pos = content.find('---', 3)
        if end_pos == -1:
            return None
            
        yaml_block = content[3:end_pos].strip()
        
        # Simple Key:Value Parser (ohne yaml dependency)
        metadata = {}
        for line in yaml_block.split('\n'):
            line = line.strip()
            if ':' in line and not line.startswith('#'):
                key, _, value = line.partition(':')
                key = key.strip()
                value = value.strip()
                # Quotes entfernen
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                if value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                metadata[key] = value
                
        return metadata if metadata else None
        
    except Exception as e:
        return None


def sync_to_db(skills, dry_run=False, verbose=False):
    """
    Synchronisiert Skills mit Datenbank
    
    TODO: INSERT/UPDATE Logik mit Duplikat-Check nach path
    """
    if dry_run:
        print(f"[DRY-RUN] Wuerde {len(skills)} Skills synchronisieren:")
        for s in skills[:10]:  # Erste 10 zeigen
            print(f"  - {s['type']}/{s['name']}")
        if len(skills) > 10:
            print(f"  ... und {len(skills) - 10} weitere")
        return
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    inserted = 0
    updated = 0
    
    for skill in skills:
        # Check ob bereits existiert
        cursor.execute("SELECT id FROM skills WHERE path = ?", (skill["path"],))
        existing = cursor.fetchone()
        
        if existing:
            # UPDATE
            cursor.execute("""
                UPDATE skills SET 
                    name = ?, type = ?, category = ?, 
                    description = ?, updated_at = ?
                WHERE path = ?
            """, (
                skill["name"], skill["type"], skill["category"],
                skill["description"], datetime.now().isoformat(),
                skill["path"]
            ))
            updated += 1
        else:
            # INSERT
            cursor.execute("""
                INSERT INTO skills (name, type, category, path, version, description, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                skill["name"], skill["type"], skill["category"],
                skill["path"], skill["version"], skill["description"],
                datetime.now().isoformat()
            ))
            inserted += 1
    
    conn.commit()
    conn.close()
    
    print(f"[SYNC] {inserted} neu, {updated} aktualisiert")


def main():
    parser = argparse.ArgumentParser(description="Synchronisiert skills/ mit DB")
    parser.add_argument("--dry-run", action="store_true", help="Nur anzeigen")
    parser.add_argument("--verbose", "-v", action="store_true", help="Details")
    args = parser.parse_args()
    
    print("[SKILL-SYNC] Scanne skills/ Verzeichnis...")
    skills = scan_skill_files()
    print(f"[SKILL-SYNC] {len(skills)} Skill-Dateien gefunden")
    
    sync_to_db(skills, dry_run=args.dry_run, verbose=args.verbose)


if __name__ == "__main__":
    main()
