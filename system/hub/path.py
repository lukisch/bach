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
Path Handler - Zeigt wichtige BACH-Pfade an (v2.0)
==================================================

Nutzt bach_paths.py als Single Source of Truth.

Befehle:
  bach path              Alle wichtigen Pfade anzeigen
  bach path root         BACH Hauptverzeichnis
  bach path tools        Tools-Verzeichnis
  bach path templates    Templates-Verzeichnis
  bach path berichte     Berichte-Verzeichnis
  bach path <name>       Spezifischen Pfad anzeigen
  bach path list         Alle verfuegbaren Pfadnamen
  bach path set <name> <pfad>  Override setzen (in DB)
  bach path overrides    DB-Overrides anzeigen
"""
from pathlib import Path
from .base import BaseHandler

# Import bach_paths als Single Source of Truth
from .bach_paths import (
    get_path, list_paths, validate,
    set_path_override, load_path_overrides_from_db,
    _PATH_REGISTRY
)


class PathHandler(BaseHandler):
    """Handler fuer bach path - zeigt Systempfade an (v2.0).

    Nutzt bach_paths.py als zentrale Pfad-Quelle.
    """

    def __init__(self, base_path: Path):
        super().__init__(base_path)

    @property
    def profile_name(self) -> str:
        return "path"

    @property
    def target_file(self) -> Path:
        return self.base_path

    def get_operations(self) -> dict:
        return {
            "show": "Alle wichtigen Pfade anzeigen (Standard)",
            "list": "Alle verfuegbaren Pfadnamen auflisten",
            "set": "Pfad-Override setzen: bach path set <name> <pfad>",
            "overrides": "DB-Overrides anzeigen",
            "validate": "Alle Pfade validieren",
        }

    def handle(self, operation: str, args: list, dry_run: bool = False) -> tuple:
        # Hilfe
        if operation in ("help", "--help", "-h"):
            return self._show_help()

        # Alle Pfade auflisten (Namen)
        if operation == "list":
            return self._list_path_names()

        # Alle Pfade anzeigen
        if operation in ("all", "show", ""):
            return self._show_all_paths()

        # Override setzen: bach path set <name> <pfad>
        if operation == "set":
            if len(args) < 2:
                return False, "[FEHLER] Nutzung: bach path set <name> <pfad>"
            name, pfad = args[0], args[1]
            if dry_run:
                return True, f"[DRY-RUN] Wuerde setzen: {name} -> {pfad}"
            if set_path_override(name, pfad):
                return True, f"[OK] Override gesetzt: {name} -> {pfad}"
            return False, f"[FEHLER] Konnte Override nicht setzen"

        # DB-Overrides anzeigen
        if operation == "overrides":
            return self._show_overrides()

        # Validierung
        if operation == "validate":
            return self._validate_paths()

        # Spezifischer Pfad abfragen
        path_name = operation.lower()
        try:
            return self._show_path(path_name)
        except KeyError:
            available = ", ".join(sorted(_PATH_REGISTRY.keys())[:15]) + ", ..."
            return False, f"Unbekannter Pfad: '{operation}'\nVerfuegbar: {available}\n\nNutze 'bach path list' fuer alle Pfadnamen."

    def _show_help(self) -> tuple:
        available_paths = sorted(_PATH_REGISTRY.keys())
        path_list = "\n".join(f"  {name}" for name in available_paths[:20])
        if len(available_paths) > 20:
            path_list += f"\n  ... und {len(available_paths) - 20} weitere"

        help_text = f"""BACH PATH v2.0 - Systempfade anzeigen
=====================================

Nutzt bach_paths.py als Single Source of Truth.

Befehle:
  bach path              Alle wichtigen Pfade anzeigen
  bach path <name>       Spezifischen Pfad anzeigen
  bach path list         Alle verfuegbaren Pfadnamen
  bach path set <n> <p>  Pfad-Override in DB setzen
  bach path overrides    DB-Overrides anzeigen
  bach path validate     Pfade validieren

Beispiele:
  bach path templates    Pfad zum Templates-Verzeichnis
  bach path berichte     Pfad zum Berichte-Verzeichnis
  bach path db           Pfad zur Haupt-Datenbank
  bach path set wissensdatenbank D:\\Meine\\Wissensdatenbank

