#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
B008 - Alter-Analyse
====================
Analysiert Aktualitaet und letzte Aenderungen.

Output: JSON mit Zeitstempel-Analyse
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

def analyze_age(root_path: str) -> dict:
    """Analysiert Alter und Aktivitaet eines Systems."""
    
    root = Path(root_path)
    if not root.exists():
        return {"error": f"Pfad existiert nicht: {root_path}"}
    
    now = datetime.now()
    
    result = {
        "system_path": str(root),
        "scan_date": now.isoformat(),
        "activity": {},
        "recently_modified": [],
        "oldest_files": [],
        "age_distribution": {},
        "summary": {},
        "score": 0.0
    }
    
    all_files = []
    mod_times = []
    
    # Zeitrahmen
    day_ago = now - timedelta(days=1)
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    quarter_ago = now - timedelta(days=90)
    year_ago = now - timedelta(days=365)
    
    age_buckets = {
        "last_24h": 0,
        "last_week": 0,
        "last_month": 0,
        "last_quarter": 0,
        "last_year": 0,
        "older": 0
    }
    
    for f in root.rglob("*"):
        if not f.is_file():
            continue
        if "__pycache__" in str(f) or "node_modules" in str(f):
            continue
        if any(part.startswith('.') for part in f.relative_to(root).parts):
            continue
        
        try:
            stat = f.stat()
            mtime = datetime.fromtimestamp(stat.st_mtime)
            mod_times.append(mtime)
            
            all_files.append({
                "path": str(f.relative_to(root)),
                "modified": mtime.isoformat(),
                "size": stat.st_size
            })
            
            # Einsortieren
            if mtime > day_ago:
                age_buckets["last_24h"] += 1
            elif mtime > week_ago:
                age_buckets["last_week"] += 1
            elif mtime > month_ago:
                age_buckets["last_month"] += 1
            elif mtime > quarter_ago:
                age_buckets["last_quarter"] += 1
            elif mtime > year_ago:
                age_buckets["last_year"] += 1
            else:
                age_buckets["older"] += 1
                
        except:
            continue
    
    result["age_distribution"] = age_buckets
    
    # Sortiere nach Aenderungszeit
    all_files.sort(key=lambda x: x["modified"], reverse=True)
    result["recently_modified"] = all_files[:15]
    
    all_files.sort(key=lambda x: x["modified"])
    result["oldest_files"] = all_files[:10]
    
    # Aktivitaets-Metriken
    if mod_times:
        newest = max(mod_times)
        oldest = min(mod_times)
        
        result["activity"] = {
            "newest_file": newest.isoformat(),
            "oldest_file": oldest.isoformat(),
            "age_span_days": (newest - oldest).days,
            "last_activity_days_ago": (now - newest).days
        }
        
        # Summary
        total = len(all_files)
        recent = age_buckets["last_24h"] + age_buckets["last_week"]
        
        result["summary"] = {
            "total_files_analyzed": total,
            "files_modified_last_week": recent,
            "activity_ratio": round(recent / max(total, 1) * 100, 1),
            "is_active": (now - newest).days < 7,
            "is_maintained": (now - newest).days < 30
        }
    else:
        result["activity"] = {"error": "Keine Dateien gefunden"}
        result["summary"] = {"total_files_analyzed": 0}
    
    # Score berechnen
    # Aktiv = gut, aber auch Stabilitaet ist gut
    score = 3.0
    
    if result["summary"].get("is_active"):
        score += 1.5
    elif result["summary"].get("is_maintained"):
        score += 1.0
    
    # Gute Verteilung: Nicht alles uralt, nicht alles brandneu
    if age_buckets["last_month"] > 0 and age_buckets["last_quarter"] > 0:
        score += 0.5
    
    result["score"] = min(5.0, max(1.0, round(score, 2)))
    
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python B008_age_analysis.py <system_path> [output_json]")
        sys.exit(1)
    
    result = analyze_age(sys.argv[1])
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Ergebnis gespeichert: {output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
