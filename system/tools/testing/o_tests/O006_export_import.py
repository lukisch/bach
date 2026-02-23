#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
O006 - Export-Import
====================
Testet Export/Import-Faehigkeiten eines Systems.

Output: JSON mit Export-Import-Test-Ergebnis
"""

import os
import json
import sys
import re
from pathlib import Path
from datetime import datetime

def test_export_import(root_path: str) -> dict:
    """Testet Export-Import-Faehigkeiten eines Systems."""
    
    root = Path(root_path)
    if not root.exists():
        return {"error": f"Pfad existiert nicht: {root_path}"}
    
    result = {
        "system_path": str(root),
        "test_date": datetime.now().isoformat(),
        "test_id": "O006",
        "test_name": "Export-Import",
        "checks": [],
        "export_capabilities": [],
        "status": "UNKNOWN",
        "score": 0.0
    }
    
    checks_passed = 0
    total_checks = 0
    
    # Check 1: Export-Verzeichnis/Dateien
    total_checks += 1
    export_patterns = ["OUTPUT", "output", "EXPORT", "export", "OUT", "REPORTS"]
    export_dirs = []
    for pattern in export_patterns:
        found = list(root.glob(pattern)) + list(root.glob(f"*/{pattern}"))
        export_dirs.extend([d for d in found if d.is_dir()])
    
    if export_dirs:
        checks_passed += 1
        result["checks"].append({
            "name": "export_dir_exists",
            "passed": True,
            "details": f"Export-Verzeichnis: {[str(d.relative_to(root)) for d in export_dirs[:2]]}"
        })
        result["export_capabilities"].append("Dediziertes Export-Verzeichnis")
    else:
        result["checks"].append({
            "name": "export_dir_exists",
            "passed": False,
            "details": "Kein Export-Verzeichnis"
        })
    
    # Check 2: Import-Verzeichnis
    total_checks += 1
    import_patterns = ["INPUT", "input", "IMPORT", "import", "INBOX", "USER"]
    import_dirs = []
    for pattern in import_patterns:
        found = list(root.glob(pattern)) + list(root.glob(f"*/{pattern}"))
        import_dirs.extend([d for d in found if d.is_dir()])
    
    if import_dirs:
        checks_passed += 1
        result["checks"].append({
            "name": "import_dir_exists",
            "passed": True,
            "details": f"Import-Verzeichnis: {[str(d.relative_to(root)) for d in import_dirs[:2]]}"
        })
        result["export_capabilities"].append("Dediziertes Import-Verzeichnis")
    else:
        result["checks"].append({
            "name": "import_dir_exists",
            "passed": False,
            "details": "Kein Import-Verzeichnis"
        })
    
    # Check 3: Export-Skripte/Tools
    total_checks += 1
    export_scripts = []
    for f in root.rglob("*.py"):
        if "__pycache__" in str(f):
            continue
        name = f.stem.lower()
        if any(kw in name for kw in ['export', 'report', 'bundle', 'dump', 'save']):
            export_scripts.append(f.name)
    
    if export_scripts:
        checks_passed += 1
        result["checks"].append({
            "name": "export_scripts",
            "passed": True,
            "details": f"Export-Tools: {export_scripts[:3]}"
        })
        result["export_capabilities"].append("Export-Skripte vorhanden")
    else:
        result["checks"].append({
            "name": "export_scripts",
            "passed": False,
            "details": "Keine Export-Skripte"
        })
    
    # Check 4: Standardformate unterstuetzt
    total_checks += 1
    format_indicators = {
        "JSON": list(root.rglob("*.json")),
        "CSV": list(root.rglob("*.csv")),
        "Markdown": list(root.rglob("*.md")),
        "SQL": list(root.rglob("*.sql"))
    }
    
    supported_formats = [fmt for fmt, files in format_indicators.items() if files]
    
    if len(supported_formats) >= 2:
        checks_passed += 1
        result["checks"].append({
            "name": "standard_formats",
            "passed": True,
            "details": f"Formate: {supported_formats}"
        })
        result["export_capabilities"].extend([f"{fmt}-Format" for fmt in supported_formats])
    else:
        result["checks"].append({
            "name": "standard_formats",
            "passed": False,
            "details": f"Nur {len(supported_formats)} Standardformat(e)"
        })
    
    # Check 5: Dokumentation von Export/Import
    total_checks += 1
    documented = False
    
    skill_files = list(root.glob("SKILL.md")) + list(root.glob("SKILL.txt"))
    for sf in skill_files:
        try:
            content = sf.read_text(encoding='utf-8', errors='ignore').lower()
            if 'export' in content or 'import' in content or 'output' in content:
                documented = True
                break
        except:
            pass
    
    if documented:
        checks_passed += 1
        result["checks"].append({
            "name": "export_documented",
            "passed": True,
            "details": "Export/Import in SKILL dokumentiert"
        })
    else:
        result["checks"].append({
            "name": "export_documented",
            "passed": False,
            "details": "Keine Export-Dokumentation"
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
        print("Usage: python O006_export_import.py <system_path> [output_json]")
        sys.exit(1)
    
    result = test_export_import(sys.argv[1])
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Ergebnis gespeichert: {output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
