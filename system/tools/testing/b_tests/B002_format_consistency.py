#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
B002 - Format-Konsistenz
========================
Prueft Einheitlichkeit der Dateiformate und Strukturen.

Output: JSON mit Konsistenz-Score und Abweichungen
"""

import os
import json
import sys
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def check_format_consistency(root_path: str) -> dict:
    """Prueft Format-Konsistenz eines Systems."""
    
    root = Path(root_path)
    if not root.exists():
        return {"error": f"Pfad existiert nicht: {root_path}"}
    
    result = {
        "system_path": str(root),
        "scan_date": datetime.now().isoformat(),
        "checks": {},
        "issues": [],
        "score": 0.0
    }
    
    # Check 1: Markdown-Header-Konsistenz
    md_files = list(root.rglob("*.md")) + list(root.rglob("*.txt"))
    header_styles = defaultdict(int)
    
    for f in md_files:
        if "__pycache__" in str(f):
            continue
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')[:500]
            if content.startswith("# "):
                header_styles["h1_hash"] += 1
            elif content.startswith("=="):
                header_styles["underline"] += 1
            elif re.match(r'^[A-Z][A-Z\s_-]+\n[=-]+', content):
                header_styles["title_underline"] += 1
            else:
                header_styles["other"] += 1
        except:
            pass
    
    total_docs = sum(header_styles.values())
    dominant_style = max(header_styles, key=header_styles.get) if header_styles else "none"
    header_consistency = header_styles.get(dominant_style, 0) / max(total_docs, 1)
    
    result["checks"]["header_style"] = {
        "dominant": dominant_style,
        "consistency": round(header_consistency * 100, 1),
        "distribution": dict(header_styles)
    }
    
    # Check 2: Dateinamen-Konventionen
    naming_patterns = {
        "UPPERCASE": 0,
        "lowercase": 0,
        "snake_case": 0,
        "kebab-case": 0,
        "camelCase": 0,
        "mixed": 0
    }
    
    for item in root.rglob("*"):
        if item.is_file() and "__pycache__" not in str(item):
            name = item.stem
            if name.isupper():
                naming_patterns["UPPERCASE"] += 1
            elif name.islower() and "_" not in name and "-" not in name:
                naming_patterns["lowercase"] += 1
            elif "_" in name and name.lower() == name:
                naming_patterns["snake_case"] += 1
            elif "-" in name and name.lower() == name:
                naming_patterns["kebab-case"] += 1
            elif name[0].islower() and any(c.isupper() for c in name):
                naming_patterns["camelCase"] += 1
            else:
                naming_patterns["mixed"] += 1
    
    total_names = sum(naming_patterns.values())
    dominant_naming = max(naming_patterns, key=naming_patterns.get) if naming_patterns else "none"
    naming_consistency = naming_patterns.get(dominant_naming, 0) / max(total_names, 1)
    
    result["checks"]["naming_convention"] = {
        "dominant": dominant_naming,
        "consistency": round(naming_consistency * 100, 1),
        "distribution": naming_patterns
    }
    
    # Check 3: JSON-Formatierung (Einrueckung)
    json_files = list(root.rglob("*.json"))
    json_indent = {"2_spaces": 0, "4_spaces": 0, "tabs": 0, "minified": 0, "invalid": 0}
    
    for f in json_files:
        if "__pycache__" in str(f):
            continue
        try:
            content = f.read_text(encoding='utf-8')
            if "\n" not in content.strip():
                json_indent["minified"] += 1
            elif "    " in content:
                json_indent["4_spaces"] += 1
            elif "  " in content:
                json_indent["2_spaces"] += 1
            elif "\t" in content:
                json_indent["tabs"] += 1
        except:
            json_indent["invalid"] += 1
    
    total_json = sum(json_indent.values())
    result["checks"]["json_formatting"] = {
        "distribution": json_indent,
        "total": total_json
    }
    
    # Check 4: Encoding-Check
    encoding_issues = []
    for f in root.rglob("*"):
        if f.is_file() and f.suffix in ['.md', '.txt', '.json', '.py']:
            if "__pycache__" in str(f):
                continue
            try:
                f.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                encoding_issues.append(str(f.relative_to(root)))
    
    result["checks"]["encoding"] = {
        "utf8_compatible": total_docs - len(encoding_issues),
        "issues": encoding_issues[:10]  # Max 10
    }
    
    # Gesamtscore berechnen
    scores = [
        header_consistency,
        naming_consistency,
        1.0 if not encoding_issues else 0.5
    ]
    result["score"] = round(sum(scores) / len(scores) * 5, 2)
    
    # Issues sammeln
    if header_consistency < 0.7:
        result["issues"].append(f"Header-Stil inkonsistent ({round(header_consistency*100)}%)")
    if naming_consistency < 0.5:
        result["issues"].append(f"Dateinamen-Konvention uneinheitlich ({round(naming_consistency*100)}%)")
    if encoding_issues:
        result["issues"].append(f"{len(encoding_issues)} Dateien mit Encoding-Problemen")
    
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python B002_format_consistency.py <system_path> [output_json]")
        sys.exit(1)
    
    result = check_format_consistency(sys.argv[1])
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Ergebnis gespeichert: {output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
