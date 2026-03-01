#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
Privacy Classifier — Datenschutz-Ampel fuer Dokumente (INT06)

Portiert aus ProFiler Datenschutzampel. Klassifiziert Texte/Dateien
nach Sensitivitaet anhand von Regex-Patterns.

Ampel-Stufen:
  ROT   - Sensible personenbezogene Daten (IBAN, Steuernr, Gesundheit)
  GELB  - Potenziell interne Daten (Namen, Adressen, Kontodaten)
  GRUEN - Keine sensiblen Daten erkannt
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

AMPEL_ROT = "ROT"
AMPEL_GELB = "GELB"
AMPEL_GRUEN = "GRUEN"

# ================================================================
# PATTERN-DEFINITIONEN
# ================================================================

# ROT: Definitiv sensible Daten
PATTERNS_ROT = {
    "IBAN (DE)": r"DE\d{2}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{2}",
    "Steuernummer": r"\b\d{2,3}/\d{3}/\d{5}\b",
    "Steuer-ID": r"\b\d{2}\s?\d{3}\s?\d{3}\s?\d{3}\b",
    "Sozialversicherungsnr": r"\b\d{2}\s?\d{6}\s?[A-Z]\s?\d{3}\b",
    "Kreditkarte": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
    "Personalausweis": r"\b[A-Z]{1,2}\d{7}[0-9A-Z]\b",
    "Gesundheitsdaten": r"\b(?:Diagnose|Befund|Krankheit|Medikament|Therapie|Rezept|Patient(?:in)?)\b",
}

# GELB: Potenziell sensibel
PATTERNS_GELB = {
    "Geburtsdatum": r"\b(?:geb\.|geboren|Geburtsdatum)[:\s]*\d{1,2}\.\d{1,2}\.\d{2,4}\b",
    "Telefonnummer": r"\b(?:Tel|Fon|Telefon|Mobil)[.:\s]*[+\d][\d\s/()-]{8,}\b",
    "Email-Adresse": r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",
    "Kontonummer": r"\b(?:Konto(?:nr)?|BLZ)[.:\s]*\d{6,}\b",
    "Adresse": r"\b(?:Straße|Str\.|Weg|Platz|Gasse)\s+\d{1,4}[a-z]?\b",
}


class PrivacyClassifier:
    """Klassifiziert Texte nach Datenschutz-Sensitivitaet."""

    def __init__(self):
        self._compiled_rot = {
            name: re.compile(pattern, re.IGNORECASE)
            for name, pattern in PATTERNS_ROT.items()
        }
        self._compiled_gelb = {
            name: re.compile(pattern, re.IGNORECASE)
            for name, pattern in PATTERNS_GELB.items()
        }

    def classify_text(self, text: str) -> Dict:
        """Klassifiziert einen Text.

        Returns:
            {
                "ampel": "ROT"|"GELB"|"GRUEN",
                "findings": [{"pattern": str, "matches": [str], "level": str}, ...],
            }
        """
        findings = []

        # ROT-Patterns pruefen
        for name, regex in self._compiled_rot.items():
            matches = regex.findall(text)
            if matches:
                findings.append({
                    "pattern": name,
                    "matches": matches[:5],  # Max 5 Treffer
                    "level": AMPEL_ROT,
                })

        # GELB-Patterns pruefen
        for name, regex in self._compiled_gelb.items():
            matches = regex.findall(text)
            if matches:
                findings.append({
                    "pattern": name,
                    "matches": matches[:5],
                    "level": AMPEL_GELB,
                })

        # Ampel bestimmen
        if any(f["level"] == AMPEL_ROT for f in findings):
            ampel = AMPEL_ROT
        elif any(f["level"] == AMPEL_GELB for f in findings):
            ampel = AMPEL_GELB
        else:
            ampel = AMPEL_GRUEN

        return {"ampel": ampel, "findings": findings}

    def classify_file(self, path: Path, max_bytes: int = 1024 * 1024) -> Dict:
        """Klassifiziert eine Textdatei.

        Returns:
            {"path": str, "ampel": str, "findings": [...], "error": str|None}
        """
        path = Path(path)
        result = {"path": str(path), "ampel": AMPEL_GRUEN, "findings": [], "error": None}

        if not path.exists():
            result["error"] = "Datei nicht gefunden"
            return result

        # Nur Textdateien
        text_extensions = {
            ".txt", ".csv", ".md", ".json", ".xml", ".html", ".htm",
            ".log", ".py", ".sql", ".yaml", ".yml", ".toml", ".ini",
            ".cfg", ".conf", ".tex", ".bib", ".rtf",
        }
        if path.suffix.lower() not in text_extensions:
            result["error"] = "Kein Textformat"
            return result

        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            if len(content) > max_bytes:
                content = content[:max_bytes]
            classification = self.classify_text(content)
            result["ampel"] = classification["ampel"]
            result["findings"] = classification["findings"]
        except Exception as e:
            result["error"] = str(e)

        return result

    def scan_directory(self, path: Path, recursive: bool = True) -> Dict:
        """Scannt Verzeichnis und klassifiziert alle Textdateien.

        Returns:
            {
                "total_files": int,
                "classified": int,
                "skipped": int,
                "rot": int,
                "gelb": int,
                "gruen": int,
                "findings": [{"path": str, "ampel": str, "findings": [...]}, ...],
            }
        """
        path = Path(path)
        if not path.exists():
            raise ValueError(f"Pfad existiert nicht: {path}")

        results = []
        skipped = 0

        if path.is_file():
            files = [path]
        elif recursive:
            files = [f for f in path.rglob("*") if f.is_file()]
        else:
            files = [f for f in path.iterdir() if f.is_file()]

        for fpath in files:
            r = self.classify_file(fpath)
            if r["error"]:
                skipped += 1
                continue
            if r["findings"]:  # Nur Dateien mit Treffern speichern
                results.append(r)

        rot = sum(1 for r in results if r["ampel"] == AMPEL_ROT)
        gelb = sum(1 for r in results if r["ampel"] == AMPEL_GELB)

        return {
            "total_files": len(files),
            "classified": len(files) - skipped,
            "skipped": skipped,
            "rot": rot,
            "gelb": gelb,
            "gruen": len(files) - skipped - rot - gelb,
            "findings": sorted(results, key=lambda x: (0 if x["ampel"] == AMPEL_ROT else 1, x["path"])),
        }

    @staticmethod
    def format_report(result: Dict) -> str:
        """Formatiert Scan-Ergebnis als Text-Report."""
        lines = [
            "DATENSCHUTZ-SCAN ERGEBNIS",
            "=" * 50,
            "",
            f"  Dateien gesamt:    {result['total_files']}",
            f"  Klassifiziert:     {result['classified']}",
            f"  Uebersprungen:     {result['skipped']}",
            "",
            f"  ROT  (sensibel):   {result['rot']}",
            f"  GELB (intern):     {result['gelb']}",
            f"  GRUEN (ok):        {result['gruen']}",
        ]

        findings = result["findings"]
        if not findings:
            lines.append("")
            lines.append("  Keine sensiblen Daten erkannt.")
            return "\n".join(lines)

        lines.append("")
        for r in findings[:30]:  # Max 30 Dateien
            lines.append(f"  [{r['ampel']}] {r['path']}")
            for f in r["findings"]:
                match_str = ", ".join(f["matches"][:3])
                lines.append(f"        {f['pattern']}: {match_str}")

        if len(findings) > 30:
            lines.append(f"\n  ... und {len(findings) - 30} weitere Dateien")

        return "\n".join(lines)
