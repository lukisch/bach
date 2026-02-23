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
Tool: translate_batch
Version: 1.0.0
Author: BACH Team
Created: 2026-02-04
Updated: 2026-02-04
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version translate_batch

Description:
    [Beschreibung hinzufügen]

Usage:
    python translate_batch.py [args]
"""

__version__ = "1.0.0"
__author__ = "BACH Team"

"""
translate_batch.py - Batch-Übersetzung DE->EN für BACH
======================================================

Übersetzt deutsche Strings ins Englische.
Verwendet einfache Wort-für-Wort Ersetzung + Regeln.

Usage:
    python translate_batch.py <input.json> <output.json>
"""

import json
import re
import sys
from pathlib import Path

# Basis-Wörterbuch für häufige Begriffe
TRANSLATIONS = {
    # Verben
    "anzeigen": "show", "auflisten": "list", "erstellen": "create",
    "löschen": "delete", "loeschen": "delete", "bearbeiten": "edit",
    "speichern": "save", "laden": "load", "öffnen": "open", "oeffnen": "open",
    "schließen": "close", "schliessen": "close", "suchen": "search",
    "finden": "find", "aktualisieren": "update", "hinzufügen": "add",
    "hinzufuegen": "add", "entfernen": "remove", "kopieren": "copy",
    "einfügen": "paste", "einfuegen": "paste", "starten": "start",
    "stoppen": "stop", "abbrechen": "cancel", "bestätigen": "confirm",
    "bestaetigen": "confirm", "prüfen": "check", "pruefen": "check",
    "exportieren": "export", "importieren": "import", "scannen": "scan",
    "durchsuchen": "search through", "zurückgeben": "return",
    "zurueckgeben": "return", "ausführen": "execute", "ausfuehren": "execute",
    "verarbeiten": "process", "analysieren": "analyze", "generieren": "generate",
    "initialisieren": "initialize", "konfigurieren": "configure",
    "registrieren": "register", "synchronisieren": "sync",

    # Substantive
    "Datei": "file", "Dateien": "files", "Ordner": "folder", "Verzeichnis": "directory",
    "Dokument": "document", "Dokumente": "documents", "Eintrag": "entry",
    "Einträge": "entries", "Eintraege": "entries", "Liste": "list",
    "Tabelle": "table", "Datenbank": "database", "Konfiguration": "configuration",
    "Einstellungen": "settings", "Optionen": "options", "Parameter": "parameters",
    "Fehler": "error", "Warnung": "warning", "Hinweis": "notice", "Info": "info",
    "Status": "status", "Ergebnis": "result", "Ausgabe": "output",
    "Eingabe": "input", "Befehl": "command", "Befehle": "commands",
    "Aufgabe": "task", "Aufgaben": "tasks", "Termin": "appointment",
    "Termine": "appointments", "Nachricht": "message", "Nachrichten": "messages",
    "Benutzer": "user", "Profil": "profile", "Konto": "account",
    "System": "system", "Programm": "program", "Anwendung": "application",
    "Handler": "handler", "Agent": "agent", "Agenten": "agents",
    "Skill": "skill", "Skills": "skills", "Tool": "tool", "Tools": "tools",
    "Workflow": "workflow", "Daemon": "daemon", "Session": "session",
    "Backup": "backup", "Export": "export", "Import": "import",
    "Übersetzung": "translation", "Uebersetzung": "translation",
    "Sprache": "language", "Wörterbuch": "dictionary", "Woerterbuch": "dictionary",

    # Adjektive/Adverbien
    "alle": "all", "keine": "none", "verfügbar": "available",
    "verfuegbar": "available", "aktiv": "active", "inaktiv": "inactive",
    "gültig": "valid", "gueltig": "valid", "ungültig": "invalid",
    "ungueltig": "invalid", "erforderlich": "required", "optional": "optional",
    "erfolgreich": "successful", "fehlgeschlagen": "failed",
    "gefunden": "found", "nicht gefunden": "not found",
    "geladen": "loaded", "gespeichert": "saved", "gelöscht": "deleted",
    "geloescht": "deleted", "erstellt": "created", "aktualisiert": "updated",
    "ausstehend": "pending", "abgeschlossen": "completed", "fertig": "done",
    "neu": "new", "alt": "old", "leer": "empty", "voll": "full",

    # BACH-spezifisch
    "Steuer": "tax", "Abo": "subscription", "Abonnement": "subscription",
    "Haushalt": "household", "Gesundheit": "health", "Kontakt": "contact",
    "Kontakte": "contacts", "Kalender": "calendar", "Routine": "routine",
    "Routinen": "routines", "Lektion": "lesson", "Lektionen": "lessons",
    "Wiki": "wiki", "Artikel": "article", "Thema": "topic",
    "Posten": "item", "Buchung": "booking", "Beleg": "receipt",

    # Phrasen
    "Keine Treffer": "No matches", "Nicht gefunden": "Not found",
    "Erfolgreich": "Successfully", "Fehler beim": "Error while",
    "Zeigt": "Shows", "Gibt": "Returns", "Führt aus": "Executes",
    "Fuehrt aus": "Executes", "Lädt": "Loads", "Laedt": "Loads",
    "Speichert": "Saves", "Löscht": "Deletes", "Loescht": "Deletes",
    "Erstellt": "Creates", "Aktualisiert": "Updates",
    "Durchsucht": "Searches", "Analysiert": "Analyzes",
    "Initialisiert": "Initializes", "Konfiguriert": "Configures",

    # Erweiterte Verben
    "Anonymisiert": "Anonymizes", "anonymisiert": "anonymizes",
    "Bereinigen": "Clean up", "bereinigen": "clean up",
    "Berechnet": "Calculates", "berechnet": "calculates",
    "Bereitet": "Prepares", "bereitet": "prepares",
    "Entfernt": "Removes", "entfernt": "removes",
    "Erkennt": "Detects", "erkennt": "detects",
    "Erneuert": "Renews", "erneuert": "renews",
    "Fügt": "Adds", "Fuegt": "Adds", "fügt": "adds", "fuegt": "adds",
    "Führt": "Performs", "führt": "performs",

    # Erweiterte Substantive
    "Zeitreihen": "time series", "Zeitreihenanalyse": "time series analysis",
    "Volatilität": "volatility", "Volatilitaet": "volatility",
    "Simulation": "simulation", "Prognose": "forecast", "Prognosen": "forecasts",
    "Treffer": "match", "Instanz": "instance", "Sequenz": "sequence",
    "Dateinamen": "file names", "Dateiname": "file name",
    "Zeichen": "characters", "Stationarität": "stationarity",
    "Stationaritaet": "stationarity",
    "Trendstärke": "trend strength", "Trendstaerke": "trend strength",
    "Watchlist": "watchlist", "Asset": "asset",
    "Blacklist": "blacklist", "Whitelist": "whitelist",
    "Wörter": "words", "Woerter": "words",
    "Dokumenttyp": "document type", "Text": "text",
    "Daten": "data", "sensible": "sensitive",

    # Technische Begriffe
    "ARIMA": "ARIMA", "LSTM": "LSTM", "RNN": "RNN",
    "Monte-Carlo": "Monte Carlo", "Mean Reversion": "mean reversion",
    "Half-Life": "half-life", "Dickey-Fuller": "Dickey-Fuller",
    "Context Manager": "context manager",

    # Zeit
    "tägliche": "daily", "taegliche": "daily",
    "älter": "older", "aelter": "older",
    "Tage": "days", "Tag": "day",
    "heute": "today", "Heute-Board": "today board",

    # Erweiterte Adjektive
    "annualisierte": "annualized", "normalisierte": "normalized",
    "überlappende": "overlapping", "ueberlappende": "overlapping",
    "ungueltige": "invalid", "sensible": "sensitive",

    # Weitere Phrasen
    "Alte Logs": "Old logs", "Ein gefundener": "A found",
    "zur": "to the", "zum": "to the", "anhand": "based on",
    "für": "for", "fuer": "for", "nach": "after",
}

# Regex-Patterns für strukturierte Übersetzungen
PATTERNS = [
    # "bach X Y" Befehle beibehalten
    (r'bach\s+(\w+)\s+(\w+)', r'bach \1 \2'),
    # Variablen in geschweiften Klammern beibehalten
    (r'\{([^}]+)\}', r'{\1}'),
    # CLI-Flags beibehalten
    (r'--(\w+)', r'--\1'),
    (r'-(\w)\s', r'-\1 '),
]


def translate_simple(text: str) -> str:
    """Einfache Wort-für-Wort Übersetzung."""
    if not text:
        return ""

    result = text

    # Sortiere nach Länge (längere zuerst) für bessere Matches
    sorted_trans = sorted(TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)

    for de, en in sorted_trans:
        # Case-insensitive replacement mit Wortgrenzen
        pattern = r'\b' + re.escape(de) + r'\b'
        result = re.sub(pattern, en, result, flags=re.IGNORECASE)

    return result


def translate_text(de_text: str) -> str:
    """Übersetzt deutschen Text ins Englische."""
    if not de_text or not de_text.strip():
        return ""

    # Kurze technische Strings (Befehle, Pfade) nicht übersetzen
    if de_text.startswith("bach ") or de_text.startswith("--"):
        return de_text

    # Mehrzeilige Help-Texte: Zeile für Zeile
    if "\n" in de_text:
        lines = de_text.split("\n")
        translated_lines = []
        for line in lines:
            if line.strip().startswith("bach ") or line.strip().startswith("--"):
                translated_lines.append(line)  # CLI-Befehle beibehalten
            elif line.strip().startswith("=") or line.strip().startswith("-"):
                translated_lines.append(line)  # Trennlinien beibehalten
            else:
                translated_lines.append(translate_simple(line))
        return "\n".join(translated_lines)

    return translate_simple(de_text)


def main():
    if len(sys.argv) < 3:
        print("Usage: python translate_batch.py <input.json> <output.json>")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    if not input_file.exists():
        print(f"Error: {input_file} not found")
        sys.exit(1)

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    translated_count = 0
    for item in data:
        de_text = item.get('de', '')
        if de_text and not item.get('en'):
            en_text = translate_text(de_text)
            if en_text != de_text:  # Nur wenn tatsächlich übersetzt
                item['en'] = en_text
                translated_count += 1

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[OK] {translated_count} Einträge übersetzt")
    print(f"[OK] Ausgabe: {output_file}")


if __name__ == "__main__":
    main()
