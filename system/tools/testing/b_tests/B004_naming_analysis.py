#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
B004 - Naming-Analyse
=====================
Analysiert Benennungskonventionen fuer Dateien und Ordner.

Output: JSON mit Naming-Patterns und Konsistenz-Score
"""

import os
import json
import sys
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def analyze_naming(root_path: str) -> dict:
    """Analysiert Naming-Konventionen eines Systems."""
    
    root = Path(root_path)
    if not root.exists():
        return {"error": f"Pfad existiert nicht: {root_path}"}
    
    result = {
        "system_path": str(root),
        "scan_date": datetime.now().isoformat(),
        "files": {"patterns": defaultdict(int), "prefixes": defaultdict(int), "issues": []},
        "dirs": {"patterns": defaultdict(int), "issues": []},
        "conventions_detected": [],
        "score": 0.0
    }
    
    def classify_name(name: str) -> str:
        """Klassifiziert einen Namen nach Pattern."""
        if name.isupper():
            return "SCREAMING_CASE"
        elif name.islower() and "_" in name:
            return "snake_case"
        elif name.islower() and "-" in name:
            return "kebab-case"
        elif name.islower():
            return "lowercase"
        elif name[0].isupper() and "_" not in name and "-" not in name:
            if name.isupper():
                return "SCREAMING_CASE"
            return "PascalCase"
        elif name[0].islower() and any(c.isupper() for c in name[1:]):
            return "camelCase"
        else:
            return "Mixed"
    
    def extract_prefix(name: str) -> str:
        """Extrahiert Prefix wie B001_, E001_, etc."""
        match = re.match(r'^([A-Z]{1,3}\d{2,4})[_-]', name)
        if match:
            prefix = match.group(1)
            return prefix[0] + "xxx"  # Generalisieren: B001 -> Bxxx
        return None
    
    # Dateien analysieren
    for item in root.rglob("*"):
        if "__pycache__" in str(item) or "node_modules" in str(item):
            continue
        rel_path = item.relative_to(root)
        if any(part.startswith('.') for part in rel_path.parts):
            continue
        
        name = item.stem
        if not name:
            continue
        
        if item.is_file():
            pattern = classify_name(name)
            result["files"]["patterns"][pattern] += 1
            
            prefix = extract_prefix(name)
            if prefix:
                result["files"]["prefixes"][prefix] += 1
            
            # Issue: Leerzeichen im Namen
            if " " in item.name:
                result["files"]["issues"].append(f"Leerzeichen: {rel_path}")
            # Issue: Sonderzeichen
            if re.search(r'[äöüßÄÖÜ]', item.name):
                result["files"]["issues"].append(f"Umlaute: {rel_path}")
                
        elif item.is_dir():
            pattern = classify_name(name)
            result["dirs"]["patterns"][pattern] += 1
            
            if " " in name:
                result["dirs"]["issues"].append(f"Leerzeichen: {rel_path}")
    
    # Konvertiere defaultdicts
    result["files"]["patterns"] = dict(result["files"]["patterns"])
    result["files"]["prefixes"] = dict(result["files"]["prefixes"])
    result["dirs"]["patterns"] = dict(result["dirs"]["patterns"])
    
    # Limit issues
    result["files"]["issues"] = result["files"]["issues"][:10]
    result["dirs"]["issues"] = result["dirs"]["issues"][:10]
    
    # Konventionen erkennen
    file_patterns = result["files"]["patterns"]
    dir_patterns = result["dirs"]["patterns"]
    
    if file_patterns:
        dominant_file = max(file_patterns, key=file_patterns.get)
        file_consistency = file_patterns[dominant_file] / sum(file_patterns.values())
        result["conventions_detected"].append(f"Dateien: {dominant_file} ({round(file_consistency*100)}%)")
    else:
        file_consistency = 0
    
    if dir_patterns:
        dominant_dir = max(dir_patterns, key=dir_patterns.get)
        dir_consistency = dir_patterns[dominant_dir] / sum(dir_patterns.values())
        result["conventions_detected"].append(f"Ordner: {dominant_dir} ({round(dir_consistency*100)}%)")
    else:
        dir_consistency = 0
    
    # Prefix-System erkannt?
    if result["files"]["prefixes"]:
        result["conventions_detected"].append(f"Prefix-System: {list(result['files']['prefixes'].keys())}")
    
    # Score berechnen
    issue_penalty = (len(result["files"]["issues"]) + len(result["dirs"]["issues"])) * 0.1
    base_score = (file_consistency + dir_consistency) / 2 * 5
    result["score"] = max(1.0, round(base_score - issue_penalty, 2))
    
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python B004_naming_analysis.py <system_path> [output_json]")
        sys.exit(1)
    
    result = analyze_naming(sys.argv[1])
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Ergebnis gespeichert: {output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
