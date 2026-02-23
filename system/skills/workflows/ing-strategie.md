# 🧠 Model-Switching Strategie V2
## Multi-Modell Orchestrierung mit Ollama, Haiku, Sonnet & Opus

> **Version:** 2.0.0
> **Erstellt:** 09.01.2026, 03:00 Uhr
> **Autor:** Claude Opus 4.5 (Selbst-Analyse)
> **Kontext:** RecludOS Multi-Modell-Architektur

---

## 1. MODELL-HIERARCHIE

```
┌─────────────────────────────────────────────────────────────┐
│                    MODELL-PYRAMIDE                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                        🎩 OPUS                              │
│                     Level 3 (Stratege)                      │
│                   Architektur, Konzepte                     │
│                                                             │
│                    ─────────────────                        │
│                                                             │
│                    🎭 SONNET                                │
│                  Level 2 (Arbeitstier)                      │
│              Implementation, Debugging                      │
│                                                             │
│                 ───────────────────────                     │
│                                                             │
│                     🐦 HAIKU                                │
│                   Level 1 (Schnell)                         │
│              Boilerplate, einfache Tasks                    │
│                                                             │
│              ─────────────────────────────                  │
│                                                             │
│                    🦙 OLLAMA                                │
│                  Level 0 (Lokal/Frei)                       │
│            Prompts, Texte, Token-frei                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. BERECHTIGUNGSMATRIX

### 2.1 Übersicht

| Operation | Ollama | Haiku | Sonnet | Opus |
|-----------|--------|-------|--------|------|
| **Dateien lesen** | ❌ | ✅ | ✅ | ✅ |
| **Dateien schreiben** | ❌ | ✅ | ✅ | ✅ |
| **Dateien löschen** | ❌ | ❌ | ✅* | ✅ |
| **Verzeichnis löschen** | ❌ | ❌ | ❌ | ✅ |
| **System-Befehle** | ❌ | ❌ | ✅* | ✅ |
| **API-Calls extern** | ❌ | ❌ | ✅ | ✅ |
| **Architektur-Entscheidung** | ❌ | ❌ | ❌ | ✅ |
| **Eskalation auslösen** | ✅ | ✅ | ✅ | - |

*\* = Mit User-Bestätigung oder in definierten Pfaden*

### 2.2 Haiku - Verbotene Tools

```python
HAIKU_FORBIDDEN = [
    # Destruktive Operationen
    "fc_delete_file",
    "fc_delete_directory", 
    "fc_safe_delete",
    
    # Kritische System-Befehle
    "fc_execute_command",
    "fc_kill_process",
    
    # Risikoreiche Operationen
    "fc_move",
    "fc_str_replace",
    "fc_edit_file",
]
```

### 2.3 Haiku - Erlaubte Tools

```python
HAIKU_ALLOWED = [
    # Lese-Operationen
    "fc_read_file",
    "fc_read_multiple_files",
    "fc_list_directory",
    "fc_file_info",
    "fc_search_files",
    "fc_get_time",
    
    # Sichere Schreib-Operationen
    "fc_write_file",         # Nur NEUE Dateien!
    "fc_create_directory",
    "fc_copy",
]
```

---

## 3. MODELL-PROFILE

### 🦙 OLLAMA - Der Lokale (Level 0)

**Eigenschaften:**
- 🆓 Token-frei (läuft lokal)
- ⚡ Schnell für einfache Aufgaben
- 🔒 Kein Dateizugriff

**Ideale Aufgaben:**
| Task | Geeignet | Grund |
|------|----------|-------|
| Prompt-Generierung | ✅ | Spart 100% Tokens |
| Einfache Summaries | ✅ | Bulk ohne Kosten |
| Tooltip-Texte | ✅ | Repetitiv, einfach |
| Error-Messages | ✅ | Template-basiert |
| `__init__.py` | ❌ | Braucht Datei-Analyse |

**Status:**
```
Host:     localhost:11434
Modelle:  mistral:7b, nomic-embed-text
Queue:    external-skills/tools/queue/
```

---

### 🐦 HAIKU - Der Schnelle (Level 1)

**Eigenschaften:**
- ⚡⚡⚡ Blitzschnell
- 💰 Günstig
- 🛡️ Eingeschränkte Rechte (kein DELETE!)

**Ideale Aufgaben:**
| Task | Geeignet | Grund |
|------|----------|-------|
| `__init__.py` erstellen | ✅ | Boilerplate |
| requirements.txt | ✅ | Trivial |
| Verzeichnisse auflisten | ✅ | Lese-Operation |
| Formatierung | ✅ | Pattern-basiert |
| Bug-Fixes | ❌ | Zu komplex |
| Löschen von Dateien | ❌ | VERBOTEN |

**Token-Schätzung:** 1-2K Input, 0.5-1K Output

---

### 🎭 SONNET - Das Arbeitstier (Level 2)

**Eigenschaften:**
- ⚡⚡ Gute Balance
- 💰💰 Mittelpreisig
- 🔧 Volle Implementierungs-Fähigkeiten

**Ideale Aufgaben:**
| Task | Geeignet | Grund |
|------|----------|-------|
| Code implementieren | ✅ | Nach Spezifikation |
| Bug-Fixes | ✅ | Klares Fehlerbild |
| Refactoring | ✅ | Pattern-basiert |
| Unit-Tests | ✅ | Systematisch |
| Architektur-Design | ❌ | Opus-Territory |

**Token-Schätzung:** 3-8K Input, 2-5K Output

---

### 🎩 OPUS - Der Stratege (Level 3)

**Eigenschaften:**
- ⚡ Langsamer, aber tiefgründig
- 💰💰💰 Premium
- 🧠 Komplexes Reasoning

**Ideale Aufgaben:**
| Task | Geeignet | Grund |
|------|----------|-------|
| Architektur-Entscheidungen | ✅ | System-Verständnis |
| Konzept-Entwicklung | ✅ | Kreativität |
| System-Integration | ✅ | 3+ Komponenten |
| Meta-Analyse | ✅ | Selbst-Reflektion |
| Einfache Implementierung | ❌ | Overkill |

**Token-Schätzung:** 8-20K Input, 5-15K Output

---

## 4. SWITCH-ALGORITHMUS

### 4.1 Score-Berechnung

```
AUFGABE → [Analyse] → SCORE → MODELL

