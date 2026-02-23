#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
task_statistics.py - Statistik-Auswertung für _done.json

Analysiert erledigte Tasks und liefert:
- Tasks pro Woche
- Aufwand-Verteilung
- Sessions pro Tag
- Tool-Aktivität

Version: 1.0
Erstellt: 2026-01-10
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path

# Pfade
SCRIPT_DIR = Path(__file__).parent
BATCH_DIR = SCRIPT_DIR.parent
DONE_JSON = BATCH_DIR / "DATA" / "LONGTERM-MEMORY" / "_done.json"


def load_done_tasks():
    """Lädt erledigte Tasks aus _done.json"""
    if not DONE_JSON.exists():
        print(f"❌ Datei nicht gefunden: {DONE_JSON}")
        return []
    
    with open(DONE_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data.get('tasks', [])


def parse_timestamp(ts_string):
    """Parst verschiedene Zeitstempel-Formate"""
    if not ts_string:
        return None
    
    formats = [
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(ts_string, fmt)
        except ValueError:
            continue
    return None


def get_week_key(dt):
    """Gibt Kalenderwoche als String zurück (YYYY-WXX)"""
    iso_cal = dt.isocalendar()
    return f"{iso_cal.year}-W{iso_cal.week:02d}"


def calculate_statistics(tasks):
    """Berechnet alle Statistiken"""
    
    stats = {
        'total_tasks': len(tasks),
        'tasks_per_week': defaultdict(int),
        'tasks_per_day': defaultdict(int),
        'aufwand_distribution': defaultdict(int),
        'tasks_per_tool': defaultdict(int),
        'tasks_per_completed_by': defaultdict(int),
        'sessions_per_day': defaultdict(set),
        'earliest_task': None,
        'latest_task': None
    }
    
    for task in tasks:
        completed_at = parse_timestamp(task.get('completed_at'))
        if not completed_at:
            continue
        
        # Zeitraum tracken
        if stats['earliest_task'] is None or completed_at < stats['earliest_task']:
            stats['earliest_task'] = completed_at
        if stats['latest_task'] is None or completed_at > stats['latest_task']:
            stats['latest_task'] = completed_at
        
        # Tasks pro Woche
        week_key = get_week_key(completed_at)
        stats['tasks_per_week'][week_key] += 1
        
        # Tasks pro Tag
        day_key = completed_at.strftime("%Y-%m-%d")
        stats['tasks_per_day'][day_key] += 1
        
        # Aufwand-Verteilung
        aufwand = task.get('aufwand', 'unbekannt')
        stats['aufwand_distribution'][aufwand] += 1
        
        # Tasks pro Tool
        tool = task.get('tool', 'unbekannt')
        stats['tasks_per_tool'][tool] += 1
        
        # Completed by
        completed_by = task.get('completed_by', 'unbekannt')
        stats['tasks_per_completed_by'][completed_by] += 1
        
        # Sessions pro Tag
        session_id = task.get('session_id', '')
        if session_id:
            stats['sessions_per_day'][day_key].add(session_id)
    
    return stats


def format_report(stats):
    """Formatiert den Statistik-Bericht"""
    
    lines = []
    lines.append("=" * 60)
    lines.append("        📊 TASK STATISTIK - _done.json")
    lines.append("=" * 60)
    lines.append("")
    
    # Übersicht
    lines.append("📌 ÜBERSICHT")
    lines.append("-" * 40)
    lines.append(f"  Gesamt Tasks:     {stats['total_tasks']}")
    
    if stats['earliest_task'] and stats['latest_task']:
        delta = stats['latest_task'] - stats['earliest_task']
        days = delta.days + 1
        lines.append(f"  Zeitraum:         {stats['earliest_task'].strftime('%Y-%m-%d')} bis {stats['latest_task'].strftime('%Y-%m-%d')}")
        lines.append(f"  Tage aktiv:       {days}")
        lines.append(f"  Ø Tasks/Tag:      {stats['total_tasks'] / max(days, 1):.1f}")
    lines.append("")
    
    # Tasks pro Woche
    lines.append("📅 TASKS PRO WOCHE")
    lines.append("-" * 40)
    
    weeks = sorted(stats['tasks_per_week'].keys())
    if weeks:
        avg_per_week = stats['total_tasks'] / len(weeks)
        lines.append(f"  Ø Tasks/Woche:    {avg_per_week:.1f}")
        lines.append("")
        
        for week in weeks[-8:]:  # Letzte 8 Wochen
            count = stats['tasks_per_week'][week]
            bar = "█" * min(count / 2, 25)
            lines.append(f"  {week}: {count:3d} {bar}")
    lines.append("")
    
    # Aufwand-Verteilung
    lines.append("⚡ AUFWAND-VERTEILUNG")
    lines.append("-" * 40)
    
    aufwand_order = ['niedrig', 'mittel', 'hoch', 'unbekannt']
    for aufwand in aufwand_order:
        if aufwand in stats['aufwand_distribution']:
            count = stats['aufwand_distribution'][aufwand]
            pct = (count / stats['total_tasks'] * 100) if stats['total_tasks'] > 0 else 0
            lines.append(f"  {aufwand:12s}: {count:4d} ({pct:5.1f}%)")
    lines.append("")
    
    # Completed by
    lines.append("👤 ERLEDIGT DURCH")
    lines.append("-" * 40)
    
    for who, count in sorted(stats['tasks_per_completed_by'].items(), key=lambda x: -x[1]):
        pct = (count / stats['total_tasks'] * 100) if stats['total_tasks'] > 0 else 0
        lines.append(f"  {who:12s}: {count:4d} ({pct:5.1f}%)")
    lines.append("")
    
    # Sessions pro Tag (letzte 7 Tage)
    lines.append("🔄 SESSIONS/TAG (letzte 7 Tage)")
    lines.append("-" * 40)
    
    days = sorted(stats['sessions_per_day'].keys())[-7:]
    total_sessions = 0
    for day in days:
        session_count = len(stats['sessions_per_day'][day])
        total_sessions += session_count
        lines.append(f"  {day}: {session_count:2d} Sessions")
    
    if days:
        lines.append(f"  Ø Sessions/Tag:   {total_sessions / len(days):.1f}")
    lines.append("")
    
    # Top 10 Tools
    lines.append("🔧 TOP 10 TOOLS (nach Tasks)")
    lines.append("-" * 40)
    
    top_tools = sorted(stats['tasks_per_tool'].items(), key=lambda x: -x[1])[:10]
    for tool, count in top_tools:
        lines.append(f"  {count:4d}  {tool[:40]}")
    lines.append("")
    
    lines.append("=" * 60)
    
    return "\n".join(lines)


def export_json(stats, output_path):
    """Exportiert Statistiken als JSON"""
    
    export_data = {
        'generated_at': datetime.now().isoformat(),
        'total_tasks': stats['total_tasks'],
        'tasks_per_week': dict(stats['tasks_per_week']),
        'aufwand_distribution': dict(stats['aufwand_distribution']),
        'completed_by': dict(stats['tasks_per_completed_by']),
        'top_tools': dict(sorted(stats['tasks_per_tool'].items(), key=lambda x: -x[1])[:20])
    }
    
    if stats['earliest_task']:
        export_data['period'] = {
            'from': stats['earliest_task'].isoformat(),
            'to': stats['latest_task'].isoformat()
        }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ JSON exportiert: {output_path}")


def main():
    """Hauptfunktion"""
    import argparse
    import sys
    
    # UTF-8 Konsole
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    
    parser = argparse.ArgumentParser(description='Task Statistik für _done.json')
    parser.add_argument('--json', type=str, help='Exportiere als JSON in Datei')
    parser.add_argument('--quiet', '-q', action='store_true', help='Keine Konsolenausgabe')
    args = parser.parse_args()
    
    # Tasks laden
    tasks = load_done_tasks()
    
    if not tasks:
        print("❌ Keine Tasks gefunden!")
        return
    
    # Statistiken berechnen
    stats = calculate_statistics(tasks)
    
    # Bericht ausgeben
    if not args.quiet:
        report = format_report(stats)
        print(report)
    
    # Optional: JSON Export
    if args.json:
        export_json(stats, args.json)


if __name__ == '__main__':
    main()
