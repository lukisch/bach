#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (c) 2026 Lukas Geiger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
Tool: c_json_registry_cleaner
Version: 1.0.0
Author: BACH Team
Created: 2026-02-04
Updated: 2026-02-04
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version c_json_registry_cleaner

Description:
    [Beschreibung hinzufügen]

Usage:
    python c_json_registry_cleaner.py [args]
"""

__version__ = "1.0.0"
__author__ = "BACH Team"

"""
json_registry_cleaner.py - Analysiert JSON-Dateien und vergleicht mit Bach DB

Heuristisches Matching:
- Dateiname enthält Begriff → DB-Tabelle/Kategorie Match
- Übergeordnete Registry-JSONs erkennen
- Duplikate/Untergeordnete löschen

Usage:
    python json_registry_cleaner.py <ordner> --dry-run
    python json_registry_cleaner.py <ordner> --delete
    python json_registry_cleaner.py <ordner> --tree
"""

import sys
import io
import json
import sqlite3
import argparse
from pathlib import Path
from collections import defaultdict

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BACH_DB = Path(r"C:\Users\User\OneDrive\KI&AI\BACH_STREAM\PRODUCTION\CONSTRUCTION_AREA\BACH_v1\Bach\bach.db")

# Heuristische Mapping: Begriff im Dateinamen → Kategorie/Aktion
DELETE_PATTERNS = {
    # Bereits in DB integriert
    'registry': 'In DB: connections/tools/agents',
    'config': 'In DB: system_config',
    'skill_registry': 'In DB: skills Tabelle',
    'tool_registry': 'In DB: tools Tabelle',
    'system-registry': 'In DB: system_config',
    'system-components': 'In DB: system_config',
    'system-inventory': 'In DB: system_config',
    'system-resources': 'In DB: system_config',
    'master_config': 'In DB: system_config',
    'master_registry': 'In DB: connections',
    'master_communication': 'In DB: connections',
    'external-tools': 'In DB: tools (external)',
    
    # Backup/Archiv - veraltet
    'backup': 'Backup-Datei (veraltet)',
    '_backup': 'Backup-Datei (veraltet)',
    'archiv_registry': 'Archiv-Registry (veraltet)',
    
    # Timeline/Logs - temporär
    'timeline_': 'Timeline-Log (temporär)',
    'healing_protocol': 'Healing-Log (temporär)',
    'healing_report': 'Healing-Report (temporär)',
    
    # Spezifische veraltete
    'boot-config': 'Boot-Config (RecludOS-spezifisch)',
    'boot-report': 'Boot-Report (temporär)',
    'shutdown-protocol': 'Shutdown-Protocol (RecludOS)',
    'shutdown-task': 'Shutdown-Tasks (RecludOS)',
    'startup-scripts': 'Startup-Scripts (RecludOS)',
    'triggers': 'Triggers (RecludOS)',
    'intervals': 'Intervals (RecludOS)',
    'micro-routines': 'Micro-Routines (RecludOS)',
    
    # Queue/Job - temporär
    'pending_job': 'Pending Job (temporär)',
    'queue_config': 'Queue-Config (RecludOS)',
    
    # Watcher-Daten - temporär
    'active_tasks': 'Watcher-Daten (temporär)',
    'actor_status': 'Watcher-Daten (temporär)',
    'actor_performance': 'Watcher-Daten (temporär)',
    'actor_profiles': 'Watcher-Daten (temporär)',
    'current_session': 'Session-Daten (temporär)',
    'token_budget': 'Token-Daten (temporär)',
    'delegation_decisions': 'Delegation-Daten (temporär)',
    'delegation_patterns': 'Delegation-Daten (temporär)',
    
    # Beispiele/Templates
    'examples_': 'Beispiel-Datei',
    
    # Scan-Results - temporär
    'scan_result': 'Scan-Result (temporär)',
    'snippet_index': 'Snippet-Index (temporär)',
    'standalone_candidates': 'Scan-Kandidaten (temporär)',
    'last_partner_scan': 'Scan-Result (temporär)',
    'integration_suggestions': 'Scan-Suggestions (temporär)',
    'software_registry': 'Software-Registry (veraltet)',
    
    # Protokolle - RecludOS-spezifisch
    'protocol.json': 'Kommunikations-Protokoll (RecludOS)',
    'INDEX.json': 'Index (RecludOS)',
    
    # Receipts - temporär
    'receipts_rcp': 'Receipt (temporär)',
    
    # Papierkorb
    'papierkorb_registry': 'Papierkorb-Registry (RecludOS)',
    'papierkorb_tracking': 'Papierkorb-Tracking (temporär)',
    
    # Path/Migration
    'path_migration': 'Path-Migration (einmalig)',
    
    # Dictionary/Locale
    'dictionary': 'Dictionary (RecludOS)',
    'locales_': 'Locale (RecludOS)',
    
    # Export/Circle
    'export_circle': 'Export-Config (RecludOS)',
    'extensions_': 'Extensions (RecludOS)',
    
    # Network
    'network-inventory': 'Network-Inventory (veraltet)',
    'ollama-memory': 'Ollama-Memory (veraltet)',
    'terminal-chat': 'Terminal-Chat (veraltet)',
    
    # Evolution/Learning
    'evolution_config': 'Evolution-Config (RecludOS)',
    'evolution_tools_config': 'Evolution-Tools (RecludOS)',
    'survival_success_criteria': 'Evolution-Criteria (RecludOS)',
    'lessons-learned': 'Lessons-Learned (RecludOS)',
    'learning-routines_config': 'Learning-Config (RecludOS)',
    'process-watcher_config': 'Watcher-Config (RecludOS)',
    'success-watcher_config': 'Watcher-Config (RecludOS)',
    'token-watcher_config': 'Watcher-Config (RecludOS)',
    'pricing_config': 'Pricing-Config (RecludOS)',
    'orchestration_config': 'Orchestration-Config (RecludOS)',
    
    # Sonstige Configs
    'document_output_rules': 'Output-Rules (RecludOS)',
    'excluded_folders': 'Excluded-Folders (RecludOS)',
    'ignore_patterns': 'Ignore-Patterns (RecludOS)',
    'last_backup_status': 'Backup-Status (temporär)',
}

# Diese behalten (wichtig/einzigartig)
KEEP_PATTERNS = [
    'identity.json',  # Wichtig
]


def get_db_tables():
    """Holt DB-Tabellen und Inhalte"""
    if not BACH_DB.exists():
        return {}
    
    conn = sqlite3.connect(BACH_DB)
    cursor = conn.cursor()
    
    # Tabellen auflisten
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    # Counts
    counts = {}
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        counts[table] = cursor.fetchone()[0]
    
    conn.close()
    return counts


def analyze_json_files(directory: Path):
    """Analysiert alle JSON-Dateien"""
    json_files = list(directory.glob("*.json"))
    
    to_delete = []
    to_keep = []
    
    for f in json_files:
        name = f.name
        
        # Prüfe KEEP Patterns
        if any(keep in name for keep in KEEP_PATTERNS):
            to_keep.append((f, "Wichtig/Einzigartig"))
            continue
        
        # Prüfe DELETE Patterns
        matched = False
        for pattern, reason in DELETE_PATTERNS.items():
            if pattern in name:
                to_delete.append((f, reason))
                matched = True
                break
        
        if not matched:
            to_keep.append((f, "Nicht zugeordnet"))
    
    return to_delete, to_keep


def print_tree(to_delete, to_keep):
    """Gibt Baumstruktur aus"""
    print("\n" + "=" * 70)
    print("  JSON-ANALYSE")
    print("=" * 70)
    
    # Gruppiere nach Grund
    delete_groups = defaultdict(list)
    for f, reason in to_delete:
        delete_groups[reason].append(f.name)
    
    print(f"\n  ZUM LÖSCHEN ({len(to_delete)} Dateien):")
    print("  " + "-" * 60)
    for reason, files in sorted(delete_groups.items()):
        print(f"\n  [{reason}] ({len(files)})")
        for name in sorted(files)[:5]:  # Max 5 pro Gruppe
            print(f"    ├─ {name}")
        if len(files) > 5:
            print(f"    └─ ... und {len(files) - 5} weitere")
    
    print(f"\n\n  VERBLEIBEND ({len(to_keep)} Dateien):")
    print("  " + "-" * 60)
    for f, reason in sorted(to_keep, key=lambda x: x[0].name):
        print(f"    📄 {f.name}")
        print(f"       └─ {reason}")
    
    print("\n" + "=" * 70)


def delete_files(to_delete, dry_run=False):
    """Löscht die Dateien"""
    print(f"\n{'[DRY-RUN] ' if dry_run else ''}Lösche {len(to_delete)} Dateien...")
    
    count = 0
    for f, reason in to_delete:
        if not dry_run:
            f.unlink()
        count += 1
    
    print(f"{'Würde löschen' if dry_run else 'Gelöscht'}: {count} Dateien")
    return count


def main():
    parser = argparse.ArgumentParser(description="JSON Registry Cleaner")
    parser.add_argument("directory", help="Ordner mit JSON-Dateien")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Nur anzeigen")
    parser.add_argument("--delete", "-d", action="store_true", help="Löschen ausführen")
    parser.add_argument("--tree", "-t", action="store_true", help="Baumansicht")
    
    args = parser.parse_args()
    directory = Path(args.directory)
    
    if not directory.exists():
        print(f"Ordner nicht gefunden: {directory}")
        sys.exit(1)
    
    # DB-Status
    db_counts = get_db_tables()
    if db_counts:
        print(f"\n  Bach DB: {sum(db_counts.values())} Einträge in {len(db_counts)} Tabellen")
    
    # Analyse
    to_delete, to_keep = analyze_json_files(directory)
    
    # Ausgabe
    print_tree(to_delete, to_keep)
    
    # Löschen
    if args.delete and not args.dry_run:
        delete_files(to_delete, dry_run=False)
    elif args.dry_run:
        delete_files(to_delete, dry_run=True)


if __name__ == "__main__":
    main()
