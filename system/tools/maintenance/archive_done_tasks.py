#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
archive_done_tasks.py - Verschiebt done-Tasks aus tasks.json nach _done.json

Verwendung:
    python archive_done_tasks.py          # Dry-run (zeigt was passieren würde)
    python archive_done_tasks.py --apply  # Wirklich ausführen
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Windows Console Encoding Fix
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BATCH_DIR = Path(__file__).parent.parent  # Eine Ebene höher (_BATCH)
TASKS_FILE = BATCH_DIR / "DATA" / "system-tasks.json"
DONE_FILE = BATCH_DIR / "DATA" / "LONGTERM-MEMORY" / "_done.json"

def main():
    apply = "--apply" in sys.argv
    
    # tasks.json laden
    tasks_data = json.loads(TASKS_FILE.read_text(encoding='utf-8'))
    tasks = tasks_data.get('tasks', [])
    
    # Done-Tasks finden
    done_tasks = [t for t in tasks if t.get('status') == 'done']
    open_tasks = [t for t in tasks if t.get('status') != 'done']
    
    print(f"Tasks gesamt: {len(tasks)}")
    print(f"Done-Tasks: {len(done_tasks)}")
    print(f"Open-Tasks: {len(open_tasks)}")
    print()
    
    if not done_tasks:
        print("Keine done-Tasks zum Archivieren.")
        return
    
    if not apply:
        print("DRY-RUN: Würde folgende Tasks archivieren:")
        for t in done_tasks[:10]:
            print(f"  - {t.get('id')}: {t.get('task', '')[:40]}")
        if len(done_tasks) > 10:
            print(f"  ... und {len(done_tasks) - 10} weitere")
        print()
        print("Mit --apply ausführen um wirklich zu archivieren.")
        return
    
    # _done.json laden
    if DONE_FILE.exists():
        done_data = json.loads(DONE_FILE.read_text(encoding='utf-8'))
    else:
        done_data = {"version": "1.0", "tasks": []}
    
    # Format prüfen (alte Version war Liste)
    if isinstance(done_data, list):
        done_data = {"version": "1.0", "tasks": done_data}
    
    # Done-Tasks konvertieren und anhängen
    for t in done_tasks:
        entry = {
            "id": t.get('id', f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
            "tool": t.get('component', '_BATCH'),
            "task": t.get('task', ''),
            "completed_at": t.get('completed_at', datetime.now().isoformat()),
            "completed_by": "user" if t.get('source') == 'user' else 'claude',
            "session_id": "archive_" + datetime.now().strftime('%Y%m%d'),
            "aufwand": t.get('aufwand', 'mittel'),
            "note": t.get('note', '')
        }
        done_data['tasks'].append(entry)
    
    # Speichern
    DONE_FILE.write_text(json.dumps(done_data, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"✅ {len(done_tasks)} Tasks nach _done.json archiviert")
    
    # tasks.json aktualisieren (nur open-Tasks behalten)
    tasks_data['tasks'] = open_tasks
    tasks_data['meta']['last_updated'] = datetime.now().isoformat()
    TASKS_FILE.write_text(json.dumps(tasks_data, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"✅ tasks.json bereinigt ({len(open_tasks)} Tasks verbleiben)")
    
    # Statistik
    new_size = TASKS_FILE.stat().st_size / 1024
    print(f"📊 Neue Dateigröße: {new_size:.1f} KB")

if __name__ == "__main__":
    main()
