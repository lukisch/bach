#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
O004 - Backup-Restore
=====================
Testet Backup/Recovery-Infrastruktur.

Output: JSON mit Backup-Test-Ergebnis
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime

def test_backup_restore(root_path: str) -> dict:
    """Testet Backup-Infrastruktur eines Systems."""
    
    root = Path(root_path)
    if not root.exists():
        return {"error": f"Pfad existiert nicht: {root_path}"}
    
    result = {
        "system_path": str(root),
        "test_date": datetime.now().isoformat(),
        "test_id": "O004",
        "test_name": "Backup-Restore",
        "checks": [],
        "backup_locations": [],
        "status": "UNKNOWN",
        "score": 0.0
    }
    
    checks_passed = 0
    total_checks = 0
    
    # Check 1: Backup-Verzeichnis existiert
    total_checks += 1
    backup_patterns = ["BACKUP", "backup", "_BACKUP", "ARCHIV", "archive", "_PAPIERKORB", "trash"]
    backup_dirs = []
    for pattern in backup_patterns:
        found = list(root.rglob(pattern))
        backup_dirs.extend([d for d in found if d.is_dir()])
    
    if backup_dirs:
        checks_passed += 1
        result["checks"].append({
            "name": "backup_dir_exists",
            "passed": True,
            "details": f"Gefunden: {[str(d.relative_to(root)) for d in backup_dirs[:3]]}"
        })
        result["backup_locations"] = [str(d.relative_to(root)) for d in backup_dirs]
    else:
        result["checks"].append({
            "name": "backup_dir_exists",
            "passed": False,
            "details": "Kein Backup-Verzeichnis gefunden"
        })
    
    # Check 2: Backup-Dateien vorhanden
    total_checks += 1
    backup_extensions = ['.bak', '.backup', '.old', '.prev']
    backup_files = []
    for ext in backup_extensions:
        backup_files.extend(root.rglob(f"*{ext}"))
    
    # Auch Dateien in Backup-Ordnern zaehlen
    backup_count = len(backup_files)
    for bd in backup_dirs:
        backup_count += len(list(bd.rglob("*")))
    
    if backup_count > 0:
        checks_passed += 1
        result["checks"].append({
            "name": "backup_files_exist",
            "passed": True,
            "details": f"{backup_count} Backup-Elemente"
        })
    else:
        result["checks"].append({
            "name": "backup_files_exist",
            "passed": False,
            "details": "Keine Backup-Dateien"
        })
    
    # Check 3: Papierkorb-System
    total_checks += 1
    trash_patterns = ["_PAPIERKORB", "PAPIERKORB", "trash", "TRASH", "deleted"]
    trash_dirs = []
    for pattern in trash_patterns:
        found = list(root.rglob(pattern))
        trash_dirs.extend([d for d in found if d.is_dir()])
    
    if trash_dirs:
        checks_passed += 1
        result["checks"].append({
            "name": "trash_system",
            "passed": True,
            "details": f"Papierkorb: {trash_dirs[0].relative_to(root)}"
        })
    else:
        result["checks"].append({
            "name": "trash_system",
            "passed": False,
            "details": "Kein Papierkorb-System"
        })
    
    # Check 4: Backup-Dokumentation/Anleitung
    total_checks += 1
    backup_docs = False
    
    # In SKILL.md nach Backup-Referenzen suchen
    skill_files = list(root.glob("SKILL.md")) + list(root.glob("SKILL.txt"))
    for sf in skill_files:
        try:
            content = sf.read_text(encoding='utf-8', errors='ignore').lower()
            if 'backup' in content or 'restore' in content or 'recovery' in content:
                backup_docs = True
                break
        except:
            pass
    
    if backup_docs:
        checks_passed += 1
        result["checks"].append({
            "name": "backup_documented",
            "passed": True,
            "details": "Backup in SKILL dokumentiert"
        })
    else:
        result["checks"].append({
            "name": "backup_documented",
            "passed": False,
            "details": "Keine Backup-Dokumentation"
        })
    
    # Ergebnis
    result["score"] = round(checks_passed / total_checks * 5, 2)
    
    if checks_passed >= total_checks * 0.75:
        result["status"] = "PASS"
    elif checks_passed >= total_checks * 0.5:
        result["status"] = "PARTIAL"
    else:
        result["status"] = "FAIL"
    
    result["summary"] = f"{checks_passed}/{total_checks} Checks bestanden"
    
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python O004_backup_restore.py <system_path> [output_json]")
        sys.exit(1)
    
    result = test_backup_restore(sys.argv[1])
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Ergebnis gespeichert: {output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
