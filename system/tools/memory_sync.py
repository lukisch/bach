#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
memory_sync.py - Bidirektionaler Memory-Sync
=============================================

BACH Memory-CMS: DB ↔ MEMORY.md
- Generate: DB → MEMORY.md (auto-generierte Sektionen)
- Ingest: MEMORY.md → DB (manueller Bereich)
- Daily Logs: Tages-Log YYYY-MM-DD.md

Teil von SQ065: MEMORY.md Auto-Export & memory_sync
Referenz: BACH_Dev/docs/MEMORY_SYNC_DESIGN.md
"""

from pathlib import Path
from datetime import datetime
from typing import Optional
import sqlite3
import re

# SQ039 Integration (Runde 6)
try:
    from silo_scanner import SiloScanner
except ImportError:
    # Fallback wenn silo_scanner nicht gefunden
    SiloScanner = None


class MemorySync:
    """Bidirektionaler Memory-Sync: DB ↔ MEMORY.md"""

    def __init__(self, bach_root: Path):
        self.bach_root = Path(bach_root)

        # Auto-Detect: Root vs. system/ Installation
        if (self.bach_root / "system").exists():
            # Root-Installation (Strawberry)
            self.system_root = self.bach_root / "system"
        else:
            # Legacy (Vanilla, bach_root = system/)
            self.system_root = self.bach_root
            self.bach_root = self.system_root.parent

        self.db_path = self.system_root / "data" / "bach.db"
        self.memory_md_path = self.bach_root / "MEMORY.md"

    def generate(self, partner: str = "user", project: str = "BACH") -> tuple[bool, str]:
        """Generiert MEMORY.md aus DB."""
        generator = MemoryGenerator(self.db_path)

        content = generator.build(
            current_task=generator.get_current_task(),
            system_status=generator.get_system_status(),
            top_lessons=generator.get_top_lessons(limit=10),
            active_projects=generator.get_active_projects(limit=5),
            important_settings=generator.get_important_settings(),
            silo_index=generator.scan_silos(),
            manual_content=generator.extract_manual_section(self.memory_md_path)
        )

        self.memory_md_path.write_text(content, encoding='utf-8')
        return True, f"✓ MEMORY.md generiert: {self.memory_md_path}"

    def ingest(self, file_path: Optional[Path] = None) -> tuple[bool, str]:
        """Parst MEMORY.md und schreibt manuellen Bereich zurück in DB."""
        target = Path(file_path) if file_path else self.memory_md_path

        if not target.exists():
            return False, f"✗ Datei nicht gefunden: {target}"

        ingestor = MemoryIngest(self.db_path)
        manual_content = ingestor.extract_manual_section(target)

        if not manual_content:
            return True, "✓ Kein manueller Inhalt zum Ingestieren"

        # Speichere manuellen Content in memory_facts
        ingestor.save_manual_notes(manual_content, source="MEMORY.md")

        return True, f"✓ Manueller Bereich aus MEMORY.md ingestiert"

    def status(self) -> tuple[bool, str]:
        """Zeigt Sync-Status."""
        status_lines = []

        # Datei-Existenz
        exists = "✓" if self.memory_md_path.exists() else "✗"
        status_lines.append(f"{exists} MEMORY.md: {self.memory_md_path}")

        # Letzter Sync
        if self.memory_md_path.exists():
            mtime = self.memory_md_path.stat().st_mtime
            last_sync = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
            status_lines.append(f"   Letzter Sync: {last_sync}")

        # DB-Status
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT COUNT(*) FROM memory_lessons WHERE is_active=1")
        lesson_count = cursor.fetchone()[0]
        status_lines.append(f"✓ DB Lessons: {lesson_count} aktiv")

        cursor = conn.execute("SELECT COUNT(*) FROM tasks WHERE status='in_progress'")
        task_count = cursor.fetchone()[0]
        status_lines.append(f"✓ DB Tasks: {task_count} in_progress")

        conn.close()

        return True, "\n".join(status_lines)


class MemoryGenerator:
    """Generiert MEMORY.md-Sektionen aus DB."""

    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)

    def get_current_task(self) -> str:
        """Holt Current Task(s) aus tasks-Tabelle (SQ065 Current-Task-Block).

        Returns:
            Formatierte Liste der Top 3-5 pending/in_progress Tasks
        """
        conn = sqlite3.connect(self.db_path)

        # Versuche zuerst continuation_context (Legacy)
        cursor = conn.execute("""
            SELECT continuation_context
            FROM memory_sessions
            ORDER BY started_at DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        session_context = row[0] if row and row[0] else None

        # Hole Top 5 aktuelle Tasks (pending/in_progress, sortiert nach Priorität)
        cursor = conn.execute("""
            SELECT id, title, status, priority, category
            FROM tasks
            WHERE status IN ('pending', 'in_progress')
            ORDER BY
                CASE
                    WHEN priority = 'KRITISCH' THEN 1
                    WHEN priority = 'HOCH' THEN 2
                    WHEN priority LIKE '%9%' THEN 3
                    WHEN priority = 'MITTEL' THEN 4
                    WHEN priority = 'NIEDRIG' THEN 5
                    ELSE 6
                END,
                created_at DESC
            LIMIT 5
        """)
        tasks = cursor.fetchall()
        conn.close()

        # Formatierung
        lines = []

        # Session-Context parsen (falls JSON)
        if session_context:
            try:
                import json
                ctx = json.loads(session_context)
                if isinstance(ctx, dict):
                    # JSON-Format (seit Block 5.8)
                    if ctx.get("session_summary"):
                        lines.append(f"**Letzter Stand:** {ctx['session_summary']}")
                    if ctx.get("tasks_completed") or ctx.get("tasks_created"):
                        tc = ctx.get("tasks_created", 0)
                        td = ctx.get("tasks_completed", 0)
                        lines.append(f"*(+{tc} erstellt, {td} erledigt)*")
                    lines.append("")
                else:
                    # Legacy-Format (Plain-Text)
                    lines.append(f"**Session-Kontext:** {session_context}")
                    lines.append("")
            except (json.JSONDecodeError, TypeError):
                # Fallback: Plain-Text
                lines.append(f"**Session-Kontext:** {session_context}")
                lines.append("")

        if tasks:
            lines.append("**Offene Tasks:**")
            lines.append("")
            for task_id, title, status, priority, category in tasks:
                status_icon = "🔄" if status == "in_progress" else "⏸"
                cat_label = f" [{category}]" if category else ""
                lines.append(f"{status_icon} **#{task_id}** {title}{cat_label}")
                lines.append(f"   *Priorität: {priority}, Status: {status}*")
            return "\n".join(lines)

        if session_context:
            return "\n".join(lines)

        return "*Kein aktiver Task*"

    def get_system_status(self) -> dict:
        """Holt System-Status aus verschiedenen Tabellen."""
        conn = sqlite3.connect(self.db_path)

        status = {}

        # Robuste Abfragen mit Fallbacks
        try:
            status['handlers'] = conn.execute("SELECT COUNT(*) FROM bach_handlers").fetchone()[0]
        except sqlite3.OperationalError:
            status['handlers'] = 0

        try:
            status['tools'] = conn.execute("SELECT COUNT(*) FROM tools").fetchone()[0]
        except sqlite3.OperationalError:
            status['tools'] = 0

        status['tables'] = conn.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
        status['tasks_open'] = conn.execute("SELECT COUNT(*) FROM tasks WHERE status IN ('pending', 'in_progress')").fetchone()[0]
        status['skills'] = conn.execute("SELECT COUNT(*) FROM skills WHERE is_active=1").fetchone()[0]

        conn.close()
        return status

    def get_top_lessons(self, limit: int = 10) -> list[dict]:
        """Top-Lessons nach Severity sortiert."""
        conn = sqlite3.connect(self.db_path)

        # Severity-Mapping: critical > high > medium > low
        severity_order = """
            CASE severity
                WHEN 'critical' THEN 1
                WHEN 'high' THEN 2
                WHEN 'medium' THEN 3
                WHEN 'low' THEN 4
                ELSE 5
            END
        """

        cursor = conn.execute(f"""
            SELECT title, problem, solution, severity
            FROM memory_lessons
            WHERE is_active = 1
            ORDER BY {severity_order}, created_at DESC
            LIMIT ?
        """, (limit,))

        lessons = []
        for row in cursor.fetchall():
            lessons.append({
                'title': row[0],
                'problem': row[1],
                'solution': row[2],
                'severity': row[3]
            })

        conn.close()
        return lessons

    def get_active_projects(self, limit: int = 5) -> list[dict]:
        """Top-Projekte aus Tasks, nach Priorität."""
        conn = sqlite3.connect(self.db_path)

        cursor = conn.execute("""
            SELECT category, COUNT(*) as count, MIN(priority) as min_prio
            FROM tasks
            WHERE status IN ('pending', 'in_progress')
            GROUP BY category
            ORDER BY min_prio ASC, count DESC
            LIMIT ?
        """, (limit,))

        projects = []
        for row in cursor.fetchall():
            projects.append({
                'name': row[0] if row[0] else "Unkategorisiert",
                'open_tasks': row[1],
                'priority': row[2]
            })

        conn.close()
        return projects

    def get_important_settings(self) -> dict:
        """Holt wichtige System-Settings für LLM-Kontext (SQ037)."""
        conn = sqlite3.connect(self.db_path)

        settings = {}

        # Integration-Level (claude-code)
        try:
            row = conn.execute("""
                SELECT value FROM system_config
                WHERE key='integration.claude-code.level'
            """).fetchone()
            settings['integration_level'] = row[0] if row else "off"
        except:
            settings['integration_level'] = "off"

        # Backup-Strategie
        try:
            row = conn.execute("""
                SELECT value FROM system_config
                WHERE key='backup_local_retention'
            """).fetchone()
            settings['backup_retention'] = row[0] if row else "7"
        except:
            settings['backup_retention'] = "7"

        # Token-Limits
        try:
            warn = conn.execute("""
                SELECT value FROM system_config
                WHERE key='token_warning_threshold'
            """).fetchone()
            crit = conn.execute("""
                SELECT value FROM system_config
                WHERE key='token_critical_threshold'
            """).fetchone()
            settings['token_warning'] = warn[0] if warn else "70"
            settings['token_critical'] = crit[0] if crit else "85"
        except:
            settings['token_warning'] = "70"
            settings['token_critical'] = "85"

        # Auto-Sync
        try:
            row = conn.execute("""
                SELECT value FROM system_config
                WHERE key='auto_sync_enabled'
            """).fetchone()
            settings['auto_sync'] = row[0] if row else "false"
        except:
            settings['auto_sync'] = "false"

        conn.close()
        return settings

    def scan_silos(self) -> list[dict]:
        """Scannt ~/.claude/projects/ nach Memory-Silos.

        Returns:
            Liste von Dicts mit 'project', 'path', 'file_count', 'last_modified'
            oder leere Liste im Fallback-Modus
        """
        # SQ039 Integration: Nutze SiloScanner wenn verfügbar
        if SiloScanner:
            scanner = SiloScanner()
            return scanner.scan_silos()

        # Fallback: Einfache Pfad-Liste (Legacy)
        home = Path.home()
        claude_projects = home / ".claude" / "projects"

        if not claude_projects.exists():
            return []

        silos = []
        for project_dir in claude_projects.iterdir():
            if not project_dir.is_dir():
                continue
            memory_dir = project_dir / "memory"
            if memory_dir.exists():
                # Fallback-Format für Rückwärtskompatibilität
                silos.append({
                    'project': project_dir.name,
                    'path': str(memory_dir),
                    'file_count': 0,
                    'last_modified': 'N/A'
                })

        return silos

    def extract_manual_section(self, memory_md: Path) -> str:
        """Extrahiert manuellen Bereich aus bestehendem MEMORY.md."""
        if not memory_md.exists():
            return ""

        content = memory_md.read_text(encoding='utf-8')

        # Suche <!-- MANUELL START --> ... <!-- MANUELL END -->
        match = re.search(r'<!-- MANUELL START -->(.*?)<!-- MANUELL END -->', content, re.DOTALL)

        if match:
            return match.group(1).strip()
        return ""

    def build(self, current_task, system_status, top_lessons, active_projects, important_settings, silo_index, manual_content) -> str:
        """Baut MEMORY.md aus Komponenten zusammen."""
        lines = []
        lines.append("# BACH Session Memory")
        lines.append("")
        lines.append(f"**Generiert:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 🎯 Current Task")
        lines.append("")
        lines.append(current_task)
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 📊 System-Status")
        lines.append("")
        lines.append(f"- **Handler:** {system_status['handlers']} registriert")
        lines.append(f"- **Tools:** {system_status['tools']} verfügbar")
        lines.append(f"- **Tabellen:** {system_status['tables']} (bach.db)")
        lines.append(f"- **Tasks:** {system_status['tasks_open']} offen")
        lines.append(f"- **Skills:** {system_status['skills']} aktiv")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 🧠 Lessons")
        lines.append("")
        lines.append("*→ Siehe **CLAUDE.md** (Live-Push, automatisch aktualisiert)*")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 📋 Aktive Projekte")
        lines.append("")

        if active_projects:
            for i, proj in enumerate(active_projects, 1):
                lines.append(f"{i}. **{proj['name']}** (Prio: {proj['priority']})")
                lines.append(f"   - {proj['open_tasks']} offene Tasks")
                lines.append("")
        else:
            lines.append("*Keine aktiven Projekte*")
            lines.append("")

        lines.append("---")
        lines.append("")
        lines.append("## ⚙️ Einstellungen")
        lines.append("")
        lines.append(f"- **Integration:** {important_settings.get('integration_level', 'off')} (claude-code)")
        lines.append(f"- **Backup-Retention:** {important_settings.get('backup_retention', '7')} Tage")
        lines.append(f"- **Token-Limits:** Warnung {important_settings.get('token_warning', '70')}%, Kritisch {important_settings.get('token_critical', '85')}%")
        lines.append(f"- **Auto-Sync:** {important_settings.get('auto_sync', 'false')}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 📂 Silo-Index")
        lines.append("")
        lines.append("*Claude Code Project Memories (andere Projekte neben BACH)*")
        lines.append("")

        if silo_index:
            # SQ039: Strukturierte Ausgabe mit Metadaten
            for silo in silo_index:
                if isinstance(silo, dict):
                    # Strukturierte Daten von SiloScanner
                    lines.append(f"- **{silo['project']}**")
                    lines.append(f"  - Pfad: `{silo['path']}`")
                    lines.append(f"  - Dateien: {silo['file_count']}, Aktualisiert: {silo['last_modified']}")
                else:
                    # Fallback: Einfacher String-Pfad (Legacy)
                    lines.append(f"- `{silo}`")
        else:
            lines.append("*Keine Silos gefunden*")

        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("<!-- MANUELL START -->")
        lines.append("")
        lines.append("## ✍️ Manuelle Notizen")
        lines.append("")
        lines.append(manual_content if manual_content else "*Keine manuellen Notizen*")
        lines.append("")
        lines.append("<!-- MANUELL END -->")

        return "\n".join(lines)


