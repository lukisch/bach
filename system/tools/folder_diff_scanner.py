#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Tool: folder_diff_scanner
Version: 1.0.0
Author: BACH Team
Created: 2026-02-04
Updated: 2026-02-04
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version folder_diff_scanner

Description:
    [Beschreibung hinzufügen]

Usage:
    python folder_diff_scanner.py [args]
"""

__version__ = "1.0.0"
__author__ = "BACH Team"

# -*- coding: utf-8 -*-
"""
Folder Diff Scanner - Verzeichnis-Ueberwachung mit Diff-Erkennung
=================================================================

Scannt registrierte User-Ordner, vergleicht mit letztem Scan,
identifiziert neue/geaenderte/geloeschte Dateien.

Basis-Service fuer alle automatisierten Import-Workflows:
  - Health Document Import
  - Versicherungs-Scan Import
  - Inbox Datei-Erkennung

Nutzt: bach.db / folder_scans, user_data_folders

Ref: docs/WICHTIG_SYSTEMISCH_FIRST.md
"""

import sqlite3
import hashlib
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class FolderDiffScanner:
    """Scannt User-Ordner und erkennt Aenderungen seit letztem Scan."""

    # Dateien die ignoriert werden sollen
    IGNORE_FILES = {
        "desktop.ini", "Thumbs.db", ".DS_Store",
        ".gitkeep", ".gitignore",
    }

    IGNORE_EXTENSIONS = {
        ".tmp", ".bak", ".swp", ".lock",
    }

    def __init__(self, user_db_path: str):
        self.user_db_path = user_db_path
        self._ensure_tables()

    def _get_db(self):
        conn = sqlite3.connect(self.user_db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_tables(self):
        """Erstellt folder_scans und folder_scan_files Tabellen."""
        conn = self._get_db()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS folder_scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                folder_path TEXT NOT NULL,
                scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                files_total INTEGER DEFAULT 0,
                files_new INTEGER DEFAULT 0,
                files_modified INTEGER DEFAULT 0,
                files_deleted INTEGER DEFAULT 0,
                triggered_by TEXT DEFAULT 'manual',
                dist_type INTEGER DEFAULT 0
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS folder_scan_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                folder_path TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_name TEXT NOT NULL,
                file_ext TEXT,
                file_size INTEGER,
                file_hash TEXT,
                last_modified TIMESTAMP,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_scan TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active',
                processed INTEGER DEFAULT 0,
                dist_type INTEGER DEFAULT 0,
                UNIQUE(folder_path, file_path)
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_fsf_folder ON folder_scan_files(folder_path)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_fsf_status ON folder_scan_files(status)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_fsf_processed ON folder_scan_files(processed)")
        conn.commit()
        conn.close()

    def _should_ignore(self, file_path: Path) -> bool:
        """Prueft ob Datei ignoriert werden soll."""
        if file_path.name in self.IGNORE_FILES:
            return True
        if file_path.suffix.lower() in self.IGNORE_EXTENSIONS:
            return True
        return False

    def _file_hash(self, file_path: Path, max_size: int = 500000) -> str:
        """Berechnet MD5-Hash einer Datei (max 500KB lesen)."""
        try:
            size = file_path.stat().st_size
            if size > max_size:
                # Fuer grosse Dateien: Nur Anfang + Ende hashen
                with open(file_path, "rb") as f:
                    head = f.read(8192)
                    f.seek(-8192, 2)
                    tail = f.read(8192)
                return hashlib.md5(head + tail + str(size).encode()).hexdigest()[:12]
            else:
                content = file_path.read_bytes()
                return hashlib.md5(content).hexdigest()[:12]
        except Exception:
            return "error"

    def scan_folder(self, folder_path: str, recursive: bool = True,
                    extensions: Optional[List[str]] = None,
                    triggered_by: str = "manual") -> Dict:
        """
        Scannt einen Ordner und vergleicht mit letztem bekannten Zustand.

        Args:
            folder_path: Absoluter Pfad zum Ordner
            recursive: Auch Unterordner scannen
            extensions: Nur bestimmte Dateitypen (z.B. ['.pdf', '.docx'])
            triggered_by: Wer hat den Scan ausgeloest

        Returns:
            Dict mit new_files, modified_files, deleted_files, unchanged_files
        """
        folder = Path(folder_path)
        if not folder.exists():
            return {"error": f"Ordner nicht gefunden: {folder_path}"}
        if not folder.is_dir():
            return {"error": f"Kein Ordner: {folder_path}"}

        conn = self._get_db()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            # Aktuelle Dateien im Ordner sammeln
            current_files = {}
            if recursive:
                file_iter = folder.rglob("*")
            else:
                file_iter = folder.glob("*")

            for fp in file_iter:
                if not fp.is_file():
                    continue
                if self._should_ignore(fp):
                    continue
                if extensions and fp.suffix.lower() not in extensions:
                    continue

                rel_path = str(fp.relative_to(folder))
                stat = fp.stat()

                current_files[rel_path] = {
                    "abs_path": str(fp),
                    "name": fp.name,
                    "ext": fp.suffix.lower(),
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    "hash": self._file_hash(fp),
                }

            # Bekannte Dateien aus DB laden
            known_files = {}
            rows = conn.execute(
                "SELECT * FROM folder_scan_files WHERE folder_path = ? AND status = 'active'",
                (folder_path,)
            ).fetchall()
            for r in rows:
                known_files[r["file_path"]] = dict(r)

            # Vergleich
            current_paths = set(current_files.keys())
            known_paths = set(known_files.keys())

            new_paths = current_paths - known_paths
            deleted_paths = known_paths - current_paths
            common_paths = current_paths & known_paths

            new_files = []
            modified_files = []
            unchanged_files = []
            deleted_files = []

            # Neue Dateien
            for path in sorted(new_paths):
                info = current_files[path]
                new_files.append({
                    "path": path,
                    "abs_path": info["abs_path"],
                    "name": info["name"],
                    "ext": info["ext"],
                    "size": info["size"],
                })
                # In DB eintragen
                conn.execute("""
                    INSERT OR REPLACE INTO folder_scan_files
                    (folder_path, file_path, file_name, file_ext, file_size, file_hash,
                     last_modified, first_seen, last_scan, status, processed)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'active', 0)
                """, (folder_path, path, info["name"], info["ext"],
                      info["size"], info["hash"], info["modified"], now, now))

            # Geaenderte Dateien
            for path in sorted(common_paths):
                current = current_files[path]
                known = known_files[path]

                if current["hash"] != known["file_hash"]:
                    modified_files.append({
                        "path": path,
                        "abs_path": current["abs_path"],
                        "name": current["name"],
                        "old_size": known["file_size"],
                        "new_size": current["size"],
                    })
                    # DB aktualisieren
                    conn.execute("""
                        UPDATE folder_scan_files
                        SET file_hash = ?, file_size = ?, last_modified = ?, last_scan = ?, processed = 0
                        WHERE folder_path = ? AND file_path = ?
                    """, (current["hash"], current["size"], current["modified"],
                          now, folder_path, path))
                else:
                    unchanged_files.append(path)
                    # Nur last_scan aktualisieren
                    conn.execute("""
                        UPDATE folder_scan_files SET last_scan = ?
                        WHERE folder_path = ? AND file_path = ?
                    """, (now, folder_path, path))

            # Geloeschte Dateien
            for path in sorted(deleted_paths):
                known = known_files[path]
                deleted_files.append({
                    "path": path,
                    "name": known["file_name"],
                })
                conn.execute("""
                    UPDATE folder_scan_files SET status = 'deleted', last_scan = ?
                    WHERE folder_path = ? AND file_path = ?
                """, (now, folder_path, path))

            # Scan-Run protokollieren
            conn.execute("""
                INSERT INTO folder_scans
                (folder_path, files_total, files_new, files_modified, files_deleted, triggered_by)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (folder_path, len(current_files), len(new_files),
                  len(modified_files), len(deleted_files), triggered_by))

            conn.commit()

            return {
                "folder": folder_path,
                "scan_date": now,
                "total": len(current_files),
                "new_files": new_files,
                "modified_files": modified_files,
                "deleted_files": deleted_files,
                "unchanged": len(unchanged_files),
            }
        finally:
            conn.close()

    def get_unprocessed(self, folder_path: str,
                        extensions: Optional[List[str]] = None) -> List[Dict]:
        """
        Gibt alle unverarbeiteten Dateien eines Ordners zurueck.

        Args:
            folder_path: Ordnerpfad
            extensions: Nur bestimmte Dateitypen

        Returns:
            Liste von Datei-Infos
        """
        conn = self._get_db()
        try:
            query = """
                SELECT * FROM folder_scan_files
                WHERE folder_path = ? AND status = 'active' AND processed = 0
            """
            params = [folder_path]

            if extensions:
                placeholders = ", ".join("?" * len(extensions))
                query += f" AND file_ext IN ({placeholders})"
                params.extend(extensions)

            query += " ORDER BY first_seen ASC"
            rows = conn.execute(query, params).fetchall()

            return [dict(r) for r in rows]
        finally:
            conn.close()

    def mark_processed(self, folder_path: str, file_paths: List[str]) -> int:
        """
        Markiert Dateien als verarbeitet.

        Args:
            folder_path: Ordnerpfad
            file_paths: Liste der relativen Dateipfade

        Returns:
            Anzahl markierter Dateien
        """
        conn = self._get_db()
        try:
            count = 0
            for fp in file_paths:
                result = conn.execute("""
                    UPDATE folder_scan_files SET processed = 1
                    WHERE folder_path = ? AND file_path = ?
                """, (folder_path, fp))
                count += result.rowcount
            conn.commit()
            return count
        finally:
            conn.close()

    def get_scan_history(self, folder_path: str, limit: int = 10) -> List[Dict]:
        """Gibt Scan-Historie fuer einen Ordner zurueck."""
        conn = self._get_db()
        try:
            rows = conn.execute("""
                SELECT * FROM folder_scans
                WHERE folder_path = ?
                ORDER BY scan_date DESC LIMIT ?
            """, (folder_path, limit)).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def get_folder_stats(self, folder_path: str) -> Dict:
        """Gibt Statistiken fuer einen Ordner zurueck."""
        conn = self._get_db()
        try:
            total = conn.execute(
                "SELECT COUNT(*) FROM folder_scan_files WHERE folder_path = ? AND status = 'active'",
                (folder_path,)
            ).fetchone()[0]
            processed = conn.execute(
                "SELECT COUNT(*) FROM folder_scan_files WHERE folder_path = ? AND status = 'active' AND processed = 1",
                (folder_path,)
            ).fetchone()[0]
            unprocessed = total - processed
            last_scan = conn.execute(
                "SELECT MAX(scan_date) FROM folder_scans WHERE folder_path = ?",
                (folder_path,)
            ).fetchone()[0]

            return {
                "folder": folder_path,
                "total_files": total,
                "processed": processed,
                "unprocessed": unprocessed,
                "last_scan": last_scan,
            }
        finally:
            conn.close()