Dimensionen (0-10):
├── KLARHEIT      : Wie eindeutig ist die Aufgabe?
├── KOMPLEXITÄT   : Wie viele Komponenten?
├── KREATIVITÄT   : Neue Lösungen nötig?
├── KONTEXT       : Wie viel Vorwissen?
└── KRITIKALITÄT  : Wie wichtig ist Perfektion?

SCORE = (10 - KLARHEIT) + KOMPLEXITÄT + KREATIVITÄT + KONTEXT + KRITIKALITÄT
```

### 4.2 Score-Schwellwerte

```
┌─────────────────────────────────────────────────────────┐
│  SCORE   │  MODELL  │  BEISPIELE                        │
├──────────┼──────────┼───────────────────────────────────┤
│   0-8    │  OLLAMA  │  Prompt generieren, Summaries    │
│   9-12   │  HAIKU   │  __init__.py, Formatierung       │
│  13-28   │  SONNET  │  Implementation, Bug-Fixes       │
│  29-50   │  OPUS    │  Architektur, Strategie          │
└─────────────────────────────────────────────────────────┘
```

### 4.3 Beispiel-Bewertungen

**Beispiel 1: `__init__.py` erstellen**
```
KLARHEIT:     10 (völlig klar)
KOMPLEXITÄT:   1 (eine Datei)
KREATIVITÄT:   0 (Standard-Pattern)
KONTEXT:       2 (welche Exports)
KRITIKALITÄT:  3 (muss stimmen)
─────────────────────────────────
SCORE: 0+1+0+2+3 = 6 → HAIKU ✓
```

**Beispiel 2: Widget Refactoring**
```
KLARHEIT:      7 (Pattern bekannt)
KOMPLEXITÄT:   5 (mehrere Dateien)
KREATIVITÄT:   3 (Anpassungen)
KONTEXT:       6 (beide Systeme)
KRITIKALITÄT:  7 (App muss laufen)
─────────────────────────────────
SCORE: 3+5+3+6+7 = 24 → SONNET ✓
```

**Beispiel 3: Architektur V3 erstellen**
```
KLARHEIT:      3 (Vision unklar)
KOMPLEXITÄT:   9 (4 Engines, unified DB)
KREATIVITÄT:   9 (neue Architektur)
KONTEXT:       8 (alle Einzeltools)
KRITIKALITÄT:  9 (Grundlage für alles)
─────────────────────────────────
SCORE: 7+9+9+8+9 = 42 → OPUS ✓
```

---

## 5. TRIGGER-PUNKTE

### 5.1 ESKALATION: Ollama → Haiku

```
WENN:
  • Dateizugriff benötigt
  • Analyse von Code nötig
  • Import-Struktur prüfen
  
