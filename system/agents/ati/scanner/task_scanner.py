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
ATI Task Scanner v1.3.0
=====================
Scannt Software-Ordner nach AUFGABEN.txt und synchronisiert mit bach.db

Migriert von: scanner/task_scanner.py (Task 81)
Original: _BATCH/scanner.py

v1.3.0 (2026-02-01): Migration auf bach.db - Tabellen umbenannt zu ati_*
v1.2.1 (2026-01-25): Duplikaterkennung - Prueft vor INSERT ob task_text bereits existiert
"""

import sqlite3
import hashlib
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import json

class TaskScanner:
    """Scannt dezentrale AUFGABEN.txt Dateien und synchronisiert mit DB."""
    
    def __init__(self, db_path: Path, config: Optional[Dict] = None):
        self.db_path = db_path
        self.config = config or self._load_config_from_db()
        self.base_path = Path(self.config.get('base_path', '.'))
        self.task_files = self.config.get('task_files', ['AUFGABEN.txt'])
        self.ignore_folders = self.config.get('ignore_folders', [])
        self.scan_folders = self.config.get('scan_folders', [])
        
    def _load_config_from_db(self) -> Dict:
        """Laedt Konfiguration aus ati_scan_config Tabelle."""
        config = {}
        try:
            conn = sqlite3.connect(self.db_path)
            rows = conn.execute("SELECT key, value FROM ati_scan_config").fetchall()
            for key, value in rows:
                try:
                    config[key] = json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    config[key] = value
            conn.close()
        except Exception as e:
            print(f"[WARN] Config-Laden fehlgeschlagen: {e}")
        return config
    
    def scan_all(self) -> Dict:
        """Scannt alle konfigurierten Ordner."""
        result = {
            'tools_scanned': 0,
            'tasks_found': 0,
            'tasks_new': 0,
            'tasks_updated': 0,
            'tasks_removed': 0,
            'errors': []
        }
        
        conn = sqlite3.connect(self.db_path)
        start_time = datetime.now()
        
        # Scan-Run protokollieren
        cursor = conn.execute(
            "INSERT INTO ati_scan_runs (started_at, triggered_by) VALUES (?, 'manual')",
            (start_time.isoformat(),)
        )
        run_id = cursor.lastrowid
        conn.commit()
        
        print(f"[SCAN] Scanne {self.base_path}...")
        print(f"[SCAN] Ordner: {self.scan_folders}")
        
        for folder in self.scan_folders:
            folder_path = self.base_path / folder
            if folder_path.exists():
                self._scan_folder(folder_path, conn, result)
            else:
                print(f"[WARN] Ordner nicht gefunden: {folder_path}")
        
        # Scan-Run abschliessen
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        conn.execute("""
            UPDATE ati_scan_runs
            SET finished_at = ?, duration_seconds = ?,
                tools_scanned = ?, tasks_found = ?,
                tasks_new = ?, tasks_updated = ?, tasks_removed = ?,
                errors = ?
            WHERE id = ?
        """, (
            end_time.isoformat(),
            duration,
            result['tools_scanned'],
            result['tasks_found'],
            result['tasks_new'],
            result['tasks_updated'],
            result['tasks_removed'],
            json.dumps(result['errors']) if result['errors'] else None,
            run_id
        ))
        
        conn.commit()
        conn.close()
        
        print(f"[OK] Scan abgeschlossen in {duration:.2f}s")
        print(f"     Tools: {result['tools_scanned']}, Tasks: {result['tasks_found']}")
        print(f"     Neu: {result['tasks_new']}, Aktualisiert: {result['tasks_updated']}")
        
        return result
    
    def _scan_folder(self, folder: Path, conn, result: Dict, depth: int = 0):
        """Scannt einen Ordner rekursiv."""
        if depth > 5:  # Max Tiefe
            return
            
        try:
            for item in folder.iterdir():
                if item.is_dir():
                    if item.name in self.ignore_folders:
                        continue
                    if item.name.startswith('_') or item.name.startswith('.'):
                        continue
                    
                    # Pruefen ob AUFGABEN.txt existiert
                    for task_file in self.task_files:
                        aufgaben_path = item / task_file
                        if aufgaben_path.exists():
                            self._process_tool(item, aufgaben_path, conn, result)
                            break
                    
                    # Rekursiv scannen
                    self._scan_folder(item, conn, result, depth + 1)
                    
        except PermissionError:
            result['errors'].append(f"Zugriff verweigert: {folder}")
    
    def _process_tool(self, tool_path: Path, aufgaben_path: Path, conn, result: Dict):
        """Verarbeitet ein Tool mit AUFGABEN.txt."""
        result['tools_scanned'] += 1
        tool_name = tool_path.name
        
        # Tool-Registry synchronisieren
        tool_id = self._register_tool(tool_path, conn)
        
        # Datei-Hash berechnen
        content = aufgaben_path.read_text(encoding='utf-8', errors='replace')
        file_hash = hashlib.md5(content.encode()).hexdigest()
        
        # Pruefen ob Datei geaendert wurde
        existing = conn.execute(
            "SELECT file_hash FROM ati_tasks WHERE source_file = ? LIMIT 1",
            (str(aufgaben_path),)
        ).fetchone()
        
        if existing and existing[0] == file_hash:
            # Keine Aenderung - Tasks zaehlen
            count = conn.execute(
                "SELECT COUNT(*) FROM ati_tasks WHERE source_file = ?",
                (str(aufgaben_path),)
            ).fetchone()[0]
            result['tasks_found'] += count
            return
        
        # Tasks parsen
        tasks = self._parse_aufgaben(content)
        
        # Alte Tasks entfernen
        old_count = conn.execute(
            "SELECT COUNT(*) FROM ati_tasks WHERE source_file = ?",
            (str(aufgaben_path),)
        ).fetchone()[0]
        
        conn.execute("DELETE FROM ati_tasks WHERE source_file = ?", (str(aufgaben_path),))
        
        if old_count > 0:
            result['tasks_removed'] += old_count
        
        # Neue Tasks einfuegen
        file_mtime = datetime.fromtimestamp(aufgaben_path.stat().st_mtime).isoformat()
        
        duplicates_skipped = 0
        for idx, task in enumerate(tasks, 1):
            # Status bleibt deutsch (Schema unverändert)
            status = task.get('status', 'offen')
            aufwand = task.get('aufwand', 'mittel')
            task_text = task['text']
            
            # DUPLIKATERKENNUNG: Pruefen ob task_text bereits existiert (v1.2.1)
            # Gleicher Task-Text in anderem Tool ist erlaubt, aber gleicher Text
            # im selben Tool (andere source_file) wird uebersprungen
            duplicate = conn.execute("""
                SELECT id, source_file FROM ati_tasks 
                WHERE task_text = ? AND tool_name = ?
                LIMIT 1
            """, (task_text, tool_name)).fetchone()
            
            if duplicate:
                duplicates_skipped += 1
                continue  # Task bereits vorhanden, ueberspringe

            conn.execute("""
                INSERT INTO ati_tasks
                (tool_name, tool_path, task_text, aufwand, status, priority_score,
                 source_file, line_number, file_hash, last_modified, synced_at, is_synced)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            """, (
                tool_name,
                str(tool_path),
                task_text,
                aufwand,
                status,
                task.get('priority', 50),
                str(aufgaben_path),
                idx,
                file_hash,
                file_mtime,
                datetime.now().isoformat()
            ))
            
            result['tasks_found'] += 1
            if existing:
                result['tasks_updated'] += 1
            else:
                result['tasks_new'] += 1
        
        if duplicates_skipped > 0:
            print(f"     [~] {tool_name}: {duplicates_skipped} Duplikate uebersprungen")
        
        # Tool-Registry-Update (Last Scan & Task Count)
        conn.execute("""
            UPDATE ati_tool_registry
            SET last_scan = ?, task_count = ?, updated_at = ?
            WHERE id = ?
        """, (datetime.now().isoformat(), len(tasks), datetime.now().isoformat(), tool_id))
        
        conn.commit()
        print(f"     [+] {tool_name}: {len(tasks)} Tasks")
    
    def _register_tool(self, tool_path: Path, conn) -> int:
        """Registriert Tool in ati_tool_registry, gibt ID zurueck."""
        existing = conn.execute(
            "SELECT id FROM ati_tool_registry WHERE path = ?",
            (str(tool_path),)
        ).fetchone()

        if existing:
            return existing[0]

        # Pruefen ob TEST.txt oder TESTERGEBNIS.txt existiert
        has_test = any((tool_path / f).exists() for f in ['TEST.txt', 'Test.txt'])
        has_feedback = any((tool_path / f).exists() for f in ['TESTERGEBNIS.txt', 'AENDERUNGEN.txt'])

        cursor = conn.execute("""
            INSERT INTO ati_tool_registry (name, path, has_aufgaben, has_test, has_feedback, created_at)
            VALUES (?, ?, 1, ?, ?, ?)
        """, (
            tool_path.name,
            str(tool_path),
            1 if has_test else 0,
            1 if has_feedback else 0,
            datetime.now().isoformat()
        ))
        conn.commit()
        return cursor.lastrowid
    
    def _parse_aufgaben(self, content: str) -> List[Dict]:
        """Parst AUFGABEN.txt Format."""
        tasks = []
        
        # Verschiedene Formate unterstuetzen
        lines = content.split('\n')
        current_task = None
        
        for line in lines:
            line_stripped = line.strip()
            
            # Format 1: [ ] Task oder [x] Task (unterstuetzt optionales - oder * am Anfang)
            checkbox_match = re.match(r'^(?:[-*]\s+)?\[([ xX])\]\s*(.+)', line_stripped)
            if checkbox_match:
                if current_task:
                    tasks.append(current_task)
                
                checked = checkbox_match.group(1).lower() == 'x'
                text = checkbox_match.group(2).strip()
                
                current_task = {
                    'text': text,
                    'status': 'erledigt' if checked else 'offen',
                    'aufwand': self._detect_aufwand(text),
                    'priority': self._calculate_priority(text)
                }
                continue
            
            # Format 2: [!] Kritischer Task (unterstuetzt optionales - oder * am Anfang)
            critical_match = re.match(r'^(?:[-*]\s+)?\[!\]\s*(.+)', line_stripped)
            if critical_match:
                if current_task:
                    tasks.append(current_task)
                
                text = critical_match.group(1).strip()
                current_task = {
                    'text': text,
                    'status': 'offen',
                    'aufwand': self._detect_aufwand(text),
                    'priority': self._calculate_priority(text) + 100,  # Kritisch = hoechste Prio
                    'critical': True
                }
                continue
            
            # Format 3: TODO: oder FIXME: (Code-Kommentar-Stil)
            todo_match = re.match(r'(?:TODO|FIXME|XXX)[:.]?\s*(.+)', line_stripped, re.IGNORECASE)
            if todo_match:
                if current_task:
                    tasks.append(current_task)
                
                text = todo_match.group(1).strip()
                is_fixme = line_stripped.upper().startswith('FIXME')
                
                current_task = {
                    'text': text,
                    'status': 'offen',
                    'aufwand': self._detect_aufwand(text),
                    'priority': self._calculate_priority(text) + (70 if is_fixme else 50),
                    'source': 'FIXME' if is_fixme else 'TODO'
                }
                continue
            
            # Format 4: - Task (einfache Liste) - NUR WENN NICHT EINGERUECKT
            # FIX v1.3.1: Check auf line[0].isspace() fängt Spaces und Tabs
            if line_stripped.startswith('- ') and not line_stripped.startswith('- -') and not (line and line[0].isspace()):
                if current_task:
                    tasks.append(current_task)
                
                text = line_stripped[2:].strip()
                current_task = {
                    'text': text,
                    'status': 'offen',
                    'aufwand': self._detect_aufwand(text),
                    'priority': self._calculate_priority(text)
                }
                continue
            
            # Fortsetzung des aktuellen Tasks
            if current_task and line_stripped and not line_stripped.startswith('#'):
                # FIX v1.3.1: Pruefung auf Original-Line fuer Einrueckung
                # FIX v1.3.1: Pruefung auf Original-Line fuer Einrueckung
                if line and line[0].isspace():
                    current_task['text'] += ' ' + line_stripped.strip()
        
        if current_task:
            tasks.append(current_task)
        
        # Nachbearbeitung: blocked Status erkennen
        for task in tasks:
            if self._is_blocked(task['text']):
                task['status'] = 'blockiert'
                task['priority'] -= 50  # Blockierte Tasks zurueckstellen
        
        return tasks
    
    def _is_blocked(self, text: str) -> bool:
        """Prueft ob ein Task als blockiert markiert ist."""
        text_lower = text.lower()
        blocked_patterns = [
            'blocked', 'blockiert', 'wartet auf', 'waiting for',
            'abhaengig von', 'depends on', 'needs first'
        ]
        return any(pattern in text_lower for pattern in blocked_patterns)
    
    def _detect_aufwand(self, text: str) -> str:
        """Erkennt Aufwand aus Task-Text."""
        text_lower = text.lower()
        
        # Hoch
        if any(kw in text_lower for kw in ['refactor', 'redesign', 'komplex', 'architektur', 'migration']):
            return 'hoch'
        
        # Niedrig
        if any(kw in text_lower for kw in ['fix', 'typo', 'kommentar', 'readme', 'cleanup', 'klein']):
            return 'niedrig'
        
        return 'mittel'
    
    def _calculate_priority(self, text: str) -> float:
        """Berechnet Prioritaets-Score."""
        score = 0.0
        text_lower = text.lower()
        
        # Kritische Keywords (hoechste Prio)
        if any(kw in text_lower for kw in ['bug', 'fix', 'crash', 'fehler', 'broken', 'blocker', 'critical']):
            score += 80
        
        # TODO/FIXME/XXX Keywords (bereits im Parse erkannt, aber fuer Inline auch hier)
        if any(kw in text_lower for kw in ['todo', 'fixme', 'xxx', 'hack']):
            score += 60
        
        # Feature Keywords
        if any(kw in text_lower for kw in ['feature', 'neu', 'implementieren', 'hinzufuegen']):
            score += 50
        
        # Aufwand-Bonus (Quick Wins bevorzugen)
        aufwand = self._detect_aufwand(text)
        if aufwand == 'niedrig':
            score += 30
        elif aufwand == 'hoch':
            score -= 10
        
        # Blocked/Wartet reduziert Prio (diese werden spaeter ohnehin zurueckgestellt)
        if any(kw in text_lower for kw in ['blocked', 'blockiert', 'wartet', 'waiting']):
            score -= 30
        
        return score


def scan_now(db_path: Path = None) -> Dict:
    """Convenience-Funktion fuer direkten Scan."""
    if db_path is None:
        # ATI Scanner nutzt user.db (Agent-Daten = User-Daten)
        db_path = Path(__file__).parent.parent.parent.parent.parent / "data" / "bach.db"

    scanner = TaskScanner(db_path)
    return scanner.scan_all()


def sync_db_to_aufgaben(db_path: Path = None, task_ids: List[int] = None) -> Dict:
    """
    Synchronisiert DB-Status zurueck zu AUFGABEN.txt Dateien.
    Schreibt [x] fuer erledigte Tasks in die Quelldateien.

    Args:
        db_path: Pfad zur bach.db
        task_ids: Optional - nur diese Task-IDs synchronisieren

    Returns:
        Dict mit Statistiken: files_updated, tasks_synced, errors
    """
    if db_path is None:
        db_path = Path(__file__).parent.parent.parent.parent.parent / "data" / "bach.db"

    result = {
        'files_updated': 0,
        'tasks_synced': 0,
        'errors': []
    }

    try:
        conn = sqlite3.connect(db_path)

        # Query: Alle erledigten Tasks mit source_file Info
        if task_ids:
            placeholders = ','.join('?' * len(task_ids))
            query = f"""
                SELECT id, task_text, source_file, line_number, status
                FROM ati_tasks
                WHERE id IN ({placeholders}) AND status = 'erledigt'
                ORDER BY source_file, line_number
            """
            tasks = conn.execute(query, task_ids).fetchall()
        else:
            tasks = conn.execute("""
                SELECT id, task_text, source_file, line_number, status
                FROM ati_tasks
                WHERE status = 'erledigt' AND source_file IS NOT NULL
                ORDER BY source_file, line_number
            """).fetchall()

        conn.close()

        if not tasks:
            return result

        # Gruppiere Tasks nach Datei
        tasks_by_file = {}
        for task_id, text, source_file, line_num, status in tasks:
            if source_file not in tasks_by_file:
                tasks_by_file[source_file] = []
            tasks_by_file[source_file].append({
                'id': task_id,
                'text': text,
                'line': line_num
            })

        # Jede Datei bearbeiten
        for file_path, file_tasks in tasks_by_file.items():
            try:
                path = Path(file_path)
                if not path.exists():
                    result['errors'].append(f"Datei nicht gefunden: {file_path}")
                    continue

                # Datei lesen
                content = path.read_text(encoding='utf-8', errors='replace')
                lines = content.split('\n')
                modified = False

                # Tasks in dieser Datei als erledigt markieren
                for task in file_tasks:
                    line_idx = task['line'] - 1  # Line numbers sind 1-basiert

                    if 0 <= line_idx < len(lines):
                        line = lines[line_idx]

                        # Verschiedene Checkbox-Formate unterstuetzen
                        # Format: [ ] oder - [ ] oder * [ ]
                        if re.search(r'(?:^|\s)(?:[-*]\s+)?\[\s\]', line):
                            # Ersetze [ ] durch [x]
                            new_line = re.sub(r'(\s*(?:[-*]\s+)?)\[\s\]', r'\1[x]', line, count=1)
                            if new_line != line:
                                lines[line_idx] = new_line
                                modified = True
                                result['tasks_synced'] += 1

                # Datei zurueckschreiben wenn geaendert
                if modified:
                    path.write_text('\n'.join(lines), encoding='utf-8')
                    result['files_updated'] += 1

            except Exception as e:
                result['errors'].append(f"Fehler bei {file_path}: {e}")

        return result

    except Exception as e:
        result['errors'].append(f"DB-Fehler: {e}")
        return result


if __name__ == "__main__":
    import sys

    # Optional: Pfad als Argument
    if len(sys.argv) > 1:
        db_path = Path(sys.argv[1])
    else:
        db_path = Path(__file__).parent.parent.parent.parent.parent / "data" / "bach.db"

    print(f"[INFO] DB: {db_path}")
    result = scan_now(db_path)
    print(f"\n[RESULT] {json.dumps(result, indent=2)}")
