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
Tool: document_indexer
Version: 1.0.0
Author: Claude
Created: 2026-02-04
Updated: 2026-02-04
Anthropic-Compatible: True

Description:
    Volltext-Indexierung und Suche fuer Dokumente.
    Nutzt SQLite FTS5 fuer schnelle Volltextsuche.

Usage:
    python document_indexer.py index <folder>        # Ordner indizieren
    python document_indexer.py search "suchbegriff"  # Volltextsuche
    python document_indexer.py status                # Index-Status
    python document_indexer.py rebuild               # Index neu aufbauen
"""

__version__ = "1.0.0"
__author__ = "Claude"

import sqlite3
import hashlib
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# BACH Root
BACH_ROOT = Path(__file__).parent.parent
DB_PATH = BACH_ROOT / "data" / "bach.db"

# Unterstuetzte Dateitypen
SUPPORTED_EXTENSIONS = {
    '.txt': 'text',
    '.md': 'text',
    '.py': 'code',
    '.js': 'code',
    '.json': 'data',
    '.csv': 'data',
    '.xml': 'data',
    '.html': 'text',
    '.htm': 'text',
    '.log': 'text',
    '.cfg': 'config',
    '.ini': 'config',
    '.yaml': 'config',
    '.yml': 'config',
}

# Kategorien nach Extension
FILE_CATEGORIES = {
    '.txt': 'dokument',
    '.md': 'dokument',
    '.pdf': 'dokument',
    '.docx': 'dokument',
    '.doc': 'dokument',
    '.odt': 'dokument',
    '.py': 'code',
    '.js': 'code',
    '.ts': 'code',
    '.java': 'code',
    '.cpp': 'code',
    '.c': 'code',
    '.h': 'code',
    '.json': 'daten',
    '.csv': 'daten',
    '.xml': 'daten',
    '.jpg': 'bild',
    '.jpeg': 'bild',
    '.png': 'bild',
    '.gif': 'bild',
    '.mp3': 'audio',
    '.wav': 'audio',
    '.mp4': 'video',
    '.avi': 'video',
    '.zip': 'archiv',
    '.tar': 'archiv',
    '.gz': 'archiv',
}


class DocumentIndexer:
    """Indiziert und durchsucht Dokumente mit FTS5."""

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path

    def _get_db(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _file_hash(self, file_path: Path) -> str:
        """Berechnet MD5-Hash einer Datei."""
        hasher = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return ""

    def _extract_text(self, file_path: Path) -> str:
        """Extrahiert Text aus einer Datei."""
        ext = file_path.suffix.lower()

        # Textdateien direkt lesen
        if ext in ['.txt', '.md', '.py', '.js', '.json', '.csv', '.xml',
                   '.html', '.htm', '.log', '.cfg', '.ini', '.yaml', '.yml']:
            try:
                return file_path.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                try:
                    return file_path.read_text(encoding='latin-1', errors='ignore')
                except Exception:
                    return ""

        # PDF: pypdf (MIT) primaer, pdfplumber als Fallback, PyMuPDF optional
        if ext == '.pdf':
            # Primaer: pypdf (MIT-Lizenz)
            try:
                from pypdf import PdfReader
                reader = PdfReader(str(file_path))
                text = ""
                for page in reader.pages:
                    text += (page.extract_text() or "")
                if text.strip():
                    return text
            except ImportError:
                pass
            except Exception:
                pass

            # Fallback: pdfplumber (MIT-Lizenz)
            try:
                import pdfplumber
                text = ""
                with pdfplumber.open(str(file_path)) as pdf:
                    for page in pdf.pages:
                        text += (page.extract_text() or "")
                if text.strip():
                    return text
            except ImportError:
                pass
            except Exception:
                pass

            # Optional: PyMuPDF (AGPL) -- nur wenn verfuegbar
            try:
                import fitz  # PyMuPDF optional
                doc = fitz.open(str(file_path))
                text = ""
                for page in doc:
                    text += page.get_text()
                doc.close()
                if text.strip():
                    return text
            except ImportError:
                pass
            except Exception as e:
                return f"[PDF Fehler: {e}]"

            return "[PDF - pypdf, pdfplumber und PyMuPDF nicht installiert]"

        # DOCX (falls python-docx verfuegbar)
        if ext == '.docx':
            try:
                from docx import Document
                doc = Document(str(file_path))
                return "\n".join(p.text for p in doc.paragraphs)
            except ImportError:
                return "[DOCX - python-docx nicht installiert]"
            except Exception as e:
                return f"[DOCX Fehler: {e}]"

        return ""

    def _get_category(self, file_path: Path) -> str:
        """Ermittelt Kategorie einer Datei."""
        ext = file_path.suffix.lower()
        return FILE_CATEGORIES.get(ext, 'sonstiges')

    def index_file(self, file_path: Path, force: bool = False) -> Tuple[bool, str]:
        """Indiziert eine einzelne Datei."""
        if not file_path.exists():
            return False, f"Datei nicht gefunden: {file_path}"

        conn = self._get_db()

        try:
            # Pruefen ob bereits indiziert
            file_hash = self._file_hash(file_path)
            existing = conn.execute(
                "SELECT id, file_hash FROM document_index WHERE file_path = ?",
                (str(file_path),)
            ).fetchone()

            if existing and not force:
                if existing['file_hash'] == file_hash:
                    return True, f"Bereits indiziert (unveraendert): {file_path.name}"

            # Text extrahieren
            content = self._extract_text(file_path)
            word_count = len(content.split()) if content else 0

            # Metadaten
            stat = file_path.stat()
            category = self._get_category(file_path)

            if existing:
                # Update
                conn.execute("""
                    UPDATE document_index SET
                        file_name = ?, file_ext = ?, file_size = ?, file_hash = ?,
                        file_category = ?, content_text = ?, word_count = ?,
                        indexed_at = datetime('now'), modified_at = ?
                    WHERE id = ?
                """, (
                    file_path.name,
                    file_path.suffix.lower(),
                    stat.st_size,
                    file_hash,
                    category,
                    content[:100000] if content else None,  # Max 100k chars
                    word_count,
                    datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    existing['id']
                ))
                action = "aktualisiert"
            else:
                # Insert
                conn.execute("""
                    INSERT INTO document_index
                    (file_path, file_name, file_ext, file_size, file_hash,
                     file_category, content_text, word_count, modified_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(file_path),
                    file_path.name,
                    file_path.suffix.lower(),
                    stat.st_size,
                    file_hash,
                    category,
                    content[:100000] if content else None,
                    word_count,
                    datetime.fromtimestamp(stat.st_mtime).isoformat()
                ))
                action = "indiziert"

            conn.commit()
            return True, f"[OK] {action}: {file_path.name} ({word_count} Woerter)"

        except Exception as e:
            return False, f"[ERROR] {file_path.name}: {e}"
        finally:
            conn.close()

    def index_folder(self, folder_path: Path, recursive: bool = True,
                    extensions: List[str] = None) -> Tuple[bool, str]:
        """Indiziert alle Dateien in einem Ordner."""
        if not folder_path.exists():
            return False, f"Ordner nicht gefunden: {folder_path}"

        if extensions is None:
            extensions = list(SUPPORTED_EXTENSIONS.keys()) + ['.pdf', '.docx']

        pattern = "**/*" if recursive else "*"
        files = []
        for ext in extensions:
            files.extend(folder_path.glob(f"{pattern}{ext}"))

        if not files:
            return True, f"Keine passenden Dateien in {folder_path}"

        results = []
        indexed = 0
        errors = 0

        for f in files:
            if f.is_file() and not any(part.startswith('.') for part in f.parts):
                success, msg = self.index_file(f)
                if success:
                    indexed += 1
                else:
                    errors += 1
                    results.append(msg)

        output = [
            f"\n[INDEX] Ordner indiziert: {folder_path}",
            f"  Dateien gefunden: {len(files)}",
            f"  Erfolgreich: {indexed}",
            f"  Fehler: {errors}",
        ]

        if errors > 0 and results:
            output.append("\nFehler:")
            output.extend(results[:5])

        return True, "\n".join(output)

    def search(self, query: str, limit: int = 20) -> Tuple[bool, str]:
        """Durchsucht den Index mit FTS5."""
        conn = self._get_db()

        try:
            # FTS5 Suche mit Highlighting
            rows = conn.execute("""
                SELECT
                    di.id,
                    di.file_path,
                    di.file_name,
                    di.file_category,
                    di.word_count,
                    snippet(document_fts, 1, '>>>', '<<<', '...', 30) as snippet
                FROM document_fts
                JOIN document_index di ON document_fts.rowid = di.id
                WHERE document_fts MATCH ?
                ORDER BY rank
                LIMIT ?
            """, (query, limit)).fetchall()

            if not rows:
                return True, f"Keine Treffer fuer: {query}"

            output = [f"\n[SUCHE] '{query}' - {len(rows)} Treffer:\n"]

            for r in rows:
                path = Path(r['file_path'])
                rel_path = path.name
                try:
                    rel_path = path.relative_to(BACH_ROOT)
                except ValueError:
                    pass

                output.append(f"  [{r['id']}] {rel_path}")
                output.append(f"      Kategorie: {r['file_category']}, {r['word_count']} Woerter")
                if r['snippet']:
                    snippet = r['snippet'].replace('\n', ' ')[:100]
                    output.append(f"      ...{snippet}...")
                output.append("")

            return True, "\n".join(output)

        except Exception as e:
            return False, f"[ERROR] Suche fehlgeschlagen: {e}"
        finally:
            conn.close()

    def status(self) -> Tuple[bool, str]:
        """Zeigt Index-Status."""
        conn = self._get_db()

        try:
            total = conn.execute("SELECT COUNT(*) FROM document_index").fetchone()[0]
            by_category = conn.execute("""
                SELECT file_category, COUNT(*) as cnt, SUM(word_count) as words
                FROM document_index
                GROUP BY file_category
                ORDER BY cnt DESC
            """).fetchall()

            total_words = conn.execute("SELECT SUM(word_count) FROM document_index").fetchone()[0] or 0

            output = [
                "\n=== DOCUMENT INDEX STATUS ===",
                f"Gesamt-Dokumente: {total}",
                f"Gesamt-Woerter:   {total_words:,}",
                "",
                "Nach Kategorie:",
            ]

            for r in by_category:
                words = r['words'] or 0
                output.append(f"  {r['file_category']:<15} {r['cnt']:>5} Dateien, {words:>8,} Woerter")

            output.extend([
                "",
                "Befehle:",
                "  index <folder>   Ordner indizieren",
                "  search <query>   Volltextsuche",
                "  rebuild          Index neu aufbauen",
            ])

            return True, "\n".join(output)

        except Exception as e:
            return False, f"[ERROR] {e}"
        finally:
            conn.close()

    def rebuild(self) -> Tuple[bool, str]:
        """Baut den FTS-Index neu auf."""
        conn = self._get_db()

        try:
            # FTS-Index leeren und neu aufbauen
            conn.execute("INSERT INTO document_fts(document_fts) VALUES('rebuild')")
            conn.commit()
            return True, "[OK] FTS-Index neu aufgebaut"
        except Exception as e:
            return False, f"[ERROR] Rebuild fehlgeschlagen: {e}"
        finally:
            conn.close()

    def clear(self) -> Tuple[bool, str]:
        """Leert den gesamten Index."""
        conn = self._get_db()

        try:
            conn.execute("DELETE FROM document_index")
            conn.commit()
            return True, "[OK] Index geleert"
        except Exception as e:
            return False, f"[ERROR] {e}"
        finally:
            conn.close()


