#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
Tool: nulcleaner
Version: 1.0.0
Author: BACH Team
Created: 2026-02-04
Updated: 2026-02-04
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version nulcleaner

Description:
    [Beschreibung hinzufügen]

Usage:
    python nulcleaner.py [args]
"""

__version__ = "1.0.0"
__author__ = "BACH Team"

import os
import argparse
import tkinter as tk
from tkinter import filedialog, messagebox

def find_nul_files(root):
    nul_files = []
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.lower() == "nul":
                full = os.path.join(dirpath, f)
                nul_files.append(full)
    return nul_files

def delete_nul_file(path):
    r"""
    Loescht NUL-Datei mit UNC-Pfad (Windows-spezifisch).

    Windows reserviert "NUL" als Device-Name, daher muss der
    erweiterte UNC-Pfad (\\?\) verwendet werden.
    """
    # Normalisiere Pfad ohne abspath (das wuerde NUL zu \\.\NUL machen)
    normalized = os.path.normpath(path)

    # UNC-Pfad fuer erweiterte Pfadlaenge und reservierte Namen
    if not normalized.startswith("\\\\?\\"):
        unc = "\\\\?\\" + normalized
    else:
        unc = normalized

    try:
        os.remove(unc)
        return True
    except Exception as e:
        return False, str(e)


def clean_nul_files_headless(root_path, verbose=False):
    """
    Entfernt NUL-Dateien automatisch (ohne GUI).

    Wird von startup.py und dist.py aufgerufen.

    Args:
        root_path: Basis-Verzeichnis zum Scannen
        verbose: Wenn True, gibt Details aus

    Returns:
        dict: {'found': int, 'deleted': int, 'errors': list}
    """
    result = {'found': 0, 'deleted': 0, 'errors': []}

    nul_files = find_nul_files(root_path)
    result['found'] = len(nul_files)

    if not nul_files:
        return result

    for f in nul_files:
        ok = delete_nul_file(f)
        if ok is True:
            result['deleted'] += 1
            if verbose:
                print(f"  [OK] Geloescht: {f}")
        else:
            result['errors'].append(f)
            if verbose:
                print(f"  [ERR] Fehler bei: {f}")

    return result

# ---------------- GUI ----------------

class NulCleanerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NUL Cleaner")

        self.path_var = tk.StringVar()

        tk.Label(root, text="Verzeichnis:").pack(anchor="w")
        tk.Entry(root, textvariable=self.path_var, width=50).pack(side="left", padx=5)
        tk.Button(root, text="Auswählen", command=self.select_dir).pack(side="left")

        tk.Button(root, text="Scan starten", command=self.scan).pack(pady=10)

        self.listbox = tk.Listbox(root, width=80, height=15)
        self.listbox.pack()

        tk.Button(root, text="Ausgewählte löschen", command=self.delete_selected).pack(pady=10)

    def select_dir(self):
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)

    def scan(self):
        path = self.path_var.get()
        if not os.path.isdir(path):
            messagebox.showerror("Fehler", "Ungültiges Verzeichnis")
            return

        self.listbox.delete(0, tk.END)
        files = find_nul_files(path)
        for f in files:
            self.listbox.insert(tk.END, f)

        messagebox.showinfo("Scan abgeschlossen", f"{len(files)} NUL-Dateien gefunden")

    def delete_selected(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Hinweis", "Keine Datei ausgewählt")
            return

        for idx in reversed(selected):
            path = self.listbox.get(idx)
            ok = delete_nul_file(path)
            if ok is True:
                self.listbox.delete(idx)
            else:
                messagebox.showerror("Fehler", f"Konnte {path} nicht löschen")

        messagebox.showinfo("Fertig", "Löschvorgang abgeschlossen")

# ---------------- CLI ----------------

def cli():
    parser = argparse.ArgumentParser(description="NUL Cleaner Tool")
    parser.add_argument("mode", choices=["scan", "delete", "gui"])
    parser.add_argument("path", nargs="?", default=None)

    args = parser.parse_args()

    if args.mode == "gui":
        root = tk.Tk()
        app = NulCleanerGUI(root)
        root.mainloop()
        return

    if not args.path:
        print("Pfad fehlt")
        return

    if args.mode == "scan":
        files = find_nul_files(args.path)
        print("\nGefundene NUL-Dateien:")
        for f in files:
            print(f)
        print(f"\n{len(files)} Dateien gefunden")

    elif args.mode == "delete":
        files = find_nul_files(args.path)
        for f in files:
            ok = delete_nul_file(f)
            if ok is True:
                print(f"Gelöscht: {f}")
            else:
                print(f"Fehler bei {f}: {ok[1]}")

if __name__ == "__main__":
    cli()