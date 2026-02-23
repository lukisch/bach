#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
B003 - Verzeichnistiefe
=======================
Analysiert die Struktur und Tiefe des Verzeichnisbaums.

Output: JSON mit Tiefenmetriken und Strukturanalyse
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def analyze_directory_depth(root_path: str) -> dict:
    """Analysiert Verzeichnistiefe und -struktur."""
    
    root = Path(root_path)
    if not root.exists():
        return {"error": f"Pfad existiert nicht: {root_path}"}
    
    result = {
        "system_path": str(root),
        "scan_date": datetime.now().isoformat(),
        "metrics": {},
        "depth_distribution": defaultdict(int),
        "deepest_paths": [],
        "structure_tree": {}
    }
    
    depths = []
    all_dirs = []
    files_per_level = defaultdict(int)
    dirs_per_level = defaultdict(int)
    
    for item in root.rglob("*"):
        # Ignoriere versteckte und temp
        rel_path = item.relative_to(root)
        if any(part.startswith('.') for part in rel_path.parts):
            continue
        if "__pycache__" in str(item) or "node_modules" in str(item):
            continue
        
        depth = len(rel_path.parts)
        
        if item.is_dir():
            dirs_per_level[depth] += 1
            all_dirs.append({
                "path": str(rel_path),
                "depth": depth,
                "items": len(list(item.iterdir())) if item.exists() else 0
            })
        else:
            files_per_level[depth] += 1
            depths.append(depth)
    
    # Metriken berechnen
    if depths:
        result["metrics"] = {
            "max_depth": max(depths),
            "min_depth": min(depths),
            "avg_depth": round(sum(depths) / len(depths), 2),
            "total_files": len(depths),
            "total_dirs": len(all_dirs)
        }
    else:
        result["metrics"] = {
            "max_depth": 0,
            "min_depth": 0,
            "avg_depth": 0,
            "total_files": 0,
            "total_dirs": 0
        }
    
    # Tiefenverteilung
    for d in depths:
        result["depth_distribution"][str(d)] += 1
    result["depth_distribution"] = dict(result["depth_distribution"])
    
    # Tiefste Pfade
    sorted_dirs = sorted(all_dirs, key=lambda x: x["depth"], reverse=True)
    result["deepest_paths"] = sorted_dirs[:5]
    
    # Breiteste Verzeichnisse (meiste direkte Kinder)
    sorted_by_items = sorted(all_dirs, key=lambda x: x["items"], reverse=True)
    result["widest_dirs"] = sorted_by_items[:5]
    
    # Struktur-Baum (Level 0-2)
    tree = {}
    for item in root.iterdir():
        if item.name.startswith('.') or item.name in ["__pycache__", "node_modules"]:
            continue
        if item.is_dir():
            subtree = {}
            for subitem in item.iterdir():
                if subitem.name.startswith('.'):
                    continue
                subtree[subitem.name] = "dir" if subitem.is_dir() else "file"
            tree[item.name + "/"] = subtree
        else:
            tree[item.name] = "file"
    result["structure_tree"] = tree
    
    # Bewertung
    max_depth = result["metrics"]["max_depth"]
    avg_depth = result["metrics"]["avg_depth"]
    
    # Score: Ideal ist 2-4 Ebenen Tiefe, >6 ist zu tief
    if max_depth <= 4:
        depth_score = 5.0
    elif max_depth <= 6:
        depth_score = 4.0
    elif max_depth <= 8:
        depth_score = 3.0
    else:
        depth_score = 2.0
    
    result["evaluation"] = {
        "depth_score": depth_score,
        "recommendation": "Gut strukturiert" if depth_score >= 4 else 
                         "Ueberdenke tiefe Verschachtelung" if depth_score >= 3 else
                         "Zu tiefe Struktur - Refactoring empfohlen"
    }
    
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python B003_directory_depth.py <system_path> [output_json]")
        sys.exit(1)
    
    result = analyze_directory_depth(sys.argv[1])
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Ergebnis gespeichert: {output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
