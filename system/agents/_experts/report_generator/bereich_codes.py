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
Bereich-Codes - Strukturierte Textgenerierung für Förderberichte
=================================================================

Jeder Bereich hat Sub-Codes. Das LLM schreibt Text pro relevantem Code.
Wenn mindestens ein Code Text hat, wird der Bereich aufgenommen.

WICHTIG: Diese Codes entsprechen EXAKT der Textvorlage!

Version: 2.0.0
Aktualisiert: 2026-02-05
"""

from typing import Dict, List, Optional, Tuple

# ═══════════════════════════════════════════════════════════════
# BEREICHE mit ihren Sub-Codes und Beschreibungen
# Codes entsprechen EXAKT der Textvorlage
# ═══════════════════════════════════════════════════════════════

BEREICH_STRUKTUR = {
    "mobilitaet": {
        "name": "Mobilität",
        "codes": {
            "D4700": "Fahrradfahren",
            "D4751": "Umgang mit motorisierten Fahrzeugen/E-Rollern",
            "D4702": "Nutzung öffentlicher Verkehrsmittel",
        }
    },
    "selbstversorgung": {
        "name": "Selbstversorgung",
        "codes": {
            # Körperpflege
            "D510": "Waschen/Körperpflege",
            "D520": "Pflege einzelner Körperbereiche",
            # Toilettengang (granular)
            "D53000": "Wahrnehmen und Mitteilen des Harndrangs",
            "D53001": "Durchführung des Toilettengangs (Harndrang)",
            "D53010": "Wahrnehmen und Mitteilen des Defäkationsbedarfs",
            "D5302": "Umgang mit Menstruation",
            # An-/Ausziehen (granular)
            "D5400": "Anziehen",
            "D5401": "Ausziehen",
            "D5402": "Schuhe anziehen",
            "D5403": "Schuhe ausziehen",
            "D5404": "Auswahl angemessener Kleidung",
            # Essen/Trinken (granular)
            "D5500": "Hungersignale wahrnehmen",
            "D560": "Durstsignale wahrnehmen",
            "D5501": "Essen unter Nutzung gesellschaftlicher Regeln",
            # Gesundheit (granular)
            "D5701": "Ernährung und Fitness",
            "D5702": "Allgemeine Gesundheitsfürsorge",
            "D57020": "Medikamenteneinnahme",
            "D57021": "Einholen von Hilfe",
            "D57022": "Risikoabschätzung",
            "D571": "Sicherheit",
        }
    },
    "haushalt": {
        "name": "Haushalt",
        "codes": {
            "D6200": "Einkaufen (planen und durchführen)",
            "D6300": "Einfache Mahlzeiten zubereiten",
            "D6301": "Komplexe Mahlzeiten/Beim Kochen unterstützen",
            "D640": "Hausarbeit",
            "D650": "Haushaltsgegenstände pflegen",
            "D660": "Anderen helfen (Care-Arbeit)",
        }
    },
    "lebensbereiche": {
        "name": "Lebensbereiche",
        "codes": {
            "D820": "Schulische Anforderungen",
            "D825": "Berufsorientierung",
            "D830": "Arbeiten mit Einschränkungen",
            "D845": "Einen Arbeitsplatz finden/behalten",
            "D850": "Bezahlte Arbeit",
            "D860": "Umgang mit Geld",
            "D870": "Wirtschaftliche Selbstständigkeit",
        }
    },
    "gesellschaft_freizeit": {
        "name": "Gesellschaft und Freizeit",
        "codes": {
            "D910": "Gesellschaftliche Teilhabe",
            "D9100": "Verständnis sozialer Strukturen",
            "D9109": "Verständnis gesellschaftlicher Abläufe",
            "D920": "Freizeitgestaltung",
            "D9200": "Hobbys/strukturierte Angebote",
            "D9201": "Sport (individuell angeben)",
            "D9202": "Gestalterische/handwerkliche Aktivitäten",
            "D9204": "Sonstige Hobbys (individuell angeben)",
        }
    },
}

UMWELT_STRUKTUR = {
    "wahrnehmung": {
        "name": "Wahrnehmung",
        "codes": {
            "E240": "Lichtempfindlichkeit",
            "E250": "Geräuschempfindlichkeit",
            "B1562": "Geruchswahrnehmung",
            "B1563": "Geschmackswahrnehmung",
            "B1564": "Taktile Wahrnehmung",
            "B2700": "Temperaturempfinden",
            "B2702": "Druck- und Berührungsempfinden",
            "B2703": "Wahrnehmung schädlicher Reize",
        }
    },
    "kommunikation": {
        "name": "Kommunikation",
        "codes": {
            "E1251": "Unterstützende Kommunikationshilfen (UK)",
            "E1250": "Allgemeine Kommunikationsprodukte",
        }
    },
    "kognition_motorik": {
        "name": "Kognition und Motorik",
        "codes": {
            "B117": "Kognitive Besonderheiten",
            "B3300": "Sprechflüssigkeit",
            "B3301": "Sprechrhythmus",
            "B3302": "Sprechtempo",
            "B3303": "Melodik des Sprechens",
            "B760": "Koordinationsschwierigkeiten",
            "B7651": "Tremor",
            "B7652": "Tics und Manierismen",
            "B7653": "Stereotypien/Perseverationen",
            "B1602": "Spezialinteressen/thematische Fixierungen",
        }
    },
    "medizinisches": {
        "name": "Medizinisches",
        "codes": {
            "B134": "Schlafprobleme",
            "B130": "Affektive Begleitprobleme",
            "B164": "Aufmerksamkeit",
            "B140": "Organisation und Planung",
            "E1101": "Medizinische Bedingungen (Allergien, Epilepsie)",
        }
    },
}


def get_alle_bereich_codes() -> Dict[str, Dict[str, str]]:
    """Gibt alle Bereich-Codes mit Beschreibungen zurück."""
    result = {}
    for bereich_key, bereich_def in BEREICH_STRUKTUR.items():
        result[bereich_key] = bereich_def["codes"].copy()
    return result


def get_alle_umwelt_codes() -> Dict[str, Dict[str, str]]:
    """Gibt alle Umwelt-Codes mit Beschreibungen zurück."""
    result = {}
    for umwelt_key, umwelt_def in UMWELT_STRUKTUR.items():
        result[umwelt_key] = umwelt_def["codes"].copy()
    return result


def build_bereich_text_from_codes(
    bereich_key: str,
    code_texte: Dict[str, Optional[str]],
    name: str
) -> Tuple[str, List[str]]:
    """
    Baut den Text für einen Bereich aus den Code-Texten.

    Args:
        bereich_key: z.B. "mobilitaet"
        code_texte: Dict mit Code -> Text (None = nicht relevant)
        name: Klientenname für [Name]-Ersetzung

    Returns:
        (zusammengesetzter_text, verwendete_codes)
    """
    if bereich_key not in BEREICH_STRUKTUR:
        return "", []

    bereich_def = BEREICH_STRUKTUR[bereich_key]
    valid_codes = set(bereich_def["codes"].keys())

    # Sammle Texte für gültige Codes
    texte = []
    verwendete_codes = []

    for code, text in code_texte.items():
        if code in valid_codes and text:
            # [Name] ersetzen
            text = text.replace("[Name]", name)
            texte.append(text)
            verwendete_codes.append(code)

    if not texte:
        return "", []

    # Texte zusammenfügen
    zusammen = " ".join(texte)
    return zusammen, verwendete_codes


def build_umwelt_text_from_codes(
    umwelt_key: str,
    code_texte: Dict[str, Optional[str]],
    name: str
) -> Tuple[str, List[str]]:
    """
    Baut den Text für einen Umweltfaktor aus den Code-Texten.
    """
    if umwelt_key not in UMWELT_STRUKTUR:
        return "", []

    umwelt_def = UMWELT_STRUKTUR[umwelt_key]
    valid_codes = set(umwelt_def["codes"].keys())

    texte = []
    verwendete_codes = []

    for code, text in code_texte.items():
        if code in valid_codes and text:
            text = text.replace("[Name]", name)
            texte.append(text)
            verwendete_codes.append(code)

    if not texte:
        return "", []

    zusammen = " ".join(texte)
    return zusammen, verwendete_codes


def get_bereich_name(bereich_key: str) -> str:
    """Gibt den Anzeigenamen eines Bereichs zurück."""
    if bereich_key in BEREICH_STRUKTUR:
        return BEREICH_STRUKTUR[bereich_key]["name"]
    return bereich_key


def get_umwelt_name(umwelt_key: str) -> str:
    """Gibt den Anzeigenamen eines Umweltfaktors zurück."""
    if umwelt_key in UMWELT_STRUKTUR:
        return UMWELT_STRUKTUR[umwelt_key]["name"]
    return umwelt_key


def build_prompt_code_reference() -> str:
    """
    Erstellt eine Referenz aller Codes für den LLM-Prompt.
    """
    lines = [
        "=== BEREICHE (Förderverlauf) ===",
        "Für jeden relevanten Code einen kurzen Text schreiben.",
        "Codes ohne Text werden übersprungen.",
        ""
    ]

    for bereich_key, bereich_def in BEREICH_STRUKTUR.items():
        lines.append(f"[{bereich_def['name'].upper()}]")
        for code, beschreibung in bereich_def["codes"].items():
            lines.append(f"  {code}: {beschreibung}")
        lines.append("")

    lines.append("=== UMWELTFAKTOREN ===")
    lines.append("")

    for umwelt_key, umwelt_def in UMWELT_STRUKTUR.items():
        lines.append(f"[{umwelt_def['name'].upper()}]")
        for code, beschreibung in umwelt_def["codes"].items():
            lines.append(f"  {code}: {beschreibung}")
        lines.append("")

    return "\n".join(lines)
