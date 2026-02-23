# SPDX-License-Identifier: MIT
"""
Startup Handler - Session starten (DB-basiert)
==============================================

Mit Directory-Scan, Memory-Check, und Session-Kontinuitaet.

Nutzermodi (v1.1.37):
    gui     - Startet GUI Dashboard (Default)
    text    - Startet nur Konsole, kein Browser
    dual    - Startet GUI + Konsole
    silent  - Startet nichts automatisch
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from .base import BaseHandler


class StartupHandler(BaseHandler):
    """Handler fuer --startup - DB-basiert"""

    def __init__(self, base_path: Path):
        super().__init__(base_path)
        self.db_path = base_path / "data" / "bach.db"
        self.user_config_path = base_path / "data" / "user_config.json"

    @property
    def profile_name(self) -> str:
        return "startup"

    @property
    def target_file(self) -> Path:
        return self.db_path

    def get_operations(self) -> dict:
        return {
            "run": "Komplettes Startprotokoll (Standard)",
            "quick": "Schnellstart ohne Dir-Scan",
            "mode": "Modus aendern: gui|text|dual|silent"
        }

    def _load_user_config(self) -> dict:
        """Laedt User-Config fuer Startup-Modus."""
        if self.user_config_path.exists():
            try:
                return json.loads(self.user_config_path.read_text(encoding='utf-8'))
            except:
                pass
        # Default-Config
        return {
            "startup_mode": "gui",
            "startup_modes": {
                "gui": {"gui": True, "console": False},
                "text": {"gui": False, "console": True},
                "dual": {"gui": True, "console": True},
                "silent": {"gui": False, "console": False}
            }
        }

    def _save_user_config(self, config: dict):
        """Speichert User-Config."""
        config["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        self.user_config_path.write_text(
            json.dumps(config, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )

    def _get_startup_mode(self, args: list) -> str:
        """Ermittelt Startup-Modus aus Args oder Config."""
        # 1. Flag-Argument pruefen: --mode=gui oder --mode gui
        for i, arg in enumerate(args):
            if arg.startswith("--mode="):
                return arg.split("=", 1)[1].lower()
            if arg == "--mode" and i + 1 < len(args):
                return args[i + 1].lower()

        # 2. Aus Config laden
        config = self._load_user_config()
        return config.get("startup_mode", "gui")

    def handle(self, operation: str, args: list, dry_run: bool = False) -> tuple:
        # Modus-Aenderung
        if operation == "mode" and args:
            new_mode = args[0].lower()
            valid_modes = ["gui", "text", "dual", "silent"]
            if new_mode in valid_modes:
                config = self._load_user_config()
                old_mode = config.get("startup_mode", "gui")
                config["startup_mode"] = new_mode
                self._save_user_config(config)
                return True, f"[OK] Startup-Modus geaendert: {old_mode} -> {new_mode}"
            else:
                return False, f"[ERROR] Ungueltiger Modus: {new_mode}\nGueltig: {', '.join(valid_modes)}"

        quick = operation == "quick"
        startup_mode = self._get_startup_mode(args)
        return self._run_startup(quick, dry_run, startup_mode)
    
    def _get_conn(self):
        return sqlite3.connect(self.db_path)
    
    def _run_startup(self, quick: bool, dry_run: bool, startup_mode: str = "gui") -> tuple:
        results = []
        now = datetime.now()
        
        results.append("=" * 55)
        results.append("         BACH SESSION STARTUP")
        results.append("=" * 55)
        results.append(f" Zeit: {now.strftime('%Y-%m-%d %H:%M:%S')} ({now.strftime('%A')})")
        results.append(f" Modus: {startup_mode.upper()}")
        results.append("=" * 55)
        
        if dry_run:
            results.append("[DRY-RUN] Keine Aenderungen")
        
        # 0. Directory Scan (nicht bei quick)
        if not quick:
            results.append("")
            results.append("[DIRECTORY SCAN]")
            try:
                from tools.dirscan import DirectoryScanner
                scanner = DirectoryScanner(self.base_path)
                has_changes, scan_report = scanner.startup_check()
                results.append(scan_report)
            except Exception as e:
                results.append(f" [SKIP] Dir-Scan: {e}")
        
        # ══════════════════════════════════════════════════════════════
        # 0.5 PROBLEMS FIRST - Fehler automatisch melden (von CHIAH)
        # ══════════════════════════════════════════════════════════════
        try:
            from tools.problems_first import scan_problems, format_problems_report
            problems = scan_problems(self.base_path, hours=24)
            if problems['total'] > 0:
                results.append("")
                results.append(format_problems_report(problems))
        except Exception as e:
            pass  # Silent fail - nicht kritisch
        
        # ══════════════════════════════════════════════════════════════
        # 0.6 PATH HEALER CHECK (dry-run) - Pfadprobleme erkennen
        # ══════════════════════════════════════════════════════════════
        try:
            from tools.path_healer import BachPathHealer
            healer = BachPathHealer(str(self.base_path))
            heal_result = healer.heal_all(dry_run=True)
            
            healed_count = len(heal_result.get('healed_files', []))
            if healed_count > 0:
                results.append("")
                results.append("[PATH HEALER]")
                results.append(f" [!] {healed_count} Dateien mit Pfadproblemen gefunden")
                for f in heal_result['healed_files'][:3]:
                    fname = Path(f['file']).name if isinstance(f, dict) and 'file' in f else str(f)[:30]
                    results.append(f"   - {fname}")
                if healed_count > 3:
                    results.append(f"   ... und {healed_count - 3} weitere")
                results.append(" --> bach maintain heal --execute zum Reparieren")
        except Exception as e:
            pass  # Silent fail - nicht kritisch
        
        # ══════════════════════════════════════════════════════════════
        # 0.7 REGISTRY WATCHER CHECK - Datenbank/JSON Konsistenz
        # ══════════════════════════════════════════════════════════════
        try:
            import sys
            sys.path.insert(0, str(self.base_path / "tools" / "maintenance"))
            from registry_watcher import RegistryWatcher
            watcher = RegistryWatcher(self.base_path)
            is_healthy, report = watcher.check_all()
            
            if not is_healthy:
                results.append("")
                results.append("[REGISTRY WATCHER]")
                missing = report.get('missing_tables', [])
                invalid = report.get('invalid_json', [])
                if missing:
                    results.append(f" [!] {len(missing)} fehlende DB-Tabellen")
                    for t in missing[:3]:
                        results.append(f"   - {t}")
                if invalid:
                    results.append(f" [!] {len(invalid)} ungueltige JSON-Dateien")
                results.append(" --> bach maintain registry fuer Details")
        except Exception as e:
            pass  # Silent fail - nicht kritisch
        
        # ══════════════════════════════════════════════════════════════
        # 0.8 SKILL HEALTH MONITOR - Skill/Agent Validierung
        # ══════════════════════════════════════════════════════════════
        try:
            from skill_health_monitor import SkillHealthMonitor
            monitor = SkillHealthMonitor(self.base_path)
            is_healthy, report = monitor.check_all()
            
            if not is_healthy and monitor.issues:
                results.append("")
                results.append("[SKILL HEALTH]")
                results.append(f" [!] {len(monitor.issues)} Skill-Probleme gefunden")
                for issue in monitor.issues[:3]:
                    results.append(f"   - {issue.get('message', '')[:40]}")
                if len(monitor.issues) > 3:
                    results.append(f"   ... und {len(monitor.issues) - 3} weitere")
                results.append(" --> bach maintain skills fuer Details")
        except Exception as e:
            pass  # Silent fail - nicht kritisch
        
        # ══════════════════════════════════════════════════════════════
        # 1. LETZTE SESSION - Kontinuitaet herstellen
        # ══════════════════════════════════════════════════════════════
        results.append("")
        results.append("[LETZTE SESSION]")
        try:
            conn = self._get_conn()
            last_session = conn.execute("""
                SELECT session_id, started_at, ended_at, summary, 
                       tasks_created, tasks_completed, continuation_context
                FROM memory_sessions 
                WHERE ended_at IS NOT NULL
                ORDER BY id DESC LIMIT 1
            """).fetchone()
            
            if last_session:
                sid, started, ended, summary, created, completed, continuation = last_session
                
                # Datum formatieren
                date = ended[:10] if ended else "?"
                time_end = ended[11:16] if ended and len(ended) > 11 else "?"
                
                results.append(f" Session: {sid}")
                results.append(f" Beendet: {date} {time_end}")
                results.append(f" Tasks: +{created or 0} erstellt, {completed or 0} erledigt")
                
                # Summary (erste Zeile)
                if summary:
                    first_line = summary.split('\n')[0][:50]
                    results.append(f" Thema: {first_line}...")
                
                # WICHTIG: continuation_context = was als naechstes kommt
                if continuation:
                    results.append("")
                    results.append(" *** NAECHSTE SCHRITTE ***")
                    for line in continuation.split('\n')[:3]:
                        if line.strip():
                            results.append(f"   {line.strip()[:50]}")
            else:
                results.append(" Keine vorherige Session gefunden")
            
            conn.close()
        except Exception as e:
            results.append(f" [ERROR] {e}")
        
        # ══════════════════════════════════════════════════════════════
        # 1.5 SNAPSHOT CHECK - Letzten Snapshot anzeigen
        # ══════════════════════════════════════════════════════════════
        try:
            conn = self._get_conn()
            import json
            snapshot = conn.execute("""
                SELECT id, name, snapshot_data, created_at FROM session_snapshots 
                ORDER BY created_at DESC LIMIT 1
            """).fetchone()
            
            if snapshot:
                snap_id, snap_name, snap_data, snap_time = snapshot
                # Nur anzeigen wenn Snapshot heute oder gestern erstellt wurde
                snap_date = snap_time[:10] if snap_time else ""
                today = datetime.now().strftime('%Y-%m-%d')
                
                if snap_date == today:
                    results.append("")
                    results.append("[SNAPSHOT VERFUEGBAR]")
                    results.append(f" Letzter: {snap_name} ({snap_time[11:16]})")
                    
                    # Offene Tasks aus Snapshot
                    try:
                        data = json.loads(snap_data) if snap_data else {}
                        tasks = data.get("open_tasks", [])
                        if tasks:
                            results.append(f" Tasks im Snapshot: {len(tasks)}")
                    except:
                        pass
                    
                    results.append(" --> bach snapshot load zum Fortsetzen")
            
            conn.close()
        except Exception as e:
            pass  # Silent fail - nicht kritisch
        
        # ══════════════════════════════════════════════════════════════
        # 2. MEMORY CHECK - Aktuelle Notizen und Fakten
        # ══════════════════════════════════════════════════════════════
        results.append("")
        results.append("[MEMORY CHECK]")
        try:
            conn = self._get_conn()
            working = conn.execute("SELECT COUNT(*) FROM memory_working WHERE is_active=1").fetchone()[0]
            facts = conn.execute("SELECT COUNT(*) FROM memory_facts").fetchone()[0]
            lessons = conn.execute("SELECT COUNT(*) FROM memory_lessons WHERE is_active=1").fetchone()[0]
            
            results.append(f" Working: {working} | Facts: {facts} | Lessons: {lessons}")
            
            # Letzte Notiz anzeigen
            last_note = conn.execute("""
                SELECT content, created_at FROM memory_working 
                WHERE is_active=1 ORDER BY created_at DESC LIMIT 1
            """).fetchone()
            if last_note:
                time = last_note[1][11:16] if last_note[1] else "?"
                results.append(f" Letzte Notiz [{time}]: {last_note[0][:40]}...")
            
            conn.close()
        except Exception as e:
            results.append(f" [ERROR] {e}")
        
        # ══════════════════════════════════════════════════════════════
        # 3. NEUE SESSION REGISTRIEREN
        # ══════════════════════════════════════════════════════════════
        if not dry_run:
            try:
                conn = self._get_conn()
                session_id = f"session_{now.strftime('%Y%m%d_%H%M%S')}"
                conn.execute("""
                    INSERT INTO memory_sessions (session_id, started_at, tasks_created, tasks_completed)
                    VALUES (?, ?, 0, 0)
                """, (session_id, now.isoformat()))
                conn.commit()
                conn.close()
                results.append("")
                results.append(f"[SESSION] {session_id} gestartet")
            except Exception as e:
                pass  # Nicht kritisch
        
        # ══════════════════════════════════════════════════════════════
        # 4. NACHRICHTEN CHECK
        # ══════════════════════════════════════════════════════════════
        results.append("")
        results.append("[NACHRICHTEN]")
        try:
            user_db = self.base_path / "data" / "user.db"
            if user_db.exists():
                conn_user = sqlite3.connect(user_db)
                unread = conn_user.execute(
                    "SELECT COUNT(*) FROM messages WHERE status = 'unread'"
                ).fetchone()[0]
                total = conn_user.execute("SELECT COUNT(*) FROM messages").fetchone()[0]

                if unread > 0:
                    results.append(f" *** {unread} UNGELESENE NACHRICHT(EN) ***")
                    # Letzte ungelesene anzeigen
                    recent = conn_user.execute("""
                        SELECT sender, subject, created_at FROM messages
                        WHERE status = 'unread' ORDER BY created_at DESC LIMIT 3
                    """).fetchall()
                    for sender, subject, created in recent:
                        subj = (subject or "(kein Betreff)")[:30]
                        results.append(f"   Von: {sender} - {subj}")
                    results.append(" --> bach msg unread fuer Details")
                else:
                    results.append(f" {total} Nachrichten, keine ungelesen")
                conn_user.close()
            else:
                results.append(" [SKIP] user.db nicht gefunden")
        except Exception as e:
            results.append(f" [ERROR] {e}")

        # ══════════════════════════════════════════════════════════════
        # 4.5 RECURRING TASKS CHECK - Faellige periodische Tasks
        # ══════════════════════════════════════════════════════════════
        results.append("")
        results.append("[PERIODISCHE TASKS]")
        try:
            import sys
            recurring_path = self.base_path / "skills" / "_services" / "recurring"
            sys.path.insert(0, str(recurring_path))
            from recurring_tasks import list_recurring_tasks
            
            tasks = list_recurring_tasks()
            due_tasks = [(tid, info) for tid, info in tasks.items() 
                        if info.get('is_due') and info.get('enabled')]
            
            if due_tasks:
                results.append(f" *** {len(due_tasks)} TASK(S) FAELLIG ***")
                for tid, info in due_tasks[:3]:
                    target = "ATI" if info.get('target') == 'ati_tasks' else "BACH"
                    results.append(f"   [{tid}] {info.get('task_text', '')[:40]} -> {target}")
                if len(due_tasks) > 3:
                    results.append(f"   ... und {len(due_tasks) - 3} weitere")
                results.append(" --> bach --recurring check zum Erstellen")
            else:
                active = sum(1 for t in tasks.values() if t.get('enabled'))
                results.append(f" {len(tasks)} Tasks konfiguriert, {active} aktiv, keine faellig")
        except Exception as e:
            results.append(f" [SKIP] Recurring: {e}")

        # ══════════════════════════════════════════════════════════════
        # 5. BACH SYSTEM-TASKS
        # ══════════════════════════════════════════════════════════════
        results.append("")
        results.append("[BACH SYSTEM-TASKS]")
        try:
            conn = self._get_conn()
            
            # System-Tasks aus bach.db/tasks
            open_tasks = conn.execute("""
                SELECT COUNT(*) FROM tasks WHERE status IN ('pending', 'open', 'in_progress')
            """).fetchone()[0]
            done_tasks = conn.execute("""
                SELECT COUNT(*) FROM tasks WHERE status = 'done'
            """).fetchone()[0]
            
            results.append(f" {open_tasks} offen, {done_tasks} erledigt")
            
            # Top 3 nach Prioritaet
            top_tasks = conn.execute("""
                SELECT id, title FROM tasks 
                WHERE status IN ('pending', 'open', 'in_progress')
                ORDER BY 
                    CASE WHEN title LIKE 'P1%' THEN 1
                         WHEN title LIKE 'P2%' THEN 2
                         WHEN title LIKE 'P3%' THEN 3
                         ELSE 4 END,
                    id
                LIMIT 3
            """).fetchall()
            
            if top_tasks:
                results.append(" Top-Aufgaben:")
                for tid, title in top_tasks:
                    results.append(f"   [{tid}] {title[:45]}")
                results.append("")
                results.append(" --> bach task list fuer alle")
            
            conn.close()
        except Exception as e:
            results.append(f" [ERROR] {e}")
        
        # ══════════════════════════════════════════════════════════════
        # 5.5 DELEGATION-VORSCHLAEGE - Tasks mit Partner-Keywords matchen
        # ══════════════════════════════════════════════════════════════
        results.append("")
        results.append("[DELEGATION-VORSCHLAEGE]")
        try:
            conn = self._get_conn()
            
            # Keyword -> Partner Mapping (aus partner_registry.json abgeleitet)
            delegation_keywords = {
                "ollama": ["embed", "draft", "bulk", "zusammenfass", "embedding", "vektor"],
                "gemini": ["research", "analyse", "recherche", "dokument", "lang", "deep"],
                "copilot": ["code", "review", "refactor", "implement", "debug", "fix"],
                "perplexity": ["quelle", "source", "web", "aktuell", "news", "search"]
            }
            
            # Offene Tasks holen
            tasks = conn.execute("""
                SELECT id, title FROM tasks 
                WHERE status IN ('pending', 'open', 'in_progress')
                ORDER BY id
            """).fetchall()
            
            suggestions = []
            for task_id, title in tasks:
                title_lower = title.lower()
                for partner, keywords in delegation_keywords.items():
                    for kw in keywords:
                        if kw in title_lower:
                            suggestions.append((task_id, title[:35], partner))
                            break
                    else:
                        continue
                    break
            
            if suggestions:
                results.append(f" {len(suggestions)} Task(s) mit Delegations-Potenzial:")
                for task_id, title, partner in suggestions[:3]:
                    results.append(f"   [{task_id}] {title}... -> {partner.upper()}")
                if len(suggestions) > 3:
                    results.append(f"   ... +{len(suggestions)-3} weitere")
                results.append(" --> bach partner delegate \"task\" --to=PARTNER")
            else:
                results.append(" Keine passenden Keywords in offenen Tasks")
            
            conn.close()
        except Exception as e:
            results.append(f" [SKIP] {e}")
        
        # ══════════════════════════════════════════════════════════════
        # 5.6 PARTNER-AUSLASTUNG WARNUNG - Doppelbearbeitung verhindern
        # ══════════════════════════════════════════════════════════════
        try:
            conn = self._get_conn()
            
            # Tasks nach Partner-Zuweisung (category-Feld) gruppieren
            partner_tasks = conn.execute("""
                SELECT LOWER(category) as cat, COUNT(*) as cnt 
                FROM tasks 
                WHERE status IN ('pending', 'open', 'in_progress')
                AND LOWER(category) NOT IN ('user', 'bach', 'system', 'gui', 'wiki', 'agents', 'core', 'mail', 'integ', 'ollama', 'task', 'deprecate')
                AND category IS NOT NULL
                AND category != ''
                GROUP BY LOWER(category)
                HAVING cnt > 1
                ORDER BY cnt DESC
            """).fetchall()
            
            if partner_tasks:
                results.append("")
                results.append("[PARTNER-AUSLASTUNG WARNUNG]")
                results.append(" *** PARTNER MIT MEHREREN OFFENEN TASKS ***")
                for partner, count in partner_tasks:
                    results.append(f"   {partner.upper()}: {count} offene Tasks")
                results.append(" HINWEIS: Doppelbearbeitung vermeiden!")
                results.append(" --> bach task list --filter PARTNER fuer Details")
            
            conn.close()
        except Exception as e:
            pass  # Silent fail - nicht kritisch
        
        # ══════════════════════════════════════════════════════════════
        # 6. ATI-HINWEIS (Software-Entwickler-Agent)
        # ══════════════════════════════════════════════════════════════
        # Der Scanner fuer AUFGABEN.txt gehoert zu ATI, nicht zu BACH!
        # Wenn ATI implementiert ist: bach ati status
        results.append("")
        results.append("[ATI AGENT]")
        ati_path = self.base_path / "skills" / "_agents" / "ati"
        if ati_path.exists():
            results.append(" ATI Ordner vorhanden")
            results.append(" Software-Entwicklungs-Tasks: bach ati task list (geplant)")
            results.append(" AUFGABEN.txt Scanner: bach ati scan (geplant)")
        else:
            results.append(" [SKIP] ATI Agent nicht eingerichtet")
        
        # ══════════════════════════════════════════════════════════════
        # 7. LESSONS LEARNED
        # ══════════════════════════════════════════════════════════════
        results.append("")
        results.append("[LESSONS LEARNED]")
        try:
            conn = self._get_conn()
            count = conn.execute("SELECT COUNT(*) FROM memory_lessons WHERE is_active=1").fetchone()[0]
            if count > 0:
                results.append(f" {count} Lessons gespeichert")
                lessons = conn.execute("""
                    SELECT category, title FROM memory_lessons 
                    WHERE is_active=1 ORDER BY created_at DESC LIMIT 3
                """).fetchall()
                for cat, title in lessons:
                    results.append(f"   [{cat}] {title[:40]}")
                results.append(" --> bach lesson last fuer Details")
            else:
                results.append(" Keine Lessons vorhanden")
            conn.close()
        except Exception as e:
            results.append(f" [ERROR] {e}")
        
        # ══════════════════════════════════════════════════════════════
        # 8. AUTOLOG (.txt - bleibt Datei-basiert!)
        # ══════════════════════════════════════════════════════════════
        results.append("")
        results.append("[AUTOLOG]")
        autolog = self.base_path / "logs" / "auto_log.txt"
        if autolog.exists():
            try:
                content = autolog.read_text(encoding="utf-8")
                lines = content.strip().split("\n")
                results.append(f" {len(lines)} Eintraege")
                # Letzte 3 Befehle
                cmd_lines = [l for l in lines if "CMD:" in l][-3:]
                if cmd_lines:
                    results.append(" Letzte Befehle:")
                    for line in cmd_lines:
                        parts = line.split("CMD:")
                        if len(parts) > 1:
                            results.append(f"   {parts[1].strip()[:40]}")
                results.append(" --> bach logs tail 20 fuer mehr")
            except:
                results.append(" [?] Nicht lesbar")
        else:
            results.append(" Kein Autolog vorhanden")
        
        # ══════════════════════════════════════════════════════════════
        # 9. INJEKTOREN
        # ══════════════════════════════════════════════════════════════
        results.append("")
        results.append("[INJEKTOREN]")
        try:
            from tools.injectors import InjectorConfig
            config = InjectorConfig(self.base_path / "config.json")
            active = [k.replace("_injector", "") for k, v in config.config.items() 
                     if k.endswith("_injector") and v]
            if active:
                results.append(f" Aktiv: {', '.join(active)}")
            else:
                results.append(" Alle deaktiviert")
        except:
            results.append(" [SKIP] Injektoren nicht verfuegbar")
        
        # ══════════════════════════════════════════════════════════════
        # 10. HOUSEKEEPING-CHECK (alte Analysen in user/)
        # ══════════════════════════════════════════════════════════════
        results.append("")
        results.append("[HOUSEKEEPING]")
        try:
            user_dir = self.base_path / "user"
            archive_patterns = ["*_ANALYSE_*", "ANALYSE_*", "*_synopse*", "*_vergleich*", 
                              "*_MAPPING*", "*_Landkarte*", "*_INTEGRATION_*"]
            old_docs = []
            for pattern in archive_patterns:
                for f in user_dir.glob(pattern):
                    if f.is_file() and "_archive" not in str(f):
                        old_docs.append(f.name)
            if old_docs:
                results.append(f" *** {len(old_docs)} ALTE ANALYSE-DOCS in user/ ***")
                for doc in old_docs[:3]:
                    results.append(f"   -> {doc}")
                if len(old_docs) > 3:
                    results.append(f"   ... +{len(old_docs)-3} weitere")
                results.append(" HINWEIS: Nach Bearbeitung in user/_archive verschieben")
            else:
                results.append(" [OK] Keine alten Analysen in user/")
        except Exception as e:
            results.append(f" [SKIP] Housekeeping: {e}")

        # ══════════════════════════════════════════════════════════════
        # 11. GUI/KONSOLE START (abhaengig vom Modus)
        # ══════════════════════════════════════════════════════════════
        config = self._load_user_config()
        mode_config = config.get("startup_modes", {}).get(startup_mode, {})
        start_gui = mode_config.get("gui", True)
        start_console = mode_config.get("console", False)

        results.append("")
        results.append(f"[STARTUP MODUS: {startup_mode.upper()}]")

        if startup_mode == "silent":
            results.append(" [SILENT] Kein automatischer Start")
        elif not dry_run:
            if start_gui:
                gui_started = self._start_gui_background()
                if gui_started:
                    results.append(" [OK] GUI Server gestartet (http:/127.0.0.1:8000)")
                else:
                    results.append(" [SKIP] GUI bereits aktiv oder Fehler")
            else:
                results.append(" [SKIP] GUI deaktiviert (Modus: {})".format(startup_mode))

            if start_console:
                console_started = self._start_console_background()
                if console_started:
                    results.append(" [OK] Konsole gestartet")
                else:
                    results.append(" [SKIP] Konsole nicht gestartet")
        else:
            results.append(" [DRY-RUN] GUI/Konsole wuerde gestartet")
        
        # ══════════════════════════════════════════════════════════════
        # 12. TOKEN-ZONE CHECK (NEU v1.1.34)
        # ══════════════════════════════════════════════════════════════
        results.append("")
        results.append("[TOKEN-ZONE]")
        try:
            from tools.token_monitor import get_token_zone, format_zone_status, check_emergency_shutdown
            zone, desc, details = get_token_zone()
            results.append(format_zone_status(zone, desc, details))
            
            # TOKEN_001: Emergency Check bei 95%+
            should_stop, emergency_msg = check_emergency_shutdown(details.get('budget_percent'))
            if should_stop:
                results.append(emergency_msg)
        except Exception as e:
            results.append(f" [SKIP] Token-Monitor nicht verfuegbar: {e}")
        
        # ══════════════════════════════════════════════════════════════
        # 13. SYNC CHECK (SYNC_004b - Optional bei auto_sync_enabled)
        # ══════════════════════════════════════════════════════════════
        try:
            conn = self._get_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM system_config WHERE key = 'auto_sync_enabled'")
            row = cursor.fetchone()
            auto_sync = row and row[0] == 'true'
            conn.close()
            
            if auto_sync:
                results.append("")
                results.append("[SYNC CHECK]")
                from .sync import SyncHandler
                sync = SyncHandler(self.base_path)
                success, status_msg = sync._status()
                # Nur Zusammenfassung anzeigen
                for line in status_msg.split('\n'):
                    if 'ZUSAMMENFASSUNG' in line or 'geaendert' in line or 'bach --sync' in line or 'Alles synchron' in line:
                        results.append(f" {line.strip()}")
        except Exception as e:
            pass  # Silent fail - nicht kritisch
        
        # Footer
        results.append("")
        results.append("=" * 55)
        results.append(" READY - Session gestartet")
        results.append("")
        results.append(" HINWEIS: Bei Shutdown -> bach --memory session \"...\"")
        results.append("=" * 55)
        
        return True, "\n".join(results)
    
    def _start_gui_background(self) -> bool:
        """Startet GUI-Server im Hintergrund und oeffnet Browser."""
        import socket
        import sys
        import subprocess
        import webbrowser
        
        port = 8000
        url = f"http:/127.0.0.1:{port}"
        server_script = self.base_path / "gui" / "server.py"
        
        # Pruefen ob Script existiert
        if not server_script.exists():
            return False
        
        # Pruefen ob bereits laeuft
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        
        already_running = (result == 0)
        
        if not already_running:
            # Server im Hintergrund starten
            try:
                if sys.platform == "win32":
                    import os
                    cmd = f'start /b python "{server_script}" --port {port}'
                    os.system(cmd)
                else:
                    subprocess.Popen(
                        [sys.executable, str(server_script), "--port", str(port)],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        start_new_session=True
                    )
                
                import time
                time.sleep(1.5)  # Kurz warten bis Server hochfaehrt
                
                # Pruefen ob gestartet
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex(('127.0.0.1', port))
                sock.close()
                
                if result != 0:
                    return False
                    
            except Exception:
                return False
        
        # Browser oeffnen (immer, auch wenn Server schon lief)
        try:
            webbrowser.open(url)
        except Exception:
            pass  # Browser-Fehler nicht kritisch

        return True

    def _start_console_background(self) -> bool:
        """Startet eine neue Konsole mit bach.py im Text-Modus."""
        import sys
        import subprocess

        bach_py = self.base_path / "bach.py"
        if not bach_py.exists():
            return False

        try:
            if sys.platform == "win32":
                import os
                # Neues CMD-Fenster oeffnen mit bach.py
                cmd = f'start cmd /k "cd /d {self.base_path} && python bach.py --help"'
                os.system(cmd)
            else:
                # Linux/Mac: xterm oder gnome-terminal
                subprocess.Popen(
                    ["x-terminal-emulator", "-e", f"cd {self.base_path} && python bach.py --help"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True
                )
            return True
        except Exception:
            return False
