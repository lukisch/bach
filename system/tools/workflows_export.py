#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
workflows_export.py - WORKFLOWS.md Generator
=============================================

Generiert WORKFLOWS.md aus skills/workflows/ Verzeichnis.

Teil von SQ071: Spiegel-Dateien Auto-Export
"""

from pathlib import Path
from datetime import datetime
import re


class WorkflowsExporter:
    """Generiert WORKFLOWS.md aus Dateisystem."""

    def __init__(self, bach_root: Path):
        self.bach_root = Path(bach_root)

        # Auto-Detect: Root vs. system/ Installation
        if (self.bach_root / "system").exists():
            self.system_root = self.bach_root / "system"
        else:
            self.system_root = self.bach_root
            self.bach_root = self.system_root.parent

        self.workflows_dir = self.system_root / "skills" / "workflows"
        self.output_path = self.bach_root / "WORKFLOWS.md"

    def generate(self) -> tuple[bool, str]:
        """Generiert WORKFLOWS.md aus Dateisystem."""
        if not self.workflows_dir.exists():
            return False, f"✗ Workflows-Verzeichnis nicht gefunden: {self.workflows_dir}"

        workflows = self._scan_workflows()
        content = self._build_content(workflows)

        self.output_path.write_text(content, encoding='utf-8')
        return True, f"✓ WORKFLOWS.md generiert: {self.output_path}"

    def _scan_workflows(self) -> list[dict]:
        """Scannt skills/workflows/ nach .md Dateien (inkl. Unterordner)."""
        workflows = []

        # Scanne rekursiv (SQ050-2: Unterordner-Struktur)
        for md_file in sorted(self.workflows_dir.rglob("*.md")):
            # Skip _archive
            if '_archive' in md_file.parts:
                continue

            # Parse erste Zeilen für Metadaten
            content = md_file.read_text(encoding='utf-8', errors='replace')
            lines = content.split('\n')

            title = md_file.stem.replace('_', ' ').title()
            description = ""

            # Kategorie aus Verzeichnisstruktur
            relative_path = md_file.relative_to(self.workflows_dir)
            if len(relative_path.parts) > 1:
                category = relative_path.parts[0].title()
            else:
                category = "Workflows"

            # Extrahiere Titel und Beschreibung
            for i, line in enumerate(lines[:20]):
                # H1 Titel
                if line.startswith('# '):
                    title = line[2:].strip()

                # Beschreibung (erste Textzeile nach Titel)
                if not line.startswith('#') and line.strip() and not description:
                    if i > 0:  # Nach Titel
                        description = line.strip()
                        if len(description) > 200:
                            description = description[:200] + "..."
                        break

            workflows.append({
                'name': title,
                'file': str(relative_path),
                'description': description,
                'category': category
            })

        return workflows

    def _build_content(self, workflows: list[dict]) -> str:
        """Baut WORKFLOWS.md Content."""
        lines = []
        lines.append("# BACH Workflows")
        lines.append("")
        lines.append("Automatisch generiert aus dem Dateisystem (skills/workflows/).")
        lines.append(f"Letzte Aktualisierung: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("")
        lines.append(f"**Total:** {len(workflows)} Workflows")
        lines.append("")

        # Gruppiere nach Kategorie (SQ050-2)
        by_category = {}
        for wf in workflows:
            cat = wf['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(wf)

        # Kategorien sortiert ausgeben
        for cat in sorted(by_category.keys()):
            lines.append(f"## {cat}")
            lines.append("")

            for wf in by_category[cat]:
                lines.append(f"### {wf['name']}")

                if wf['description']:
                    lines.append("")
                    lines.append(wf['description'])

                lines.append("")
                lines.append(f"**Datei:** `skills/workflows/{wf['file']}`")
                lines.append("")

        return "\n".join(lines)
