#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Tool: autolog_analyzer
Version: 1.0.0
Author: BACH Team
Created: 2026-02-04
Updated: 2026-02-04
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version autolog_analyzer

Description:
    [Beschreibung hinzufügen]

Usage:
    python autolog_analyzer.py [args]
"""

__version__ = "1.0.0"
__author__ = "BACH Team"

import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, field

# BACH Root finden
BACH_ROOT = Path(__file__).parent.parent
AUTOLOG_PATH = BACH_ROOT / "logs" / "auto_log_extended.txt"


@dataclass
class LogEntry:
    """Einzelner Autolog-Eintrag."""
    timestamp: datetime
    entry_type: str  # CMD, TOOL, ERROR, etc.
    content: str
    raw: str


@dataclass
class SessionActivity:
    """Gruppierte Aktivitaeten einer Session."""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    commands: List[str] = field(default_factory=list)
    tasks_created: List[str] = field(default_factory=list)
    tasks_completed: List[str] = field(default_factory=list)
    files_changed: List[str] = field(default_factory=list)
    memory_entries: List[str] = field(default_factory=list)
    tool_calls: List[str] = field(default_factory=list)
    session_summary: Optional[str] = None


class AutologAnalyzer:
    """Hauptklasse fuer Autolog-Analyse."""
    
    # Regex-Patterns
    TIMESTAMP_PATTERN = re.compile(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]')
    CMD_PATTERN = re.compile(r'\[[\d\- :]+\] CMD: (.+)')
    TOOL_PATTERN = re.compile(r'\[[\d\- :]+\] \[TOOL\] (.+)')
    
    def __init__(self, log_path: Path = AUTOLOG_PATH):
        self.log_path = log_path
        self.entries: List[LogEntry] = []
        
    def parse_log(self, last_n_lines: int = 100) -> List[LogEntry]:
        """Parst die letzten N Zeilen des Autologs."""
        if not self.log_path.exists():
            return []
        
        with open(self.log_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()[-last_n_lines:]
        
        self.entries = []
        for line in lines:
            entry = self._parse_line(line.strip())
            if entry:
                self.entries.append(entry)
        
        return self.entries
    
    def _parse_line(self, line: str) -> Optional[LogEntry]:
        """Parst eine einzelne Zeile."""
        if not line:
            return None
            
        # Timestamp extrahieren
        ts_match = self.TIMESTAMP_PATTERN.match(line)
        if not ts_match:
            return None
            
        timestamp = datetime.strptime(ts_match.group(1), '%Y-%m-%d %H:%M:%S')
        
        # Typ und Inhalt bestimmen
        cmd_match = self.CMD_PATTERN.match(line)
        if cmd_match:
            return LogEntry(
                timestamp=timestamp,
                entry_type='CMD',
                content=cmd_match.group(1),
                raw=line
            )
        
        tool_match = self.TOOL_PATTERN.match(line)
        if tool_match:
            return LogEntry(
                timestamp=timestamp,
                entry_type='TOOL',
                content=tool_match.group(1),
                raw=line
            )
        
        return LogEntry(
            timestamp=timestamp,
            entry_type='OTHER',
            content=line,
            raw=line
        )
    
    def extract_session(self, entries: List[LogEntry] = None) -> SessionActivity:
        """Extrahiert Aktivitaeten aus der letzten Session."""
        if entries is None:
            entries = self.entries or self.parse_log()
        
        activity = SessionActivity()
        
        # Letzte Session finden (von shutdown rueckwaerts bis startup)
        session_entries = []
        in_session = False
        
        for entry in reversed(entries):
            if entry.entry_type == 'CMD' and entry.content == 'shutdown':
                in_session = True
                activity.end_time = entry.timestamp
            elif in_session:
                session_entries.insert(0, entry)
                if entry.entry_type == 'CMD' and entry.content == 'startup':
                    activity.start_time = entry.timestamp
                    break
        
        # Kategorisieren
        for entry in session_entries:
            self._categorize_entry(entry, activity)
        
        return activity
    
    def _categorize_entry(self, entry: LogEntry, activity: SessionActivity):
        """Kategorisiert einen Eintrag in die passende Aktivitaetsgruppe."""
        content = entry.content
        
        # Session-Berichte
        if content.startswith('memory session'):
            summary = content.replace('memory session', '').strip()
            activity.session_summary = summary
            activity.memory_entries.append(summary)
            return
        
        # Task-Operationen
        if content.startswith('task '):
            if 'add' in content or 'create' in content:
                activity.tasks_created.append(content)
            elif 'done' in content or 'complete' in content:
                activity.tasks_completed.append(content)
            activity.commands.append(content)
            return
        
        # Tool-Aufrufe
        if entry.entry_type == 'TOOL':
            activity.tool_calls.append(content)
            return
        
        # Allgemeine Befehle
        if entry.entry_type == 'CMD':
            activity.commands.append(content)
    
    def generate_summary(self, activity: SessionActivity = None) -> str:
        """Generiert einen komprimierten Session-Bericht."""
        if activity is None:
            activity = self.extract_session()
        
        lines = []
        
        # Zeitraum
        if activity.start_time and activity.end_time:
            duration = (activity.end_time - activity.start_time).total_seconds() / 60
            lines.append(f"ZEITRAUM: {activity.start_time.strftime('%H:%M')} - {activity.end_time.strftime('%H:%M')} ({duration:.0f} min)")
        
        # Tasks
        if activity.tasks_completed:
            lines.append(f"ERLEDIGT: {len(activity.tasks_completed)} Task(s)")
        if activity.tasks_created:
            lines.append(f"ERSTELLT: {len(activity.tasks_created)} Task(s)")
        
        # Vorhandener Summary
        if activity.session_summary:
            # Kuerzen falls zu lang
            summary = activity.session_summary[:300]
            if len(activity.session_summary) > 300:
                summary += "..."
            lines.append(f"THEMA: {summary}")
        
        # Befehle
        cmd_count = len([c for c in activity.commands if c not in ('startup', 'shutdown')])
        if cmd_count > 0:
            lines.append(f"BEFEHLE: {cmd_count}")
        
        return " | ".join(lines) if lines else "Keine Aktivitaeten erfasst."


def main():
    """CLI-Einstiegspunkt."""
    import sys
    
    analyzer = AutologAnalyzer()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--last':
            n = int(sys.argv[2]) if len(sys.argv) > 2 else 100
            entries = analyzer.parse_log(last_n_lines=n)
            print(f"[AUTOLOG] {len(entries)} Eintraege geparst")
            return
        elif sys.argv[1] == '--session':
            activity = analyzer.extract_session()
            summary = analyzer.generate_summary(activity)
            print(f"[SESSION SUMMARY]\n{summary}")
            return
        elif sys.argv[1] == '--detail':
            activity = analyzer.extract_session()
            print(f"Start: {activity.start_time}")
            print(f"Ende: {activity.end_time}")
            print(f"Befehle: {len(activity.commands)}")
            print(f"Tasks erstellt: {activity.tasks_created}")
            print(f"Tasks erledigt: {activity.tasks_completed}")
            print(f"Tool-Aufrufe: {len(activity.tool_calls)}")
            return
    
    # Default: Summary generieren
    activity = analyzer.extract_session()
    summary = analyzer.generate_summary(activity)
    print(summary)


if __name__ == '__main__':
    main()