def main():
    parser = argparse.ArgumentParser(description="BACH Document Indexer")
    subparsers = parser.add_subparsers(dest="command", help="Verfuegbare Befehle")

    # index
    index_p = subparsers.add_parser("index", help="Ordner indizieren")
    index_p.add_argument("folder", help="Zu indizierender Ordner")
    index_p.add_argument("--no-recursive", "-n", action="store_true",
                        help="Nicht rekursiv")

    # search
    search_p = subparsers.add_parser("search", help="Volltextsuche")
    search_p.add_argument("query", help="Suchbegriff")
    search_p.add_argument("--limit", "-l", type=int, default=20,
                         help="Max. Ergebnisse")

    # status
    subparsers.add_parser("status", help="Index-Status anzeigen")

    # rebuild
    subparsers.add_parser("rebuild", help="FTS-Index neu aufbauen")

    # clear
    subparsers.add_parser("clear", help="Index leeren")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    indexer = DocumentIndexer()

    if args.command == "index":
        folder = Path(args.folder)
        if not folder.is_absolute():
            folder = Path.cwd() / folder
        success, msg = indexer.index_folder(folder, not args.no_recursive)
    elif args.command == "search":
        success, msg = indexer.search(args.query, args.limit)
    elif args.command == "status":
        success, msg = indexer.status()
    elif args.command == "rebuild":
        success, msg = indexer.rebuild()
    elif args.command == "clear":
        success, msg = indexer.clear()
    else:
        parser.print_help()
        return 1

    print(msg)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
