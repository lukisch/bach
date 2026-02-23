#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
O002 - Memory-Persistenz
========================
Testet Memory-Infrastruktur:
- Kurzzeit-Memory (Session)
- Langzeit-Memory (Global)
- Persistenz-Mechanismen

Output: JSON mit Memory-Test-Ergebnis
"""

import os
import json
import sys
import re
from pathlib import Path
from datetime import datetime

def test_memory_persistence(root_path: str) -> dict:
    """Testet Memory-Infrastruktur eines Systems."""
    
    root = Path(root_path)
    if not root.exists():
        return {"error": f"Pfad existiert nicht: {root_path}"}
    
    result = {
        "system_path": str(root),
        "test_date": datetime.now().isoformat(),
        "test_id": "O002",
        "test_name": "Memory-Persistenz",
        "checks": [],
        "status": "UNKNOWN",
        "score": 0.0
    }
    
    checks_passed = 0
    total_checks = 0
    
    # Check 1: Memory-Verzeichnis existiert
    total_checks += 1
    memory_patterns = ["MEMORY", "memory", "CONTEXT", "context", "STATE"]
    memory_dirs = []
    for pattern in memory_patterns:
        found = list(root.glob(pattern)) + list(root.glob(f"*/{pattern}"))
        memory_dirs.extend([d for d in found if d.is_dir()])
    
    if memory_dirs:
        checks_passed += 1
        result["checks"].append({
            "name": "memory_dir_exists",
            "passed": True,
            "details": f"Gefunden: {[str(d.relative_to(root)) for d in memory_dirs[:3]]}"
        })
    else:
        result["checks"].append({
            "name": "memory_dir_exists",
            "passed": False,
            "details": "Kein Memory-Verzeichnis gefunden"
        })
    
    # Check 2: Kurzzeit-Memory (Session)
    total_checks += 1
    session_patterns = ["SESSION*", "session*", "SHORT*", "short*", "CURRENT*"]
    session_files = []
    for pattern in session_patterns:
        session_files.extend(root.rglob(pattern))
    session_files = [f for f in session_files if f.is_file()]
    
    if session_files:
        checks_passed += 1
        result["checks"].append({
            "name": "shortterm_memory",
            "passed": True,
            "details": f"Session-Memory: {len(session_files)} Dateien"
        })
    else:
        result["checks"].append({
            "name": "shortterm_memory",
            "passed": False,
            "details": "Keine Session-Memory-Dateien"
        })
    
    # Check 3: Langzeit-Memory (Global/Persistent)
    total_checks += 1
    global_patterns = ["GLOBAL*", "global*", "LONG*", "long*", "PERSISTENT*", "REMEMBER*"]
    global_files = []
    for pattern in global_patterns:
        global_files.extend(root.rglob(pattern))
    global_files = [f for f in global_files if f.is_file()]
    
    if global_files:
        checks_passed += 1
        result["checks"].append({
            "name": "longterm_memory",
            "passed": True,
            "details": f"Global-Memory: {len(global_files)} Dateien"
        })
    else:
        result["checks"].append({
            "name": "longterm_memory",
            "passed": False,
            "details": "Keine Langzeit-Memory-Dateien"
        })
    
    # Check 4: Memory-Dateien haben Inhalt
    total_checks += 1
    all_memory_files = session_files + global_files
    files_with_content = 0
    
    for f in all_memory_files[:10]:  # Max 10 pruefen
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
            if len(content.strip()) > 50:
                files_with_content += 1
        except:
            pass
    
    if files_with_content > 0:
        checks_passed += 1
        result["checks"].append({
            "name": "memory_has_content",
            "passed": True,
            "details": f"{files_with_content} Dateien mit Inhalt"
        })
    else:
        result["checks"].append({
            "name": "memory_has_content",
            "passed": False,
            "details": "Memory-Dateien leer oder nicht lesbar"
        })
    
    # Check 5: DB-basierte Persistenz (optional, Bonus)
    total_checks += 1
    db_files = list(root.rglob("*.db")) + list(root.rglob("*.sqlite"))
    db_files = [f for f in db_files if "test" not in f.name.lower()]
    
    if db_files:
        checks_passed += 1
        result["checks"].append({
            "name": "database_storage",
            "passed": True,
            "details": f"DB-Persistenz: {[f.name for f in db_files[:3]]}"
        })
    else:
        result["checks"].append({
            "name": "database_storage",
            "passed": False,
            "details": "Keine Datenbank-Persistenz (optional)"
        })
    
    # Ergebnis
    result["score"] = round(checks_passed / total_checks * 5, 2)
    
    if checks_passed >= total_checks * 0.8:
        result["status"] = "PASS"
    elif checks_passed >= total_checks * 0.5:
        result["status"] = "PARTIAL"
    else:
        result["status"] = "FAIL"
    
    result["summary"] = f"{checks_passed}/{total_checks} Checks bestanden"
    
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python O002_memory_persistence.py <system_path> [output_json]")
        sys.exit(1)
    
    result = test_memory_persistence(sys.argv[1])
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Ergebnis gespeichert: {output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
