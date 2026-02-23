---
name: delegate
metadata:
  version: 1.0.0
  last_updated: 2025-12-29
  status: active
description: >
  Delegiert Aufgaben an die 6 Akteur-Kategorien basierend auf
  Effizienz-Metriken aus success-watcher und token-watcher.
  Orchestriert die Zusammenarbeit aller System-Akteure.
  Siehe auch: ACTORS_MODEL.md für vollständige Dokumentation.
---

# Delegate - Kollaborative Aufgabenverteilung

> **Sechs Akteur-Kategorien, ein Ziel: Effiziente Zusammenarbeit**
> 
> 📖 **Vollständige Dokumentation:** `main/main/main/system/boot/ACTORS_MODEL.md`

---

## Die Sechs Akteur-Kategorien (v2.0)

```
┌──────────────────────────────────────────────────────────────┐
│                    WATCH (Metriken)                          │
│         success-watcher  ←→  token-watcher                   │
│              ↓                    ↓                          │
│         Fitness-Score      Token-Budget                      │
└──────────────────────────────────────────────────────────────┘
                              ↓
              ┌───────────────────────────────┐
              │      DELEGATIONS-ENGINE       │
              │   "Wer kann das am besten?"   │
              └───────────────────────────────┘
                              ↓
┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
│ 🌐      │ ⚙️      │ 💻      │ 🧠      │ 🤖      │ 👤      │
│ Online  │ Tools & │ OS      │ Geist   │ Weitere │ User    │
│ Tools   │ Scripts │         │ (Claude)│ AIs     │         │
└─────────┴─────────┴─────────┴─────────┴─────────┴─────────┘
```

---

## Akteur-Kategorien im Detail

### 🌐 Online-Tools (ohne AI)
| Eigenschaft | Wert |
|-------------|------|
| **Beispiele** | Generatoren, Datenbanken, Konverter, APIs |
| **Stärken** | Spezialisiert, sofort verfügbar |
| **Kosten** | Meist kostenlos |
| **Ideal für** | Spezialaufgaben (QR-Codes, Formatierung, etc.) |

### ⚙️ Integrierte Tools & Scripts
| Eigenschaft | Wert |
|-------------|------|
| **Beispiele** | Python-Scripts, Batch-Tools, Eigenentwicklungen |
| **Stärken** | Schnell, wiederholbar, anpassbar |
| **Kosten** | CPU (vernachlässigbar) |
| **Kanal** | `main/skills/tools/` oder direkte Ausführung |
| **Ideal für** | Batch-Ops, Datei-Handling, Automatisierung |

### 💻 Operating System
| Eigenschaft | Wert |
|-------------|------|
| **Beispiele** | Windows, installierte Software, Ollama |
| **Stärken** | Volle Systemkontrolle, lokale LLMs |
| **Kosten** | Lokal (kostenlos) |
| **Kanal** | Desktop Commander, PowerShell |
| **Ideal für** | Systemaufgaben, lokale AI-Inferenz |

### 🧠 Operierende AI ("Geist in der Flasche")
| Eigenschaft | Wert |
|-------------|------|
| **Aktuell** | Claude (Sonnet 4.5) |
| **Stärken** | Komplexes Reasoning, Planung, Orchestrierung |
| **Schwächen** | Token-Kosten, Kontextlimit |
| **Kosten** | Tokens (begrenzt) |
| **Kanal** | Diese Session |
| **Ideal für** | Architektur, Strategie, komplexe Probleme |
| **Hinweis** | Austauschbar - System ist AI-agnostisch |

### 🤖 Weitere AIs/LLMs
| Eigenschaft | Wert |
|-------------|------|
| **Beispiele** | Gemini, Copilot, ChatGPT, Ollama-Modelle |
| **Stärken** | Spezialisierung, alternative Perspektiven |
| **Kosten** | Variabel (API oder kostenlos) |
| **Kanal** | Delegation via User oder API |
| **Ideal für** | Recherche, Bulk-Text, Office-Integration |

### 👤 User
| Eigenschaft | Wert |
|-------------|------|
| **Stärken** | Entscheidungen, Kreativität, manuelle Aktionen |
| **Schwächen** | Langsam, begrenzte Verfügbarkeit |
| **Kosten** | Zeit (wertvoll) |
| **Kanal** | `User/MessageBox/` |
| **Ideal für** | Finale Freigaben, Klicks, Entscheidungen |

---

## Delegations-Matrix (v2.0)

| Aufgabe | Online | Tools | OS | Geist | AIs | User |
|---------|:------:|:-----:|:--:|:-----:|:---:|:----:|
| Finale Entscheidung | | | | | | ⭐ |
| Komplexe Architektur | | | | ⭐ | | |
| Multi-Step-Planung | | | | ⭐ | | |
| Batch-Umbenennung | | ⭐ | | | | |
| Datei-Kopieren (viele) | | ⭐ | ⭐ | | | |
| Einfache Zusammenfassung | | | ⭐ | | ⭐ | |
| RAG-Dokumentensuche | | | ⭐ | | | |
| QR-Code generieren | ⭐ | | | | | |
| Excel-Formeln | | | | | ⭐ | |
| Code-Review (komplex) | | | | ⭐ | | |
| Code-Formatting | | ⭐ | | | | |
| Recherche (lang) | | | | | ⭐ | |
| Manuelle Klicks (UI) | | | | | | ⭐ |

