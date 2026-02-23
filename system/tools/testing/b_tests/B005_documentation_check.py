#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
B005 - Dokumentations-Check
===========================
Prueft Vollstaendigkeit und Qualitaet der Dokumentation.

Output: JSON mit Dokumentations-Metriken und Luecken
"""

import os
import json
import sys
import re
from pathlib import Path
from datetime import datetime

def check_documentation(root_path: str) -> dict:
    """Prueft Dokumentation eines Systems."""
    
    root = Path(root_path)
    if not root.exists():
        return {"error": f"Pfad existiert nicht: {root_path}"}
    
    result = {
        "system_path": str(root),
        "scan_date": datetime.now().isoformat(),
        "entry_points": [],
        "doc_files": [],
        "coverage": {},
        "quality_checks": {},
        "missing": [],
        "score": 0.0
    }
    
    # Erwartete Dokumentationsdateien
    expected_docs = [
        ("SKILL.md", "Haupt-Einstiegspunkt", 10),
        ("SKILL.txt", "Haupt-Einstiegspunkt (alt)", 10),
        ("README.md", "Projekt-Beschreibung", 5),
        ("CHANGELOG.md", "Aenderungshistorie", 3),
        ("CHANGELOG.txt", "Aenderungshistorie (alt)", 3),
    ]
    
    # Suche Entry-Points
    for name, desc, weight in expected_docs:
        found = list(root.rglob(name))
        if found:
            for f in found:
                rel = str(f.relative_to(root))
                size = f.stat().st_size
                result["entry_points"].append({
                    "file": name,
                    "path": rel,
                    "size": size,
                    "description": desc
                })
    
    # Sammle alle Dokumentationsdateien
    doc_extensions = ['.md', '.txt', '.rst']
    total_doc_size = 0
    doc_count = 0
    
    for ext in doc_extensions:
        for f in root.rglob(f"*{ext}"):
            if "__pycache__" in str(f):
                continue
            rel = str(f.relative_to(root))
            size = f.stat().st_size
            total_doc_size += size
            doc_count += 1
            
            # Nur groessere Dateien listen
            if size > 500:
                result["doc_files"].append({
                    "path": rel,
                    "size": size
                })
    
    result["doc_files"] = sorted(result["doc_files"], key=lambda x: x["size"], reverse=True)[:20]
    
    # Coverage: Haben Unterordner READMEs?
    dirs_with_readme = 0
    dirs_without_readme = []
    
    for d in root.iterdir():
        if d.is_dir() and not d.name.startswith('.') and d.name not in ["__pycache__", "node_modules"]:
            has_readme = any((d / f).exists() for f in ["README.md", "README.txt", "SKILL.md", "SKILL.txt"])
            if has_readme:
                dirs_with_readme += 1
            else:
                dirs_without_readme.append(d.name)
    
    total_top_dirs = dirs_with_readme + len(dirs_without_readme)
    result["coverage"] = {
        "top_level_dirs_documented": dirs_with_readme,
        "top_level_dirs_total": total_top_dirs,
        "coverage_percent": round(dirs_with_readme / max(total_top_dirs, 1) * 100, 1),
        "undocumented_dirs": dirs_without_readme[:10]
    }
    
    # Qualitaetschecks auf Haupt-SKILL
    skill_files = list(root.glob("SKILL.md")) + list(root.glob("SKILL.txt"))
    if skill_files:
        skill_file = skill_files[0]
        try:
            content = skill_file.read_text(encoding='utf-8', errors='ignore')
            
            result["quality_checks"] = {
                "has_quick_start": bool(re.search(r'(?i)quick\s*start|getting\s*started|einstieg', content)),
                "has_structure": bool(re.search(r'(?i)struktur|structure|ordner|folder', content)),
                "has_examples": bool(re.search(r'(?i)beispiel|example|demo', content)),
                "has_version": bool(re.search(r'(?i)version|v\d+\.\d+', content)),
                "word_count": len(content.split()),
                "section_count": len(re.findall(r'^#+\s|\n[=-]+\n', content, re.MULTILINE))
            }
        except:
            result["quality_checks"] = {"error": "Konnte SKILL nicht lesen"}
    else:
        result["missing"].append("Kein SKILL.md/txt im Root gefunden!")
    
    # Fehlende wichtige Docs
    for name, desc, weight in expected_docs:
        if not any(e["file"] == name for e in result["entry_points"]):
            # Nur melden wenn wichtig (weight > 5)
            if weight > 5:
                result["missing"].append(f"{name} ({desc})")
    
    # Score berechnen
    score = 0.0
    
    # Entry-Point vorhanden? (+2)
    if result["entry_points"]:
        score += 2.0
    
    # Coverage gut? (+1.5)
    if result["coverage"]["coverage_percent"] >= 50:
        score += 1.5
    elif result["coverage"]["coverage_percent"] >= 25:
        score += 0.75
    
    # Qualitaetschecks (+1.5)
    if result["quality_checks"]:
        checks = result["quality_checks"]
        if checks.get("has_quick_start"):
            score += 0.3
        if checks.get("has_structure"):
            score += 0.3
        if checks.get("has_examples"):
            score += 0.3
        if checks.get("word_count", 0) > 500:
            score += 0.3
        if checks.get("section_count", 0) >= 5:
            score += 0.3
    
    result["score"] = min(5.0, round(score, 2))
    
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python B005_documentation_check.py <system_path> [output_json]")
        sys.exit(1)
    
    result = check_documentation(sys.argv[1])
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Ergebnis gespeichert: {output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
