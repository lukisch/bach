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
Tool: c_project_bundler
Version: 1.0.0
Author: BACH Team
Created: 2026-02-04
Updated: 2026-02-04
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version c_project_bundler

Description:
    [Beschreibung hinzufügen]

Usage:
    python c_project_bundler.py [args]
"""

__version__ = "1.0.0"
__author__ = "BACH Team"

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# Konfiguration
SOURCE_DIR = Path(".")  # Aktueller Ordner (oder Pfad anpassen)
OUTPUT_FILE = "COMPLETE_PROJECT_CONTEXT.txt"
AUDIT_DIR = "_AUDIT_PACKAGE"

# Was ignoriert werden soll
IGNORE_DIRS = {
    "__pycache__", ".git", ".idea", ".vscode", "venv", "env", 
    "node_modules", "build", "dist", "_archived-docu", AUDIT_DIR
}

# Welche Dateiendungen wir wollen (Text-basiert)
ALLOWED_EXTENSIONS = {
    ".py", ".md", ".json", ".txt", ".bat", ".ps1", ".yml", ".yaml", 
    ".html", ".css", ".js", ".ini", ".cfg"
}

# Dateien, die wir explizit ignorieren (z.B. das Script selbst oder der Output)
IGNORE_FILES = {
    "project_bundler.py", 
    "project_bundler1.py",
    OUTPUT_FILE,
    "package-lock.json"
}

# Audit-Dateien (relativ zum _BATCH Root)
AUDIT_FILES = {
    "SKILL.md": "SKILL.md",
    "LESSONS_LEARNED.md": "LESSONS_LEARNED.md",
    "SYSTEM/SELF-CHECK-PROCEDURE.md": "SELF-CHECK-PROCEDURE.md",
    "SYSTEM/DIRECTORY_TRUTH.md": "DIRECTORY_TRUTH.md",
    "SYSTEM/SYSTEM-HEALTH-CHECK.txt": "SYSTEM-HEALTH-CHECK.txt",
}

AUDIT_MISSION_TEMPLATE = '''# 🕵️ MISSION: SYSTEM-AUDIT (EXTERNAL REVIEW)

**Erstellt:** {date}
**System:** Claude Batch System (_BATCH)

---

Hallo Gemini,
du agierst hier als externer Auditor für das "Claude Batch System".
Deine Aufgabe ist ein unvoreingenommener SELF-CHECK gemäß den beiliegenden Dokumenten.

## 📋 Beiliegende Dateien

| Datei | Beschreibung |
|-------|--------------|
| SKILL.md | Hauptdokumentation - "Das Gesetzbuch" |
| LESSONS_LEARNED.md | Erfahrungswerte und Problemlösungen |
| SELF-CHECK-PROCEDURE.md | Prüfanleitung für das System |
| DIRECTORY_TRUTH.md | Ordnerstruktur und Dateibeschreibungen |
| SYSTEM-HEALTH-CHECK.txt | Aktueller Wartungsstatus |

---

## 1. Prüfung der Dokumentation (SKILL.md & Co)

Bitte prüfe die beiliegenden Markdown-Dateien auf:
- **Logik-Lücken:** Widersprechen sich die Dokumente gegenseitig?
- **Veraltete Pfade:** Stimmen Referenzen noch (basierend auf Standard-Python/Batch-Strukturen)?
- **Verständlichkeit:** Würdest du als KI das System basierend auf SKILL.md bedienen können?
- **Vollständigkeit:** Fehlen wichtige Informationen für einen neuen Bearbeiter?

---

## 2. Prüfung der Problemlösungen (LESSONS_LEARNED.md)

- Sind die Lösungen in LESSONS_LEARNED.md technisch valide (Python/Powershell Best Practices)?
- Gibt es sicherere oder modernere Alternativen?
- Sind die Workarounds noch notwendig oder könnten sie vereinfacht werden?

---

## 3. Red Teaming

Suche aktiv nach Schwächen:
- Wo könnte das System versagen?
- Welche Edge Cases sind nicht abgedeckt?
- Gibt es Sicherheitsrisiken?
- Wo ist die Dokumentation irreführend?

---

## 4. Output-Format

Erstelle einen Bericht mit folgendem Format:

### 🔴 Kritische Fehler (Sofortmaßnahmen)
- Fehler die das System unbrauchbar machen könnten

### 🟡 Warnungen (Wichtige Verbesserungen)
- Ungenaue Formulierungen
- Potenzielle Probleme

### 🟢 Optimierungsvorschläge (Best Practices)
- Nice-to-have Verbesserungen
- Modernisierungen

### 📊 Zusammenfassung
- Gesamteindruck (1-10)
- Top 3 Prioritäten

---

## 5. Rückgabe

Der Bericht wird als **AUDIT_ERGEBNIS_{date}.md** gespeichert
und nach _BATCH/DATA/BERICHTE/ kopiert.

---

*Dieses Audit wurde automatisch von project_bundler1.py --audit generiert.*
'''


def is_text_file(file_path):
    """Prüft auf erlaubte Endung."""
    return file_path.suffix.lower() in ALLOWED_EXTENSIONS


def bundle_project():
    """Bündelt das gesamte Projekt in eine TXT-Datei."""
    print(f"📦 Starte Bündelung von: {SOURCE_DIR.resolve()}")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        # Header schreiben
        outfile.write(f"# PROJECT DUMP\n")
        outfile.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        outfile.write("="*50 + "\n\n")

        file_count = 0

        # Durch alle Ordner laufen
        for root, dirs, files in os.walk(SOURCE_DIR):
            # Ignorierte Ordner entfernen (in-place modification für os.walk)
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

            for file in files:
                if file in IGNORE_FILES:
                    continue
                
                path = Path(root) / file
                
                # Nur Textdateien verarbeiten
                if is_text_file(path):
                    try:
                        # Relativen Pfad für den Header berechnen
                        rel_path = path.relative_to(SOURCE_DIR)
                        
                        # Header für die Datei schreiben
                        outfile.write(f"\n\n{'='*20} START FILE: {rel_path} {'='*20}\n")
                        
                        # Inhalt lesen und schreiben
                        content = path.read_text(encoding="utf-8", errors="ignore")
                        outfile.write(content)
                        
                        # Footer schreiben
                        outfile.write(f"\n{'='*20} END FILE: {rel_path} {'='*20}\n")
                        
                        print(f"  + Hinzugefügt: {rel_path}")
                        file_count += 1
                        
                    except Exception as e:
                        print(f"  ! Fehler bei {path}: {e}")

    print(f"\n✅ Fertig! {file_count} Dateien in '{OUTPUT_FILE}' gebündelt.")


def prepare_audit():
    """Bereitet Audit-Dateien für externes Review vor (einzelne Dateien, kein ZIP)."""
    print(f"🕵️ Bereite Audit-Paket vor...")
    
    # Basis-Pfad ermitteln (_BATCH Root)
    batch_root = SOURCE_DIR.resolve()
    if batch_root.name != "_BATCH":
        # Versuche _BATCH im Parent zu finden
        for parent in batch_root.parents:
            if parent.name == "_BATCH":
                batch_root = parent
                break
        else:
            # Annahme: Wir sind bereits in _BATCH
            pass
    
    audit_path = batch_root / AUDIT_DIR
    
    # Alten Audit-Ordner löschen falls vorhanden
    if audit_path.exists():
        shutil.rmtree(audit_path)
        print(f"  🗑️ Alter Audit-Ordner gelöscht")
    
    # Neuen Ordner erstellen
    audit_path.mkdir(exist_ok=True)
    
    file_count = 0
    missing_files = []
    
    # Audit-Dateien kopieren
    for source_rel, target_name in AUDIT_FILES.items():
        source_path = batch_root / source_rel
        target_path = audit_path / target_name
        
        if source_path.exists():
            shutil.copy2(source_path, target_path)
            print(f"  + Kopiert: {source_rel} → {target_name}")
            file_count += 1
        else:
            print(f"  ⚠️ Nicht gefunden: {source_rel}")
            missing_files.append(source_rel)
    
    # Mission-Datei generieren
    date_str = datetime.now().strftime("%Y-%m-%d")
    mission_content = AUDIT_MISSION_TEMPLATE.format(date=date_str)
    mission_path = audit_path / "GEMINI_AUDIT_MISSION.md"
    mission_path.write_text(mission_content, encoding="utf-8")
    print(f"  + Generiert: GEMINI_AUDIT_MISSION.md")
    file_count += 1
    
    # Zusammenfassung
    print(f"\n{'='*50}")
    print(f"✅ Audit-Paket erstellt: {audit_path}")
    print(f"   📄 {file_count} Dateien")
    
    if missing_files:
        print(f"   ⚠️ {len(missing_files)} Dateien fehlen:")
        for f in missing_files:
            print(f"      - {f}")
    
    print(f"\n📋 Nächste Schritte:")
    print(f"   1. Öffne Gemini (gemini.google.com)")
    print(f"   2. Lade die Dateien aus {AUDIT_DIR}/ einzeln hoch")
    print(f"   3. Beginne mit GEMINI_AUDIT_MISSION.md")
    print(f"   4. Speichere das Ergebnis als AUDIT_ERGEBNIS_{date_str}.md")
    print(f"   5. Kopiere es nach DATA/BERICHTE/")


def print_usage():
    """Zeigt Hilfe an."""
    print("""
project_bundler1.py - Projekt-Bündelung und Audit-Vorbereitung

Verwendung:
    python project_bundler1.py          # Bündelt Projekt in TXT
    python project_bundler1.py --audit  # Erstellt Audit-Paket für Gemini
    python project_bundler1.py --help   # Zeigt diese Hilfe

Modi:
    Standard    Bündelt alle Textdateien in COMPLETE_PROJECT_CONTEXT.txt
    --audit     Erstellt _AUDIT_PACKAGE/ mit Einzeldateien für externes Review
    """)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == "--audit":
            prepare_audit()
        elif arg in ("--help", "-h", "/?"):
            print_usage()
        else:
            print(f"Unbekanntes Argument: {arg}")
            print_usage()
    else:
        bundle_project()
