#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
PartnerConfigManager - LLM-Partner-Konfiguration
================================================

Verwaltet Auto-Eintragung von BACH in Partner-Config-Dateien:
- CLAUDE.md für Claude Code
- GEMINI.md für Gemini
- OLLAMA.md für Ollama

Teil von SQ015: LLM-Agnostik & Registrierungsprozess
"""

from pathlib import Path
from typing import Tuple, List


class PartnerConfigManager:
    """Verwaltet Auto-Eintragung in Partner-Config-Dateien."""

    SUPPORTED_PARTNERS = {
        "claude-code": {
            "config_file": "CLAUDE.md",
            "detection_dir": ".claude",
            "template_file": "CLAUDE_MD_TEMPLATE.md"
        },
        "gemini": {
            "config_file": "GEMINI.md",
            "detection_dir": ".gemini",
            "template_file": "GEMINI_MD_TEMPLATE.md"
        },
        "ollama": {
            "config_file": "OLLAMA.md",
            "detection_dir": ".ollama",
            "template_file": "OLLAMA_MD_TEMPLATE.md"
        }
    }

    def __init__(self, bach_root: Path):
        self.bach_root = Path(bach_root)
        self.home = Path.home()
        self.templates_dir = self.bach_root / "templates"

    def detect_active_partners(self) -> List[str]:
        """
        Erkennt installierte LLM-Partner.

        Returns:
            Liste der erkannten Partner (z.B. ["claude-code", "ollama"])
        """
        partners = []

        for partner_name, partner_info in self.SUPPORTED_PARTNERS.items():
            detection_dir = self.home / partner_info["detection_dir"]
            if detection_dir.exists():
                partners.append(partner_name)

        return partners

    def register_partner(self, partner: str) -> Tuple[bool, str]:
        """
        Trägt BACH in Partner-Config ein.

        Args:
            partner: Name des Partners ("claude-code", "gemini", "ollama")

        Returns:
            (success, message)
        """
        if partner not in self.SUPPORTED_PARTNERS:
            return False, f"✗ Unbekannter Partner: {partner}"

        partner_info = self.SUPPORTED_PARTNERS[partner]
        config_file = self.home / partner_info["config_file"]
        template_file = self.templates_dir / partner_info["template_file"]

        # Template laden
        if not template_file.exists():
            return False, f"✗ Template nicht gefunden: {template_file}"

        template = template_file.read_text(encoding='utf-8')
        content = template.replace("[BACH_ROOT_PATH]", str(self.bach_root))

        # Neue Datei erstellen
        if not config_file.exists():
            config_file.write_text(content, encoding='utf-8')
            return True, f"✓ {partner_info['config_file']} erstellt: {config_file}"

        # Prüfen ob BACH bereits eingetragen
        existing = config_file.read_text(encoding='utf-8')
        if "# BACH Integration" in existing:
            return True, f"✓ BACH bereits in {partner_info['config_file']} eingetragen"

        # Am Ende anhängen
        config_file.write_text(existing + "\n\n" + content, encoding='utf-8')
        return True, f"✓ BACH in {partner_info['config_file']} eingetragen: {config_file}"

    def unregister_partner(self, partner: str) -> Tuple[bool, str]:
        """
        Entfernt BACH-Block aus Partner-Config.

        Args:
            partner: Name des Partners

        Returns:
            (success, message)
        """
        if partner not in self.SUPPORTED_PARTNERS:
            return False, f"✗ Unbekannter Partner: {partner}"

        partner_info = self.SUPPORTED_PARTNERS[partner]
        config_file = self.home / partner_info["config_file"]

        if not config_file.exists():
            return True, f"✓ {partner_info['config_file']} existiert nicht"

        # Datei lesen
        content = config_file.read_text(encoding='utf-8')

        # BACH-Block entfernen
        if "# BACH Integration" not in content:
            return True, f"✓ Kein BACH-Block in {partner_info['config_file']}"

        # Einfache Implementierung: Entferne alles ab "# BACH Integration"
        # TODO: Verbesserung mit Marker-System (siehe SQ038)
        lines = content.split('\n')
        new_lines = []
        skip = False

        for line in lines:
            if line.strip() == "# BACH Integration":
                skip = True
            elif skip and line.startswith('#') and not line.startswith('##'):
                # Neuer Top-Level-Header → Ende des BACH-Blocks
                skip = False
                new_lines.append(line)
            elif not skip:
                new_lines.append(line)

        # Schreibe zurück
        config_file.write_text('\n'.join(new_lines).strip() + '\n', encoding='utf-8')
        return True, f"✓ BACH-Block aus {partner_info['config_file']} entfernt"

    def register_all_detected(self) -> List[Tuple[str, bool, str]]:
        """
        Trägt BACH in alle erkannten Partner ein.

        Returns:
            Liste von (partner, success, message)
        """
        detected = self.detect_active_partners()
        results = []

        for partner in detected:
            success, message = self.register_partner(partner)
            results.append((partner, success, message))

        return results


# ═══════════════════════════════════════════════════════════════
# CLI-Integration (für bach.py)
# ═══════════════════════════════════════════════════════════════

def cli_partner_register(bach_root: Path, partner: str = None):
    """CLI: bach partner register <name>"""
    manager = PartnerConfigManager(bach_root)

    if partner:
        # Einzelner Partner
        success, message = manager.register_partner(partner)
        print(message)
        return 0 if success else 1
    else:
        # Alle erkannten Partner
        results = manager.register_all_detected()

        if not results:
            print("✗ Keine LLM-Partner erkannt")
            print("Tipp: Stelle sicher dass ~/.claude/ oder ~/.gemini/ existiert")
            return 1

        for partner, success, message in results:
            print(message)

        return 0


def cli_partner_unregister(bach_root: Path, partner: str):
    """CLI: bach partner unregister <name>"""
    manager = PartnerConfigManager(bach_root)
    success, message = manager.unregister_partner(partner)
    print(message)
    return 0 if success else 1


def cli_partner_detect(bach_root: Path):
    """CLI: bach partner detect"""
    manager = PartnerConfigManager(bach_root)
    detected = manager.detect_active_partners()

    if detected:
        print("Erkannte LLM-Partner:")
        for partner in detected:
            print(f"  - {partner}")
    else:
        print("Keine LLM-Partner erkannt")

    return 0
