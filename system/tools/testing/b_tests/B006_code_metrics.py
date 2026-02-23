#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
B006 - Code-Metriken
====================
Analysiert Code-Dateien: LOC, Komplexitaet, Sprachen.

Output: JSON mit Code-Statistiken
"""

import os
import json
import sys
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def analyze_code(root_path: str) -> dict:
    """Analysiert Code-Dateien eines Systems."""
    
    root = Path(root_path)
    if not root.exists():
        return {"error": f"Pfad existiert nicht: {root_path}"}
    
    result = {
        "system_path": str(root),
        "scan_date": datetime.now().isoformat(),
        "summary": {},
        "by_language": {},
        "largest_files": [],
        "complexity_indicators": {},
        "score": 0.0
    }
    
    # Sprach-Mapping
    lang_map = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".sh": "Shell",
        ".bat": "Batch",
        ".ps1": "PowerShell",
        ".sql": "SQL",
        ".json": "JSON",
        ".yaml": "YAML",
        ".yml": "YAML",
    }
    
    # Zaehler pro Sprache
    lang_stats = defaultdict(lambda: {
        "files": 0,
        "lines_total": 0,
        "lines_code": 0,
        "lines_comment": 0,
        "lines_blank": 0
    })
    
    all_files = []
    
    for f in root.rglob("*"):
        if not f.is_file():
            continue
        if "__pycache__" in str(f) or "node_modules" in str(f):
            continue
        if f.suffix not in lang_map:
            continue
        
        lang = lang_map[f.suffix]
        
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            
            total = len(lines)
            blank = sum(1 for l in lines if not l.strip())
            
            # Einfache Kommentar-Erkennung
            if lang == "Python":
                comments = sum(1 for l in lines if l.strip().startswith('#'))
            elif lang in ["JavaScript", "TypeScript"]:
                comments = sum(1 for l in lines if l.strip().startswith('/'))
            elif lang in ["Shell", "PowerShell"]:
                comments = sum(1 for l in lines if l.strip().startswith('#'))
            elif lang == "SQL":
                comments = sum(1 for l in lines if l.strip().startswith('--'))
            else:
                comments = 0
            
            code = total - blank - comments
            
            lang_stats[lang]["files"] += 1
            lang_stats[lang]["lines_total"] += total
            lang_stats[lang]["lines_code"] += code
            lang_stats[lang]["lines_comment"] += comments
            lang_stats[lang]["lines_blank"] += blank
            
            all_files.append({
                "path": str(f.relative_to(root)),
                "language": lang,
                "lines": total,
                "code_lines": code
            })
            
        except Exception as e:
            continue
    
    # Konvertiere zu dict
    result["by_language"] = dict(lang_stats)
    
    # Summary
    total_files = sum(s["files"] for s in lang_stats.values())
    total_lines = sum(s["lines_total"] for s in lang_stats.values())
    total_code = sum(s["lines_code"] for s in lang_stats.values())
    total_comments = sum(s["lines_comment"] for s in lang_stats.values())
    
    result["summary"] = {
        "total_code_files": total_files,
        "total_lines": total_lines,
        "total_code_lines": total_code,
        "total_comment_lines": total_comments,
        "comment_ratio": round(total_comments / max(total_code, 1) * 100, 1),
        "languages_used": list(lang_stats.keys())
    }
    
    # Groesste Dateien
    all_files.sort(key=lambda x: x["lines"], reverse=True)
    result["largest_files"] = all_files[:10]
    
    # Komplexitaets-Indikatoren (vereinfacht)
    complexity = {
        "large_files_500plus": sum(1 for f in all_files if f["lines"] > 500),
        "medium_files_200_500": sum(1 for f in all_files if 200 <= f["lines"] <= 500),
        "small_files_under_200": sum(1 for f in all_files if f["lines"] < 200),
    }
    
    # Durchschnittliche Dateigroesse
    if total_files > 0:
        complexity["avg_lines_per_file"] = round(total_lines / total_files, 1)
    else:
        complexity["avg_lines_per_file"] = 0
    
    result["complexity_indicators"] = complexity
    
    # Score berechnen
    # Gute Werte: Comment-Ratio > 10%, keine riesigen Dateien, moderate Groesse
    score = 3.0  # Basis
    
    if result["summary"]["comment_ratio"] >= 15:
        score += 1.0
    elif result["summary"]["comment_ratio"] >= 10:
        score += 0.5
    
    if complexity["large_files_500plus"] == 0:
        score += 0.5
    elif complexity["large_files_500plus"] > 5:
        score -= 0.5
    
    if 50 <= complexity["avg_lines_per_file"] <= 200:
        score += 0.5
    
    result["score"] = min(5.0, max(1.0, round(score, 2)))
    
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python B006_code_metrics.py <system_path> [output_json]")
        sys.exit(1)
    
    result = analyze_code(sys.argv[1])
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Ergebnis gespeichert: {output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
