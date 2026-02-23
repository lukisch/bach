#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
O001 - Task-Roundtrip
=====================
Testet den kompletten Task-Lifecycle:
Erstellen → Lesen → Aendern → Loeschen

Dieser Test ist SEMI-AUTOMATISCH:
- Prueft ob Task-Infrastruktur existiert
- Validiert Dateiformate
- Simuliert keinen Claude-Workflow (das waeren E-Tests)

Output: JSON mit Roundtrip-Ergebnis
"""

import os
import json
import sys
import re
from pathlib import Path
from datetime import datetime

def test_task_roundtrip(root_path: str) -> dict:
    """Testet Task-Infrastruktur eines Systems."""
    
    root = Path(root_path)
    if not root.exists():
        return {"error": f"Pfad existiert nicht: {root_path}"}
    
    result = {
        "system_path": str(root),
        "test_date": datetime.now().isoformat(),
        "test_id": "O001",
        "test_name": "Task-Roundtrip",
        "checks": [],
        "status": "UNKNOWN",
        "score": 0.0
    }
    
    checks_passed = 0
    total_checks = 0
    
    # Check 1: Task-Datei existiert
    total_checks += 1
    task_patterns = ["AUFGABEN.txt", "TASKS.txt", "TODO.txt", "tasks.json", "AUFGABEN.md"]
    task_files = []
    for pattern in task_patterns:
        found = list(root.rglob(pattern))
        task_files.extend(found)
    
    if task_files:
        checks_passed += 1
        result["checks"].append({
            "name": "task_file_exists",
            "passed": True,
            "details": f"Gefunden: {[str(f.relative_to(root)) for f in task_files[:3]]}"
        })
    else:
        result["checks"].append({
            "name": "task_file_exists",
            "passed": False,
            "details": "Keine Task-Datei gefunden"
        })
    
    # Check 2: Task-Datei ist lesbar und hat Struktur
    total_checks += 1
    if task_files:
        task_file = task_files[0]
        try:
            content = task_file.read_text(encoding='utf-8')
            
            # Hat Sektionen?
            has_open = bool(re.search(r'(?i)(OPEN|TODO|OFFEN|PENDING)', content))
            has_done = bool(re.search(r'(?i)(DONE|ERLEDIGT|COMPLETED)', content))
            has_checkboxes = bool(re.search(r'\[\s*[xX ]?\s*\]', content))
            
            if has_open or has_done or has_checkboxes:
                checks_passed += 1
                result["checks"].append({
                    "name": "task_structure",
                    "passed": True,
                    "details": f"OPEN: {has_open}, DONE: {has_done}, Checkboxes: {has_checkboxes}"
                })
            else:
                result["checks"].append({
                    "name": "task_structure",
                    "passed": False,
                    "details": "Keine erkennbare Task-Struktur"
                })
        except Exception as e:
            result["checks"].append({
                "name": "task_structure",
                "passed": False,
                "details": f"Lesefehler: {e}"
            })
    else:
        result["checks"].append({
            "name": "task_structure",
            "passed": False,
            "details": "Keine Task-Datei zum Pruefen"
        })
    
    # Check 3: Task-Datei ist schreibbar (Simulationstest)
    total_checks += 1
    if task_files:
        task_file = task_files[0]
        try:
            # Teste ob wir schreiben koennten (ohne tatsaechlich zu schreiben)
            if os.access(task_file, os.W_OK):
                checks_passed += 1
                result["checks"].append({
                    "name": "task_writable",
                    "passed": True,
                    "details": "Schreibzugriff moeglich"
                })
            else:
                result["checks"].append({
                    "name": "task_writable",
                    "passed": False,
                    "details": "Kein Schreibzugriff"
                })
        except:
            result["checks"].append({
                "name": "task_writable",
                "passed": False,
                "details": "Zugriffspruefung fehlgeschlagen"
            })
    else:
        result["checks"].append({
            "name": "task_writable",
            "passed": False,
            "details": "Keine Task-Datei"
        })
    
    # Check 4: Archiv/History vorhanden
    total_checks += 1
    archive_patterns = ["ARCHIV", "archive", "DONE", "history", "completed"]
    has_archive = any(
        (root / p).exists() or list(root.rglob(p))
        for p in archive_patterns
    )
    
    if has_archive:
        checks_passed += 1
        result["checks"].append({
            "name": "task_archive",
            "passed": True,
            "details": "Archiv/History-Struktur gefunden"
        })
    else:
        result["checks"].append({
            "name": "task_archive",
            "passed": False,
            "details": "Kein Archiv gefunden"
        })
    
    # Ergebnis
    result["score"] = round(checks_passed / total_checks * 5, 2)
    
    if checks_passed == total_checks:
        result["status"] = "PASS"
    elif checks_passed >= total_checks * 0.5:
        result["status"] = "PARTIAL"
    else:
        result["status"] = "FAIL"
    
    result["summary"] = f"{checks_passed}/{total_checks} Checks bestanden"
    
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python O001_task_roundtrip.py <system_path> [output_json]")
        sys.exit(1)
    
    result = test_task_roundtrip(sys.argv[1])
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Ergebnis gespeichert: {output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
