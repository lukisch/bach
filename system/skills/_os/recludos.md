---
name: reclud-os
metadata:
  version: 3.3.0
  last_updated: 2026-01-01
description: >
  Zentrales Verwaltungssystem fuer RecludOS. Dies ist der EINZIGE Skill 
  der bei Claude hochgeladen werden muss. Er kennt alle lokalen Skills, 
  fuehrt Versions-Checks durch und laedt bei Bedarf aktuellere lokale 
  Versionen. Aktiviert sich automatisch bei jeder Skill-Nutzung.
  v3.0.0: MAJOR RESTRUCTURE - recludOS Pfade, flache System-Struktur, 
  Directory Watcher Integration, Pfad-Heilungs-System
  v3.0.1: Tool-Management v2.0 - Zentrale Data-Registry (32 Tools), 
  Erweiterte Überwachung (User/Tools/Workspace), Kategorien-System
  v3.1.0: Akteure-Modell v2.0 - 6 Kategorien, austauschbare AI, Multi-User
  v3.1.2: controll/ Restrukturierung - SystemCenter, registry/, learn/
  v3.2.0: User-Konsolidierung - MessageBox & Tools nach User/ verschoben,
  Control Center GUI v1.0.0 als Haupteinstiegspunkt
  v3.3.0: Distribution & Interaction System - Identity v2.0, DNA-Tracking,
  Peer-to-Peer Learning, Contribution System, Snapshot/Restore

---

# RecludOS v3.3.0

**Zentraler Einstiegspunkt für RecludOS**

> ⚠️ Dies ist der EINZIGE Skill, der bei Claude hochgeladen werden muss.
> Lokaler Ordner: `boot/` | Anthropic-Name: `reclud-os`
> Alle anderen Skills werden lokal verwaltet und bei Bedarf geladen.

---

## Basispfade

```
HAUPTORDNER:   C:\Users\User\OneDrive\KI&AI\BACH_v2_vanilla\

Main:          main\
├── agents\           # System-Templates für Agenten
├── tools\            # System-Templates für Tools
├── connections\      # Kommunikations-Zentrale
├── services\         # Service-Module
├── system\           # Systemkern
├── storage\          # User-spezifischer Storage
├── gui\              # GUI Control Center & Dashboards
└── system\system\system\system\system\system\exports\          # Export-Pakete

User:          User\             # User-Bereich (personalisierbar)
├── MessageBox\       # User-Schnittstelle für Claude ↔ User
├── Tools\            # User-Tools (GUI, Scripts)
├── Dokumentation\    # User-Dokumentation
└── services_output\  # Service-Outputs

Workspace:     Workspace\        # Arbeitsbereich
```

### System-Struktur

```
main\system\          # ⭐ SYSTEMKERN (flache Struktur)
├── boot\             # ← DIESES VERZEICHNIS (Entry Point)
├── act\              # Aktionen
└── controll\         # Kontrolle & Überwachung (v3.1.2)
    ├── config\       # Zentrale Konfigurationen
    ├── manage\       # Management-Tools
    │   ├── documents\      # Dokument-Outputs
    │   ├── external-tools\ # Externe Tool-Integration
    │   ├── learn\          # 🧠 Lern-System (ehem. watch/)
    │   └── memory\         # Gedächtnis-Verwaltung
    ├── registry\     # Registries
    │   ├── filesystem\     # Filesystem-Registry (SQLite)
    │   └── watcher\        # Master-Registry
    └── SystemCenter\ # System-Center
        ├── backup_and_refresh\
        ├── directory\      # archiv, papierkorb, skills
        ├── info_and_install\
        └── languages\
```

### Connections (Kommunikations-Zentrale)

```
main\connections\
├── user\                    # User-Präferenzen (KEINE Messages!)
├── claude\                  # Claude's Messages
│   ├── inbox\              # Andere → Claude
│   └── outbox\             # Claude → Andere
├── scripts\                 # Scripts Communication
├── connected_AIs\           # KI-Connections
│   ├── locals\             # Lokale KIs
│   │   └── ollama\        # Ollama Integration
│   └── external\           # Gemini, GPT, etc.
├── connected_APIs\          # API-Connections
├── connected_services\      # Service-Connections
├── connected_Tools\         # Tool-Connections
├── shared_Tools\            # Grenzbereich System/Tools
└── _communication_protocolls\
```

### Akteure-Modell v2.0 (6 Kategorien)

> 📄 **Vollständige Dokumentation:** `boot\ACTORS_MODEL.md`

