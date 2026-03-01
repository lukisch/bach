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
Textbausteine für Förderberichte
================================

Vorlagen für Bereiche und Umweltfaktoren.
[Name] wird automatisch durch den Klientennamen ersetzt.

Version: 1.0.0
Erstellt: 2026-02-05
"""

# ═══════════════════════════════════════════════════════════════
# BEREICHE (Förderverlauf)
# ═══════════════════════════════════════════════════════════════

BEREICH_MOBILITAET = """Aufgrund der autistischen Symptomatik zeigen sich bei [Name] Einschränkungen im Bereich Fahrradfahren (D4700). Auch der Umgang mit motorisierten Fahrzeugen oder E-Rollern (D4751) ist erschwert. Die Nutzung öffentlicher Verkehrsmittel (D4702) gelingt nur eingeschränkt oder unter Anleitung."""

BEREICH_SELBSTVERSORGUNG = """Bei [Name] bestehen Einschränkungen im Bereich der Körperpflege, insbesondere beim Waschen (D510) und der Pflege einzelner Körperbereiche (D520). Auch der Toilettengang ist betroffen, sowohl das Wahrnehmen und Mitteilen des Harndrangs (D53000) als auch die Durchführung (D53001) sowie das Wahrnehmen und Mitteilen des Defäkationsbedarfs (D53010) und die Durchführung (D53010). Der Umgang mit Menstruation (D5302) kann zusätzliche Unterstützung erfordern. Beim An- und Ausziehen (D5400, D5401), beim Umgang mit Schuhen (D5402, D5403) sowie bei der Auswahl angemessener Kleidung (D5404) bestehen ebenfalls Schwierigkeiten. Hunger- und Durstsignale werden nicht immer zuverlässig wahrgenommen (D5500, D560), und das Essen unter Nutzung gesellschaftlicher Regeln (D5501) fällt schwer. Auch im Bereich Gesundheit zeigen sich Einschränkungen, etwa bei Ernährung und Fitness (D5701), allgemeiner Gesundheitsfürsorge (D5702), Medikamenteneinnahme (D57020), dem Einholen von Hilfe (D57021) sowie der Risikoabschätzung (D57022). Zudem bestehen Schwierigkeiten im Bereich Sicherheit (D571)."""

BEREICH_HAUSHALT = """Bei [Name] bestehen Einschränkungen im häuslichen Leben, insbesondere beim Planen und Durchführen von Einkäufen (D6200). Auch das Planen und Zubereiten einfacher (D6300) oder komplexer Mahlzeiten (D6301) gelingt nur eingeschränkt. [Name] kann beim Kochen unterstützen, benötigt dabei jedoch Anleitung (D6301). Die Beteiligung an Hausarbeit (D640) und die Pflege von Haushaltsgegenständen (D650) sind ebenfalls erschwert. Care-Arbeit, also das Kümmern um andere, gelingt nur eingeschränkt (D660)."""

BEREICH_LEBENSBEREICHE = """Bei [Name] bestehen Schwierigkeiten im Umgang mit Geld (D860). Im schulischen Kontext zeigen sich Einschränkungen im Verständnis von Anforderungen und im Umgang mit der eigenen Beeinträchtigung (D820). Auch im Bereich Berufsorientierung und Arbeiten mit Einschränkungen bestehen Herausforderungen (D825, D830, D845, D850, D870)."""

BEREICH_GESELLSCHAFT_FREIZEIT = """Aufgrund der autistischen Symptomatik von [Name] kommt es zu Einschränkungen der gesellschaftlichen Teilhabe (D910). Zusätzlich bestehen Schwierigkeiten im Verständnis sozialer Strukturen und gesellschaftlicher Abläufe (D9100–D9109). [Name] ist in der Freizeitgestaltung eingeschränkt (D920). Empfohlen ist die Aufnahme eines Hobbys, beispielsweise der Besuch eines Schachclubs oder anderer strukturierter Angebote (D9200)."""


# ═══════════════════════════════════════════════════════════════
# UMWELTFAKTOREN (Besondere Fähigkeiten / Unterstützungsbedarf)
# ═══════════════════════════════════════════════════════════════

UMWELT_WAHRNEHMUNG = """Aufgrund der autistischen Wahrnehmungsbesonderheiten von [Name] bestehen Empfindlichkeiten gegenüber Licht (E240) und Geräuschen (E250). Zusätzlich zeigen sich Besonderheiten in der Geruchswahrnehmung (B1562), Geschmackswahrnehmung (B1563) und der taktilen Wahrnehmung (B1564). Auch Temperaturempfinden (B2700), Druck- und Berührungsempfinden (B2702) sowie die Wahrnehmung schädlicher Reize (B2703) sind betroffen."""

UMWELT_KOMMUNIKATION = """Bei [Name] besteht ein Bedarf an unterstützenden Kommunikationshilfen und Technologien (E1251). Diese können genutzt werden, um die verbale oder nonverbale Kommunikation zu erleichtern und die Teilhabe zu verbessern."""

UMWELT_KOGNITION_MOTORIK = """Bei [Name] liegen kognitive Besonderheiten (B117) vor, ebenso Auffälligkeiten in Sprechflüssigkeit (B3300), Sprechrhythmus (B3301), Sprechtempo (B3302) und Melodik des Sprechens (B3303). Zusätzlich zeigen sich motorische Besonderheiten wie Koordinationsschwierigkeiten (B760), Tremor (B7651), Tics und Manierismen (B7652) sowie Stereotypien oder Perseverationen (B7653). Weiterhin bestehen ausgeprägte Spezialinteressen oder thematische Fixierungen (B1602)."""

UMWELT_MEDIZINISCHES = """Bei [Name] bestehen medizinisch relevante Faktoren wie Schlafprobleme (B134) und affektive Begleitprobleme (B130). Zusätzlich zeigen sich Schwierigkeiten in Aufmerksamkeit, Organisation und Planung (B164, B140). Weiterhin liegen medizinische Bedingungen wie Allergien oder Epilepsie vor (E1101), die im Alltag berücksichtigt werden müssen."""


# ═══════════════════════════════════════════════════════════════
# Mapping für einfachen Zugriff
# ═══════════════════════════════════════════════════════════════

BEREICH_VORLAGEN = {
    "mobilitaet": BEREICH_MOBILITAET,
    "selbstversorgung": BEREICH_SELBSTVERSORGUNG,
    "haushalt": BEREICH_HAUSHALT,
    "lebensbereiche": BEREICH_LEBENSBEREICHE,
    "gesellschaft_freizeit": BEREICH_GESELLSCHAFT_FREIZEIT,
}

UMWELT_VORLAGEN = {
    "wahrnehmung": UMWELT_WAHRNEHMUNG,
    "kommunikation": UMWELT_KOMMUNIKATION,
    "kognition_motorik": UMWELT_KOGNITION_MOTORIK,
    "medizinisches": UMWELT_MEDIZINISCHES,
}


def get_bereich_text(bereich_key: str, name: str, custom_text: str = None) -> str:
    """
    Gibt den Bereichstext zurück.

    Wenn custom_text angegeben ist, wird dieser verwendet.
    Sonst wird die Vorlage mit ersetztem [Name] zurückgegeben.
    """
    if custom_text:
        return custom_text.replace("[Name]", name)

    vorlage = BEREICH_VORLAGEN.get(bereich_key, "")
    return vorlage.replace("[Name]", name)


def get_umwelt_text(umwelt_key: str, name: str, custom_text: str = None) -> str:
    """
    Gibt den Umweltfaktor-Text zurück.

    Wenn custom_text angegeben ist, wird dieser verwendet.
    Sonst wird die Vorlage mit ersetztem [Name] zurückgegeben.
    """
    if custom_text:
        return custom_text.replace("[Name]", name)

    vorlage = UMWELT_VORLAGEN.get(umwelt_key, "")
    return vorlage.replace("[Name]", name)