class MemoryIngest:
    """Ingestiert MEMORY.md → DB (manueller Bereich)."""

    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)

    def extract_manual_section(self, memory_md: Path) -> str:
        """Extrahiert manuellen Bereich aus MEMORY.md."""
        if not memory_md.exists():
            return ""

        content = memory_md.read_text(encoding='utf-8')

        # Suche <!-- MANUELL START --> ... <!-- MANUELL END -->
        match = re.search(r'<!-- MANUELL START -->(.*?)<!-- MANUELL END -->', content, re.DOTALL)

        if match:
            return match.group(1).strip()
        return ""

    def save_manual_notes(self, content: str, source: str = "MEMORY.md"):
        """Speichert manuellen Content in memory_facts."""
        conn = sqlite3.connect(self.db_path)

        # Speichere als memory_fact mit category="manual_notes"
        conn.execute("""
            INSERT INTO memory_facts (category, fact, source, created_at, dist_type)
            VALUES (?, ?, ?, datetime('now'), 0)
        """, ("manual_notes", content, source))

        conn.commit()
        conn.close()


class DailyLogGenerator:
    """Generiert Tages-Log YYYY-MM-DD.md."""

    def __init__(self, bach_root: Path):
        self.bach_root = Path(bach_root)

        # Auto-Detect
        if (self.bach_root / "system").exists():
            self.system_root = self.bach_root / "system"
        else:
            self.system_root = self.bach_root
            self.bach_root = self.system_root.parent

        self.db_path = self.system_root / "data" / "bach.db"
        self.log_dir = self.bach_root / "logs" / "daily"
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def write_log(self):
        """Schreibt Tages-Log für heute."""
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.log_dir / f"{today}.md"

        # Sammle Daten aus DB
        completed_tasks = self._get_completed_tasks_today()
        new_lessons = self._get_new_lessons_today()

        # Baue Content
        content = self._build_log(today, completed_tasks, new_lessons)

        # Append (nicht überschreiben!)
        if log_file.exists():
            existing = log_file.read_text(encoding='utf-8')
            log_file.write_text(existing + "\n\n---\n\n" + content, encoding='utf-8')
        else:
            log_file.write_text(content, encoding='utf-8')

        return log_file

    def _get_completed_tasks_today(self) -> list[dict]:
        """Hole heute abgeschlossene Tasks."""
        conn = sqlite3.connect(self.db_path)
        today = datetime.now().strftime("%Y-%m-%d")

        cursor = conn.execute("""
            SELECT title, category
            FROM tasks
            WHERE status = 'completed'
            AND DATE(updated_at) = ?
            ORDER BY updated_at DESC
        """, (today,))

        tasks = [{'title': row[0], 'category': row[1]} for row in cursor.fetchall()]
        conn.close()
        return tasks

    def _get_new_lessons_today(self) -> list[dict]:
        """Hole heute erstellte Lessons."""
        conn = sqlite3.connect(self.db_path)
        today = datetime.now().strftime("%Y-%m-%d")

        cursor = conn.execute("""
            SELECT title, solution
            FROM memory_lessons
            WHERE DATE(created_at) = ?
            ORDER BY created_at DESC
        """, (today,))

        lessons = [{'title': row[0], 'solution': row[1]} for row in cursor.fetchall()]
        conn.close()
        return lessons

    def _build_log(self, date: str, completed_tasks: list, new_lessons: list) -> str:
        """Baut Log-Content."""
        lines = []
        lines.append(f"# Session-Log: {date}")
        lines.append("")
        lines.append(f"**Zeit:** {datetime.now().strftime('%H:%M')}")
        lines.append("")
        lines.append("---")
        lines.append("")

        if completed_tasks:
            lines.append("## Abgeschlossene Tasks")
            lines.append("")
            for task in completed_tasks:
                cat = f" ({task['category']})" if task['category'] else ""
                lines.append(f"- [x] {task['title']}{cat}")
            lines.append("")

        if new_lessons:
            lines.append("## Neue Lessons")
            lines.append("")
            for lesson in new_lessons:
                lines.append(f"- **{lesson['title']}:** {lesson['solution']}")
            lines.append("")

        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# CLI-Entry-Point
# ═══════════════════════════════════════════════════════════════

def main():
    """CLI für memory_sync."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python memory_sync.py <generate|ingest|status>")
        return 1

    # BACH_ROOT ermitteln
    script_dir = Path(__file__).parent.parent  # system/
    bach_root = script_dir.parent  # BACH_v2_vanilla/

    sync = MemorySync(bach_root)
    command = sys.argv[1]

    if command == "generate":
        success, message = sync.generate()
        print(message)
        return 0 if success else 1

    elif command == "ingest":
        success, message = sync.ingest()
        print(message)
        return 0 if success else 1

    elif command == "status":
        success, message = sync.status()
        print(message)
        return 0 if success else 1

    else:
        print(f"Unknown command: {command}")
        return 1


if __name__ == "__main__":
    exit(main())
