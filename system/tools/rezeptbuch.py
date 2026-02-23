#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Rezeptbuch - Doku-Generator aus DB-Tabellen (SQ069)
====================================================

Konzept: Aus Kombination von DB-Tabellen (tools, agents, skills, protocols)
automatisch Rohfassungen für Dokumentation erstellen.

Workflow:
1. Rezept definieren (welche Tabellen, welche Spalten)
2. Tool ausführen -> Rohfassung generieren
3. Mit help.txt / wiki / .md Dateien ergänzen

Usage:
    python rezeptbuch.py agents         # Generiert AGENTS.md aus bach_agents Tabelle
    python rezeptbuch.py skills         # Generiert SKILLS.md aus skills Tabelle
    python rezeptbuch.py tools          # Generiert TOOLS.md aus tools Tabelle
    python rezeptbuch.py protocols      # Generiert PROTOCOLS.md aus protocols Tabelle
    python rezeptbuch.py custom <name>  # Generiert aus custom Rezept

Author: BACH Development Team
Created: 2026-02-21 (SQ069, Runde 19)
"""

import sqlite3
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class Rezeptbuch:
    """Generator für Dokumentation aus DB-Tabellen."""

    def __init__(self, db_path: Path, bach_root: Path):
        self.db_path = Path(db_path)
        self.bach_root = Path(bach_root)

    @staticmethod
    def _filter_shebang(text: str) -> str:
        """
        Filtert Shebangs aus Beschreibungstexten.

        Wenn Text mit #! beginnt (Shebang), wird stattdessen ein
        Platzhalter zurückgegeben, da Shebangs keine sinnvolle
        Dokumentation sind.

        Args:
            text: Der zu filternde Text

        Returns:
            Gefilterter Text oder Platzhalter bei Shebang
        """
        if not text:
            return text

        text = text.strip()

        # Prüfe ob Text mit Shebang beginnt
        # DB enthält Varianten: "#!/usr/bin/...", "!/usr/bin/..." (ohne #), BOM + "#!"
        if text.startswith('#!') or text.startswith('!/usr/bin'):
            return "(Keine Beschreibung verfügbar)"

        return text

    def _get_db(self):
        """DB-Verbindung."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def generate_agents_doc(self) -> Tuple[bool, str]:
        """Generiert AGENTS.md aus bach_agents Tabelle."""
        try:
            conn = self._get_db()
            try:
                # Hole alle Agenten (angepasst an tatsächliches Schema)
                cursor = conn.execute("""
                    SELECT name, display_name, type, category, description, is_active, created_at
                    FROM bach_agents
                    ORDER BY name
                """)
                agents = cursor.fetchall()

                if not agents:
                    return False, "Keine Agenten in DB gefunden"

                # Generiere Markdown
                lines = []
                lines.append("# BACH Agenten")
                lines.append("")
                lines.append(f"Auto-generiert: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                lines.append("")
                lines.append(f"**Anzahl**: {len(agents)} Agenten")
                lines.append("")

                for agent in agents:
                    display = agent['display_name'] or agent['name']
                    lines.append(f"## {display}")
                    lines.append("")
                    lines.append(f"**Name**: {agent['name']}")
                    if agent['type']:
                        lines.append(f"**Typ**: {agent['type']}")
                    if agent['category']:
                        lines.append(f"**Kategorie**: {agent['category']}")
                    if agent['description']:
                        desc = self._filter_shebang(agent['description'])
                        lines.append(f"**Beschreibung**: {desc}")
                    status = 'Aktiv' if agent['is_active'] else 'Inaktiv'
                    lines.append(f"**Status**: {status}")
                    lines.append("")

                content = "\n".join(lines)

                # Speichern
                output_file = self.bach_root / "AGENTS_GENERATED.md"
                output_file.write_text(content, encoding='utf-8')

                return True, f"✓ AGENTS_GENERATED.md erstellt: {len(agents)} Agenten"

            finally:
                conn.close()

        except Exception as e:
            return False, f"Fehler bei Agenten-Doku: {e}"

    def generate_tools_doc(self) -> Tuple[bool, str]:
        """Generiert TOOLS.md aus tools Tabelle."""
        try:
            conn = self._get_db()
            try:
                # Hole alle Tools
                cursor = conn.execute("""
                    SELECT name, version, category, description, type, path
                    FROM tools
                    WHERE name IS NOT NULL
                    ORDER BY category, name
                """)
                tools = cursor.fetchall()

                if not tools:
                    return False, "Keine Tools in DB gefunden"

                # Gruppiere nach Kategorie
                by_category: Dict[str, List] = {}
                for tool in tools:
                    cat = tool['category'] or 'Unkategorisiert'
                    if cat not in by_category:
                        by_category[cat] = []
                    by_category[cat].append(tool)

                # Generiere Markdown
                lines = []
                lines.append("# BACH Tools")
                lines.append("")
                lines.append(f"Auto-generiert: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                lines.append("")
                lines.append(f"**Anzahl**: {len(tools)} Tools in {len(by_category)} Kategorien")
                lines.append("")

                for category in sorted(by_category.keys()):
                    lines.append(f"## {category}")
                    lines.append("")

                    for tool in by_category[category]:
                        lines.append(f"### {tool['name']}")
                        if tool['version']:
                            lines.append(f"**Version**: {tool['version']}")
                        if tool['type']:
                            lines.append(f"**Typ**: {tool['type']}")
                        if tool['path']:
                            lines.append(f"**Pfad**: {tool['path']}")
                        if tool['description']:
                            desc = self._filter_shebang(tool['description'])
                            lines.append(f"**Beschreibung**: {desc}")
                        lines.append("")

                content = "\n".join(lines)

                # Speichern
                output_file = self.bach_root / "TOOLS_GENERATED.md"
                output_file.write_text(content, encoding='utf-8')

                return True, f"✓ TOOLS_GENERATED.md erstellt: {len(tools)} Tools"

            finally:
                conn.close()

        except Exception as e:
            return False, f"Fehler bei Tools-Doku: {e}"

    def generate_skills_doc(self) -> Tuple[bool, str]:
        """Generiert SKILLS.md aus skills Tabelle."""
        try:
            conn = self._get_db()
            try:
                # Hole alle Skills
                cursor = conn.execute("""
                    SELECT name, type, category, version, description, is_active, trigger_phrases
                    FROM skills
                    WHERE name IS NOT NULL
                    ORDER BY category, name
                """)
                skills = cursor.fetchall()

                if not skills:
                    return False, "Keine Skills in DB gefunden"

                # Gruppiere nach Kategorie
                by_category: Dict[str, List] = {}
                for skill in skills:
                    cat = skill['category'] or 'Unkategorisiert'
                    if cat not in by_category:
                        by_category[cat] = []
                    by_category[cat].append(skill)

                # Generiere Markdown
                lines = []
                lines.append("# BACH Skills")
                lines.append("")
                lines.append(f"Auto-generiert: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                lines.append("")
                lines.append(f"**Anzahl**: {len(skills)} Skills in {len(by_category)} Kategorien")
                lines.append("")

                for category in sorted(by_category.keys()):
                    lines.append(f"## {category}")
                    lines.append("")

                    for skill in by_category[category]:
                        lines.append(f"### {skill['name']}")
                        if skill['type']:
                            lines.append(f"**Typ**: {skill['type']}")
                        if skill['version']:
                            lines.append(f"**Version**: {skill['version']}")
                        if skill['description']:
                            desc = self._filter_shebang(skill['description'])
                            lines.append(f"**Beschreibung**: {desc}")
                        if skill['trigger_phrases']:
                            lines.append(f"**Trigger**: {skill['trigger_phrases']}")
                        status = 'Aktiv' if skill['is_active'] else 'Inaktiv'
                        lines.append(f"**Status**: {status}")
                        lines.append("")

                content = "\n".join(lines)

                # Speichern
                output_file = self.bach_root / "SKILLS_GENERATED.md"
                output_file.write_text(content, encoding='utf-8')

                return True, f"✓ SKILLS_GENERATED.md erstellt: {len(skills)} Skills"

            finally:
                conn.close()

        except Exception as e:
            return False, f"Fehler bei Skills-Doku: {e}"

    def generate_protocols_doc(self) -> Tuple[bool, str]:
        """Generiert PROTOCOLS.md aus interaction_protocols Tabelle."""
        try:
            conn = self._get_db()
            try:
                # Hole alle Protocols
                cursor = conn.execute("""
                    SELECT protocol_name, protocol_type, description, status, priority
                    FROM interaction_protocols
                    ORDER BY protocol_type, protocol_name
                """)
                protocols = cursor.fetchall()

                if not protocols:
                    return False, "Keine Protocols in DB gefunden"

                # Gruppiere nach Typ
                by_type: Dict[str, List] = {}
                for protocol in protocols:
                    ptype = protocol['protocol_type'] or 'Unkategorisiert'
                    if ptype not in by_type:
                        by_type[ptype] = []
                    by_type[ptype].append(protocol)

                # Generiere Markdown
                lines = []
                lines.append("# BACH Interaction Protocols")
                lines.append("")
                lines.append(f"Auto-generiert: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                lines.append("")
                lines.append(f"**Anzahl**: {len(protocols)} Protocols in {len(by_type)} Typen")
                lines.append("")

                for ptype in sorted(by_type.keys()):
                    lines.append(f"## {ptype}")
                    lines.append("")

                    for protocol in by_type[ptype]:
                        lines.append(f"### {protocol['protocol_name']}")
                        if protocol['description']:
                            desc = self._filter_shebang(protocol['description'])
                            lines.append(f"**Beschreibung**: {desc}")
                        if protocol['priority']:
                            lines.append(f"**Priorität**: {protocol['priority']}")
                        if protocol['status']:
                            lines.append(f"**Status**: {protocol['status']}")
                        lines.append("")

                content = "\n".join(lines)

                # Speichern
                output_file = self.bach_root / "PROTOCOLS_GENERATED.md"
                output_file.write_text(content, encoding='utf-8')

                return True, f"✓ PROTOCOLS_GENERATED.md erstellt: {len(protocols)} Protocols"

            finally:
                conn.close()

        except Exception as e:
            return False, f"Fehler bei Protocols-Doku: {e}"

    def generate_custom_doc(self, recipe_name: str) -> Tuple[bool, str]:
        """Generiert Dokumentation nach custom Rezept (TODO Phase 2)."""
        return False, f"Custom-Rezept '{recipe_name}' noch nicht implementiert (Phase 2)"


def main():
    """CLI Entry Point."""
    if len(sys.argv) < 2:
        print("Usage: python rezeptbuch.py [agents|tools|skills|protocols|custom <name>]")
        print("")
        print("Beispiele:")
        print("  python rezeptbuch.py agents     # Generiert AGENTS_GENERATED.md")
        print("  python rezeptbuch.py tools      # Generiert TOOLS_GENERATED.md")
        print("  python rezeptbuch.py skills     # Generiert SKILLS_GENERATED.md")
        print("  python rezeptbuch.py protocols  # Generiert PROTOCOLS_GENERATED.md")
        sys.exit(1)

    # Pfade ermitteln
    script_path = Path(__file__).resolve()
    system_root = script_path.parent.parent  # tools/ -> system/
    bach_root = system_root.parent           # system/ -> BACH_v2_vanilla/
    db_path = system_root / "data" / "bach.db"

    if not db_path.exists():
        print(f"[ERROR] bach.db nicht gefunden: {db_path}")
        sys.exit(1)

    # Rezeptbuch initialisieren
    rezeptbuch = Rezeptbuch(db_path, bach_root)

    # Befehl ausführen
    command = sys.argv[1].lower()

    if command == "agents":
        success, msg = rezeptbuch.generate_agents_doc()
    elif command == "tools":
        success, msg = rezeptbuch.generate_tools_doc()
    elif command == "skills":
        success, msg = rezeptbuch.generate_skills_doc()
    elif command == "protocols":
        success, msg = rezeptbuch.generate_protocols_doc()
    elif command == "custom":
        if len(sys.argv) < 3:
            print("[ERROR] Custom-Rezept braucht Namen")
            print("Beispiel: python rezeptbuch.py custom my-recipe")
            sys.exit(1)
        recipe_name = sys.argv[2]
        success, msg = rezeptbuch.generate_custom_doc(recipe_name)
    else:
        print(f"[ERROR] Unbekannter Befehl: {command}")
        print("Verfügbar: agents, tools, skills, protocols, custom")
        sys.exit(1)

    print(msg)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