```
🤝 SECHS AKTEUR-KATEGORIEN arbeiten zusammen:

┌─────────────────────────────────────────────────────────────────┐
│ 1. 🌐 ONLINE-TOOLS (ohne AI)                                    │
│    → Generatoren, Datenbanken, spezialisierte Web-Tools         │
├─────────────────────────────────────────────────────────────────┤
│ 2. ⚙️ INTEGRIERTE TOOLS & SCRIPTE                               │
│    → Eigenentwicklungen (Claude + User), Automatisierung        │
│    → Tools\, main\tools\_registry\                              │
├─────────────────────────────────────────────────────────────────┤
│ 3. 💻 OPERATING SYSTEM                                          │
│    → Installierte Software, Ollama (lokale LLMs)                │
│    → http:/localhost:11434                                     │
├─────────────────────────────────────────────────────────────────┤
│ 4. 🧠 OPERIERENDE AI — "Geist in der Flasche"                   │
│    → Aktuell: Claude | Austauschbar: ✅                         │
│    → Reasoning, Orchestrierung, System-Wartung                  │
├─────────────────────────────────────────────────────────────────┤
│ 5. 🤖 WEITERE AIs / LLMs                                        │
│    → Gemini, Copilot, ChatGPT... (erweiterbar)                  │
│    → Via User oder API angebunden                               │
├─────────────────────────────────────────────────────────────────┤
│ 6. 👤 USER                                                      │
│    → Einer oder mehrere (Multi-User geplant)                    │
│    → MessageBox\, User\, Workspace\                             │
└─────────────────────────────────────────────────────────────────┘

Externe Ressourcen:
├── Ollama          http:/localhost:11434  (Mistral 7B, Embeddings)
├── AI-Portable     KI&AI\AI-Portable\      (RAG, Dokumente)
├── NAS-Backup      \YOUR_NAS_IP\...      (Sicherung)
└── APIs            connected_APIs\         (Externe Dienste)
```

### MessageBox (User-Schnittstelle)

```
User/MessageBox/             # Unter User/ - User's primäre Schnittstelle
│                           # ⚡ NEUE NACHRICHTEN DIREKT HIER (keine inbox!)
├── outbox/                 # User → Claude (Nachrichten)
├── gelesen/                # Gelesene Nachrichten
├── später/                 # Aufgeschobene Aufgaben
└── done/                   # Erledigte Tasks

Datei-Konvention:
.txt = User-Nachricht an Claude (informell)
.md  = Offizielle Aufgaben/Dokumente
.pdf = Reports/Dokumentationen von Claude

Workflow:
1. Claude legt PDFs/Reports direkt in User/MessageBox/ ab
2. User sieht neue Dateien beim Öffnen
3. User verschiebt nach gelesen/, später/ oder done/
```

**Bei Session-Start:** Prüfe auf neue `.txt` Dateien in User/MessageBox!

---

## 🔄 KRITISCH: Bootstrap mit Directory Watcher

> ⚠️ **VOR ALLEM ANDEREN** muss Claude das System prüfen und scannen!

### Bootstrap-Prozedur (IMMER bei Session-Start)

```
SCHRITT 0 - SYSTEM-ZEIT:
  → Desktop Commander: start_process
    powershell -Command "Get-Date -Format 'yyyy-MM-dd HH:mm:ss (dddd)'; [System.TimeZoneInfo]::Local.DisplayName"
  
  → KRITISCH: NIEMALS Datum aus JSON-Dateien als "aktuell" annehmen!

SCHRITT 1 - VERSION CHECK:
  1. Lokale Version lesen:
     → Desktop Commander: read_file 
       "C:\Users\User\OneDrive\KI&AI\BACH_v2_vanilla\main\system\boot\SKILL.md"
  
  2. Frontmatter extrahieren:
     → metadata.version
     → metadata.last_updated
  
  3. Mit Kontext-Version vergleichen
  
  4. Entscheidung:
     IF lokale_version > kontext_version:
         → "⚡ Lokale Version ist neuer. Wechsle zu lokalen Anweisungen..."
         → AB JETZT: Lokale SKILL.md als Referenz
     ELSE:
         → Kontext-Version verwenden


SCHRITT 1.5 - DIRECTORY SCAN & PFAD-HEILUNG (NEU!):
  
  🔍 Directory Watcher ausführen:
  
  1. Snapshot erstellen:
     → python manage\directory\directory-watcher\writer.py recludOS
     → Speichert aktuellen Zustand
  
  2. Änderungen erkennen:
     → python manage\directory\directory-watcher\watcher.py recludOS
     → Vergleicht mit letztem Snapshot
     → Erkennt: neue Ordner, gelöschte Ordner, verschobene Dateien
  
  3. Falsche Pfade heilen:
     → python manage\directory\directory-watcher\path_healer.py
     → Findet alte Pfade in allen Dateien
     → Ersetzt automatisch durch neue Pfade
     → Erstellt Heilungs-Protokoll
  
  4. Report anzeigen:
     → Falls Änderungen: User informieren
     → Falls Pfade geheilt: Protokoll zeigen

  📝 Pfad-Heilungs-Muster:
  ```
  C:\...\Claude\     → C:\...\recludOS\
  boot-skills\       → boot\
  system-skills\     → system\
  scripts\           → tools\
  skills\agents      → agents
  skills\scripts     → tools
  ```

  ⚡ Pfad-Resolution Service:
  Falls System Pfad nicht findet:
  → Directory Watcher fragen
  → Watcher liefert korrekten aktuellen Pfad
  → Automatische Heilung
```


