#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
O003 - Tool-Registry
====================
Testet ob Tools registriert und dokumentiert sind.

Output: JSON mit Tool-Registry-Test-Ergebnis
"""

import os
import json
import sys
import re
from pathlib import Path
from datetime import datetime

def test_tool_registry(root_path: str) -> dict:
    """Testet Tool-Registry eines Systems."""
    
    root = Path(root_path)
    if not root.exists():
        return {"error": f"Pfad existiert nicht: {root_path}"}
    
    result = {
        "system_path": str(root),
        "test_date": datetime.now().isoformat(),
        "test_id": "O003",
        "test_name": "Tool-Registry",
        "checks": [],
        "tools_found": [],
        "status": "UNKNOWN",
        "score": 0.0
    }
    
    checks_passed = 0
    total_checks = 0
    
    # Check 1: Tool-Verzeichnis existiert
    total_checks += 1
    tool_patterns = ["TOOLS", "tools", "SCRIPTS", "scripts", "BIN", "bin", "UTILS"]
    tool_dirs = []
    for pattern in tool_patterns:
        found = list(root.glob(pattern)) + list(root.glob(f"*/{pattern}"))
        tool_dirs.extend([d for d in found if d.is_dir()])
    
    if tool_dirs:
        checks_passed += 1
        result["checks"].append({
            "name": "tool_dir_exists",
            "passed": True,
            "details": f"Gefunden: {[str(d.relative_to(root)) for d in tool_dirs[:3]]}"
        })
    else:
        result["checks"].append({
            "name": "tool_dir_exists",
            "passed": False,
            "details": "Kein Tool-Verzeichnis gefunden"
        })
    
    # Check 2: Executable Tools vorhanden
    total_checks += 1
    tool_extensions = ['.py', '.sh', '.bat', '.ps1', '.js']
    tools = []
    
    for ext in tool_extensions:
        for f in root.rglob(f"*{ext}"):
            if "__pycache__" in str(f) or "node_modules" in str(f):
                continue
            # Pruefen ob es ein Tool ist (nicht nur Config)
            name = f.stem.lower()
            if any(kw in name for kw in ['run', 'tool', 'util', 'helper', 'script', 'check', 'test', 'build']):
                tools.append({
                    "name": f.name,
                    "path": str(f.relative_to(root)),
                    "type": ext[1:]
                })
    
    if tools:
        checks_passed += 1
        result["checks"].append({
            "name": "tools_exist",
            "passed": True,
            "details": f"{len(tools)} Tools gefunden"
        })
        result["tools_found"] = tools[:20]
    else:
        result["checks"].append({
            "name": "tools_exist",
            "passed": False,
            "details": "Keine ausfuehrbaren Tools gefunden"
        })
    
    # Check 3: Tool-Dokumentation (README in Tool-Dirs oder Docstrings)
    total_checks += 1
    documented_tools = 0
    
    for tool_dir in tool_dirs:
        readme = tool_dir / "README.md"
        if readme.exists():
            documented_tools += 1
    
    # Auch in SKILL.md nach Tool-Referenzen suchen
    skill_files = list(root.glob("SKILL.md")) + list(root.glob("SKILL.txt"))
    if skill_files:
        try:
            content = skill_files[0].read_text(encoding='utf-8', errors='ignore')
            if re.search(r'(?i)tool|script|util', content):
                documented_tools += 1
        except:
            pass
    
    if documented_tools > 0:
        checks_passed += 1
        result["checks"].append({
            "name": "tools_documented",
            "passed": True,
            "details": f"{documented_tools} Dokumentationsquellen"
        })
    else:
        result["checks"].append({
            "name": "tools_documented",
            "passed": False,
            "details": "Keine Tool-Dokumentation gefunden"
        })
    
    # Check 4: Registry-Datei (z.B. tools.json, registry.json)
    total_checks += 1
    registry_patterns = ["registry.json", "tools.json", "TOOLS.txt", "tool_registry*"]
    registry_files = []
    for pattern in registry_patterns:
        registry_files.extend(root.rglob(pattern))
    
    if registry_files:
        checks_passed += 1
        result["checks"].append({
            "name": "registry_file",
            "passed": True,
            "details": f"Registry: {registry_files[0].name}"
        })
    else:
        result["checks"].append({
            "name": "registry_file",
            "passed": False,
            "details": "Keine zentrale Registry-Datei"
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
        print("Usage: python O003_tool_registry.py <system_path> [output_json]")
        sys.exit(1)
    
    result = test_tool_registry(sys.argv[1])
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Ergebnis gespeichert: {output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
