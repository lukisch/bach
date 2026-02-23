#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
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
DB-Sync-Manager - OneDrive-basiertes Backup-Sync-System
========================================================

Synchronisiert bach.db über OneDrive-Backups mit .bachdb Endung.
Live-DB bleibt lokal (keine Konflikte), Backups werden synchronisiert.

Verwendung:
    bach db backup              # Manuelles Backup
    bach db sync                # Pull + Merge + Push
    bach db sync --status       # Status anzeigen
    bach db cleanup             # Alte Backups löschen

Version: 1.0.0
Erstellt: 2026-02-14
"""

import json
import os
import socket
import sqlite3
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple

from .base import BaseHandler


class DBSyncManager:
    """Verwaltet DB-Backups und Sync zwischen PCs."""

    def __init__(self, db_path: Path = None, backup_dir: Path = None):
        self.base_path = Path(__file__).parent.parent
        self.db_path = db_path or self.base_path / "data" / "bach.db"
        self.backup_dir = backup_dir or self.base_path.parent / "backups"
        self.hostname = socket.gethostname()
        self.heartbeat_file = self.backup_dir / "heartbeat.json"

        # Stelle sicher dass Backup-Ordner existiert
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    # ==================== BACKUP (DAILY GUARD) ====================

    def _get_retention_days(self) -> int:
        """Liest backup_retention_days aus system_config (Default: 7)."""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                row = conn.execute(
                    "SELECT value FROM system_config WHERE key = 'backup_retention_days'"
                ).fetchone()
                if row:
                    return int(row[0])
        except Exception:
            pass
        return 7

    def _has_backup_today(self) -> bool:
        """Prueft ob heute schon ein Backup von diesem Host erstellt wurde."""
        today = datetime.now().strftime("%Y-%m-%d")
        pattern = f"bach_{self.hostname}_{today}*.bachdb"
        return any(self.backup_dir.glob(pattern))

    def create_backup_if_needed(self) -> Optional[Path]:
        """Erstellt Backup nur wenn heute noch keins erstellt wurde.

        Fuehrt danach automatisch Cleanup alter Backups durch.

        Returns:
            Path zum Backup oder None wenn bereits vorhanden
        """
        if self._has_backup_today():
            return None

        backup_path = self.create_backup()

        # Auto-Cleanup alter Backups
        retention_days = self._get_retention_days()
        self.cleanup_old_backups(keep_days=retention_days, keep_per_host=3)

        return backup_path

    def create_backup(self) -> Path:
        """Erstellt konsistentes Backup mit Identitätsstempel.

        Format: bach_HOSTNAME_TIMESTAMP.bachdb
        Beispiel: bach_HOSTNAME_2026-02-14T14-30-00.bachdb

        Returns:
            Path zum erstellten Backup
        """
        if not self.db_path.exists():
            raise FileNotFoundError(f"DB nicht gefunden: {self.db_path}")

        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        filename = f"bach_{self.hostname}_{timestamp}.bachdb"
        backup_path = self.backup_dir / filename

        # SQLite BACKUP (crash-safe, konsistent)
        src = sqlite3.connect(str(self.db_path))
        dst = sqlite3.connect(str(backup_path))

        with dst:
            src.backup(dst)

        dst.close()
        src.close()

        # Secrets aus Backup entfernen (ENT-44: dist_type=0, nie im Backup)
        # Die Tabelle bleibt als Schema erhalten, nur die Zeilen werden geleert.
        try:
            bkp = sqlite3.connect(str(backup_path))
            bkp.execute("DELETE FROM secrets")
            bkp.commit()
            bkp.close()
        except Exception:
            pass  # Tabelle evtl. nicht vorhanden (aeltere DB-Versionen)

        # Heartbeat aktualisieren
        self._update_heartbeat()

        return backup_path

    # ==================== SYNC ====================

    def find_newer_backups(self) -> List[Path]:
        """Findet fremde Backups die neuer sind als lokale DB.

        Returns:
            Liste von Backup-Pfaden, sortiert nach Änderungszeit (neueste zuerst)
        """
        if not self.db_path.exists():
            # DB existiert noch nicht - alle Backups sind "neuer"
            local_mtime = 0
        else:
            local_mtime = self.db_path.stat().st_mtime

        backups = []
        for backup in self.backup_dir.glob("bach_*.bachdb"):
            # Überspringe eigene Backups
            if self.hostname in backup.name:
                continue

            if backup.stat().st_mtime > local_mtime:
                backups.append(backup)

        return sorted(backups, key=lambda p: p.stat().st_mtime, reverse=True)

    def merge_backup(self, backup_path: Path) -> Dict[str, int]:
        """Merged Remote-Backup in lokale DB mit Timestamp-basierter Strategie.

        Strategie:
        - Tabellen mit timestamp-Spalte: Neuere Zeilen gewinnen (Last-Write-Wins)
        - INSERT OR REPLACE für maximale Kompatibilität

        Args:
            backup_path: Pfad zum Remote-Backup

        Returns:
            Dict mit Statistiken: {table_name: merged_count}
        """
        print(f"[DB SYNC] Merge Backup: {backup_path.name}")

        if not self.db_path.exists():
            # Keine lokale DB - einfach kopieren
            import shutil
            shutil.copy2(backup_path, self.db_path)
            print(f"[DB SYNC] Initiale DB erstellt aus {backup_path.name}")
            return {"_initial_copy": 1}

        local = sqlite3.connect(str(self.db_path))
        local.row_factory = sqlite3.Row
        remote = sqlite3.connect(str(backup_path))
        remote.row_factory = sqlite3.Row

        # Tabellen mit Timestamp-Spalten (für intelligenten Merge)
        timestamped_tables = {
            'ati_tasks': 'updated_at',
            'connector_messages': 'created_at',
            'memory_facts': 'created_at',
            'memory_context': 'created_at',
            'tasks': 'updated_at',
            'steuer_dokumente': 'created_at',
            'agent_synergies': 'updated_at',
            'bach_agents': 'updated_at',
            'assistant_calendar': 'updated_at',
        }

        stats = {}

        for table, ts_col in timestamped_tables.items():
            try:
                # Prüfe ob Tabelle existiert
                table_exists = local.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                    (table,)
                ).fetchone()

                if not table_exists:
                    continue

                # Hole Spalten-Info
                columns = [row[1] for row in local.execute(
                    f"PRAGMA table_info({table})"
                ).fetchall()]

                if ts_col not in columns:
                    continue

                # Hole neuere Rows vom Remote
                max_ts_query = f"""
                    SELECT COALESCE(MAX({ts_col}), '1970-01-01')
                    FROM {table}
                """
                max_local_ts = local.execute(max_ts_query).fetchone()[0]

                newer_rows = remote.execute(f"""
                    SELECT * FROM {table}
                    WHERE {ts_col} > ?
                """, (max_local_ts,)).fetchall()

                if newer_rows:
                    # INSERT OR REPLACE
                    placeholders = ','.join(['?'] * len(columns))
                    insert_query = f"INSERT OR REPLACE INTO {table} VALUES ({placeholders})"

                    for row in newer_rows:
                        local.execute(insert_query, tuple(row))

                    stats[table] = len(newer_rows)
                    print(f"  {table}: {len(newer_rows)} Zeilen")

            except sqlite3.Error as e:
                print(f"  FEHLER {table}: {e}")
                stats[f"{table}_error"] = str(e)

        local.commit()
        local.close()
        remote.close()

        return stats

    def sync(self, auto_confirm: bool = False) -> Tuple[bool, str]:
        """Führt vollständigen Sync durch: Pull + Merge + Push.

        Args:
            auto_confirm: Wenn False, fragt bei Konflikten nach

        Returns:
            (success, message)
        """
        # 1. Konflikt-Check
        conflicts = self.check_conflicts()
        if conflicts and not auto_confirm:
            conflict_msg = '\n'.join([f"  - {c}" for c in conflicts])
            print(f"⚠️ Andere PCs aktiv:\n{conflict_msg}")

            try:
                response = input("Fortfahren? (y/n) ").strip().lower()
                if response != 'y':
                    return False, "Sync abgebrochen (andere PCs aktiv)"
            except (EOFError, KeyboardInterrupt):
                return False, "Sync abgebrochen"

        # 2. Pull & Merge
        newer = self.find_newer_backups()
        if newer:
            latest = newer[0]
            print(f"[DB SYNC] Neueres Backup gefunden: {latest.name}")
            stats = self.merge_backup(latest)
            total = sum(v for v in stats.values() if isinstance(v, int))
            print(f"[DB SYNC] Merged: {total} Zeilen")
        else:
            print("[DB SYNC] Keine neueren Backups")

        # 3. Push (eigenes Backup)
        backup_path = self.create_backup()
        print(f"[DB SYNC] Backup erstellt: {backup_path.name}")

        return True, "Sync erfolgreich"

    # ==================== HEARTBEAT ====================

    def _update_heartbeat(self):
        """Aktualisiert Heartbeat (andere PCs sehen Aktivität)."""
        # Bestehende Heartbeats laden
        if self.heartbeat_file.exists():
            try:
                heartbeats = json.loads(self.heartbeat_file.read_text(encoding='utf-8'))
            except (json.JSONDecodeError, OSError):
                heartbeats = {}
        else:
            heartbeats = {}

        # Eigenen Heartbeat setzen
        heartbeats[self.hostname] = {
            "last_seen": datetime.now().isoformat(),
            "pid": os.getpid(),
            "active": True
        }

        self.heartbeat_file.write_text(
            json.dumps(heartbeats, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )

    def check_conflicts(self) -> List[str]:
        """Prüft ob andere PCs aktiv sind (innerhalb 5 Min).

        Returns:
            Liste von aktiven Hosts mit Zeitstempel
        """
        if not self.heartbeat_file.exists():
            return []

        try:
            heartbeats = json.loads(self.heartbeat_file.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, OSError):
            return []

        conflicts = []
        now = datetime.now()

        for host, info in heartbeats.items():
            if host == self.hostname:
                continue

            try:
                last_seen = datetime.fromisoformat(info['last_seen'])
                age_seconds = (now - last_seen).total_seconds()

                # 5 Min = aktiv
                if age_seconds < 300:
                    conflicts.append(f"{host} (vor {int(age_seconds)}s)")
            except (ValueError, KeyError):
                continue

        return conflicts

    # ==================== CLEANUP ====================

    def cleanup_old_backups(self, keep_days: int = 7, keep_per_host: int = 10) -> int:
        """Löscht alte Backups, behält neueste pro Host.

        Args:
            keep_days: Behalte alle Backups jünger als X Tage
            keep_per_host: Behalte neueste X Backups pro Host

        Returns:
            Anzahl gelöschter Backups
        """
        cutoff = datetime.now() - timedelta(days=keep_days)

        # Gruppiere nach Hostname
        by_host = {}
        for backup in self.backup_dir.glob("bach_*.bachdb"):
            parts = backup.stem.split('_')
            if len(parts) < 3:
                continue
            host = parts[1]
            by_host.setdefault(host, []).append(backup)

        deleted = 0
        for host, backups in by_host.items():
            # Sortiere nach Änderungszeit (neueste zuerst)
            backups.sort(key=lambda p: p.stat().st_mtime, reverse=True)

            for i, backup in enumerate(backups):
                mtime = datetime.fromtimestamp(backup.stat().st_mtime)

                # Behalte neueste X ODER jünger als Y Tage
                if i < keep_per_host or mtime > cutoff:
                    continue

                try:
                    backup.unlink()
                    deleted += 1
                except OSError:
                    pass

        return deleted

    # ==================== STATUS ====================

    def get_status(self) -> str:
        """Gibt formatierten Status-String zurück."""
        backups = sorted(
            self.backup_dir.glob("bach_*.bachdb"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )

        lines = ["[DB SYNC] Status:", ""]
        lines.append(f"Lokale DB: {self.db_path}")
        lines.append(f"Backup-Ordner: {self.backup_dir}")
        lines.append("")
        lines.append("Letzte Backups:")

        for backup in backups[:10]:
            mtime = datetime.fromtimestamp(backup.stat().st_mtime)
            age = datetime.now() - mtime
            parts = backup.stem.split('_')
            host = parts[1] if len(parts) > 1 else "?"

            marker = "🟢" if host == self.hostname else "⚪"
            size_mb = backup.stat().st_size / (1024 * 1024)

            lines.append(
                f"  {marker} {host}: {mtime.strftime('%Y-%m-%d %H:%M')} "
                f"(vor {int(age.total_seconds()/60)}m, {size_mb:.1f} MB)"
            )

        # Heartbeat-Info
        if self.heartbeat_file.exists():
            try:
                heartbeats = json.loads(self.heartbeat_file.read_text(encoding='utf-8'))
                lines.append("")
                lines.append("Aktive PCs:")
                for host, info in heartbeats.items():
                    last_seen = datetime.fromisoformat(info['last_seen'])
                    age = datetime.now() - last_seen
                    status = "🟢 AKTIV" if age.total_seconds() < 300 else "⚪ inaktiv"
                    lines.append(f"  {status} {host}: {last_seen.strftime('%H:%M')}")
            except (json.JSONDecodeError, OSError):
                pass

        return '\n'.join(lines)


class DBSyncHandler(BaseHandler):
    """CLI-Handler für DB-Sync-Befehle."""

    @property
    def profile_name(self) -> str:
        return "dbsync"

    @property
    def target_file(self) -> Path:
        return self.base_path / "hub" / "db_sync.py"

    def get_operations(self) -> dict:
        return {
            "backup": "Manuelles Backup erstellen",
            "sync": "Pull + Merge + Push",
            "status": "Status und Backups anzeigen",
            "cleanup": "Alte Backups löschen",
            "enable": "Auto-Sync aktivieren (bei Startup/Exit)",
            "disable": "Auto-Sync deaktivieren",
        }

    def handle(self, operation: str, args: List[str], dry_run: bool = False) -> Tuple[bool, str]:
        manager = DBSyncManager()

        if operation == "backup":
            try:
                path = manager.create_backup()
                return True, f"Backup erstellt: {path.name}"
            except Exception as e:
                return False, f"Backup fehlgeschlagen: {e}"

        elif operation == "sync":
            auto_confirm = "--auto" in args or "-y" in args
            try:
                success, msg = manager.sync(auto_confirm=auto_confirm)
                return success, msg
            except Exception as e:
                return False, f"Sync fehlgeschlagen: {e}"

        elif operation == "status":
            return True, manager.get_status()

        elif operation == "cleanup":
            try:
                deleted = manager.cleanup_old_backups()
                return True, f"Cleanup abgeschlossen: {deleted} Backups gelöscht"
            except Exception as e:
                return False, f"Cleanup fehlgeschlagen: {e}"

        elif operation == "enable":
            config_file = self.base_path / "config" / "db_sync_enabled"
            config_file.parent.mkdir(parents=True, exist_ok=True)
            config_file.write_text("enabled", encoding="utf-8")
            return True, "✅ Auto-Sync aktiviert (wirkt bei nächstem Start)"

        elif operation == "disable":
            config_file = self.base_path / "config" / "db_sync_enabled"
            if config_file.exists():
                config_file.unlink()
            return True, "❌ Auto-Sync deaktiviert"

        else:
            return False, f"Unbekannte Operation: {operation}"