def format_scan_report(result: Dict) -> str:
    """Formatiert Scan-Ergebnis als lesbaren Report."""
    if "error" in result:
        return f"[ERROR] {result['error']}"

    lines = [
        f"[FOLDER-SCAN] {result['folder']}",
        f"  Datum:       {result['scan_date']}",
        f"  Dateien:     {result['total']} gesamt",
        f"  Neu:         {len(result['new_files'])}",
        f"  Geaendert:   {len(result['modified_files'])}",
        f"  Geloescht:   {len(result['deleted_files'])}",
        f"  Unveraendert:{result['unchanged']}",
    ]

    if result["new_files"]:
        lines.append(f"\n  NEUE DATEIEN:")
        for f in result["new_files"][:20]:
            size_kb = f["size"] / 1024
            lines.append(f"    + {f['name']:<40} ({size_kb:.1f} KB)")
        if len(result["new_files"]) > 20:
            lines.append(f"    ... und {len(result['new_files']) - 20} weitere")

    if result["modified_files"]:
        lines.append(f"\n  GEAENDERTE DATEIEN:")
        for f in result["modified_files"][:10]:
            lines.append(f"    ~ {f['name']}")

    if result["deleted_files"]:
        lines.append(f"\n  GELOESCHTE DATEIEN:")
        for f in result["deleted_files"][:10]:
            lines.append(f"    - {f['name']}")

    return "\n".join(lines)


