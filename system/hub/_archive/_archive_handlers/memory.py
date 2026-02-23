# SPDX-License-Identifier: MIT
"""
Memory Handler - DB-basiertes Memory-Management
===============================================

Alles in bach.db, kein Dateisystem mehr.

Tabellen:
- memory_working:  Schnelle Notizen (scratchpad, context, note)
- memory_facts:    Persistente Fakten (user, project, system)
- memory_lessons:  Lessons Learned (eigener Handler)
- memory_sessions: Session-Tracking (automatisch)
"""
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional
from .base import BaseHandler


class MemoryHandler(BaseHandler):
    """Handler fuer --memory Operationen - DB-basiert"""
    
    def __init__(self, base_path: Path):
        super().__init__(base_path)
        self.db_path = base_path / "data" / "bach.db"
    
    @property
    def profile_name(self) -> str:
        return "memory"
    
    @property
    def target_file(self) -> Path:
        return self.db_path
    
    def get_operations(self) -> dict:
        return {
            "status": "Memory-Uebersicht (Counts)",
            "write": "Notiz schreiben (in memory_working)",
            "read": "Letzte Notizen lesen",
            "fact": "Fakt speichern (key:value)",
            "facts": "Alle Fakten anzeigen",
            "search": "Memory durchsuchen",
            "context": "Kontext fuer Claude generieren",
            "clear": "Working Memory leeren",
            "session": "Session-Bericht speichern (Shutdown)",
            "sessions": "Letzte Sessions anzeigen"
        }
    
    def handle(self, operation: str, args: list, dry_run: bool = False) -> tuple:
        if not self.db_path.exists():
            return False, f"Datenbank nicht gefunden: {self.db_path}"
        
        if operation == "status" or not operation:
            return self._status()
        elif operation == "write":
            if not args:
                return False, "Usage: --memory write \"Notiz\""
            return self._write(" ".join(args), dry_run)
        elif operation == "read":
            n = int(args[0]) if args else 10
            return self._read(n)
        elif operation == "fact":
            if not args:
                return False, "Usage: --memory fact \"key:value\""
            return self._add_fact(" ".join(args), dry_run)
        elif operation == "facts":
            category = args[0] if args else None
            return self._list_facts(category)
        elif operation == "search":
            if not args:
                return False, "Usage: --memory search \"keyword\""
            return self._search(" ".join(args))
        elif operation == "context":
            return self._generate_context()
        elif operation == "clear":
            return self._clear_working(dry_run)
        elif operation == "session":
            if not args:
                return False, "Usage: --memory session \"Zusammenfassung der Session\""
            return self._save_session(" ".join(args), dry_run)
        elif operation == "sessions":
            n = int(args[0]) if args else 5
            return self._list_sessions(n)
        else:
            return self._status()
    
    def _get_conn(self):
        return sqlite3.connect(self.db_path)
    
    def _status(self) -> tuple:
        conn = self._get_conn()
        try:
            working = conn.execute("SELECT COUNT(*) FROM memory_working WHERE is_active=1").fetchone()[0]
            facts = conn.execute("SELECT COUNT(*) FROM memory_facts").fetchone()[0]
            lessons = conn.execute("SELECT COUNT(*) FROM memory_lessons WHERE is_active=1").fetchone()[0]
            sessions = conn.execute("SELECT COUNT(*) FROM memory_sessions").fetchone()[0]
            
            results = [
                "MEMORY STATUS (DB-basiert)",
                "=" * 50,
                "",
                f"  Working Memory:  {working} aktive Eintraege",
                f"  Facts:           {facts} Fakten",
                f"  Lessons:         {lessons} Lessons",
                f"  Sessions:        {sessions} Sessions",
                "",
                "Befehle:",
                "  --memory write \"...\"   Notiz speichern",
                "  --memory read [n]      Letzte n lesen",
                "  --memory fact k:v      Fakt speichern", 
                "  --memory search \"...\" Durchsuchen",
                "  --memory context       Kontext generieren"
            ]
            return True, "\n".join(results)
        finally:
            conn.close()
    
    def _write(self, text: str, dry_run: bool) -> tuple:
        """Notiz in memory_working speichern."""
        if dry_run:
            return True, f"[DRY-RUN] Wuerde speichern: {text[:50]}..."
        
        conn = self._get_conn()
        try:
            now = datetime.now().isoformat()
            conn.execute("""
                INSERT INTO memory_working (type, content, created_at, updated_at)
                VALUES ('note', ?, ?, ?)
            """, (text, now, now))
            conn.commit()
            return True, f"[OK] Notiz gespeichert."
        except Exception as e:
            return False, f"Fehler: {e}"
        finally:
            conn.close()
    
    def _read(self, n: int = 10) -> tuple:
        """Letzte n Notizen aus memory_working lesen."""
        conn = self._get_conn()
        try:
            rows = conn.execute("""
                SELECT id, type, content, created_at 
                FROM memory_working 
                WHERE is_active = 1
                ORDER BY created_at DESC
                LIMIT ?
            """, (n,)).fetchall()
            
            if not rows:
                return True, "Keine Notizen im Working Memory."
            
            results = [f"WORKING MEMORY (letzte {len(rows)})", "=" * 50]
            for id, type, content, created in rows:
                time = created[11:16] if created else "?"
                results.append(f"[{time}] ({type}) {content[:60]}{'...' if len(content) > 60 else ''}")
            
            return True, "\n".join(results)
        finally:
            conn.close()
    
    def _add_fact(self, text: str, dry_run: bool) -> tuple:
        """Fakt in memory_facts speichern. Format: category.key:value oder key:value"""
        if ":" not in text:
            return False, "Format: key:value oder category.key:value"
        
        parts = text.split(":", 1)
        key_part = parts[0].strip()
        value = parts[1].strip()
        
        # Category.key oder nur key
        if "." in key_part:
            cat_key = key_part.split(".", 1)
            category = cat_key[0]
            key = cat_key[1]
        else:
            category = "project"
            key = key_part
        
        valid_cats = ['user', 'project', 'system', 'domain']
        if category not in valid_cats:
            category = "project"
        
        if dry_run:
            return True, f"[DRY-RUN] Fakt: [{category}] {key} = {value}"
        
        conn = self._get_conn()
        try:
            now = datetime.now().isoformat()
            # UPSERT
            conn.execute("""
                INSERT INTO memory_facts (category, key, value, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(category, key) DO UPDATE SET 
                    value = excluded.value,
                    updated_at = excluded.updated_at
            """, (category, key, value, now, now))
            conn.commit()
            return True, f"[OK] Fakt gespeichert: [{category}] {key} = {value}"
        except Exception as e:
            return False, f"Fehler: {e}"
        finally:
            conn.close()
    
    def _list_facts(self, category: str = None) -> tuple:
        """Alle Fakten anzeigen."""
        conn = self._get_conn()
        try:
            if category:
                rows = conn.execute("""
                    SELECT category, key, value, updated_at 
                    FROM memory_facts WHERE category = ?
                    ORDER BY key
                """, (category,)).fetchall()
            else:
                rows = conn.execute("""
                    SELECT category, key, value, updated_at 
                    FROM memory_facts ORDER BY category, key
                """).fetchall()
            
            if not rows:
                return True, "Keine Fakten gespeichert."
            
            results = ["MEMORY FACTS", "=" * 50]
            current_cat = None
            for cat, key, value, updated in rows:
                if cat != current_cat:
                    results.append(f"\n[{cat.upper()}]")
                    current_cat = cat
                results.append(f"  {key}: {value[:50]}{'...' if len(value) > 50 else ''}")
            
            results.append(f"\nGesamt: {len(rows)} Fakten")
            return True, "\n".join(results)
        finally:
            conn.close()
    
    def _search(self, keyword: str) -> tuple:
        """Durchsucht alle Memory-Tabellen."""
        conn = self._get_conn()
        results = [f"SUCHE: {keyword}", "=" * 50]
        
        try:
            # Working Memory
            working = conn.execute("""
                SELECT 'working' as src, content, created_at 
                FROM memory_working 
                WHERE content LIKE ? AND is_active = 1
                LIMIT 10
            """, (f"%{keyword}%",)).fetchall()
            
            # Facts
            facts = conn.execute("""
                SELECT 'fact' as src, key || ': ' || value, updated_at 
                FROM memory_facts 
                WHERE key LIKE ? OR value LIKE ?
                LIMIT 10
            """, (f"%{keyword}%", f"%{keyword}%")).fetchall()
            
            # Lessons
            lessons = conn.execute("""
                SELECT 'lesson' as src, title || ': ' || solution, created_at 
                FROM memory_lessons 
                WHERE (title LIKE ? OR solution LIKE ?) AND is_active = 1
                LIMIT 10
            """, (f"%{keyword}%", f"%{keyword}%")).fetchall()
            
            all_results = working + facts + lessons
            
            if not all_results:
                return True, f"Keine Treffer fuer: {keyword}"
            
            for src, content, date in all_results:
                results.append(f"  [{src}] {content[:50]}...")
            
            results.append(f"\n{len(all_results)} Treffer")
            return True, "\n".join(results)
        finally:
            conn.close()
    
    def _generate_context(self) -> tuple:
        """Generiert kompakten Kontext fuer Claude."""
        conn = self._get_conn()
        try:
            context_parts = []
            
            # Aktive Working Notes (letzte 5)
            working = conn.execute("""
                SELECT content FROM memory_working 
                WHERE is_active = 1 ORDER BY created_at DESC LIMIT 5
            """).fetchall()
            if working:
                context_parts.append("## Aktuelle Notizen")
                for (content,) in working:
                    context_parts.append(f"- {content[:100]}")
            
            # Wichtige Facts
            facts = conn.execute("""
                SELECT category, key, value FROM memory_facts 
                ORDER BY updated_at DESC LIMIT 10
            """).fetchall()
            if facts:
                context_parts.append("\n## Fakten")
                for cat, key, value in facts:
                    context_parts.append(f"- {key}: {value[:50]}")
            
            # Letzte Lessons (nur Titel)
            lessons = conn.execute("""
                SELECT title FROM memory_lessons 
                WHERE is_active = 1 ORDER BY created_at DESC LIMIT 5
            """).fetchall()
            if lessons:
                context_parts.append("\n## Letzte Lessons")
                for (title,) in lessons:
                    context_parts.append(f"- {title}")
            
            if not context_parts:
                return True, "Kein Kontext verfuegbar."
            
            return True, "\n".join(context_parts)
        finally:
            conn.close()
    
    def _clear_working(self, dry_run: bool) -> tuple:
        """Working Memory leeren (soft delete)."""
        if dry_run:
            return True, "[DRY-RUN] Wuerde Working Memory leeren"
        
        conn = self._get_conn()
        try:
            conn.execute("UPDATE memory_working SET is_active = 0")
            conn.commit()
            return True, "[OK] Working Memory geleert."
        finally:
            conn.close()
    
    def _save_session(self, summary: str, dry_run: bool) -> tuple:
        """Session-Bericht in memory_sessions speichern."""
        if dry_run:
            return True, f"[DRY-RUN] Wuerde Session speichern: {summary[:50]}..."
        
        conn = self._get_conn()
        try:
            now = datetime.now()
            session_id = f"session_{now.strftime('%Y%m%d_%H%M%S')}"
            
            # Pruefen ob es eine offene Session gibt
            open_session = conn.execute("""
                SELECT id, session_id FROM memory_sessions 
                WHERE ended_at IS NULL ORDER BY id DESC LIMIT 1
            """).fetchone()
            
            if open_session:
                # Offene Session abschliessen
                conn.execute("""
                    UPDATE memory_sessions 
                    SET ended_at = ?, summary = ?
                    WHERE id = ?
                """, (now.isoformat(), summary, open_session[0]))
                session_id = open_session[1]
                action = "abgeschlossen"
            else:
                # Neue Session mit gleichem Start/End (nachtraeglicher Bericht)
                conn.execute("""
                    INSERT INTO memory_sessions 
                    (session_id, started_at, ended_at, summary, tasks_created, tasks_completed)
                    VALUES (?, ?, ?, ?, 0, 0)
                """, (session_id, now.isoformat(), now.isoformat(), summary))
                action = "erstellt"
            
            conn.commit()
            return True, f"[OK] Session {session_id} {action}"
        except Exception as e:
            return False, f"Fehler: {e}"
        finally:
            conn.close()
    
    def _list_sessions(self, n: int = 5) -> tuple:
        """Letzte n Sessions anzeigen."""
        conn = self._get_conn()
        try:
            rows = conn.execute("""
                SELECT session_id, started_at, ended_at, summary, 
                       tasks_created, tasks_completed, continuation_context
                FROM memory_sessions 
                ORDER BY id DESC LIMIT ?
            """, (n,)).fetchall()
            
            if not rows:
                return True, "Keine Sessions gespeichert."
            
            results = [f"LETZTE {len(rows)} SESSIONS", "=" * 60]
            
            for sid, started, ended, summary, created, completed, continuation in rows:
                # Datum formatieren
                date = started[:10] if started else "?"
                time_start = started[11:16] if started and len(started) > 11 else "?"
                time_end = ended[11:16] if ended and len(ended) > 11 else "aktiv"
                
                results.append("")
                results.append(f"[{sid}]")
                results.append(f"  Zeit: {date} {time_start} - {time_end}")
                results.append(f"  Tasks: +{created or 0} erstellt, {completed or 0} erledigt")
                
                if summary:
                    # Erste Zeile der Summary
                    first_line = summary.split('\n')[0][:60]
                    results.append(f"  Summary: {first_line}...")
                
                if continuation:
                    results.append(f"  Naechste: {continuation[:50]}...")
            
            return True, "\n".join(results)
        finally:
            conn.close()
