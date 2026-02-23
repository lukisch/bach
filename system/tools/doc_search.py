#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Tool: doc_search
Version: 1.0.0
Author: BACH Team
Created: 2026-02-04
Updated: 2026-02-04
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version doc_search

Description:
    [Beschreibung hinzufügen]

Usage:
    python doc_search.py [args]
"""

__version__ = "1.0.0"
__author__ = "BACH Team"

# -*- coding: utf-8 -*-
"""
Document Search - Dokumenten-Suche in registrierten Ordnern
=============================================================

Durchsucht gescannte Ordner nach Dokumenten anhand von:
  - Dateinamen-Pattern (Regex/Substring)
  - Dateityp (PDF, DOCX, etc.)
  - Ordner-Kontext (Versicherungen, Steuern, etc.)
  - OCR-Cache (falls vorhanden)

Nutzt: bach.db / folder_scan_files, user_data_folders, steuer_ocr_cache

Usage:
  python tools/doc_search.py "Steuernummer"
  python tools/doc_search.py "Versicherungsschein" --type pdf
  python tools/doc_search.py "Zeugnis" --folder Arbeitgeber
  python tools/doc_search.py --scan "C:/path/to/folder"
  python tools/doc_search.py --recent 7

Ref: docs/WICHTIG_SYSTEMISCH_FIRST.md
"""

import sqlite3
import os
import sys
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class DocumentSearcher:
    """Durchsucht registrierte Dokumente."""

    def __init__(self, user_db_path: str):
        self.user_db_path = user_db_path

    def _get_db(self):
        conn = sqlite3.connect(self.user_db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def search_by_name(self, query: str,
                       extensions: Optional[List[str]] = None,
                       folder_filter: Optional[str] = None,
                       limit: int = 50) -> List[Dict]:
        """
        Durchsucht Dateinamen in folder_scan_files.

        Args:
            query: Suchbegriff (Substring oder Regex)
            extensions: Dateitypen filtern (z.B. ['.pdf'])
            folder_filter: Nur bestimmte Ordner (Substring im Pfad)
            limit: Max Ergebnisse
        """
        conn = self._get_db()
        try:
            like = f"%{query}%"
            params = [like, like]
            sql = """
                SELECT folder_path, file_path, file_name, file_ext,
                       file_size, first_seen, last_modified, status
                FROM folder_scan_files
                WHERE status = 'active'
                AND (file_name LIKE ? OR file_path LIKE ?)
            """

            if extensions:
                placeholders = ", ".join("?" for _ in extensions)
                sql += f" AND file_ext IN ({placeholders})"
                params.extend(extensions)

            if folder_filter:
                sql += " AND folder_path LIKE ?"
                params.append(f"%{folder_filter}%")

            sql += f" ORDER BY file_name ASC LIMIT ?"
            params.append(limit)

            rows = conn.execute(sql, params).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def search_filesystem(self, query: str,
                          base_paths: Optional[List[str]] = None,
                          extensions: Optional[List[str]] = None,
                          limit: int = 50) -> List[Dict]:
        """
        Direkte Dateisystem-Suche (fuer nicht-gescannte Ordner).

        Args:
            query: Suchbegriff im Dateinamen
            base_paths: Ordner zum Durchsuchen
            extensions: Dateitypen
            limit: Max Ergebnisse
        """
        if not base_paths:
            # Aus user_data_folders laden
            conn = self._get_db()
            try:
                rows = conn.execute(
                    "SELECT folder_path FROM user_data_folders"
                ).fetchall()
                base_paths = [r["folder_path"] for r in rows]
            except Exception:
                base_paths = []
            finally:
                conn.close()

        results = []
        query_lower = query.lower()

        for base in base_paths:
            base_path = Path(base)
            if not base_path.exists():
                continue

            for fp in base_path.rglob("*"):
                if not fp.is_file():
                    continue
                if fp.name in ("desktop.ini", "Thumbs.db", ".DS_Store"):
                    continue

                if extensions and fp.suffix.lower() not in extensions:
                    continue

                if query_lower in fp.name.lower() or query_lower in str(fp).lower():
                    stat = fp.stat()
                    results.append({
                        "folder_path": str(fp.parent),
                        "file_path": str(fp),
                        "file_name": fp.name,
                        "file_ext": fp.suffix.lower(),
                        "file_size": stat.st_size,
                        "last_modified": datetime.fromtimestamp(
                            stat.st_mtime
                        ).strftime("%Y-%m-%d %H:%M"),
                    })

                    if len(results) >= limit:
                        break

            if len(results) >= limit:
                break

        return results

    def search_ocr_cache(self, query: str, limit: int = 20) -> List[Dict]:
        """Durchsucht OCR-Cache fuer Volltext-Suche in PDFs."""
        conn = self._get_db()
        try:
            like = f"%{query}%"
            rows = conn.execute("""
                SELECT file_path, ocr_text, created_at
                FROM steuer_ocr_cache
                WHERE ocr_text LIKE ?
                ORDER BY created_at DESC LIMIT ?
            """, (like, limit)).fetchall()
            return [dict(r) for r in rows]
        except Exception:
            return []
        finally:
            conn.close()

    def get_recent_documents(self, days: int = 7,
                             extensions: Optional[List[str]] = None) -> List[Dict]:
        """Zeigt kuerzlich hinzugefuegte/geaenderte Dokumente."""
        conn = self._get_db()
        try:
            cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

            sql = """
                SELECT folder_path, file_path, file_name, file_ext,
                       file_size, first_seen, last_modified
                FROM folder_scan_files
                WHERE status = 'active' AND first_seen >= ?
            """
            params = [cutoff]

            if extensions:
                placeholders = ", ".join("?" for _ in extensions)
                sql += f" AND file_ext IN ({placeholders})"
                params.extend(extensions)

            sql += " ORDER BY first_seen DESC LIMIT 50"

            rows = conn.execute(sql, params).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def get_registered_folders(self) -> List[Dict]:
        """Zeigt alle registrierten Scan-Ordner mit Statistiken."""
        conn = self._get_db()
        try:
            # Distinct folders from folder_scan_files
            rows = conn.execute("""
                SELECT folder_path,
                       COUNT(*) as file_count,
                       SUM(file_size) as total_size,
                       MIN(first_seen) as first_scan,
                       MAX(last_scan) as last_scan
                FROM folder_scan_files
                WHERE status = 'active'
                GROUP BY folder_path
                ORDER BY folder_path
            """).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()


def format_search_results(results: List[Dict], query: str) -> str:
    """Formatiert Suchergebnisse als lesbaren Report."""
    if not results:
        return f"[SEARCH] Keine Dokumente gefunden fuer '{query}'."

    lines = [f"[SEARCH] {len(results)} Dokumente fuer '{query}':\n"]

    current_folder = None
    for r in results:
        folder = r.get("folder_path", "")
        if folder != current_folder:
            current_folder = folder
            # Kurzen Ordnerpfad anzeigen
            short = folder.replace("C:/Users/User/OneDrive/", "~/")
            lines.append(f"  [{short}]")

        size_kb = (r.get("file_size", 0) or 0) / 1024
        modified = r.get("last_modified", "")
        if modified and len(modified) > 10:
            modified = modified[:10]

        lines.append(
            f"    {r['file_name']:<50} {size_kb:>8.1f} KB  {modified}"
        )

    return "\n".join(lines)


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")

    import argparse
    parser = argparse.ArgumentParser(description="BACH Document Search")
    parser.add_argument("query", nargs="?", help="Suchbegriff")
    parser.add_argument("--type", "-t", help="Dateityp (pdf, docx, etc.)")
    parser.add_argument("--folder", "-f", help="Ordner-Filter (Substring)")
    parser.add_argument("--recent", "-r", type=int,
                        help="Kuerzlich hinzugefuegte Dokumente (Tage)")
    parser.add_argument("--scan", help="Ordner direkt durchsuchen (nicht DB)")
    parser.add_argument("--ocr", action="store_true",
                        help="Auch OCR-Cache durchsuchen")
    parser.add_argument("--folders", action="store_true",
                        help="Registrierte Ordner anzeigen")
    parser.add_argument("--limit", type=int, default=50,
                        help="Max Ergebnisse")

    args = parser.parse_args()

    base_path = Path(__file__).parent.parent
    db_path = str(base_path / "data" / "bach.db")

    searcher = DocumentSearcher(db_path)

    if args.folders:
        folders = searcher.get_registered_folders()
        if not folders:
            print("[SEARCH] Keine registrierten Ordner.")
            print("  Tipp: Erst scannen mit: python tools/folder_diff_scanner.py <pfad>")
        else:
            print(f"[SEARCH] {len(folders)} registrierte Ordner:\n")
            for f in folders:
                size_mb = (f["total_size"] or 0) / (1024 * 1024)
                print(f"  {f['folder_path']}")
                print(f"    {f['file_count']} Dateien, {size_mb:.1f} MB, "
                      f"Letzter Scan: {f['last_scan'][:10] if f['last_scan'] else 'nie'}")

    elif args.recent:
        exts = [f".{args.type}"] if args.type else None
        results = searcher.get_recent_documents(args.recent, exts)
        if not results:
            print(f"[SEARCH] Keine neuen Dokumente in den letzten {args.recent} Tagen.")
        else:
            print(f"[SEARCH] {len(results)} neue Dokumente (letzte {args.recent} Tage):\n")
            for r in results:
                size_kb = (r["file_size"] or 0) / 1024
                print(f"  {r['file_name']:<50} {size_kb:>8.1f} KB  {r['first_seen'][:10]}")

    elif args.query:
        exts = [f".{args.type}"] if args.type else None

        if args.scan:
            # Direkte Filesystem-Suche
            results = searcher.search_filesystem(
                args.query,
                base_paths=[args.scan],
                extensions=exts,
                limit=args.limit,
            )
        else:
            # DB-Suche (gescannte Ordner)
            results = searcher.search_by_name(
                args.query,
                extensions=exts,
                folder_filter=args.folder,
                limit=args.limit,
            )

        print(format_search_results(results, args.query))

        # Optional: OCR-Cache
        if args.ocr:
            ocr_results = searcher.search_ocr_cache(args.query)
            if ocr_results:
                print(f"\n[OCR] {len(ocr_results)} Treffer im OCR-Cache:")
                for r in ocr_results:
                    path = r["file_path"]
                    # Zeige Kontext um den Treffer
                    text = r.get("ocr_text", "")
                    idx = text.lower().find(args.query.lower())
                    if idx >= 0:
                        start = max(0, idx - 40)
                        end = min(len(text), idx + len(args.query) + 40)
                        snippet = text[start:end].replace("\n", " ")
                        print(f"  {path}")
                        print(f"    ...{snippet}...")
    else:
        parser.print_help()
