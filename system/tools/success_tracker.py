#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Tool: success_tracker
Version: 1.0.0
Author: BACH Team
Created: 2026-02-04
Updated: 2026-02-04
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version success_tracker

Description:
    [Beschreibung hinzufügen]

Usage:
    python success_tracker.py [args]
"""

__version__ = "1.0.0"
__author__ = "BACH Team"

"""
Success Tracker - Basis-Implementation
RecludOS v3.1.1

Trackt Erfolgsmetriken fuer die 6 Akteur-Kategorien.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Pfade
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
PERFORMANCE_FILE = DATA_DIR / "actor_performance.json"

# 6 Akteur-Kategorien
CATEGORIES = {
    "online": "Online-Tools",
    "tools": "Tools & Scripts", 
    "os": "Operating System",
    "geist": "Operierende AI (Claude)",
    "ais": "Weitere AIs",
    "user": "User"
}

def load_performance():
    """Laedt Performance-Daten oder erstellt Default."""
    if PERFORMANCE_FILE.exists():
        with open(PERFORMANCE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # Default-Struktur
    return {
        "version": "3.0.0",
        "last_updated": datetime.now().isoformat(),
        "categories": {
            cat: {
                "name": name,
                "total_tasks": 0,
                "completed": 0,
                "failed": 0,
                "completion_rate": 0.0,
                "fitness": 0.0
            }
            for cat, name in CATEGORIES.items()
        },
        "task_log": []
    }

def save_performance(data):
    """Speichert Performance-Daten."""
    DATA_DIR.mkdir(exist_ok=True)
    data["last_updated"] = datetime.now().isoformat()
    with open(PERFORMANCE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def calculate_fitness(cat_data):
    """Berechnet Fitness-Score (0-1)."""
    if cat_data["total_tasks"] == 0:
        return 0.0
    
    completion = cat_data["completed"] / cat_data["total_tasks"]
    # Vereinfachte Formel (nur Completion)
    # TODO: Efficiency, Quality, Reliability hinzufuegen
    return round(completion, 3)

def cmd_status():
    """Zeigt Status aller Kategorien."""
    data = load_performance()
    
    print("\n[SUCCESS-WATCHER] Akteur-Performance")
    print("=" * 50)
    
    for cat_id, cat_data in data["categories"].items():
        total = cat_data["total_tasks"]
        completed = cat_data["completed"]
        fitness = cat_data["fitness"]
        
        if total > 0:
            bar_len = int(fitness * 10)
            bar = "[" + "#" * bar_len + "-" * (10 - bar_len) + "]"
        else:
            bar = "[----------]"
        
        print(f"  {CATEGORIES[cat_id]:25} {bar} {fitness:.1%} ({completed}/{total})")
    
    print("=" * 50)
    print(f"  Letztes Update: {data['last_updated'][:19]}")
    print()

def cmd_log(category, task_desc, success):
    """Loggt einen Task."""
    if category not in CATEGORIES:
        print(f"[ERR] Unbekannte Kategorie: {category}")
        print(f"      Verfuegbar: {', '.join(CATEGORIES.keys())}")
        return
    
    success_bool = success.lower() in ['true', '1', 'yes', 'ja', 'ok']
    
    data = load_performance()
    cat_data = data["categories"][category]
    
    # Update Statistiken
    cat_data["total_tasks"] += 1
    if success_bool:
        cat_data["completed"] += 1
    else:
        cat_data["failed"] += 1
    
    cat_data["completion_rate"] = cat_data["completed"] / cat_data["total_tasks"]
    cat_data["fitness"] = calculate_fitness(cat_data)
    
    # Log-Eintrag
    data["task_log"].append({
        "timestamp": datetime.now().isoformat(),
        "category": category,
        "task": task_desc,
        "success": success_bool
    })
    
    # Nur letzte 100 Eintraege behalten
    data["task_log"] = data["task_log"][-100:]
    
    save_performance(data)
    
    status = "[OK]" if success_bool else "[FAIL]"
    print(f"{status} Task geloggt: {CATEGORIES[category]} - {task_desc}")

def cmd_recommend(task_type):
    """Empfiehlt beste Kategorie fuer Task-Typ."""
    # Statisches Mapping (TODO: dynamisch aus Performance-Daten)
    recommendations = {
        "entscheidung": "user",
        "decision": "user",
        "analyse": "geist",
        "analysis": "geist",
        "batch": "tools",
        "script": "tools",
        "zusammenfassung": "os",
        "summary": "os",
        "recherche": "ais",
        "research": "ais",
        "qr": "online",
        "convert": "online",
        "excel": "ais",
        "ui": "user",
        "klick": "user"
    }
    
    task_lower = task_type.lower()
    
    for key, cat in recommendations.items():
        if key in task_lower:
            print(f"[RECOMMEND] Fuer '{task_type}': {CATEGORIES[cat]}")
            return
    
    print(f"[RECOMMEND] Fuer '{task_type}': {CATEGORIES['geist']} (Default)")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python success_tracker.py status")
        print("  python success_tracker.py log <kategorie> <task> <success>")
        print("  python success_tracker.py recommend <task_type>")
        print()
        print(f"Kategorien: {', '.join(CATEGORIES.keys())}")
        return
    
    cmd = sys.argv[1].lower()
    
    if cmd == "status":
        cmd_status()
    elif cmd == "log" and len(sys.argv) >= 5:
        cmd_log(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "recommend" and len(sys.argv) >= 3:
        cmd_recommend(sys.argv[2])
    else:
        print("[ERR] Unbekannter Befehl oder fehlende Parameter")

if __name__ == "__main__":
    main()