Verfuegbare Pfade:
{path_list}
"""
        return True, help_text

    def _list_path_names(self) -> tuple:
        """Listet alle verfuegbaren Pfadnamen auf."""
        paths = list_paths()
        results = ["Verfuegbare Pfadnamen:", "=" * 50, ""]

        # Gruppiert nach Kategorie
        groups = {
            "Hierarchie": ["root", "bach", "system", "hub"],
            "System": ["data", "gui", "skills", "dist"],
            "Skills": ["tools", "help", "agents", "experts", "workflows", "partners", "services", "templates"],
            "Data": ["logs", "backups", "archive", "trash", "messages"],
            "User": ["user", "docs", "exports", "extensions", "user_documents", "persoenlich"],
            "Datenbanken": ["db", "bach_db", "archive_db"],
            "Berichte": ["foerderplanung", "berichte", "berichte_output", "berichte_klienten", "klienten", "bericht_template"],
            "Steuer": ["steuer", "steuer_2025", "belege", "bundles"],
            "Partner": ["gemini", "claude", "ollama"],
        }

        for group_name, path_names in groups.items():
            group_paths = [n for n in path_names if n in paths]
            if group_paths:
                results.append(f"{group_name}:")
                for name in group_paths:
                    results.append(f"  {name}")
                results.append("")

        # Restliche Pfade
        listed = set()
        for names in groups.values():
            listed.update(names)
        other = [n for n in paths.keys() if n not in listed]
        if other:
            results.append("Sonstige:")
            for name in sorted(other):
                results.append(f"  {name}")

        return True, "\n".join(results)

    def _show_all_paths(self) -> tuple:
        results = ["BACH Systempfade (v2.0)", "=" * 60, ""]

        # Gruppierte Ausgabe
        groups = {
            "Hauptverzeichnisse": ["root", "system", "hub", "data", "skills", "tools", "user"],
            "Templates & Berichte": ["templates", "berichte", "berichte_output", "bericht_template"],
            "Datenbanken": ["db", "archive_db"],
            "Partner": ["gemini", "claude", "ollama"],
        }

        for group_name, path_names in groups.items():
            results.append(f"\n{group_name}:")
            results.append("-" * 40)
            for name in path_names:
                try:
                    path = get_path(name)
                    exists = "✓" if path.exists() else "✗"
                    results.append(f"  {name:20} {exists} {path}")
                except KeyError:
                    pass

        results.append("")
        results.append("Nutze 'bach path list' fuer alle verfuegbaren Pfade.")

        return True, "\n".join(results)

    def _show_path(self, name: str) -> tuple:
        """Zeigt Details zu einem spezifischen Pfad."""
        path = get_path(name)  # Wirft KeyError wenn nicht gefunden
        exists = path.exists()

        result = f"{name}: {path}"

        # Zusatzinfo
        if exists:
            if path.is_dir():
                try:
                    count = len(list(path.iterdir()))
                    result += f"\n  ({count} Eintraege)"
                except:
                    pass
            elif path.is_file():
                size = path.stat().st_size
                if size > 1024 * 1024:
                    result += f"\n  ({size / 1024 / 1024:.1f} MB)"
                elif size > 1024:
                    result += f"\n  ({size / 1024:.1f} KB)"
                else:
                    result += f"\n  ({size} Bytes)"
        else:
            result += "\n  (existiert nicht)"

        return True, result

    def _show_overrides(self) -> tuple:
        """Zeigt DB-Overrides an."""
        overrides = load_path_overrides_from_db()

        if not overrides:
            return True, "Keine DB-Overrides gesetzt.\n\nSetze mit: bach path set <name> <pfad>"

        results = ["DB-Pfad-Overrides:", "=" * 40, ""]
        for name, path in overrides.items():
            exists = "✓" if path.exists() else "✗"
            results.append(f"  {name:20} {exists} {path}")

        return True, "\n".join(results)

    def _validate_paths(self) -> tuple:
        """Validiert alle wichtigen Pfade."""
        warnings = validate()

        if not warnings:
            return True, "[OK] Alle kritischen Pfade valide"

        results = ["Pfad-Validierung:", "=" * 40, ""]
        for w in warnings:
            results.append(f"  {w}")

        return True, "\n".join(results)