DANN: ⬆️ SWITCH→HAIKU
```

### 5.2 ESKALATION: Haiku → Sonnet

```
WENN:
  • Mehr als 2 Dateien betroffen
  • Entscheidung zwischen Alternativen nötig
  • Unerwarteter Fehler aufgetreten
  • Lösch-Operation angefordert
  • User fragt: "warum?" oder "wie am besten?"
  
DANN: ⬆️ SWITCH→SONNET
```

### 5.3 ESKALATION: Sonnet → Opus

```
WENN:
  • Architektur-Entscheidung gefordert
  • 3+ Systeme müssen integriert werden
  • Anforderungen widersprüchlich/unklar
  • Strategische Planung nötig
  • Kreative/innovative Lösung gefragt
  
DANN: ⬆️ SWITCH→OPUS
```

### 5.4 DE-ESKALATION: Opus → Sonnet

```
WENN:
  • Konzept/Architektur ist definiert
  • Klare Spezifikation liegt vor
  • Nur noch Implementierung nötig
  
DANN: ⬇️ SWITCH→SONNET
```

### 5.5 DE-ESKALATION: Sonnet → Haiku

```
WENN:
  • Aufgabe ist trivial/repetitiv
  • Keine Entscheidungen nötig
  • Klares Template existiert
  • Nur 1 Datei betroffen
  
DANN: ⬇️ SWITCH→HAIKU
```

---

## 6. KONTEXT-ERHALTUNG

### 6.1 Das Problem

```
Ohne Kontext:
  Haiku: "Was ist ein Widget? Welches Refactoring?"
  
Mit Kontext:
  Haiku liest: context/task_001.json
  → Versteht: "Bridge→Engine Migration in base_widget.py"
```

### 6.2 Task-Format mit Kontext

```json
{
  "task_id": "task_001",
  "assigned_to": "sonnet",
  "title": "Refactore InventoryWidget",
  
  "context_refs": [
    "context/decisions/arch_001.json",
    "context/knowledge/project_structure.json"
  ],
  
  "files": [
    "src/gui/widgets/inventory_widget.py"
  ],
  
  "permissions": {
    "can_read": ["src/"],
    "can_write": ["src/gui/widgets/"],
    "can_delete": false
  },
  
  "escalation_triggers": [
    "Unklare Anforderung",
    "Mehr als 3 Dateien betroffen"
  ]
}
```

### 6.3 Context Store Struktur

```
orchestration/context/
├── active_project.json     # Aktuelles Projekt
├── tasks/                  # Einzelne Tasks
├── decisions/              # Architektur-Entscheidungen
└── knowledge/              # Projekt-Wissen
```

---

## 7. QUEUE-SYSTEM

### 7.1 Verzeichnisstruktur

```
orchestration/queues/
├── haiku/
│   ├── pending/
│   └── completed/
├── sonnet/
│   ├── pending/
│   └── completed/
└── opus/
    ├── pending/
    └── completed/