---

## Token-basierte Eskalation

```
Token-Budget: [████████░░] 80%

WENN tokens > 80%:
    → Schwere Aufgaben: Geist behält
    → Leichte Aufgaben: Sammeln in MessageBox
    → Bulk-Arbeit: An Ollama (OS) oder Scripts delegieren
    → Recherche: An Gemini delegieren
    → Automatisierbar: Script erstellen/nutzen

WENN tokens > 95%:
    → NUR noch kritische Entscheidungen
    → Alles andere → MessageBox für User
```

---

## Kommunikations-Kanäle

### An USER (MessageBox)

```
User/MessageBox/                  # Direkt hier (KEINE inbox!)
├── outbox/                 # User → Geist
├── gelesen/                # Gelesene Nachrichten
├── später/                 # Aufgeschoben
└── done/                   # Erledigt
```

**Format für Tasks:**
```markdown
# Task: Dateien freigeben

**Priorität:** Normal
**Von:** Claude
**Erstellt:** 2025-12-29

## Aufgabe
Bitte diese 5 Dateien zur Löschung freigeben:
- [ ] alte_backup_2023.zip
- [ ] temp_export.csv
...
```

### An Ollama (OS - Lokale KI)

```powershell
# Direkt
ollama run mistral "Fasse diesen Text zusammen: ..."

# Via Queue-System
main/system/controll/manage/external-skills/tools/queue/pending/
```

### An Scripts (Tools)

```powershell
# Direkt aufrufen
python main/skills/tools/utilities/data/script.py --args

# Oder neues Script erstellen
→ act/code Skill
```

### An Weitere AIs (Delegation)

```
Gemini:  connections/connected_AIs/external/gemini/
Copilot: Via User (M365 Integration)
GPT:     connections/connected_AIs/external/gpt/
```

---

## Integration mit WATCH

### success-watcher liefert:
```json
{
  "actor_performance": {
    "geist": { "completion": 0.95, "efficiency": 0.7 },
    "scripts": { "completion": 0.99, "efficiency": 0.95 },
    "os_ollama": { "completion": 0.85, "efficiency": 0.9 },
    "weitere_ais": { "completion": 0.80, "efficiency": 0.85 },
    "user": { "completion": 0.8, "efficiency": 0.3 }
  }
}
```

### token-watcher liefert:
```json
{
  "session_tokens": 45000,
  "budget_percent": 75,
  "recommendation": "delegate_simple_tasks"
}
```

### Delegations-Entscheidung:
```python
def decide_actor(task):
    token_budget = token_watcher.get_budget()
    
    if token_budget > 80:
        if task.complexity == "simple":
            if task.type == "text":
                return "os_ollama"  # Lokale KI
            elif task.type == "research":
                return "weitere_ais"  # Gemini
            else:
                return "scripts"
        elif task.requires_human:
            return "user_messagebox"
    
    if task.is_batch_operation:
        return "scripts"
    
    if task.needs_rag:
        return "os_ollama"
    
    if task.is_specialized_online:
        return "online_tools"
    
    return "geist"  # Default: Operierende AI
```

---

## Verfügbare Ressourcen

### Ollama (OS - Lokal)
```
Status: ✅ Läuft (wenn aktiv)
Port: 11434
Modelle:
  - Mistral:latest → Generation
  - nomic-embed-text → Embeddings
Pfad: connections/connected_AIs/locals/ollama/
```

### Scripts (Tools)
```
main/skills/tools/
├── utilities/     # Hilfs-Scripts
├── services/      # Service-Integrationen
└── agents/        # Autonome Agenten
```

### MessageBox (User)
```
User/MessageBox/
├── [neue Dateien direkt hier]
├── outbox/        # User → Geist
├── gelesen/       # Gelesen
└── done/          # Erledigt
```

### Weitere AIs
```
connections/connected_AIs/
├── locals/ollama/
└── external/
    ├── gemini/
    ├── gpt/
    └── copilot/
```

---

## Abhängigkeiten

```
delegate/
    ├── watch/success-watcher      # Fitness-Daten
    ├── watch/token-watcher        # Token-Budget
    ├── User/MessageBox/                # User-Kommunikation
    ├── connections/connected_AIs/ # AI-Partner
    ├── main/skills/tools/                # Scripts & Tools
    └── boot/ACTORS_MODEL.md       # Vollständige Dokumentation
```

---

## Changelog

| Version | Datum | Änderung |
|---------|-------|----------|
| 0.1.0 | 2025-12-22 | Initial concept |
| 0.2.0 | 2025-12-22 | Vier-Akteure-Modell |
| **1.0.0** | **2025-12-29** | **Upgrade auf 6-Kategorien-Modell (v2.0)** |
| | | Pfade korrigiert (User/MessageBox/) |
| | | Verweis auf ACTORS_MODEL.md |
| | | Status: concept → active |