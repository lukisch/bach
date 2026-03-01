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
Worksheet Generator - Erstellt personalisierte Arbeitsblatter
Task: FOERD-01
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Basis-Pfade
BASE_PATH = Path(__file__).parent.parent.parent.parent # BACH_v2_vanilla
KLIENTEN_DIR = BASE_PATH / "user" / "foerderplaner" / "klienten"
TEMPLATES_DIR = Path(__file__).parent / "templates"
OUTPUT_DIR = Path(__file__).parent / "output"

def load_client_data(client_id):
    """Laedt Daten aus dem letzten Bericht des Klienten"""
    client_path = KLIENTEN_DIR / client_id
    bericht_file = client_path / "output" / "bericht_data.json"
    
    if bericht_file.exists():
        try:
            with open(bericht_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Fehler beim Laden von {bericht_file}: {e}")
            return None
    
    # Fallback: Suche rekursiv im Klientenordner
    # TODO: Bessere Logik fuer aktuellsten Bericht
    return None

def list_clients():
    """Listet verfuegbare Klienten (basierend auf Ordnern)"""
    if not KLIENTEN_DIR.exists():
        print(f"Klienten-Verzeichnis nicht gefunden: {KLIENTEN_DIR}")
        return

    print(f"\nVerfuegbare Klienten in {KLIENTEN_DIR}:\n")
    print(f"{'ID':<15} {'Tarnname':<20} {'Diagnose':<30}")
    print("-" * 65)

    for entry in KLIENTEN_DIR.iterdir():
        if entry.is_dir() and entry.name.startswith("K_"):
            data = load_client_data(entry.name)
            name = "???"
            diag = "???"
            if data and 'stammdaten' in data:
                name = data['stammdaten'].get('name', '???')
                diagnosen = data['stammdaten'].get('diagnosen', [])
                if diagnosen:
                    diag = diagnosen[0]
            
            print(f"{entry.name:<15} {name:<20} {diag:<30}")

def generate_prompt(client_id, type_):
    """Generiert den LLM-Prompt fuer das Arbeitsblatt"""
    data = load_client_data(client_id)
    if not data:
        print(f"Keine Daten fuer Klient {client_id} gefunden.")
        return

    # Template laden
    template_file = TEMPLATES_DIR / f"{type_}.txt"
    if not template_file.exists():
        print(f"Template nicht gefunden: {template_file}")
        print("Verfuegbare Typen: " + ", ".join([f.stem for f in TEMPLATES_DIR.glob("*.txt")]))
        return

    with open(template_file, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Kontext extrahieren
    stammdaten = data.get('stammdaten', {})
    ziele = data.get('foerderziele', [])
    neue_ziele = data.get('neue_ziele', [])
    
    alle_ziele = []
    for z in ziele:
        alle_ziele.append(f"- {z.get('zielformulierung')} (Status: {z.get('ist_stand')})")
    for z in neue_ziele:
        alle_ziele.append(f"- NEU: {z.get('zielformulierung')}")

    context = {
        "NAME": stammdaten.get('name', 'Schueler'),
        "ALTER": "Unbekannt", # TODO: Geburtsdatum rechnen
        "DIAGNOSE": ", ".join(stammdaten.get('diagnosen', [])),
        "INTERESSEN": data.get('besondere_faehigkeiten', 'Keine bekannt'),
        "ZIELE": "\n".join(alle_ziele)
    }

    # Simple Replacement (koennte man mit Jinja2 machen)
    prompt = template_content
    for key, value in context.items():
        prompt = prompt.replace(f"{{{{{key}}}}}", str(value))

    # Output speichern
    out_file = OUTPUT_DIR / f"prompt_{client_id}_{type_}.txt"
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(prompt)
    
    print(f"\nPrompt generiert: {out_file}")
    print("Sende diesen Prompt an Claude/Gemini, um das Arbeitsblatt zu erhalten.")

def main():
    parser = argparse.ArgumentParser(description="Worksheet Generator")
    subparsers = parser.add_subparsers(dest='command')

    # list
    subparsers.add_parser('list', help='Klienten auflisten')

    # generate
    gen_parser = subparsers.add_parser('generate', help='Arbeitsblatt-Prompt generieren')
    gen_parser.add_argument('client_id', help='Klienten-ID (Ordnername)')
    gen_parser.add_argument('type', help='Typ (mathe, deutsch, etc.)')

    args = parser.parse_args()

    if args.command == 'list':
        list_clients()
    elif args.command == 'generate':
        generate_prompt(args.client_id, args.type)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