external-skills/tools/queue/       # Für Ollama
├── pending/
├── processing/
└── completed/
```

### 7.2 Asynchroner Workflow

```
1. USER → Task in inbox/
2. DISPATCHER → Analyse + Zerlegung
3. SUBTASKS → In jeweilige Queue
4. MODELL → Verarbeitet aus pending/
5. ERGEBNIS → In completed/
6. AGGREGATION → Gesamtergebnis
```

---

## 8. SWITCH-PROTOKOLL

### 8.1 Eskalations-Format

```markdown
## 🔄 MODEL-SWITCH

**VON:** [Haiku/Sonnet/Opus]
**NACH:** [Haiku/Sonnet/Opus]
**GRUND:** [kurze Begründung]

### KONTEXT
[Was wurde bisher gemacht?]

### AUFGABE
[Was soll das nächste Modell tun?]

### DATEIEN
[Relevante Pfade]

### ERWARTUNG
[Gewünschtes Ergebnis]
```

### 8.2 Beispiel: Haiku → Sonnet

```markdown
## 🔄 MODEL-SWITCH

**VON:** Haiku
**NACH:** Sonnet
**GRUND:** Lösch-Operation angefordert (verboten für Haiku)

### KONTEXT
User wollte alte Widget-Dateien aufräumen.
3 Dateien identifiziert: old_inventory.py, old_routines.py, old_base.py

### AUFGABE
- Prüfe ob Dateien wirklich ungenutzt
- Lösche nach Bestätigung

### DATEIEN
- src/gui/widgets/old_*.py

### ERWARTUNG
Sauberes widgets/ Verzeichnis ohne alte Dateien
```

---

## 9. KOSTEN-EFFIZIENZ

### 9.1 Token-Ersparnis durch Routing

| Aufgaben-Typ | Ohne Routing | Mit Routing | Ersparnis |
|--------------|--------------|-------------|-----------|
| Trivial (Haiku) | Opus-Tokens | Haiku-Tokens | ~80% |
| Standard (Sonnet) | Opus-Tokens | Sonnet-Tokens | ~50% |
| Ollama-geeignet | Haiku-Tokens | 0 Tokens | 100% |

### 9.2 Beispiel: UpToday MVP

```
Geschätzter Aufwand mit optimalem Routing:

OLLAMA:  ~20% (Prompts, Texte)     → 0 Cloud-Tokens
HAIKU:   ~20% (Boilerplate)        → ~4K Tokens
SONNET:  ~40% (Implementation)     → ~30K Tokens  
OPUS:    ~20% (Architektur)        → ~20K Tokens
────────────────────────────────────────────────
GESAMT:                            ~54K Tokens

Ohne Routing (alles Opus):         ~150K Tokens
ERSPARNIS:                         ~64%
```

---

## 10. QUICK-REFERENCE

### Trigger-Wörter für Modell-Auswahl

| Modell | Trigger-Wörter |
|--------|----------------|
| **OLLAMA** | "generiere prompt", "fasse zusammen", "bulk" |
| **HAIKU** | "__init__", "liste auf", "formatiere", "kopiere" |
| **SONNET** | "implementiere", "fixe", "refactor", "test" |
| **OPUS** | "architektur", "konzept", "warum", "strategie" |

### Verbotene Operationen

| Modell | VERBOTEN |
|--------|----------|
| **OLLAMA** | Jeder Dateizugriff |
| **HAIKU** | DELETE, MOVE, SYSTEM-CMD |
| **SONNET** | DIR-DELETE ohne Bestätigung |
| **OPUS** | - (volle Rechte) |

---

## 11. FAZIT

### Die goldene Regel

> **"Opus denkt, Sonnet baut, Haiku führt aus, Ollama spart."**

### Implementierungs-Status

```
✅ Konzept dokumentiert
✅ Berechtigungsmatrix definiert
✅ Queue-Struktur angelegt
✅ Context Store vorbereitet
⏳ Dispatcher noch zu implementieren
⏳ Worker-Scripts noch zu erstellen
```

### Nächste Schritte

1. Ollama aktivieren (`ollama serve`)
2. Dispatcher-Logik implementieren
3. Worker für jede Queue erstellen
4. Praxis-Test mit echter Aufgabe

---

*Model-Switching Strategie V2.0 | RecludOS | 09.01.2026*