# CLI-Schnittstelle
if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    if len(sys.argv) < 2:
        print("Usage: python folder_diff_scanner.py <folder_path> [--ext .pdf .docx] [--stats] [--unprocessed]")
        sys.exit(1)

    folder = sys.argv[1]
    base_path = Path(__file__).parent.parent
    db_path = str(base_path / "data" / "bach.db")  # Unified DB seit v1.1.84

    scanner = FolderDiffScanner(db_path)

    if "--stats" in sys.argv:
        stats = scanner.get_folder_stats(folder)
        print(f"[STATS] {folder}")
        print(f"  Dateien:       {stats['total_files']}")
        print(f"  Verarbeitet:   {stats['processed']}")
        print(f"  Offen:         {stats['unprocessed']}")
        print(f"  Letzter Scan:  {stats['last_scan'] or 'nie'}")

    elif "--unprocessed" in sys.argv:
        exts = []
        if "--ext" in sys.argv:
            idx = sys.argv.index("--ext")
            for i in range(idx + 1, len(sys.argv)):
                if sys.argv[i].startswith("-"):
                    break
                exts.append(sys.argv[i])

        files = scanner.get_unprocessed(folder, exts or None)
        print(f"[UNPROCESSED] {folder}: {len(files)} Dateien")
        for f in files:
            print(f"  {f['file_name']:<40} ({f['file_ext']}) {f['first_seen'][:10]}")

    else:
        exts = []
        if "--ext" in sys.argv:
            idx = sys.argv.index("--ext")
            for i in range(idx + 1, len(sys.argv)):
                if sys.argv[i].startswith("-"):
                    break
                exts.append(sys.argv[i])

        result = scanner.scan_folder(folder, extensions=exts or None)
        print(format_scan_report(result))
