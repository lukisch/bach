# SPDX-License-Identifier: MIT
"""
Shutdown Handler - Session beenden (DB-basiert)
================================================

Speichert Session-Bericht in memory_sessions.
Kein Markdown-Dateisystem mehr!

NEU v1.1.15: Auto-Memory Fallback - generiert Summary aus Autolog wenn Claude vergisst
"""
import sqlite3
from datetime import datetime
from pathlib import Path
from .base import BaseHandler


class ShutdownHandler(BaseHandler):
    """Handler fuer --shutdown - DB-basiert"""
    
    def __init__(self, base_path: Path):
        super().__init__(base_path)
        self.db_path = base_path / "data" / "bach.db"
    
    @property
    def profile_name(self) -> str:
        return "shutdown"
    
    @property
    def target_file(self) -> Path:
        return self.db_path
    
    def get_operations(self) -> dict:
        return {
            "complete": "Komplett mit Dir-Scan + Session-Speicherung (Standard)",
            "quick": "Schnell ohne Dir-Scan",
            "emergency": "Notfall - nur Working Memory sichern"
        }
    
    def handle(self, operation: str, args: list, dry_run: bool = False) -> tuple:
        summary = " ".join(args) if args else None
        
        if operation == "emergency":
            return self._emergency(summary, dry_run)
        elif operation == "quick":
            return self._quick(summary, dry_run)
        else:
            return self._complete(summary, dry_run)
    
    def _get_conn(self):
        return sqlite3.connect(self.db_path)
    
    def _get_active_session(self, conn) -> tuple:
        """Findet aktive Session (ohne ended_at)."""
        row = conn.execute("""
            SELECT id, session_id, started_at, tasks_created 
            FROM memory_sessions 
            WHERE ended_at IS NULL 
            ORDER BY id DESC LIMIT 1
        """).fetchone()
        return row
    
    def _generate_fallback_summary(self, session_start: str) -> str:
        """
        Generiert automatische Zusammenfassung aus Autolog.
        
        Wird aufgerufen wenn Claude keinen Session-Bericht mitgibt.
        Liest Autolog-Eintraege seit Session-Start und extrahiert Befehle.
        
        Returns:
            str: Automatisch generierte Zusammenfassung oder None
        """
        autolog_path = self.base_path / "logs" / "auto_log_extended.txt"
        
        if not autolog_path.exists():
            return None
        
        try:
            # Session-Start parsen
            start_time = datetime.fromisoformat(session_start.replace('Z', '+00:00'))
            
            # Autolog lesen
            with open(autolog_path, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
            
            # Befehle sammeln seit Session-Start
            commands = []
            for line in lines:
                # Format: [HH:MM:SS] CMD: befehl
                if 'CMD:' in line:
                    # Zeit extrahieren (erste 10 Zeichen: [HH:MM:SS])
                    try:
                        time_str = line[1:9]  # HH:MM:SS
                        today = datetime.now().date()
                        line_time = datetime.strptime(f"{today} {time_str}", "%Y-%m-%d %H:%M:%S")
                        
                        if line_time >= start_time:
                            # Befehl extrahieren
                            cmd_part = line.split('CMD:')[1].strip()
                            if cmd_part and cmd_part not in ['startup', 'shutdown']:
                                commands.append(cmd_part)
                    except (ValueError, IndexError):
                        continue
            
            if not commands:
                return "[AUTO] Keine Befehle in dieser Session"
            
            # Zusammenfassung generieren
            unique_commands = list(dict.fromkeys(commands))  # Duplikate entfernen, Reihenfolge behalten
            summary_parts = []
            summary_parts.append("[AUTO-FALLBACK]")
            summary_parts.append(f"Befehle: {len(commands)} ({len(unique_commands)} unique)")
            
            # Top 5 Befehle zeigen
            for cmd in unique_commands[:5]:
                summary_parts.append(f"- {cmd[:60]}")
            
            if len(unique_commands) > 5:
                summary_parts.append(f"... und {len(unique_commands) - 5} weitere")
            
            return " | ".join(summary_parts[:2]) + " || " + ", ".join(unique_commands[:3])
            
        except Exception as e:
            return f"[AUTO-ERROR] {str(e)[:50]}"
    
    def _emergency(self, summary: str, dry_run: bool) -> tuple:
        """Notfall-Shutdown - nur Status sichern."""
        results = []
        results.append("=" * 55)
        results.append("         EMERGENCY SHUTDOWN")
        results.append("=" * 55)
        
        if not dry_run:
            conn = self._get_conn()
            try:
                now = datetime.now().isoformat()
                # Notiz in Working Memory
                conn.execute("""
                    INSERT INTO memory_working (type, content, priority, created_at, updated_at, is_active)
                    VALUES ('emergency', ?, 10, ?, ?, 1)
                """, (f"EMERGENCY SHUTDOWN: {summary or 'Keine Details'}", now, now))
                conn.commit()
                results.append(" [OK] Emergency-Notiz gespeichert")
            except Exception as e:
                results.append(f" [ERROR] {e}")
            finally:
                conn.close()
        else:
            results.append(" [DRY-RUN] Wuerde Emergency-Notiz speichern")
        
        results.append("")
        results.append(" Session ABGEBROCHEN")
        results.append("=" * 55)
        
        return True, "\n".join(results)
    
    def _quick(self, summary: str, dry_run: bool) -> tuple:
        """Schnell-Shutdown ohne Dir-Scan."""
        results = []
        results.append("=" * 55)
        results.append("            QUICK SHUTDOWN")
        results.append("=" * 55)
        
        if not dry_run and summary:
            conn = self._get_conn()
            try:
                now = datetime.now().isoformat()
                conn.execute("""
                    INSERT INTO memory_working (type, content, created_at, updated_at, is_active)
                    VALUES ('note', ?, ?, ?, 1)
                """, (f"Quick-Shutdown: {summary}", now, now))
                conn.commit()
                results.append(f" [OK] Notiz: {summary[:40]}...")
            except Exception as e:
                results.append(f" [WARN] {e}")
            finally:
                conn.close()
        
        results.append(" [OK] Session pausiert")
        results.append("=" * 55)
        
        return True, "\n".join(results)
    
    def _complete(self, summary: str, dry_run: bool) -> tuple:
        """Komplett-Shutdown mit Dir-Scan und Session-Speicherung."""
        results = []
        now = datetime.now()
        
        results.append("=" * 55)
        results.append("          COMPLETE SHUTDOWN")
        results.append("=" * 55)
        results.append(f" Zeit: {now.strftime('%Y-%m-%d %H:%M')}")
        results.append("=" * 55)
        
        # 1. Directory-Scan Update
        results.append("")
        results.append("[DIRECTORY SCAN]")
        change_count = 0
        if not dry_run:
            try:
                from tools.dirscan import DirectoryScanner
                scanner = DirectoryScanner(self.base_path)
                scan_result = scanner.shutdown_update()
                results.append(f" {scan_result}")
                # Aenderungen zaehlen fuer Auto-Snapshot
                if hasattr(scanner, 'last_change_count'):
                    change_count = scanner.last_change_count
                else:
                    # Fallback: Aus Text schaetzen
                    import re
                    # Suche nach "(X Änderungen" oder "X neu" oder "X geaendert"
                    match = re.search(r'(\d+)\s*(?:Änderung|aenderung|neu|geaendert|geloescht)', scan_result.lower())
                    if match:
                        change_count = int(match.group(1))
                    else:
                        # Alternative: Suche nach "X Änderungen übernommen"
                        match2 = re.search(r'\((\d+)\s*(?:Änderung|änderung)', scan_result)
                        if match2:
                            change_count = int(match2.group(1))
            except Exception as e:
                results.append(f" [SKIP] {e}")
        else:
            results.append(" [DRY-RUN] Wuerde SOLL-Zustand aktualisieren")
        
        # 1b. Auto-Snapshot bei grossen Aenderungen (NEU v1.1.17)
        results.append("")
        results.append("[AUTO-SNAPSHOT]")
        if not dry_run and change_count >= 3:
            try:
                from .snapshot import SnapshotHandler
                snap_handler = SnapshotHandler(self.base_path)
                snap_name = f"auto_{now.strftime('%Y%m%d_%H%M%S')}"
                success, snap_msg = snap_handler._create(snap_name, dry_run=False)
                if success:
                    results.append(f" [OK] Auto-Snapshot erstellt ({change_count} Aenderungen)")
                else:
                    results.append(f" [SKIP] {snap_msg}")
            except Exception as e:
                results.append(f" [SKIP] Auto-Snapshot: {e}")
        elif not dry_run:
            results.append(f" [SKIP] Nur {change_count} Aenderungen (Schwelle: 3)")
        else:
            results.append(" [DRY-RUN] Wuerde Auto-Snapshot pruefen")
        
        # 2. Session in DB speichern
        results.append("")
        results.append("[SESSION SPEICHERN]")
        if not dry_run:
            conn = self._get_conn()
            try:
                # Aktive Session finden oder neue erstellen
                active = self._get_active_session(conn)
                
                # NEU v1.1.15: Auto-Memory Fallback
                if not summary and active:
                    session_start = active[2] if active else now.isoformat()
                    summary = self._generate_fallback_summary(session_start)
                    if summary:
                        results.append(f" [FALLBACK] Auto-Summary aus Autolog generiert")
                
                if active:
                    # Bestehende Session abschliessen
                    session_id = active[1]
                    conn.execute("""
                        UPDATE memory_sessions 
                        SET ended_at = ?, summary = COALESCE(summary, '') || ?
                        WHERE session_id = ?
                    """, (now.isoformat(), f"\n{summary}" if summary else "", session_id))
                    results.append(f" [OK] Session {session_id} abgeschlossen")
                else:
                    # Falls keine aktive Session, trotzdem Notiz speichern
                    if summary:
                        session_id = f"session_{now.strftime('%Y%m%d_%H%M%S')}"
                        conn.execute("""
                            INSERT INTO memory_sessions 
                            (session_id, started_at, ended_at, summary, tasks_created, tasks_completed)
                            VALUES (?, ?, ?, ?, 0, 0)
                        """, (session_id, now.isoformat(), now.isoformat(), summary))
                        results.append(f" [OK] Session {session_id} erstellt")
                    else:
                        results.append(" [SKIP] Keine aktive Session")
                
                conn.commit()
            except Exception as e:
                results.append(f" [ERROR] {e}")
            finally:
                conn.close()
        else:
            results.append(" [DRY-RUN] Wuerde Session speichern")
        
        # 3. Working Memory Stats
        results.append("")
        results.append("[MEMORY STATUS]")
        if not dry_run:
            conn = self._get_conn()
            try:
                working = conn.execute("SELECT COUNT(*) FROM memory_working WHERE is_active=1").fetchone()[0]
                facts = conn.execute("SELECT COUNT(*) FROM memory_facts").fetchone()[0]
                sessions = conn.execute("SELECT COUNT(*) FROM memory_sessions").fetchone()[0]
                results.append(f" Working: {working} | Facts: {facts} | Sessions: {sessions}")
            except Exception as e:
                results.append(f" [ERROR] {e}")
            finally:
                conn.close()
        
        # 4. Task-Statistik (NEU v1.1.8)
        results.append("")
        results.append("[TASK-STATISTIK]")
        tasks_created = 0
        tasks_completed = 0
        if not dry_run:
            conn = self._get_conn()
            try:
                # Aktive Session finden fuer Zeitraum
                active = self._get_active_session(conn)
                session_start = active[2] if active else now.replace(hour=0, minute=0).isoformat()
                
                # Tasks aus bach.db zaehlen (tasks-Tabelle)
                # Erstellt in dieser Session
                tasks_created = conn.execute("""
                    SELECT COUNT(*) FROM tasks 
                    WHERE created_at >= ?
                """, (session_start,)).fetchone()[0]
                
                # Erledigt in dieser Session
                tasks_completed = conn.execute("""
                    SELECT COUNT(*) FROM tasks 
                    WHERE status = 'done' AND completed_at >= ?
                """, (session_start,)).fetchone()[0]
                
                results.append(f" +{tasks_created} erstellt, {tasks_completed} erledigt (diese Session)")
                
                # Zaehler in memory_sessions aktualisieren
                if active:
                    conn.execute("""
                        UPDATE memory_sessions 
                        SET tasks_created = ?, tasks_completed = ?
                        WHERE session_id = ?
                    """, (tasks_created, tasks_completed, active[1]))
                    conn.commit()
            except Exception as e:
                results.append(f" [SKIP] {e}")
            finally:
                conn.close()
        else:
            results.append(" [DRY-RUN] Wuerde Task-Statistik zaehlen")
        
        results.append("")
        results.append("=" * 55)
        results.append(" Session BEENDET")
        results.append("=" * 55)
        results.append("")
        results.append("HINWEIS FUER CLAUDE:")
        results.append("Session-Bericht gehoert in memory_sessions (DB)!")
        results.append("Format: bach --memory session \"Zusammenfassung\"")
        results.append("Oder direkt in DB: INSERT INTO memory_sessions (...)")
        
        return True, "\n".join(results)
