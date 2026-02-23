# SPDX-License-Identifier: MIT
"""
Help Handler - Zeigt Hilfe-Texte aus .txt Dateien
=================================================

Unterstuetzt auch Unterordner:
  bach --help tools                    -> docs/docs/docs/help/tools.txt
  bach --help tools/python_cli_editor  -> docs/docs/docs/help/tools/python_cli_editor.txt
  bach --help wiki/antigravity         -> wiki/antigravity.txt
  
NEU (v1.1.38): Tool-Direktzugriff
  bach --help path_healer              -> Tool-Info aus DB
  bach --help tool_scanner             -> Tool-Info aus DB
"""
from pathlib import Path
import sqlite3
from .base import BaseHandler


class HelpHandler(BaseHandler):
    """Handler fuer --help <topic>"""
    
    def __init__(self, base_path: Path):
        super().__init__(base_path)
        self.help_dir = base_path / "help"
    
    @property
    def profile_name(self) -> str:
        return "help"
    
    @property
    def target_file(self) -> Path:
        return self.help_dir
    
    def get_operations(self) -> dict:
        return {
            "list": "Alle verfuegbaren Hilfe-Themen anzeigen",
            "<topic>": "Hilfe zu einem bestimmten Thema anzeigen",
            "<folder>/<topic>": "Hilfe aus Unterordner (z.B. tools/python_cli_editor)"
        }
    
    def handle(self, operation: str, args: list, dry_run: bool = False) -> tuple:
        if not self.help_dir.exists():
            return False, f"Help-Verzeichnis nicht gefunden: {self.help_dir}"
        
        if operation == "list" or not operation:
            return self._list_topics()
        else:
            return self._show_topic(operation)
    
    def _list_topics(self) -> tuple:
        """Listet alle verfuegbaren Hilfe-Themen auf."""
        topics = []
        
        # Hauptordner
        for txt_file in sorted(self.help_dir.glob("*.txt")):
            topic = txt_file.stem
            try:
                with open(txt_file, "r", encoding="utf-8") as f:
                    first_line = f.readline().strip()
                    if first_line.startswith("="):
                        first_line = f.readline().strip()
                topics.append(f"  {topic:20} {first_line[:50]}")
            except:
                topics.append(f"  {topic}")
        
        # Unterordner
        subdirs = []
        for subdir in sorted(self.help_dir.iterdir()):
            if subdir.is_dir() and not subdir.name.startswith('_'):
                txt_count = len(list(subdir.glob("*.txt")))
                if txt_count > 0:
                    subdirs.append(f"  {subdir.name}/              ({txt_count} Themen)")
        
        if not topics and not subdirs:
            return False, "Keine Hilfe-Themen gefunden"
        
        result = "Verfuegbare Hilfe-Themen:\n\n"
        result += "\n".join(topics)
        
        if subdirs:
            result += "\n\nUnterordner:\n"
            result += "\n".join(subdirs)
            result += "\n\n  Abruf: --help <ordner>/<thema>"
            result += "\n  z.B.:  --help tools/python_cli_editor"
            result += "\n         --help wiki/antigravity"
        
        result += "\n\nNutzung: --help <topic>"
        return True, result
    
    def _show_topic(self, topic: str) -> tuple:
        """Zeigt Hilfe zu einem bestimmten Thema.
        
        Unterstuetzt:
          topic             -> docs/docs/docs/help/topic.txt
          folder/topic      -> docs/docs/docs/help/folder/topic.txt
          folder            -> docs/docs/docs/help/folder/_index.txt (falls vorhanden)
        """
        # Normalisieren: Backslash zu Slash, Leerzeichen zu Underscore
        topic = topic.lower().replace("\\", "/").replace("-", "_").replace(" ", "_")
        
        # Pfad aufbauen
        if "/" in topic:
            # Unterordner-Pfad: tools/python_cli_editor
            parts = topic.split("/", 1)
            folder = parts[0]
            subtopic = parts[1] if len(parts) > 1 else "_index"
            txt_file = self.help_dir / folder / f"{subtopic}.txt"
            
            # Fallback: Ordner-Index
            if not txt_file.exists() and len(parts) == 1:
                txt_file = self.help_dir / folder / "_index.txt"
        else:
            # Einfacher Topic-Name
            txt_file = self.help_dir / f"{topic}.txt"
            
            # Fallback: Vielleicht ist es ein Ordner?
            if not txt_file.exists():
                folder_path = self.help_dir / topic
                if folder_path.is_dir():
                    index_file = folder_path / "_index.txt"
                    if index_file.exists():
                        txt_file = index_file
        
        if not txt_file.exists():
            # NEU: Prüfe ob es ein Tool ist
            tool_help = self._get_tool_help(topic)
            if tool_help:
                return True, tool_help
            return self._suggest_topic(topic)
        
        try:
            with open(txt_file, "r", encoding="utf-8") as f:
                content = f.read()
            return True, content
        except Exception as e:
            return False, f"Fehler beim Lesen: {e}"
    
    def _get_tool_help(self, tool_name: str) -> str:
        """Holt Tool-Informationen aus der Datenbank.
        
        Returns:
            Tool-Hilfe als formatierter String oder None wenn nicht gefunden.
        """
        db_path = self.base_path / "data" / "bach.db"
        if not db_path.exists():
            return None
        
        try:
            conn = sqlite3.connect(str(db_path))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Suche Tool (case-insensitive, mit Wildcards)
            cursor.execute("""
                SELECT name, type, category, path, description, version,
                       capabilities, use_for, command, is_available
                FROM tools
                WHERE LOWER(name) = LOWER(?) OR LOWER(name) LIKE LOWER(?)
                LIMIT 1
            """, (tool_name, f"%{tool_name}%"))
            
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return None
            
            # Formatierte Ausgabe
            lines = [
                f"{'=' * 60}",
                f"TOOL: {row['name']}",
                f"{'=' * 60}",
                ""
            ]
            
            if row['description']:
                lines.append(f"Beschreibung: {row['description']}")
                lines.append("")
            
            lines.append(f"Typ:          {row['type'] or '-'}")
            lines.append(f"Kategorie:    {row['category'] or '-'}")
            lines.append(f"Version:      {row['version'] or '-'}")
            lines.append(f"Status:       {'Aktiv' if row['is_available'] else 'Inaktiv'}")
            
            if row['path']:
                lines.append(f"Pfad:         {row['path']}")
            
            if row['command']:
                lines.append(f"Befehl:       {row['command']}")
            
            if row['use_for']:
                lines.append("")
                lines.append("Verwendung:")
                for use in row['use_for'].split(','):
                    lines.append(f"  • {use.strip()}")
            
            if row['capabilities']:
                lines.append("")
                lines.append("Faehigkeiten:")
                for cap in row['capabilities'].split(','):
                    lines.append(f"  • {cap.strip()}")
            
            lines.append("")
            lines.append(f"{'=' * 60}")
            lines.append("(Daten aus tools-Tabelle, bach.db)")
            
            return "\n".join(lines)
            
        except Exception as e:
            return None

    def _suggest_topic(self, topic: str) -> tuple:
        """Schlaegt aehnliche Themen vor."""
        available = []
        
        # Hauptordner
        for f in self.help_dir.glob("*.txt"):
            available.append(f.stem)
        
        # Unterordner
        for subdir in self.help_dir.iterdir():
            if subdir.is_dir() and not subdir.name.startswith('_'):
                for f in subdir.glob("*.txt"):
                    if f.stem != "_index":
                        available.append(f"{subdir.name}/{f.stem}")
        
        # Matches finden
        topic_lower = topic.lower()
        matches = [t for t in available if topic_lower in t.lower() or t.lower() in topic_lower]
        
        if matches:
            suggestion = f"\n\nMeinten Sie:\n  " + "\n  ".join(matches[:5])
        else:
            # Zeige relevante Themen
            suggestion = f"\n\nVerfuegbar (Auswahl):\n  " + "\n  ".join(sorted(available)[:15])
            if len(available) > 15:
                suggestion += f"\n  ... und {len(available) - 15} weitere"
        
        return False, f"Hilfe-Thema '{topic}' nicht gefunden.{suggestion}"