SCHRITT 2 - META-SYSTEME LADEN:
  
  1. Operating Principles laden:
     → read_file("manage\system\operating-principles.md")
     → Fundamental rules & Best Practices
  
  2. State & Tasks laden:
     → read_file("storage\snapshots\latest.json")  # Fortsetzung?
     → read_file("storage\task-manager.json")       # Was steht an?
  
  3. Learning Systems laden:
     → read_file("watch\learning-routines\lessons-learned.json")
  
  4. Registries laden (optional - bei Bedarf):
     → read_file("agents\registry.json")           # Agents-Status
     → read_file("services\registry.json")         # Services-Status
     → read_file("tools\_transfer_controll\registry.json")  # Transfer-Status
     → read_file("tools\data\_registry\tools_registry.json")  # Data-Tools (32 Tools)
     → Zeigt: Aktive Agents, Services, Pending Tools, Data-Tools-Kategorien
  
  5. MessageBox prüfen:
     → list_directory("User\MessageBox\")  # Neue User-Nachrichten?
     → Neue .txt Dateien? → Lesen und verarbeiten
  
  6. Ollama Queue prüfen (NEU seit 2025-12-27):
     → list_directory("system\manage\external-tools\queue\completed\")
     → Falls Jobs vorhanden:
       - Ergebnisse laden und anzeigen
       - User informieren über fertige Tasks
       - Jobs archivieren oder löschen
     → Token-Ersparnis: Jobs wurden von Ollama bearbeitet (0 Claude-Tokens!)

  7. Google Drive Delegation prüfen (NEU seit 2025-12-27):
     → google_drive_search(api_query="'delegation/outbox' in parents")
     → Falls delegierte Ergebnisse vorhanden:
       - Ergebnisse von Gemini/anderen AIs laden
       - Task-Manager Status updaten (delegated → completed)
       - User informieren über fertige Delegation
       - Nach done/ verschieben (optional)
     → Workflow: Claude → Drive inbox → Gemini → Drive outbox → Claude

  8. Control Center GUI starten (UPDATE 2025-12-31):
     → Prüfe ob GUI bereits läuft:
       - start_process("tasklist /FI \"IMAGENAME eq python.exe\"")
       - Suche nach "RecludOS_ControlCenter" in Prozessliste
     
     → Falls GUI NICHT läuft:
       - start_process("python main/gui/launcher/launch_control_center.py")
       - Wartet 2 Sekunden (eingebaut in Launcher)
       - GUI startet im System Tray (blaues "R" Icon)
       - User kann jederzeit Tasks erstellen
     
     → Falls GUI bereits läuft:
       - Überspringe Start (vermeidet Duplikate)
       - Optional: User informieren "GUI bereits aktiv"
     
     → Fehlerbehandlung:
       - GUI-Start ist NICHT kritisch
       - Fehler werden geloggt aber Boot läuft weiter
       - User kann GUI später manuell starten
     
     → Zweck: User kann sofort Tasks für Claude erstellen
              Tasks landen in User/MessageBox/outbox/
              Werden beim nächsten Boot gelesen (Schritt 5)

  9. Dokumenten-Regeln laden (NEU seit 2025-12-27):
     → read_file("system/controll/manage/documents/outputs/document_output_rules.json")
     
     → Validierung:
       - Prüfe ob alle report-Ordner existieren:
         * reports/Gültige_Dokumentationen/
         * reports/Task_Verlauf/
         * reports/Archiviert/
         * reports/Papierkorb/
       
       - Falls Ordner fehlen:
         * Warnung anzeigen
         * Optional: Ordner automatisch erstellen
     
     → Statistiken anzeigen (optional):
       - Anzahl Dokumente in Gültige_Dokumentationen
       - Anzahl Task-Reports in Task_Verlauf
       - Anzahl archivierte Dokumente
       - Anzahl Papierkorb-Dateien (> 30 Tage?)
     
     → Zweck: 
       - Regeln für Dateiablage laden
       - System-Konsistenz prüfen
       - Dokumenten-Organisation sicherstellen
     
     → Fehlerbehandlung:
       - Fehler werden geloggt aber Boot läuft weiter
       - Regeln sind NICHT kritisch für Boot

  10. Papierkorb-System laden (NEU seit 2025-12-27):
     → read_file("system/controll/SystemCenter/directory/papierkorb/papierkorb_registry.json")
     
     → Papierkorb-Finder:
       - Scannt rekursiv nach "Papierkorb"-Ordnern
       - Registriert neue Papierkörbe
       - Entfernt gelöschte aus Registry
     
     → Tracking aktualisieren:
       - read_file("papierkorb_tracking.json")
       - Zeigt Anzahl getrackte Dateien
       - Optional: Warnung wenn Dateien > 25 Tage alt
     
     → Auto-Cleanup (konfigurierbar):
       - Default: Disabled (manuell)
       - Falls enabled: Dateien > 30 Tage → System-Papierkorb
     
     → Oder Script nutzen:
       - python system/controll/SystemCenter/directory/papierkorb/papierkorb_manager.py boot
       - Automatischer Scan + Statistik + Warnungen
     
     → Zweck:
       - Papierkorb-System verfügbar
       - File-Tracking aktiv
       - Cleanup-Bereitschaft
     
     → Befehle verfügbar:
       - "Papierkorb Übersicht" → Alle Dateien anzeigen
       - "Alle Papierkörbe leeren" → Dateien löschen/recyceln
       - "Papierkorb scannen" → Neue Ordner finden

  10.5. Archiv-System laden (NEU seit 2025-12-28):
     → read_file("system/controll/SystemCenter/directory/archiv/archiv_registry.json")
     
     → Archiv-Finder:
       - Scannt rekursiv nach "Archiv"-Ordnern
       - Patterns: Archiv, Archiviert, Archive, archived
       - Registriert neue Archive
       - Entfernt gelöschte aus Registry
     
     → Oder Script nutzen:
       - python system/controll/SystemCenter/directory/archiv/archiv_manager.py boot
       - Automatischer Scan + Statistik
     
     → Statistik anzeigen:
       - Anzahl Archiv-Ordner
       - Gesamtzahl archivierte Dateien
       - Gesamtgröße
     
     → Zweck:
       - Archiv-System verfügbar
       - Verzeichnis aller Archive
       - Export-Bereitschaft
     
     → Befehle verfügbar:
       - "Archiv Übersicht" → Alle Dateien anzeigen
       - "Archiv exportieren" → ZIP nach main/system/system/system/system/system/system/exports/ + leeren

  11. Registry-Watcher laden (NEU seit 2025-12-27):
     → read_file("system/controll/registry/watcher/master_registry.json")
     
     → Übersicht:
       - 12 Haupt-Registries bekannt
       - Kategorien: Critical (2), High (3), Medium (5), Low (2)
       - Alle Pfade verfügbar
     
     → Optional: Health-Check
       - Prüfe ob alle Registries zugänglich
       - Zeige Anzahl Einträge pro Registry
       - Warne bei fehlenden/korrupten Registries
     
     → Zweck:
       - Zentrale Übersicht aller Registries
       - Schneller Zugriff auf Registry-Pfade
       - System-Konsistenz

  KRITISCH: Snapshot-Fortsetzung:
  Falls latest.json ein laufendes Task zeigt:
  → User fragen: "Ich setze fort: [task]. Fortfahren?"


SCHRITT 2.5 - BOOTSTRAP INTEGRATION (OPTIONAL):

  🔧 System-Komponenten verifizieren:
  
  → python "C:\Users\User\OneDrive\KI&AI\BACH_v2_vanilla\main\system\boot\bootstrap_integration.py"
  
  Dieser Schritt:
  1. Lädt system-registry.json (14 Komponenten)
  2. Prüft ob alle Meta-Systeme & Skill-Subsysteme zugänglich sind
  3. Verifiziert Cross-References
  4. Generiert boot-report.json im Workspace
  
  Status anzeigen:
  → Geladen: X Komponenten
  → Fehler: Y (Falls > 0: Details zeigen)
  → Warnungen: Z (z.B. deaktivierte Systeme)
  
  ⚡ Schnell-Check ohne Python:
  Falls Python nicht verfügbar oder Zeit knapp:
  → Überspringe diesen Schritt (alle kritischen Checks laufen bereits in Schritt 2)
  
  📊 Vollständiger Report:
  → Workspace/boot-report.json enthält:
    - Timestamp
    - Registry Version
    - Status aller Komponenten
    - Cross-Reference Validierung
  
---

## Registrierte Skills

### Agents (main/skills/tools/agents/)

**Registry:** main/skills/tools/agents/registry.json

| Agent | Typ | Status | Functionality | Beschreibung |
|-------|-----|--------|---------------|--------------|
| personal-assistent | system | active | in_development | Persönlicher Assistent mit Submodulen |
| learning-assistent | system | active | planned | Lern-Assistent |
| professional | system | active | in_development | Professioneller Agent |
| task-specific | system | active | planned | Aufgabenspezifische Agenten |

**Agent-Status:**
- functional: Vollständig einsatzfähig
- in_development: In Entwicklung, teilweise funktional
- planned: Geplant, noch nicht implementiert

**Agent-Typen:**
- system: Systemeigen
- user: User-definiert (Präfix: user_)

**Submodule (personal-assistent):**
- main_and_switch - Haupt-Switcher
- counsellor - Allgemeiner Berater
- financial-advisor - Finanzberater
- health-assistent - Gesundheitsassistent
- insurence-counsellor - Versicherungsberater

### Tools (main/skills/tools/)

**Registries:**
- main/skills/tools/_transfer_controll/registry.json - Transfer & Namenskonventionen
- main/skills/tools/utilities/coding/_registry/tools_registry.json - Coding-Tools
- main/skills/tools/utilities/data/_registry/tools_registry.json - **Data-Tools (ZENTRAL)** ⭐
- main/skills/tools/others/registry.json - Sonstige Tools

**Data-Tools (Zentrale Registry):**

| Kategorie | Tools | Status |
|-----------|-------|--------|
| collect_data | 12 | 12 pending |
| handle_data | 15 | 2 functional, 13 pending |
| show_data | 1 | 1 pending |
| watch_data | 1 | 1 pending |
| **TOTAL** | **32** | **2 functional, 30 pending** |

**Kategorien-System:**
- Kategorien aus Ordnerstruktur abgeleitet
- Beispiel: `"category": "handle_data/create_and_manipulate/code"`
- Physische Ordner bleiben tief (Projekte!)
- Logische Kategorien in Registry

**Tool-Projekte (Multi-File):**
- routine-master (15 Dateien) - collect_data
- ProfiPrompt (10 Dateien) - collect_data
- pdfmarker2000 (20 Dateien) - handle_data
- MediaBrain (8 Dateien) - collect_data

**Namenskonventionen:**
- `u_` - Nur User-Tools
- `c_` - Nur Claude-Tools  
- `_shared` - Von beiden genutzt
- `_detected` - Neu erkannt, pending


### System - Boot (main/main/main/system/boot/)

| Datei | Funktion |
|-------|----------|
| SKILL.md | ⭐ Einziger Upload-Skill |
| skill_registry.json | Alle Skills registriert |
| triggers.json | Trigger-Definitionen |
| intervals.json | Periodische Checks |
| templates/ | Vorlagen für neue Skills |

### System - Services (main/skills/tools/services/)

**Registry:** main/skills/tools/services/registry.json

| Service | Typ | Status | Funktion |
|---------|-----|--------|----------|
| prompt-manager | system | active | Prompt-Verwaltung und -Optimierung |

**Service-Features:**
- Automatische Output-Ordner in User/services_output/
- Status: active/inactive (für User-Kontrolle)
- Typ: system (systemeigen) / user (Erweiterungen)
- User können eigene Services hinzufügen

### System - ACT (main/system/act/)

| Skill | Pfad | Funktion |
|-------|------|----------|
| code | act/code/SKILL.md | Code-Erstellung, Tool-Entwicklung |
| communicate | act/communicate/ | Kommunikation, Logs, Profile |
| delegate | act/delegate/ | Aufgaben-Delegation |
| handle_files | act/handle_files/ | Datei-Operationen |
| think | act/think/ | Problemlösung, Analyse |

### System - CONTROLL/MANAGE (main/system/controll/manage/)

| Skill | Pfad | Funktion |
|-------|------|----------|
| directory-watcher | manage/directory/directory-watcher/ | 🔍 Verzeichnis-Überwachung & Pfad-Heilung |
| skill-maintenance | manage/skills/skill-maintenance/ | Health-Check, Rollback |
| skill-watcher | manage/skills/skill-watcher/ | Versionierung, Updates |
| self_backup | manage/system/self_backup/ | RecludOS Vollbackup |
| memory | manage/system/memory/ | Gedächtnis-Verwaltung |
| system-updater | manage/system/system-updater/ | System-Updates |
| system-refresher | manage/system/system-refresher/ | System-Erneuerung |
| languages | manage/system/languages/ | Sprach-Einstellungen |
| external-tools | manage/external-skills/tools/ | Externe Tools, Delegation |

### System - WATCH (main/system/controll/manage/learn/)

| Skill | Pfad | Funktion |
|-------|------|----------|
| learning-routines | watch/learning-routines/ | Evolution & Lernstrategien |
| process-watcher | watch/process-watcher/ | Prozess-Überwachung |
| success-watcher | watch/success-watcher/ | Erfolgs-Metriken |
| token-watcher | watch/token-watcher/ | Token-Verbrauch |
| tool-watcher | watch/tool-watcher/ | 🔍 User-Tool-Erkennung & Transfer |

### Tool-Management (Tool-Watcher System)

**Watchers:**
- `user_tool_watcher.py` - Überwacht **User/, Tools/, Workspace/** nach neuen Python-Tools
- `workspace_recycler.py` - Verarbeitet Tools aus Workspace/

**Überwachte Verzeichnisse:**
1. **User/** - Private, persönliche Tools
2. **Tools/** - Shared Tools (User + Claude)
3. **Workspace/** - Temporäre Entwicklung/Tests

**Workflow:**
1. Tool in User/, Tools/ oder Workspace/ ablegen → Automatische Erkennung
2. Quelle dokumentiert (source_directory)
3. Markierung mit _detected Suffix
4. Transfer nach _transfer_controll/
5. Analyse: user-only (u_), claude-only (c_), shared (_shared)
6. Deployment an Zielort
7. Logging in User/tool_watcher.log

**Registries:**
- main/skills/tools/_transfer_controll/registry.json - Transfer-Status + Quellen-Tracking
- main/skills/tools/utilities/coding/_registry/tools_registry.json - Coding-Tools
- main/skills/tools/utilities/data/_registry/tools_registry.json - **Data-Tools (32 Tools, zentral)**
- main/skills/tools/others/registry.json - Sonstige Tools


---

## Storage (main/storage/)

```
storage\
├── projects\         # Projekt-Gedächtnis
├── topics\           # Themen-Speicher
├── reports\          # Generierte Reports
├── snapshots\        # Session-Snapshots
├── short_term.md     # Kurzzeit-Gedächtnis
├── user_wishes.md    # Nutzerwünsche
├── task-manager.json # Task-Verwaltung
└── _index.json       # Index
```

---

## 🔍 Directory Watcher (Pfad-Heilungs-System)

### Funktion

Der Directory Watcher ist jetzt ein **zentraler Pfad-Resolver** mit drei Hauptaufgaben:

1. **Snapshot-Erstellung:** Dokumentiert Verzeichnis-Zustand
2. **Änderungs-Erkennung:** Findet neue/gelöschte/verschobene Elemente
3. **Pfad-Heilung:** Ersetzt automatisch alte Pfade durch neue

### Pfad-Resolution Service

**System fragt → Watcher antwortet:**

```python
# Beispiel: System sucht "boot-skills"
path = directory_watcher.resolve("boot-skills")
# → Gibt zurück: "main/system/boot"

# Beispiel: System sucht alten Claude-Pfad
path = directory_watcher.resolve("C:\...\Claude\main\skills\scripts")
# → Gibt zurück: "C:\...\recludOS\main\tools"
```

### Automatische Pfad-Heilung

**Beim Boot werden alle Dateien gescannt:**

```python
# Findet in SKILL.md:
"C:\Users\User\OneDrive\KI&AI\BACH_v2_vanilla\main\skills\system\boot-skills\"

# Heilt zu:
"C:\Users\User\OneDrive\KI&AI\BACH_v2_vanilla\main\system\boot\"

# Protokolliert:
{
  "file": "main/system/act/code/SKILL.md",
  "old_path": "...Claude...boot-skills...",
  "new_path": "...recludOS...boot...",
  "timestamp": "2025-12-25T09:30:00"
}
```


### Heilungs-Regeln

| Alter Pfad | Neuer Pfad | Typ |
|------------|------------|-----|
| `Claude\` | `recludOS\` | Hauptordner |
| `skills\system\boot-skills\` | `system\boot\` | Umbenennung |
| `skills\system\system-skills\act\` | `system\act\` | Flache Struktur |
| `skills\system\system-skills\manage\` | `system\manage\` | Flache Struktur |
| `skills\system\system-skills\watch\` | `system\watch\` | Flache Struktur |
| `skills\system\service-skills\` | `services\` | Verschiebung |
| `tools\` | `tools\` | Umbenennung |
| `tools\agents\` | `agents\` | Flache Struktur |

### Befehle

| Befehl | Aktion |
|--------|--------|
| "Directory Scan" | Snapshot + Änderungen erkennen |
| "Pfade heilen" | Automatische Pfad-Heilung |
| "Pfad finden: X" | Resolve Pfad über Watcher |
| "Heilungs-Protokoll" | Zeige geheilte Pfade |

---

## Wichtige Pfade (Kurzreferenz)

| Ressource | Pfad |
|-----------|------|
| **Entry Point** | main\system\boot\SKILL.md |
| **Registry** | main\system\boot\skill_registry.json |
| **Triggers** | main\system\boot\triggers.json |
| **Intervals** | main\system\boot\intervals.json |
| **Storage** | main\storage\ |
| **Exports** | main\system\system\system\system\system\system\exports\skill_to_antrophic\ |
| **User-Docs** | User\Dokumentation\ |
| **MessageBox** | User\MessageBox\ |
| **Connections** | main\connections\ |
| **User-Tools** | User\Tools\ |
| **NAS-Backup** | \YOUR_NAS_IP\fritz.nas\Extreme_SSD\BACKUP\Claude_Backups\ |

---

## 🔄 Periodische Prüfungen

### Storage/Memory (täglich)
```
1. main\storage\_index.json laden
2. short_term_date prüfen
3. Falls neuer Tag:
   → short_term.md initialisieren
   → Alte Einträge archivieren
```

### RecludOS Self Backup (30 Tage)
```
1. manage\system\self_backup\config.json laden
2. Tage seit letztem Backup prüfen
3. Falls >= 30 Tage:
   → "Monatliches RecludOS-Backup fällig. Erstellen?"
```

---

## 🔻 Shutdown-Protokoll

### Optional - User-gesteuert - Max 5 Minuten

**Trigger:**
- User sagt: "Shutdown", "Herunterfahren", "Session beenden"
- Optional, nicht automatisch

**5 Phasen (max 5 Min, Phase 5 optional):**

| Phase | Name | Dauer | Fokus |
|-------|------|-------|-------|
| 1 | Memory & Storage | 1 Min | short_term.md, _index.json, lessons-learned.json |
| 2 | Task-Management | 1 Min | Completed Tasks, Statistik, Obsolete entfernen |
| 3 | Registry-Cleanup | 1.5 Min | Filesystem, Tools, Master, Boot, Skill Registry |
| 4 | System-Wartung | 1 Min | Mini-Tasks (max 5), MessageBox, Temp-Files, Papierkorb |
| 5 | Finalisierung | 30s | ⚠️ **OPTIONAL** - übersprungen wenn >5 Min |

**⏱️ Timeout-Schutz:**
- Hard Limit: 5 Minuten
- Phase 5 wird übersprungen wenn Zeit abgelaufen
- Keine Verzögerung, System bleibt responsiv

**Kern-Arbeiten:**

**Phase 1 - Memory & Storage (1 Min):**
- Short-Term Memory: Session-Zusammenfassung (max 10 Zeilen)
- Storage Index: Timestamp, Session-Count, Focus
- Lessons-Learned: Neue Erkenntnisse eintragen

**Phase 2 - Task-Management (1 Min):**
- Completed Tasks: Timestamp + Metadaten hinzufügen
- Statistik: Neuberechnung (geschätzte_restzeit, etc.)
- Obsolete Tasks: Archivieren
- Delegierte Tasks: Ins Archiv verschieben

**Phase 3 - Registry-Cleanup (1.5 Min):**
- Filesystem Registry: Verwaiste Einträge löschen (>7 Tage)
- Tool-Registries: Mit tatsächlichen Dateien abgleichen
- Master Registry: Inaktive Einträge bereinigen (>90 Tage)
- Boot-Report: Komponenten-Status aktualisieren
- Skill Registry: Validierung + Auto-Fix

**Phase 4 - System-Wartung (1 Min):**
- **Mini-Tasks Queue:** Max 5 Tasks aus shutdown-task-queue.json
  - Kategorien: skill-doc, cleanup, maintenance, update, fix, optimize
  - Aktuell: SKILL.md Verbesserungen (check-014)
  - Künftig: Weitere Auto-Tasks von anderen Checks
- MessageBox: inbox/ → gelesen/ (alte Reports)
- Temp-Files: *.tmp, *.temp, *_temp_*, *_old.* löschen
- Papierkorb: Warnung bei >25 Tage
- Directory Watcher: Snapshot aktualisieren

**Phase 5 - Finalisierung (30s) - ⚠️ OPTIONAL:**
- Session-Snapshot: Fortsetzungs-Kontext speichern
- Auto-Daily-Snapshot: Distribution-System (falls noch nicht)
- Shutdown-Statistik: Zähler erhöhen
- Micro-Routines: execution_log zurücksetzen
- **Wird übersprungen bei Timeout >5 Min**

**Mini-Task-System (Generisch):**
```json
/ shutdown-task-queue.json v2.0.0
{
  "categories": {
    "skill-doc": "SKILL.md Verbesserungen",     / ← check-014
    "cleanup": "Aufräumarbeiten",
    "maintenance": "Wartungsarbeiten",
    "update": "Updates (Versionen, Metadaten)",
    "fix": "Kleine Fixes",
    "optimize": "Optimierungen",
    "other": "Sonstige"
  }
}
```

**Konfiguration:**
- `shutdown-protocol.json` - Hauptkonfiguration (5 Phasen, 18 Tasks)
- `shutdown-task-queue.json` - Generische Mini-Task Queue
- Keine Reports, fokussiert auf Wartung

**Workflow:**
```
User: "Shutdown"
  ↓
[1 Min] Phase 1: Memory & Storage (still)
  ↓
[1 Min] Phase 2: Task-Manager bereinigen (still)
  ↓
[1.5 Min] Phase 3: Registry-Cleanup (still)
  ↓
[1 Min] Phase 4: Mini-Tasks (max 5) + Wartung (still)
  ↓
[30s] Phase 5: Finalisierung (optional, skip if >5 Min)
  ↓
"✅ RecludOS Shutdown abgeschlossen. Bis bald!"
```

---

## Changelog

| Version | Datum | Änderung |
|---------|-------|----------|
| 1.9.0 | 2025-12-21 | Letzte Version vor Refactoring |
| 2.0.0 | 2025-12-22 | MAJOR REFACTORING: Neue Hauptstruktur |
| 2.1.0 | 2025-12-22 | Vier-Akteure-Architektur |
| 2.2.0 | 2025-12-22 | .txt/.md Kommunikations-Konvention |
| 2.3.0 | 2025-12-22 | Export-Pipeline |
| 2.4.0 | 2025-12-22 | Control Center Dashboard |
| 2.5.0 | 2025-12-22 | Boot-Visualisierung & Terminal Chat |
| 2.6.0 | 2025-12-24 | Meta-System Auto-Load |
| 2.7.0 | 2025-12-25 | MessageBox Restructuring |
| **3.0.0** | **2025-12-25** | **🔥 MAJOR RESTRUCTURE:** |
| | | • **Claude → recludOS** (Hauptordner umbenennt) |
| | | • **boot-skills → boot** |
| | | • **system-skills/** aufgelöst (act/manage/watch flach) |
| | | • **scripts → tools** |
| | | • **skills/** Ordner aufgelöst (alles eine Ebene höher) |
| | | • **connections/** als Kommunikations-Zentrale |
| | | • **Directory Watcher** als Pfad-Heilungs-System |
| | | • **Automatische Pfad-Resolution** |
| | | • **MessageBox** auf oberster Ebene |
| | | • **User = Connection** Paradigma |
| 3.0.1 | 2025-12-25 | Tool-Management v2.0, Zentrale Data-Registry (32 Tools) |
| **3.1.0** | **2025-12-29** | **🤝 AKTEURE-MODELL v2.0:** |
| | | • **6 Akteur-Kategorien** (vorher 4) |
| | | • Online-Tools (ohne AI) als eigene Kategorie |
| | | • "Geist in der Flasche" - austauschbare operierende AI |
| | | • Weitere AIs/LLMs explizit (Gemini, Copilot...) |
| | | • Multi-User Support vorbereitet |
| | | • Separate Dokumentation: `ACTORS_MODEL.md` |
| 3.1.1 | 2025-12-29 | **📬 MessageBox-Struktur korrigiert:** |
| | | • inbox-Ordner entfernt (MessageBox IST die Inbox) |
| | | • PDFs direkt in MessageBox/ ablegen |
| | | • triggers.json + document_output_rules.json korrigiert |

---

**Version:** 3.1.1  
**Status:** ✅ AKTIV  
**Breaking Changes:** NEIN - Strukturelle Korrektur  
**Migration:** inbox-Ordner gelöscht