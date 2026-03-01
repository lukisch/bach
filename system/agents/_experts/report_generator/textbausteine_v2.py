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
Textbausteine v2 - Granulare ICF-Code-basierte Textgenerierung
===============================================================

Jeder Bereich hat Sub-Codes. Wenn mindestens ein Sub-Code aktiv ist,
wird der Bereich in den Bericht aufgenommen.

[Name] wird automatisch durch den Klientennamen ersetzt.

Version: 2.0.0
Erstellt: 2026-02-05
"""

from typing import Dict, List, Set

# ═══════════════════════════════════════════════════════════════
# MOBILITÄT (D4)
# ═══════════════════════════════════════════════════════════════

MOBILITAET_CODES = {
    "D4700": "zeigen sich bei [Name] Einschränkungen im Bereich Fahrradfahren",
    "D4751": "Auch der Umgang mit motorisierten Fahrzeugen oder E-Rollern ist erschwert",
    "D4702": "Die Nutzung öffentlicher Verkehrsmittel gelingt nur eingeschränkt oder unter Anleitung",
}

MOBILITAET_INTRO = "Aufgrund der autistischen Symptomatik"


# ═══════════════════════════════════════════════════════════════
# SELBSTVERSORGUNG (D5)
# ═══════════════════════════════════════════════════════════════

SELBSTVERSORGUNG_CODES = {
    "D510": "bestehen Einschränkungen im Bereich der Körperpflege, insbesondere beim Waschen",
    "D520": "und der Pflege einzelner Körperbereiche",
    "D53000": "Der Toilettengang ist betroffen, sowohl das Wahrnehmen und Mitteilen des Harndrangs",
    "D53001": "als auch die Durchführung des Toilettengangs",
    "D53010": "sowie das Wahrnehmen und Mitteilen des Defäkationsbedarfs",
    "D5302": "Der Umgang mit Menstruation kann zusätzliche Unterstützung erfordern",
    "D5400": "bestehen Schwierigkeiten beim An- und Ausziehen",
    "D5401": "Das Ausziehen erfordert Unterstützung",
    "D5402": "Der Umgang mit Schuhen (Anziehen) ist erschwert",
    "D5403": "Der Umgang mit Schuhen (Ausziehen) ist erschwert",
    "D5404": "Bei der Auswahl angemessener Kleidung bestehen ebenfalls Schwierigkeiten",
    "D5500": "Hungersignale werden nicht immer zuverlässig wahrgenommen",
    "D560": "Durstsignale werden nicht immer zuverlässig wahrgenommen",
    "D5501": "Das Essen unter Nutzung gesellschaftlicher Regeln fällt schwer",
    "D5701": "Im Bereich Gesundheit zeigen sich Einschränkungen bei Ernährung und Fitness",
    "D5702": "Die allgemeine Gesundheitsfürsorge ist eingeschränkt",
    "D57020": "Die Medikamenteneinnahme erfordert Unterstützung",
    "D57021": "Das Einholen von Hilfe ist erschwert",
    "D57022": "Die Risikoabschätzung ist eingeschränkt",
    "D571": "Zudem bestehen Schwierigkeiten im Bereich Sicherheit",
}

SELBSTVERSORGUNG_INTRO = "Bei [Name]"


# ═══════════════════════════════════════════════════════════════
# HAUSHALT (D6)
# ═══════════════════════════════════════════════════════════════

HAUSHALT_CODES = {
    "D6200": "bestehen Einschränkungen im häuslichen Leben, insbesondere beim Planen und Durchführen von Einkäufen",
    "D6300": "Auch das Planen und Zubereiten einfacher Mahlzeiten gelingt nur eingeschränkt",
    "D6301": "[Name] kann beim Kochen unterstützen, benötigt dabei jedoch Anleitung",
    "D640": "Die Beteiligung an Hausarbeit ist erschwert",
    "D650": "die Pflege von Haushaltsgegenständen ist ebenfalls erschwert",
    "D660": "Care-Arbeit, also das Kümmern um andere, gelingt nur eingeschränkt",
}

HAUSHALT_INTRO = "Bei [Name]"


# ═══════════════════════════════════════════════════════════════
# LEBENSBEREICHE (D8)
# ═══════════════════════════════════════════════════════════════

LEBENSBEREICHE_CODES = {
    "D820": "Im schulischen Kontext zeigen sich Einschränkungen im Verständnis von Anforderungen und im Umgang mit der eigenen Beeinträchtigung",
    "D825": "Im Bereich Berufsorientierung bestehen Herausforderungen",
    "D830": "Arbeiten mit Einschränkungen",
    "D845": "Einen Arbeitsplatz finden/behalten",
    "D850": "Bezahlte Arbeit",
    "D860": "bestehen Schwierigkeiten im Umgang mit Geld",
    "D870": "Wirtschaftliche Selbstständigkeit",
}

LEBENSBEREICHE_INTRO = "Bei [Name]"


# ═══════════════════════════════════════════════════════════════
# GESELLSCHAFT & FREIZEIT (D9)
# ═══════════════════════════════════════════════════════════════

GESELLSCHAFT_FREIZEIT_CODES = {
    "D910": "kommt es zu Einschränkungen der gesellschaftlichen Teilhabe",
    "D9100": "bestehen Schwierigkeiten im Verständnis sozialer Strukturen",
    "D9109": "und gesellschaftlicher Abläufe",
    "D920": "[Name] ist in der Freizeitgestaltung eingeschränkt",
    "D9200": "Empfohlen ist die Aufnahme eines Hobbys, beispielsweise der Besuch strukturierter Angebote",
    "D9201": "[Name] besucht gerne [SPORTART]",  # Platzhalter für individuelle Angabe
    "D9202": "[Name] zeigt Interesse an gestalterischen oder handwerklichen Projekten",
    "D9204": "Die Hobbys von [Name] umfassen unter anderem: [HOBBYS]",  # Platzhalter
}

GESELLSCHAFT_FREIZEIT_INTRO = "Aufgrund der autistischen Symptomatik von [Name]"


# ═══════════════════════════════════════════════════════════════
# WAHRNEHMUNG (E2, B1)
# ═══════════════════════════════════════════════════════════════

WAHRNEHMUNG_CODES = {
    "E240": "bestehen Empfindlichkeiten gegenüber Licht",
    "E250": "und Geräuschen",
    "B1562": "Zusätzlich zeigen sich Besonderheiten in der Geruchswahrnehmung",
    "B1563": "Geschmackswahrnehmung",
    "B1564": "und der taktilen Wahrnehmung",
    "B2700": "Auch Temperaturempfinden ist betroffen",
    "B2702": "Druck- und Berührungsempfinden",
    "B2703": "sowie die Wahrnehmung schädlicher Reize",
}

WAHRNEHMUNG_INTRO = "Aufgrund der autistischen Wahrnehmungsbesonderheiten von [Name]"


# ═══════════════════════════════════════════════════════════════
# KOMMUNIKATION (E1)
# ═══════════════════════════════════════════════════════════════

KOMMUNIKATION_CODES = {
    "E1251": "besteht ein Bedarf an unterstützenden Kommunikationshilfen und Technologien. Diese können genutzt werden, um die verbale oder nonverbale Kommunikation zu erleichtern und die Teilhabe zu verbessern",
}

KOMMUNIKATION_INTRO = "Bei [Name]"


# ═══════════════════════════════════════════════════════════════
# KOGNITION & MOTORIK (B1, B3, B7)
# ═══════════════════════════════════════════════════════════════

KOGNITION_MOTORIK_CODES = {
    "B117": "liegen kognitive Besonderheiten vor",
    "B3300": "Es bestehen Auffälligkeiten in der Sprechflüssigkeit",
    "B3301": "im Sprechrhythmus",
    "B3302": "im Sprechtempo",
    "B3303": "und in der Melodik des Sprechens",
    "B760": "Es zeigen sich motorische Besonderheiten wie Koordinationsschwierigkeiten",
    "B7651": "Tremor wurde beobachtet",
    "B7652": "zeigen sich Tics und Manierismen",
    "B7653": "sowie Stereotypien oder Perseverationen",
    "B1602": "Es bestehen ausgeprägte Spezialinteressen oder thematische Fixierungen",
}

KOGNITION_MOTORIK_INTRO = "Bei [Name]"


# ═══════════════════════════════════════════════════════════════
# MEDIZINISCHES (B1, E1)
# ═══════════════════════════════════════════════════════════════

MEDIZINISCHES_CODES = {
    "B134": "bestehen medizinisch relevante Faktoren wie Schlafprobleme",
    "B130": "und affektive Begleitprobleme",
    "B164": "Zusätzlich zeigen sich Schwierigkeiten in Aufmerksamkeit",
    "B140": "Organisation und Planung",
    "E1101": "Weiterhin liegen medizinische Bedingungen wie Allergien oder Epilepsie vor, die im Alltag berücksichtigt werden müssen",
}

MEDIZINISCHES_INTRO = "Bei [Name]"


# ═══════════════════════════════════════════════════════════════
# Zusammenfassung aller Bereiche
# ═══════════════════════════════════════════════════════════════

BEREICH_DEFINITIONEN = {
    "mobilitaet": {
        "name": "MOBILITÄT",
        "intro": MOBILITAET_INTRO,
        "codes": MOBILITAET_CODES,
    },
    "selbstversorgung": {
        "name": "SELBSTVERSORGUNG",
        "intro": SELBSTVERSORGUNG_INTRO,
        "codes": SELBSTVERSORGUNG_CODES,
    },
    "haushalt": {
        "name": "HAUSHALT",
        "intro": HAUSHALT_INTRO,
        "codes": HAUSHALT_CODES,
    },
    "lebensbereiche": {
        "name": "LEBENSBEREICHE",
        "intro": LEBENSBEREICHE_INTRO,
        "codes": LEBENSBEREICHE_CODES,
    },
    "gesellschaft_freizeit": {
        "name": "GESELLSCHAFT/FREIZEIT",
        "intro": GESELLSCHAFT_FREIZEIT_INTRO,
        "codes": GESELLSCHAFT_FREIZEIT_CODES,
    },
}

UMWELT_DEFINITIONEN = {
    "wahrnehmung": {
        "name": "WAHRNEHMUNG",
        "intro": WAHRNEHMUNG_INTRO,
        "codes": WAHRNEHMUNG_CODES,
    },
    "kommunikation": {
        "name": "KOMMUNIKATION",
        "intro": KOMMUNIKATION_INTRO,
        "codes": KOMMUNIKATION_CODES,
    },
    "kognition_motorik": {
        "name": "KOGNITION/MOTORIK",
        "intro": KOGNITION_MOTORIK_INTRO,
        "codes": KOGNITION_MOTORIK_CODES,
    },
    "medizinisches": {
        "name": "MEDIZINISCHES",
        "intro": MEDIZINISCHES_INTRO,
        "codes": MEDIZINISCHES_CODES,
    },
}


# ═══════════════════════════════════════════════════════════════
# Text-Generierung aus aktiven Codes
# ═══════════════════════════════════════════════════════════════

def build_bereich_text(
    bereich_key: str,
    aktive_codes: List[str],
    name: str,
    zusatz_infos: Dict[str, str] = None
) -> str:
    """
    Baut den Text für einen Bereich aus den aktiven Sub-Codes.

    Args:
        bereich_key: z.B. "mobilitaet", "selbstversorgung"
        aktive_codes: Liste der aktiven ICF-Codes z.B. ["D4700", "D4702"]
        name: Klientenname (ersetzt [Name])
        zusatz_infos: Optionale individuelle Angaben z.B. {"SPORTART": "Fußball"}

    Returns:
        Zusammengesetzter Text oder "" wenn keine Codes aktiv
    """
    if bereich_key not in BEREICH_DEFINITIONEN:
        return ""

    definition = BEREICH_DEFINITIONEN[bereich_key]
    code_texte = definition["codes"]

    # Finde aktive Codes für diesen Bereich
    relevante_codes = [c for c in aktive_codes if c in code_texte]

    if not relevante_codes:
        return ""

    # Text zusammenbauen
    intro = definition["intro"]
    teile = [code_texte[code] for code in relevante_codes]

    # Sätze verbinden
    if len(teile) == 1:
        text = f"{intro} {teile[0]}."
    else:
        text = f"{intro} {'. '.join(teile)}."

    # [Name] ersetzen
    text = text.replace("[Name]", name)

    # Zusätzliche Platzhalter ersetzen
    if zusatz_infos:
        for key, value in zusatz_infos.items():
            text = text.replace(f"[{key}]", value)

    # Unausgefüllte Platzhalter entfernen
    import re
    text = re.sub(r'\[[\w]+\]', '', text)

    return text


def build_umwelt_text(
    umwelt_key: str,
    aktive_codes: List[str],
    name: str,
    zusatz_infos: Dict[str, str] = None
) -> str:
    """
    Baut den Text für einen Umweltfaktor aus den aktiven Sub-Codes.
    """
    if umwelt_key not in UMWELT_DEFINITIONEN:
        return ""

    definition = UMWELT_DEFINITIONEN[umwelt_key]
    code_texte = definition["codes"]

    # Finde aktive Codes für diesen Bereich
    relevante_codes = [c for c in aktive_codes if c in code_texte]

    if not relevante_codes:
        return ""

    # Text zusammenbauen
    intro = definition["intro"]
    teile = [code_texte[code] for code in relevante_codes]

    # Sätze verbinden
    if len(teile) == 1:
        text = f"{intro} {teile[0]}."
    else:
        text = f"{intro} {', '.join(teile)}."

    # [Name] ersetzen
    text = text.replace("[Name]", name)

    # Zusätzliche Platzhalter ersetzen
    if zusatz_infos:
        for key, value in zusatz_infos.items():
            text = text.replace(f"[{key}]", value)

    # Unausgefüllte Platzhalter entfernen
    import re
    text = re.sub(r'\[[\w]+\]', '', text)

    return text


def get_alle_codes() -> Dict[str, Set[str]]:
    """Gibt alle verfügbaren Codes pro Bereich zurück."""
    result = {}

    for key, definition in BEREICH_DEFINITIONEN.items():
        result[key] = set(definition["codes"].keys())

    for key, definition in UMWELT_DEFINITIONEN.items():
        result[key] = set(definition["codes"].keys())

    return result


def get_code_beschreibung(code: str) -> str:
    """Gibt die Beschreibung eines Codes zurück."""
    for definition in list(BEREICH_DEFINITIONEN.values()) + list(UMWELT_DEFINITIONEN.values()):
        if code in definition["codes"]:
            return definition["codes"][code]
    return ""
