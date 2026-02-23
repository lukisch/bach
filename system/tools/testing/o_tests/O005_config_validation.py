#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
O005 - Config-Validierung
=========================
Testet ob Config-Dateien valide sind.

Output: JSON mit Validierungs-Ergebnis
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime

def test_config_validation(root_path: str) -> dict:
    """Testet Config-Dateien eines Systems."""
    
    root = Path(root_path)
    if not root.exists():
        return {"error": f"Pfad existiert nicht: {root_path}"}
    
    result = {
        "system_path": str(root),
        "test_date": datetime.now().isoformat(),
        "test_id": "O005",
        "test_name": "Config-Validierung",
        "checks": [],
        "config_files": [],
        "validation_results": [],
        "status": "UNKNOWN",
        "score": 0.0
    }
    
    # Sammle Config-Dateien
    config_extensions = ['.json', '.yaml', '.yml', '.toml', '.ini', '.cfg']
    config_files = []
    
    for ext in config_extensions:
        for f in root.rglob(f"*{ext}"):
            if "__pycache__" in str(f) or "node_modules" in str(f):
                continue
            config_files.append(f)
    
    result["config_files"] = [str(f.relative_to(root)) for f in config_files[:20]]
    
    if not config_files:
        result["checks"].append({
            "name": "config_files_found",
            "passed": False,
            "details": "Keine Config-Dateien gefunden"
        })
        result["status"] = "BLOCKED"
        result["score"] = 0
        return result
    
    # Validiere jede Config-Datei
    valid_count = 0
    invalid_files = []
    
    for cf in config_files:
        try:
            content = cf.read_text(encoding='utf-8')
            
            if cf.suffix == '.json':
                json.loads(content)
                valid_count += 1
                result["validation_results"].append({
                    "file": cf.name,
                    "valid": True
                })
            elif cf.suffix in ['.yaml', '.yml']:
                # Einfacher YAML-Check (syntaktisch)
                # Vollstaendiger Check wuerde pyyaml brauchen
                if content.strip() and not content.strip().startswith('{'):
                    valid_count += 1
                    result["validation_results"].append({
                        "file": cf.name,
                        "valid": True,
                        "note": "Basis-Check (kein YAML-Parser)"
                    })
            else:
                # Andere Formate: Nur pruefen ob lesbar
                if len(content) > 0:
                    valid_count += 1
                    result["validation_results"].append({
                        "file": cf.name,
                        "valid": True,
                        "note": "Lesbarkeits-Check"
                    })
                    
        except json.JSONDecodeError as e:
            invalid_files.append(cf.name)
            result["validation_results"].append({
                "file": cf.name,
                "valid": False,
                "error": f"JSON-Fehler: {str(e)[:100]}"
            })
        except Exception as e:
            invalid_files.append(cf.name)
            result["validation_results"].append({
                "file": cf.name,
                "valid": False,
                "error": str(e)[:100]
            })
    
    # Limit validation_results
    result["validation_results"] = result["validation_results"][:15]
    
    # Checks zusammenfassen
    total_configs = len(config_files)
    
    result["checks"].append({
        "name": "config_files_found",
        "passed": True,
        "details": f"{total_configs} Config-Dateien gefunden"
    })
    
    validation_rate = valid_count / total_configs if total_configs > 0 else 0
    
    result["checks"].append({
        "name": "configs_valid",
        "passed": validation_rate >= 0.8,
        "details": f"{valid_count}/{total_configs} valide ({round(validation_rate*100)}%)"
    })
    
    if invalid_files:
        result["checks"].append({
            "name": "invalid_configs",
            "passed": False,
            "details": f"Ungueltig: {invalid_files[:5]}"
        })
    
    # Ergebnis
    result["score"] = round(validation_rate * 5, 2)
    
    if validation_rate >= 0.9:
        result["status"] = "PASS"
    elif validation_rate >= 0.7:
        result["status"] = "PARTIAL"
    else:
        result["status"] = "FAIL"
    
    result["summary"] = f"{valid_count}/{total_configs} Config-Dateien valide"
    
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python O005_config_validation.py <system_path> [output_json]")
        sys.exit(1)
    
    result = test_config_validation(sys.argv[1])
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Ergebnis gespeichert: {output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
