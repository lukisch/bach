#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
agents_export.py - AGENTS.md Generator
======================================

Generiert AGENTS.md aus bach_agents und bach_experts Tabellen.

Teil von SQ071: Spiegel-Dateien Auto-Export
Referenz: BACH_Dev/templates/AGENTS.md
"""

from pathlib import Path
from datetime import datetime
import sqlite3


class AgentsExporter:
    """Generiert AGENTS.md aus DB."""

    def __init__(self, bach_root: Path):
        self.bach_root = Path(bach_root)

        # Auto-Detect: Root vs. system/ Installation
        if (self.bach_root / "system").exists():
            self.system_root = self.bach_root / "system"
        else:
            self.system_root = self.bach_root
            self.bach_root = self.system_root.parent

        self.db_path = self.system_root / "data" / "bach.db"
        self.output_path = self.bach_root / "AGENTS.md"

    def generate(self) -> tuple[bool, str]:
        """Generiert AGENTS.md aus DB."""
        # Prüfe ob Tabellen existieren
        if not self._check_tables():
            return False, "✗ Tabellen bach_agents oder bach_experts nicht gefunden"

        # Hole Daten
        agents = self._get_agents()
        experts = self._get_experts()

        # Baue Content
        content = self._build_content(agents, experts)

        # Schreibe Datei
        self.output_path.write_text(content, encoding='utf-8')
        return True, f"✓ AGENTS.md generiert: {self.output_path}"

    def _check_tables(self) -> bool:
        """Prüft ob bach_agents und bach_experts existieren."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("""
            SELECT COUNT(*) FROM sqlite_master
            WHERE type='table' AND name IN ('bach_agents', 'bach_experts')
        """)
        count = cursor.fetchone()[0]
        conn.close()
        return count == 2

    def _get_agents(self) -> list[dict]:
        """Hole alle Boss-Agenten aus bach_agents."""
        conn = sqlite3.connect(self.db_path)

        # Prüfe welche Spalten existieren
        cursor = conn.execute("PRAGMA table_info(bach_agents)")
        columns = [col[1] for col in cursor.fetchall()]

        # Basis-Query (angepasst an tatsächliches Schema)
        query = "SELECT name, display_name, type, category, description, skill_path, is_active, version FROM bach_agents ORDER BY name"

        cursor = conn.execute(query)
        agents = []

        for row in cursor.fetchall():
            agent = {
                'name': row[0],
                'display_name': row[1],
                'type': row[2],
                'category': row[3],
                'description': row[4],
                'path': row[5],  # skill_path
                'status': 'active' if row[6] else 'inactive',  # is_active
                'version': row[7]
            }

            agents.append(agent)

        conn.close()
        return agents

    def _get_experts(self) -> list[dict]:
        """Hole alle Experten aus bach_experts."""
        conn = sqlite3.connect(self.db_path)

        # Basis-Query (angepasst an tatsächliches Schema)
        query = "SELECT name, display_name, domain, description, skill_path, is_active, version FROM bach_experts ORDER BY name"

        cursor = conn.execute(query)
        experts = []

        for row in cursor.fetchall():
            expert = {
                'name': row[0],
                'display_name': row[1],
                'type': row[2],  # domain
                'description': row[3],
                'path': row[4],  # skill_path
                'status': 'active' if row[5] else 'inactive',  # is_active
                'version': row[6]
            }

            experts.append(expert)

        conn.close()
        return experts

    def _build_content(self, agents: list[dict], experts: list[dict]) -> str:
        """Baut AGENTS.md Content."""
        lines = []
        lines.append("# BACH Agents & Experts")
        lines.append("")
        lines.append(f"**Generiert:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("**Quelle:** bach.db (bach_agents, bach_experts)")
        lines.append("**Generator:** `bach export mirrors` oder `python tools/agents_export.py`")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Boss-Agenten (Orchestrierer)")
        lines.append("")
        lines.append("Boss-Agenten orchestrieren komplexe Workflows und delegieren an Experten.")
        lines.append("")

        # Agenten
        for agent in agents:
            display = agent.get('display_name') or agent['name']
            lines.append(f"### {display}")
            lines.append(f"- **Name:** {agent['name']}")
            lines.append(f"- **Typ:** {agent['type']}")
            lines.append(f"- **Kategorie:** {agent.get('category', 'N/A')}")
            lines.append(f"- **Pfad:** `{agent['path']}`")
            lines.append(f"- **Status:** {agent['status']}")
            lines.append(f"- **Version:** {agent.get('version', 'N/A')}")

            if agent.get('description'):
                lines.append(f"- **Beschreibung:** {agent['description']}")

            lines.append("")

        lines.append("---")
        lines.append("")
        lines.append("## Experten (Spezialisierte Ausführer)")
        lines.append("")
        lines.append("Experten führen spezifische Aufgaben aus und werden von Boss-Agenten delegiert.")
        lines.append("")

        # Experten
        for expert in experts:
            display = expert.get('display_name') or expert['name']
            lines.append(f"### {display}")
            lines.append(f"- **Name:** {expert['name']}")
            lines.append(f"- **Domain:** {expert['type']}")
            lines.append(f"- **Pfad:** `{expert['path']}`")
            lines.append(f"- **Status:** {expert['status']}")
            lines.append(f"- **Version:** {expert.get('version', 'N/A')}")

            if expert.get('description'):
                lines.append(f"- **Beschreibung:** {expert['description']}")

            lines.append("")

        lines.append("---")
        lines.append("")
        lines.append("## Status-Kategorien")
        lines.append("")
        lines.append("- **FUNCTIONAL:** Voll funktionsfähig, produktionsbereit")
        lines.append("- **PARTIAL:** Grundfunktionen vorhanden, aber unvollständig")
        lines.append("- **SKELETON:** Struktur vorhanden, aber Implementierung fehlt weitgehend")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Charakter-Modell (ENT-41)")
        lines.append("")
        lines.append("Jeder Boss-Agent hat eine `## Charakter` Section in seiner SKILL.md:")
        lines.append("- **Ton:** Wie kommuniziert der Agent?")
        lines.append("- **Schwerpunkt:** Woran orientiert er sich?")
        lines.append("- **Haltung:** Welche Werte vertritt er?")
        lines.append("")
        lines.append("Siehe: BACH_Dev/MASTERPLAN_PENDING.txt → SQ049 Agenten-Audit & Upgrade")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Arbeitsprinzipien")
        lines.append("")
        lines.append("Alle Agenten folgen den globalen Arbeitsprinzipien aus Root-SKILL.md:")
        lines.append("- Unterscheiden was eigen, was fremd")
        lines.append("- Text ist Wahrheit")
        lines.append("- Erst lesen, dann ändern")
        lines.append("- Keine Duplikate erzeugen")
        lines.append("- Flexibel auf User-Korrekturen reagieren")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Nutzung")
        lines.append("")
        lines.append("```bash")
        lines.append("# Boss-Agent starten (mit Partner-Delegation)")
        lines.append("bach agent start bueroassistent --partner=claude-code")
        lines.append("")
        lines.append("# Experten direkt aufrufen (falls erlaubt)")
        lines.append('bach expert run bewerbungsexperte --task="Anschreiben für Stelle X"')
        lines.append("")
        lines.append("# Agent-Liste anzeigen")
        lines.append("bach agent list")
        lines.append("")
        lines.append("# Expert-Liste anzeigen")
        lines.append("bach expert list")
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Datei-Synchronisation")
        lines.append("")
        lines.append("Diese Datei wird automatisch generiert aus:")
        lines.append("- `bach_agents` (Tabelle für Boss-Agenten)")
        lines.append("- `bach_experts` (Tabelle für Experten)")
        lines.append("")
        lines.append("**Trigger:**")
        lines.append("- `bach --shutdown` (via finalize_on_idle)")
        lines.append("- `bach export mirrors` (manuell)")
        lines.append("")
        lines.append("**dist_type:** 1 (TEMPLATE) - resetbar, aber anpassbar")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Siehe auch")
        lines.append("")
        lines.append("- **PARTNERS.md** - LLM-Partner und Delegation")
        lines.append("- **USECASES.md** - Anwendungsfälle")
        lines.append("- **WORKFLOWS.md** - 25 Protocol-Skills als Index")
        lines.append("- **CHAINS.md** - Toolchains")
        lines.append("")

        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# CLI-Entry-Point
# ═══════════════════════════════════════════════════════════════

def main():
    """CLI für agents_export."""
    import sys

    # BACH_ROOT ermitteln
    script_dir = Path(__file__).parent.parent  # system/
    bach_root = script_dir.parent  # BACH_v2_vanilla/

    exporter = AgentsExporter(bach_root)
    success, message = exporter.generate()
    print(message)
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
