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
BACH Text-Viewer - GUI für Wissensdatenbank (SQ068 Phase 1)
===========================================================

Features:
- Dateiliste aus document_index (Suchindex-basiert)
- Text/Markdown Editor
- Volltextsuche
- Save-Funktion

Referenz: BACH_Dev/docs/SQ067_SQ068_VIEWER_IMPLEMENTATION.md
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sqlite3
import re
from pathlib import Path
from datetime import datetime


class BACHTextViewer:
    """GUI-Tool zum Browsen und Editieren von Wissensdatenbank-Dateien."""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn = None
        self.current_file = None
        self.current_content = ""

        # Hauptfenster
        self.root = tk.Tk()
        self.root.title("BACH Text-Viewer")
        self.root.geometry("1200x800")

        # DB-Verbindung herstellen
        self._connect_db()

        # UI erstellen
        self._create_ui()

        # Initiale Dateiliste laden
        self._load_file_list()

    def _connect_db(self):
        """Verbindung zur Datenbank herstellen."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        except Exception as e:
            messagebox.showerror("Fehler", f"Kann bach.db nicht öffnen:\n{e}")
            raise

    def _create_ui(self):
        """Erstellt die Benutzeroberfläche."""
        # Hauptframe mit Paned Window (2 Spalten)
        self.paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True)

        # Linke Spalte: Dateiliste + Suche
        left_frame = ttk.Frame(self.paned, width=300)
        self.paned.add(left_frame)

        # Suchfeld
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(search_frame, text="Suche:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_entry.bind('<Return>', lambda e: self._search_files())
        ttk.Button(search_frame, text="🔍", command=self._search_files, width=3).pack(side=tk.LEFT)

        # Dateiliste
        ttk.Label(left_frame, text="Dateien:").pack(padx=5, pady=(5, 0))
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Scrollbar + Listbox
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_list = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        self.file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.file_list.yview)
        self.file_list.bind('<<ListboxSelect>>', self._on_file_select)

        # Status
        self.status_label = ttk.Label(left_frame, text="0 Dateien", relief=tk.SUNKEN)
        self.status_label.pack(fill=tk.X, padx=5, pady=5)

        # Rechte Spalte: Editor
        right_frame = ttk.Frame(self.paned)
        self.paned.add(right_frame)

        # Toolbar
        toolbar = ttk.Frame(right_frame)
        toolbar.pack(fill=tk.X, padx=5, pady=5)

        self.file_label = ttk.Label(toolbar, text="Keine Datei geöffnet", font=("Arial", 10, "bold"))
        self.file_label.pack(side=tk.LEFT, padx=5)

        ttk.Button(toolbar, text="💾 Speichern", command=self._save_file).pack(side=tk.RIGHT, padx=2)
        ttk.Button(toolbar, text="↻ Neu laden", command=self._reload_file).pack(side=tk.RIGHT, padx=2)
        ttk.Button(toolbar, text="👁 Preview", command=self._update_preview).pack(side=tk.RIGHT, padx=2)

        # Notebook mit zwei Tabs: Editor und Preview (SQ068 Phase 2b)
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Tab 1: Editor
        editor_frame = ttk.Frame(self.notebook)
        self.notebook.add(editor_frame, text="📝 Editor")

        self.editor = scrolledtext.ScrolledText(editor_frame, wrap=tk.WORD, font=("Consolas", 10))
        self.editor.pack(fill=tk.BOTH, expand=True)

        # Syntax-Highlighting Tags konfigurieren (SQ068 Phase 2)
        self._setup_syntax_tags()

        # Tab 2: Preview
        preview_frame = ttk.Frame(self.notebook)
        self.notebook.add(preview_frame, text="👁 Preview")

        self.preview = scrolledtext.ScrolledText(preview_frame, wrap=tk.WORD, font=("Arial", 11), state=tk.DISABLED)
        self.preview.pack(fill=tk.BOTH, expand=True)

        # Preview-Tags konfigurieren (für Markdown-Rendering)
        self._setup_preview_tags()

        # Statusleiste
        self.editor_status = ttk.Label(right_frame, text="Bereit", relief=tk.SUNKEN)
        self.editor_status.pack(fill=tk.X, padx=5, pady=5)

    def _load_file_list(self, search_query=None):
        """Lädt Dateiliste aus document_index."""
        try:
            cursor = self.conn.cursor()

            if search_query:
                # Volltextsuche
                cursor.execute("""
                    SELECT id, file_path, file_name, word_count, modified_at
                    FROM document_index
                    WHERE content_text LIKE ? OR file_name LIKE ?
                    ORDER BY modified_at DESC
                    LIMIT 500
                """, (f'%{search_query}%', f'%{search_query}%'))
            else:
                # Alle Dateien (.md, .txt)
                cursor.execute("""
                    SELECT id, file_path, file_name, word_count, modified_at
                    FROM document_index
                    WHERE file_ext IN ('.md', '.txt', '.markdown')
                    ORDER BY modified_at DESC
                    LIMIT 500
                """)

            rows = cursor.fetchall()

            # Listbox leeren
            self.file_list.delete(0, tk.END)

            # Datei-Mapping speichern
            self.file_data = {}

            for row in rows:
                display_name = f"{row['file_name']} ({row['word_count']} Wörter)"
                self.file_list.insert(tk.END, display_name)
                self.file_data[self.file_list.size() - 1] = {
                    'id': row['id'],
                    'path': row['file_path'],
                    'name': row['file_name']
                }

            self.status_label.config(text=f"{len(rows)} Dateien")

        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden der Dateiliste:\n{e}")

    def _search_files(self):
        """Führt Volltextsuche aus."""
        query = self.search_var.get().strip()
        if query:
            self._load_file_list(search_query=query)
        else:
            self._load_file_list()

    def _on_file_select(self, event):
        """Wird aufgerufen, wenn eine Datei in der Liste ausgewählt wird."""
        selection = self.file_list.curselection()
        if not selection:
            return

        idx = selection[0]
        file_info = self.file_data.get(idx)
        if not file_info:
            return

        self._load_file_content(file_info)

    def _load_file_content(self, file_info):
        """Lädt Dateiinhalt aus DB oder Dateisystem."""
        try:
            # Zuerst aus document_index versuchen
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT content_text, file_path
                FROM document_index
                WHERE id = ?
            """, (file_info['id'],))

            row = cursor.fetchone()
            if row and row['content_text']:
                content = row['content_text']
            else:
                # Fallback: Aus Dateisystem lesen
                file_path = Path(row['file_path']) if row else None
                if file_path and file_path.exists():
                    content = file_path.read_text(encoding='utf-8')
                else:
                    messagebox.showwarning("Warnung", f"Datei nicht gefunden:\n{file_info['path']}")
                    return

            # Editor aktualisieren
            self.editor.delete(1.0, tk.END)
            self.editor.insert(1.0, content)

            # Syntax-Highlighting anwenden (SQ068 Phase 2)
            self._apply_syntax_highlighting()

            # Status aktualisieren
            self.current_file = file_info
            self.current_content = content
            self.file_label.config(text=file_info['name'])
            self.editor_status.config(text=f"Geladen: {file_info['path']}")

        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden der Datei:\n{e}")

    def _reload_file(self):
        """Lädt aktuelle Datei neu."""
        if self.current_file:
            self._load_file_content(self.current_file)
        else:
            messagebox.showinfo("Info", "Keine Datei geöffnet")

    def _save_file(self):
        """Speichert Änderungen."""
        if not self.current_file:
            messagebox.showinfo("Info", "Keine Datei geöffnet")
            return

        try:
            new_content = self.editor.get(1.0, tk.END).rstrip()

            # Datei schreiben
            file_path = Path(self.current_file['path'])
            if not file_path.exists():
                # Warnung: Datei existiert nicht im Dateisystem
                if not messagebox.askyesno("Warnung",
                    f"Datei existiert nicht:\n{file_path}\n\nTrotzdem erstellen?"):
                    return

            file_path.write_text(new_content, encoding='utf-8')

            # document_index aktualisieren
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE document_index
                SET content_text = ?,
                    modified_at = ?,
                    word_count = ?
                WHERE id = ?
            """, (new_content, datetime.now().isoformat(), len(new_content.split()), self.current_file['id']))

            self.conn.commit()

            # Status
            self.current_content = new_content
            self.editor_status.config(text=f"Gespeichert: {datetime.now().strftime('%H:%M:%S')}")
            messagebox.showinfo("Erfolg", "Datei gespeichert")

        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern:\n{e}")

    def _setup_syntax_tags(self):
        """
        Konfiguriert Syntax-Highlighting Tags für Markdown (SQ068 Phase 2).

        Verwendet tkinter Text Tags für einfaches Highlighting ohne externe Dependencies.
        """
        # Headers (# ## ###)
        self.editor.tag_config("header1", foreground="#0066CC", font=("Consolas", 14, "bold"))
        self.editor.tag_config("header2", foreground="#0066CC", font=("Consolas", 12, "bold"))
        self.editor.tag_config("header3", foreground="#0066CC", font=("Consolas", 11, "bold"))

        # Formatting
        self.editor.tag_config("bold", font=("Consolas", 10, "bold"))
        self.editor.tag_config("italic", font=("Consolas", 10, "italic"))
        self.editor.tag_config("code", background="#F0F0F0", foreground="#CC0000", font=("Courier", 9))
        self.editor.tag_config("codeblock", background="#F0F0F0", foreground="#000088", font=("Courier", 9))

        # Links & Lists
        self.editor.tag_config("link", foreground="#0000EE", underline=True)
        self.editor.tag_config("list", foreground="#008800")

        # Quotes
        self.editor.tag_config("quote", foreground="#666666", font=("Consolas", 10, "italic"))

    def _apply_syntax_highlighting(self):
        """
        Wendet Syntax-Highlighting auf den aktuellen Editor-Inhalt an (SQ068 Phase 2).

        Nutzt regex-basiertes Highlighting für Markdown-Elemente.
        """
        # Alle Tags entfernen
        for tag in ["header1", "header2", "header3", "bold", "italic", "code", "codeblock", "link", "list", "quote"]:
            self.editor.tag_remove(tag, "1.0", tk.END)

        content = self.editor.get("1.0", tk.END)
        lines = content.split("\n")

        in_codeblock = False
        for i, line in enumerate(lines, 1):
            line_start = f"{i}.0"
            line_end = f"{i}.end"

            # Codeblocks (```)
            if line.strip().startswith("```"):
                in_codeblock = not in_codeblock
                self.editor.tag_add("codeblock", line_start, line_end)
                continue

            if in_codeblock:
                self.editor.tag_add("codeblock", line_start, line_end)
                continue

            # Headers
            if line.startswith("# "):
                self.editor.tag_add("header1", line_start, line_end)
            elif line.startswith("## "):
                self.editor.tag_add("header2", line_start, line_end)
            elif line.startswith("### "):
                self.editor.tag_add("header3", line_start, line_end)

            # Quotes
            if line.startswith("> "):
                self.editor.tag_add("quote", line_start, line_end)

            # Lists
            if re.match(r"^[\s]*[-*+]\s", line) or re.match(r"^[\s]*\d+\.\s", line):
                self.editor.tag_add("list", line_start, line_end)

            # Inline code (`code`)
            for match in re.finditer(r"`([^`]+)`", line):
                start_idx = f"{i}.{match.start()}"
                end_idx = f"{i}.{match.end()}"
                self.editor.tag_add("code", start_idx, end_idx)

            # Bold (**text**)
            for match in re.finditer(r"\*\*([^*]+)\*\*", line):
                start_idx = f"{i}.{match.start()}"
                end_idx = f"{i}.{match.end()}"
                self.editor.tag_add("bold", start_idx, end_idx)

            # Italic (*text* or _text_)
            for match in re.finditer(r"(?<!\*)\*([^*]+)\*(?!\*)", line):
                start_idx = f"{i}.{match.start()}"
                end_idx = f"{i}.{match.end()}"
                self.editor.tag_add("italic", start_idx, end_idx)

            # Links ([text](url))
            for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", line):
                start_idx = f"{i}.{match.start()}"
                end_idx = f"{i}.{match.end()}"
                self.editor.tag_add("link", start_idx, end_idx)

    def _setup_preview_tags(self):
        """
        Konfiguriert Tags für Markdown-Preview (SQ068 Phase 2b).

        Preview-Rendering verwendet größere Fonts und bessere Lesbarkeit.
        """
        # Headers
        self.preview.tag_config("h1", foreground="#003366", font=("Arial", 18, "bold"), spacing1=10, spacing3=5)
        self.preview.tag_config("h2", foreground="#003366", font=("Arial", 15, "bold"), spacing1=8, spacing3=4)
        self.preview.tag_config("h3", foreground="#003366", font=("Arial", 13, "bold"), spacing1=6, spacing3=3)

        # Formatting
        self.preview.tag_config("bold", font=("Arial", 11, "bold"))
        self.preview.tag_config("italic", font=("Arial", 11, "italic"))
        self.preview.tag_config("code", background="#F5F5F5", foreground="#CC0000", font=("Courier New", 10))
        self.preview.tag_config("codeblock", background="#F5F5F5", foreground="#000088", font=("Courier New", 10), lmargin1=20, lmargin2=20)

        # Lists
        self.preview.tag_config("list", lmargin1=20, lmargin2=40)

        # Quotes
        self.preview.tag_config("quote", foreground="#555555", font=("Arial", 11, "italic"), lmargin1=30, lmargin2=30)

    def _update_preview(self):
        """
        Aktualisiert Preview-Tab mit gerenderten Markdown (SQ068 Phase 2b).

        Einfaches Markdown-Rendering ohne externe Dependencies.
        """
        content = self.editor.get("1.0", tk.END)

        # Preview leeren
        self.preview.config(state=tk.NORMAL)
        self.preview.delete("1.0", tk.END)

        lines = content.split("\n")
        in_codeblock = False

        for line in lines:
            # Codeblocks
            if line.strip().startswith("```"):
                in_codeblock = not in_codeblock
                continue

            if in_codeblock:
                self.preview.insert(tk.END, line + "\n", "codeblock")
                continue

            # Headers
            if line.startswith("### "):
                self.preview.insert(tk.END, line[4:] + "\n", "h3")
            elif line.startswith("## "):
                self.preview.insert(tk.END, line[3:] + "\n", "h2")
            elif line.startswith("# "):
                self.preview.insert(tk.END, line[2:] + "\n", "h1")
            # Lists
            elif line.strip().startswith(("- ", "* ", "1. ", "2. ", "3. ")):
                self.preview.insert(tk.END, line + "\n", "list")
            # Quotes
            elif line.strip().startswith(">"):
                self.preview.insert(tk.END, line[1:].strip() + "\n", "quote")
            # Normal text
            else:
                # Inline formatting (bold, italic, code)
                self.preview.insert(tk.END, line + "\n")

        self.preview.config(state=tk.DISABLED)
        self.notebook.select(1)  # Switch zu Preview-Tab
        self.editor_status.config(text="Preview aktualisiert")

    def run(self):
        """Startet die GUI."""
        self.root.mainloop()

    def __del__(self):
        """Schließt DB-Verbindung beim Beenden."""
        if self.conn:
            self.conn.close()


def start_viewer():
    """Entry-Point für CLI."""
    # BACH-Pfad ermitteln
    script_dir = Path(__file__).parent
    db_path = script_dir.parent / "data" / "bach.db"

    if not db_path.exists():
        print(f"[ERROR] bach.db nicht gefunden: {db_path}")
        return 1

    viewer = BACHTextViewer(db_path)
    viewer.run()
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(start_viewer())


# TODO Phase 2:
# - Syntax-Highlighting für Markdown
# - Markdown-Preview (Live oder Tab)
# - Bessere Suchindex-Integration (FTS nutzen)
# - Datei-Metadaten anzeigen (Kategorie, Tags, etc.)
# - Export-Funktion (PDF, HTML)
# - dist_type-aware (read-only für CORE-Dateien)
