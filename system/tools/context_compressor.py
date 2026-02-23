#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Tool: context_compressor
Version: 2.0.0
Author: BACH Team
Created: 2026-02-04
Updated: 2026-02-06
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version context_compressor

Description:
    Komprimiert unkomprimierte Sessions aus memory_sessions (bach.db).
    Analysiert Session-Summaries, extrahiert Tasks/Dateien/Highlights,
    und speichert komprimierte Zusammenfassungen als memory_facts.

Usage:
    python context_compressor.py --run              Sessions aus DB komprimieren
    python context_compressor.py --run --dry-run    Vorschau ohne Aenderungen
    python context_compressor.py --run --format bullet   Anderes Format
    python context_compressor.py --status           Status anzeigen
    python context_compressor.py --config           Regeln anzeigen
    python context_compressor.py --set KEY VALUE    Regel aendern
    python context_compressor.py --test             Test mit Beispieldaten

CLI via BACH:
    bach consolidate compress --run                 Sessions komprimieren
    bach consolidate compress --run --dry-run       Vorschau
    bach consolidate compress --run --format prose  Format waehlen
"""

__version__ = "2.0.0"
__author__ = "BACH Team"

import re
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field, asdict

# BACH Root finden
BACH_ROOT = Path(__file__).parent.parent
CONFIG_FILE = BACH_ROOT / "data" / "compression_rules.json"
DB_PATH = BACH_ROOT / "data" / "bach.db"


@dataclass
class CompressedSummary:
    """Komprimierte Session-Zusammenfassung."""
    session_date: str
    duration_minutes: int = 0
    tasks_completed: List[str] = field(default_factory=list)
    tasks_created: List[str] = field(default_factory=list)
    files_modified: List[str] = field(default_factory=list)
    key_commands: List[str] = field(default_factory=list)
    highlights: List[str] = field(default_factory=list)
    next_steps: List[str] = field(default_factory=list)
    raw_summary: str = ""


class CompressionRules:
    """Konfigurierbare Komprimierungsregeln (ASM_005)."""

    DEFAULT_RULES = {
        "max_tasks": 10,
        "max_files": 10,
        "max_commands": 5,
        "max_highlights": 5,
        "ignore_patterns": [
            r"^cd\s",
            r"^ls\s",
            r"^dir\s",
            r"startup$",
            r"shutdown$"
        ],
        "highlight_patterns": [
            r"ERLEDIGT",
            r"DONE",
            r"ERSTELLT",
            r"CREATED",
            r"FIXED",
            r"BUGFIX"
        ],
        "task_patterns": [
            r"Task.*(?:erledigt|done|completed)",
            r"(?:erstellt|created).*Task",
            r"#\d+.*(?:abgeschlossen|done)"
        ],
        "file_extensions": [
            ".py", ".js", ".html", ".css", ".md", ".json", ".yaml", ".txt"
        ],
        "summary_format": "structured"  # structured, prose, bullet
    }

    def __init__(self, config_path: Path = CONFIG_FILE):
        self.config_path = config_path
        self.rules = self._load_rules()

    def _load_rules(self) -> dict:
        """Laedt Regeln aus Konfiguration."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Merge mit Defaults
                    merged = self.DEFAULT_RULES.copy()
                    merged.update(loaded)
                    return merged
            except Exception:
                pass
        return self.DEFAULT_RULES.copy()

    def save_rules(self):
        """Speichert aktuelle Regeln."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.rules, f, indent=2, ensure_ascii=False)

    def should_ignore(self, text: str) -> bool:
        """Prueft ob Text ignoriert werden soll."""
        for pattern in self.rules.get("ignore_patterns", []):
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def is_highlight(self, text: str) -> bool:
        """Prueft ob Text ein Highlight ist."""
        for pattern in self.rules.get("highlight_patterns", []):
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def is_task_related(self, text: str) -> bool:
        """Prueft ob Text task-bezogen ist."""
        for pattern in self.rules.get("task_patterns", []):
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def contains_file(self, text: str) -> Optional[str]:
        """Extrahiert Dateinamen aus Text."""
        for ext in self.rules.get("file_extensions", []):
            match = re.search(rf'\b[\w./\\-]+{re.escape(ext)}\b', text)
            if match:
                return match.group(0)
        return None


class ContextCompressor:
    """Hauptklasse fuer Kontextkomprimierung."""

    def __init__(self, rules: CompressionRules = None):
        self.rules = rules or CompressionRules()

    def compress_activities(self, activities: List[dict]) -> CompressedSummary:
        """
        Komprimiert eine Liste von Aktivitaeten zu einer Zusammenfassung.

        Args:
            activities: Liste von {time, type, summary} Dicts

        Returns:
            CompressedSummary mit kategorisierten Informationen
        """
        summary = CompressedSummary(
            session_date=datetime.now().strftime("%Y-%m-%d")
        )

        # Aktivitaeten kategorisieren
        for activity in activities:
            text = activity.get("summary", "")
            atype = activity.get("type", "other")

            # Ignorieren?
            if self.rules.should_ignore(text):
                continue

            # Highlight?
            if self.rules.is_highlight(text):
                if len(summary.highlights) < self.rules.rules["max_highlights"]:
                    summary.highlights.append(text)

            # Nach Typ sortieren
            if atype == "task":
                if "erledigt" in text.lower() or "done" in text.lower():
                    if len(summary.tasks_completed) < self.rules.rules["max_tasks"]:
                        summary.tasks_completed.append(self._clean_text(text))
                else:
                    if len(summary.tasks_created) < self.rules.rules["max_tasks"]:
                        summary.tasks_created.append(self._clean_text(text))

            elif atype == "file":
                filename = self.rules.contains_file(text)
                if filename and len(summary.files_modified) < self.rules.rules["max_files"]:
                    if filename not in summary.files_modified:
                        summary.files_modified.append(filename)

            elif atype == "command":
                if len(summary.key_commands) < self.rules.rules["max_commands"]:
                    summary.key_commands.append(self._clean_text(text))

        # Raw-Summary generieren
        summary.raw_summary = self._format_summary(summary)

        return summary

    def _clean_text(self, text: str) -> str:
        """Bereinigt Text fuer Zusammenfassung."""
        # Timestamps entfernen
        text = re.sub(r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]', '', text)
        # Mehrfache Leerzeichen
        text = re.sub(r'\s+', ' ', text)
        # Kuerzen
        return text.strip()[:100]

    def _format_summary(self, summary: CompressedSummary) -> str:
        """Formatiert Zusammenfassung nach konfigurierten Regeln."""
        fmt = self.rules.rules.get("summary_format", "structured")

        if fmt == "bullet":
            return self._format_bullet(summary)
        elif fmt == "prose":
            return self._format_prose(summary)
        else:
            return self._format_structured(summary)

    def _format_structured(self, summary: CompressedSummary) -> str:
        """Strukturiertes Format (Standard)."""
        parts = []

        if summary.tasks_completed:
            parts.append("ERLEDIGT:\n" + "\n".join(f"- {t}" for t in summary.tasks_completed))

        if summary.tasks_created:
            parts.append("ERSTELLT:\n" + "\n".join(f"- {t}" for t in summary.tasks_created))

        if summary.files_modified:
            parts.append("DATEIEN:\n" + "\n".join(f"- {f}" for f in summary.files_modified))

        if summary.highlights:
            parts.append("HIGHLIGHTS:\n" + "\n".join(f"- {h}" for h in summary.highlights))

        if summary.next_steps:
            parts.append("NAECHSTE:\n" + "\n".join(f"- {n}" for n in summary.next_steps))

        return "\n\n".join(parts) if parts else "Keine relevanten Aktivitaeten."

    def _format_bullet(self, summary: CompressedSummary) -> str:
        """Bullet-Point Format."""
        items = []
        for t in summary.tasks_completed:
            items.append(f"✓ {t}")
        for t in summary.tasks_created:
            items.append(f"+ {t}")
        for f in summary.files_modified:
            items.append(f"📄 {f}")
        for h in summary.highlights:
            items.append(f"⭐ {h}")
        return "\n".join(items) if items else "Keine Aktivitaeten."

    def _format_prose(self, summary: CompressedSummary) -> str:
        """Fliesstext Format."""
        parts = []

        if summary.tasks_completed:
            parts.append(f"Erledigt: {', '.join(summary.tasks_completed[:3])}")

        if summary.files_modified:
            parts.append(f"Bearbeitet: {', '.join(summary.files_modified[:3])}")

        if summary.highlights:
            parts.append(f"Highlights: {', '.join(summary.highlights[:3])}")

        return ". ".join(parts) + "." if parts else "Keine Aktivitaeten."

    def to_dict(self, summary: CompressedSummary) -> dict:
        """Konvertiert Summary zu Dictionary."""
        return asdict(summary)

    def compress_session_text(self, summary_text: str, session_date: str) -> CompressedSummary:
        """Komprimiert einen einzelnen Session-Summary-Text.

        Zerlegt den Text in Zeilen und klassifiziert jede als
        task/file/command/other anhand der Regeln.
        """
        activities = []
        for line in summary_text.split('\n'):
            line = line.strip()
            if not line or line.startswith('=') or line.startswith('-' * 5):
                continue

            # Typ erkennen
            if self.rules.is_task_related(line):
                activities.append({"type": "task", "summary": line})
            elif self.rules.contains_file(line):
                activities.append({"type": "file", "summary": line})
            else:
                activities.append({"type": "other", "summary": line})

        result = self.compress_activities(activities)
        result.session_date = session_date
        return result


class SessionCompressor:
    """Liest unkomprimierte Sessions aus bach.db und komprimiert sie."""

    def __init__(self, db_path: Path = DB_PATH, rules: CompressionRules = None):
        self.db_path = db_path
        self.rules = rules or CompressionRules()
        self.compressor = ContextCompressor(self.rules)

    def _get_db(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_status(self) -> str:
        """Zeigt Komprimierungs-Status."""
        conn = self._get_db()
        c = conn.cursor()

        c.execute("SELECT COUNT(*) FROM memory_sessions WHERE is_compressed = 0 OR is_compressed IS NULL")
        uncompressed = c.fetchone()[0]

        c.execute("""
            SELECT COUNT(*) FROM memory_sessions
            WHERE (summary IS NULL OR summary = '' OR length(summary) <= 50
                   OR summary LIKE '%AUTO-CLOSED%')
            AND (is_compressed = 0 OR is_compressed IS NULL)
        """)
        empty = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM memory_sessions WHERE is_compressed = 1")
        compressed = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM memory_sessions")
        total = c.fetchone()[0]

        c.execute("""
            SELECT MIN(started_at), MAX(started_at) FROM memory_sessions
            WHERE is_compressed = 0 OR is_compressed IS NULL
        """)
        date_range = c.fetchone()

        # Komprimierbare Sessions (nicht-leer, unkomprimiert)
        c.execute("""
            SELECT COUNT(*) FROM memory_sessions
            WHERE (is_compressed = 0 OR is_compressed IS NULL)
            AND summary IS NOT NULL AND summary != ''
            AND length(summary) > 50
            AND summary NOT LIKE '%AUTO-CLOSED%'
            AND summary NOT LIKE '%CLEANUP%'
        """)
        compressible = c.fetchone()[0]

        conn.close()

        lines = [
            "[CONTEXT COMPRESSOR] Status",
            "=" * 50,
            "",
            f"Sessions gesamt:          {total}",
            f"  Bereits komprimiert:    {compressed}",
            f"  Unkomprimiert:          {uncompressed}",
            f"    davon leer/kurz:      {empty}",
            f"    davon komprimierbar:  {compressible}",
        ]
        if date_range[0]:
            von = date_range[0][:10] if date_range[0] else "?"
            bis = date_range[1][:10] if date_range[1] else "heute"
            lines.append(f"  Zeitraum:               {von} bis {bis}")

        lines.extend([
            "",
            "Aktionen:",
            "  bach consolidate compress --cleanup     Leere bereinigen",
            "  bach consolidate compress --run         Komprimieren",
            "  bach consolidate compress --run --dry-run  Vorschau",
        ])
        return "\n".join(lines)

    def get_uncompressed_sessions(self) -> List[dict]:
        """Holt alle komprimierbaren Sessions."""
        conn = self._get_db()
        rows = conn.execute("""
            SELECT id, session_id, started_at, ended_at, summary,
                   tasks_completed, tasks_created
            FROM memory_sessions
            WHERE (is_compressed = 0 OR is_compressed IS NULL)
            AND summary IS NOT NULL AND summary != ''
            AND length(summary) > 50
            AND summary NOT LIKE '%AUTO-CLOSED%'
            AND summary NOT LIKE '%CLEANUP%'
            ORDER BY started_at
        """).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def compress_and_store(self, fmt: str = "structured",
                           dry_run: bool = False) -> Tuple[bool, str]:
        """Komprimiert alle offenen Sessions.

        Sessions bleiben episodisches Gedaechtnis - die Summary wird
        durch eine komprimierte Version ersetzt und is_compressed=1 gesetzt.
        Keine Duplizierung in memory_facts.
        """
        self.rules.rules["summary_format"] = fmt
        sessions = self.get_uncompressed_sessions()

        if not sessions:
            return True, "[COMPRESS] Keine komprimierbaren Sessions gefunden."

        output = [
            "[COMPRESS] Kontext-Komprimierung",
            "=" * 50,
            "",
        ]

        total_compressed = 0
        conn = self._get_db() if not dry_run else None

        for s in sessions:
            day = s["started_at"][:10] if s["started_at"] else "unknown"
            result = self.compressor.compress_session_text(s["summary"], day)

            # Tasks aus DB-Feldern ergaenzen
            if s.get("tasks_completed") and s["tasks_completed"] > 0:
                result.tasks_completed.append(
                    f"({s['tasks_completed']} Tasks erledigt)")
            if s.get("tasks_created") and s["tasks_created"] > 0:
                result.tasks_created.append(
                    f"({s['tasks_created']} Tasks erstellt)")

            compressed_summary = result.raw_summary
            if not compressed_summary or compressed_summary == "Keine relevanten Aktivitaeten.":
                # Originaltext kuerzen statt leere Komprimierung
                compressed_summary = s["summary"][:500]

            if not dry_run and conn:
                # Summary durch komprimierte Version ersetzen
                conn.execute("""
                    UPDATE memory_sessions
                    SET is_compressed = 1,
                        summary = ?
                    WHERE id = ?
                """, (compressed_summary, s["id"]))

            total_compressed += 1

        if not dry_run and conn:
            conn.commit()
            conn.close()

        output.append(f"  {total_compressed} Sessions komprimiert")

        prefix = "[DRY-RUN] " if dry_run else ""
        output.extend([
            "",
            f"{prefix}Ergebnis: {total_compressed} Sessions komprimiert "
            f"(episodisch, in memory_sessions).",
        ])

        return True, "\n".join(output)


# CLI Interface
def main():
    import argparse

    parser = argparse.ArgumentParser(description="BACH Context Compressor v2")
    parser.add_argument('--run', action='store_true',
                        help='Sessions aus DB komprimieren')
    parser.add_argument('--status', action='store_true',
                        help='Komprimierungs-Status anzeigen')
    parser.add_argument('--dry-run', action='store_true',
                        help='Vorschau ohne Aenderungen')
    parser.add_argument('--test', action='store_true',
                        help='Test mit Beispieldaten')
    parser.add_argument('--format', choices=['structured', 'bullet', 'prose'],
                        default='structured', help='Ausgabeformat')
    parser.add_argument('--config', action='store_true',
                        help='Konfiguration anzeigen')
    parser.add_argument('--set', nargs=2, metavar=('KEY', 'VALUE'),
                        help='Regel setzen (z.B. --set max_tasks 10)')
    parser.add_argument('--db', type=str, default=None,
                        help='Pfad zur bach.db (Standard: auto)')

    args = parser.parse_args()

    rules = CompressionRules()
    db_path = Path(args.db) if args.db else DB_PATH

    if args.config:
        print(json.dumps(rules.rules, indent=2, ensure_ascii=False))
        return

    if args.set:
        key, value = args.set
        try:
            rules.rules[key] = int(value)
        except ValueError:
            rules.rules[key] = value
        rules.save_rules()
        print(f"Regel gesetzt: {key} = {value}")
        return

    if args.status:
        sc = SessionCompressor(db_path, rules)
        print(sc.get_status())
        return

    if args.run:
        sc = SessionCompressor(db_path, rules)
        success, msg = sc.compress_and_store(
            fmt=args.format, dry_run=args.dry_run)
        print(msg)
        return

    # Test-Modus
    if args.test:
        rules.rules["summary_format"] = args.format
        compressor = ContextCompressor(rules)

        test_activities = [
            {"time": "14:30", "type": "task", "summary": "Task 123 erledigt: Feature X implementiert"},
            {"time": "14:45", "type": "file", "summary": "Edit: gui/templates/index.html"},
            {"time": "15:00", "type": "task", "summary": "Task erstellt: Bug in Login"},
            {"time": "15:15", "type": "other", "summary": "ERLEDIGT: Migration abgeschlossen"},
            {"time": "15:30", "type": "file", "summary": "Write: tools/helper.py"},
        ]

        result = compressor.compress_activities(test_activities)
        print("=== Komprimierte Zusammenfassung ===\n")
        print(result.raw_summary)
        print("\n=== JSON ===")
        print(json.dumps(compressor.to_dict(result), indent=2, ensure_ascii=False))
        return

    # Ohne Argumente: Status anzeigen
    sc = SessionCompressor(db_path, rules)
    print(sc.get_status())


if __name__ == "__main__":
    main()
