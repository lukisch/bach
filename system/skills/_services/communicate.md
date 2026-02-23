---
name: communicate
metadata:
  version: 2.1.0
  last_updated: 2025-12-31
description: >
  Kommunikations-Management für RecludOS.
  Master-Registry mit 8 Partnern, Automatische Partner-Erkennung,
  Communication Executor für Auto-Routing, Protokollierung und Profile.
---

# Communicate v2.0 - Kommunikationssystem

> **💬 Zentrales Kommunikations-Management mit automatischer Partner-Erkennung**

---

## 🎯 Konzept

Dieses Skill-System verwaltet die gesamte Kommunikation im RecludOS:

1. **Partner-Registries** - Zentrale + 8 Sub-Registries
2. **Erkennungssystem** - Automatische Partner-Identifikation
3. **Profile** - Kommunikationsstrategien pro Partner
4. **Logs** - Protokollierung wichtiger Kommunikation

---

## 📊 Systemübersicht

```
Communicate System v2.1.0
├── master_communication_registry.json  (398 Zeilen, v2.0.0)
├── communication_executor.py           (678 Zeilen, v1.0.0) ← NEU
├── profiles/
│   ├── COMMUNICATION_PROFILES.md      (350 Zeilen, 8 Partner)
│   └── RECOGNITION_SYSTEM.md          (393 Zeilen, Auto-Detection)
├── logs/
│   └── communication_log.txt
├── system-explorer/
│   ├── system_explorer.py             (407 Zeilen)
│   ├── software_registry.json         (115k+ Zeilen)
│   └── config.json
└── Sub-Registries in connections/
    ├── ../user/registry.json              (102 Zeilen)
    ├── claude/registry.json            (91 Zeilen)
    ├── connected_AIs/
    │   ├── locals/ollama/              (149 Zeilen)
    │   └── external/gemini|gpt/        (48 Zeilen)
    ├── connected_APIs/pubmed/          (129 Zeilen)
    ├── connected_services/google_drive/(131 Zeilen)
    └── connected_Tools/canva/          (73 Zeilen)

TOTAL: 1401 Zeilen in Sub-Registries + 678 Zeilen Executor
```

---

## 🚀 Communication Executor (NEU v2.1.0)

Der **communication_executor.py** ist das zentrale Routing-Modul für alle Kommunikation.

### CLI-Befehle

```bash
# Partner erkennen
python communication_executor.py detect "Search for gene mutations"
python communication_executor.py detect "Create a presentation"

# Health-Checks
python communication_executor.py health

# Nachricht routen
python communication_executor.py route --partner ollama --message "Draft email"
python communication_executor.py route --partner ollama --channel queue --message "Bulk task"
python communication_executor.py route --partner gemini --message "Research task"

# Status
python communication_executor.py status

# Selbsttest
python communication_executor.py test
```

### Partner-Erkennung

| Partner | Keywords | Patterns |
|---------|----------|----------|
| **ollama** | bulk, embedding, token-free, draft email | localhost:11434 |
| **pubmed** | gene, protein, disease, clinical, biomedical | PMID:\d+, doi: |
| **google_drive** | google drive, find document, search drive | docs.google.com |
| **canva** | design, presentation, poster, infographic | canva.com |
| **gemini** | deep research, long document, concept analysis | - |

### Routing-Kanäle

| Partner | Kanäle | Implementiert |
|---------|--------|---------------|
| **ollama** | Direct API, Queue | ✅ Beide |
| **user** | MessageBox | ✅ |
| **pubmed** | MCP Server | ✅ |
| **canva** | MCP Server | ✅ |
| **google_drive** | API | ✅ |
| **gemini** | Drive Delegation | ✅ |

---

## 🤝 Registrierte Partner (8)

### Internal System (2)
| ID | Partner | Status | Priorität |
|----|---------|--------|-----------|
| partner-001 | User (Lukas) | ✅ Active | Critical |
| partner-002 | Claude (Sonnet 4.5) | ✅ Active | Critical |

### Local AI (1)
| ID | Partner | Status | Priorität |
|----|---------|--------|-----------|
| partner-003 | Ollama (mistral:7b) | ✅ Active | High |

### External AI (2)
| ID | Partner | Status | Priorität |
|----|---------|--------|-----------|
| partner-004 | Google Gemini | ⚪ Inactive | Medium |
| partner-005 | OpenAI GPT | ⚪ Inactive | Low |

### APIs (1)
| ID | Partner | Status | Priorität |
|----|---------|--------|-----------|
| partner-006 | PubMed API | ✅ Active | Medium |

### Services (1)
| ID | Partner | Status | Priorität |
|----|---------|--------|-----------|
| partner-007 | Google Drive | ✅ Active | High |

### Tools (1)
| ID | Partner | Status | Priorität |
|----|---------|--------|-----------|
| partner-008 | Canva | ✅ Active | Low |

---

## 🔍 Automatisches Erkennungssystem

### Workflow

```
1. USER INPUT
   ↓
2. PATTERN ANALYSIS
   • Keyword Matching
   • URL Detection
   • Context Understanding
   ↓
3. PARTNER SELECTION
   • Multi-Pattern-Matching
   • Prioritäts-Scoring
   ↓
4. CHANNEL INIT
   • API/Queue/MCP Setup
   ↓
5. COMMUNICATION
```

### Erkennungsmuster

**User (MessageBox):**
```
Pattern: Neue .txt in User/MessageBox/outbox/
Trigger: Bei jedem Boot + User-Prompt
Action: Sofort lesen und verarbeiten
```

**Ollama (Queue):**
```
Keywords: "bulk processing", "embeddings", "token-free"
Health: curl localhost:11434/api/tags
Action: Queue-Job oder Direct API
```

**PubMed (Biomedical):**
```
Keywords: "gene", "protein", "disease", "clinical"
Domain: ONLY biomedical/life sciences
Action: MCP-Tools verwenden
```

**Google Drive (Documents):**
```
URL: "https:/docs.google.com/"
Keywords: "find document", "search drive"
Action: Drive Search oder Fetch
```

**Canva (Design):**
```
Keywords: "design", "presentation", "poster"
Action: Generate Design, Export
```

### Multi-Partner-Routing

Beispiel: Research + Presentation
```
1. PubMed → Search literature
2. Claude → Analyze results
3. Canva → Create presentation
```

---

## 📋 Komponenten

### Master Communication Registry

**Pfad:** `master_communication_registry.json`
**Version:** 2.0.0
**Größe:** 376 Zeilen

**Enthält:**
- 8 Partner-Definitionen
- Erkennungsregeln
- Kommunikationsprotokolle
- Integration mit 8 Sub-Registries
- Statistiken

### Communication Profiles

**Pfad:** `profiles/COMMUNICATION_PROFILES.md`
**Größe:** 350 Zeilen

**Pro Partner:**
- Profil (Typ, Status, Expertise)
- Erkennungsprozeduren
- Kommunikationsstrategie
- Use Cases

### Recognition System

**Pfad:** `profiles/RECOGNITION_SYSTEM.md`
**Größe:** 393 Zeilen

**Features:**
- Auto-Detection-Workflow
- Pattern-Matching-Regeln
- Multi-Partner-Routing
- Confidence-Scoring
- Test-Cases

### Sub-Registries (8)

**Locations:**
```
main/connections/../user/registry.json
main/connections/claude/registry.json
main/connections/connected_AIs/locals/ollama/registry.json
main/connections/connected_AIs/external/gemini/registry.json
main/connections/connected_AIs/external/gpt/registry.json
main/connections/connected_APIs/pubmed/registry.json
main/connections/connected_services/google_drive/registry.json
main/connections/connected_Tools/canva/registry.json
```

**Jede Registry enthält:**
- partner_id, name, type, status
- communication_channels
- recognition_rules
- capabilities
- use_cases

---

## 🔄 Integration

### Registry-Watcher

**Status:** ✅ Integriert
**Registry:** `manage/registry-watcher/master_registry.json`
**Entry:**
```json
{
  "name": "communication_registry",
  "path": "main/system/act/communicate/master_communication_registry.json",
  "type": "communication",
  "purpose": "Kommunikationspartner-Verwaltung (8 Partner, 8 Sub-Registries)",
  "priority": "high",
  "boot_step": 2,
  "version": "2.0.0"
}
```

### Boot-Integration

**Schritt 2:** Meta-Systeme laden
- Master Communication Registry laden
- Partner-Status prüfen
- Verfügbarkeit testen (Ollama Health-Check)

**Schritt 2.6:** Ollama Queue prüfen
```
manage/external-skills/tools/queue/completed/
→ Fertige Jobs laden und anzeigen
```

**Schritt 2.7:** Google Drive Delegation prüfen
```
Google Drive: delegation/outbox/
→ Ergebnisse von Gemini laden
```

### Operating Principles

**Script-First Approach:**
- Partner-Erkennung → Registry checken
- Delegation → Optimal routen

**Token-Conscious:**
- Bei >80% Token → Ollama delegieren
- Bei >85% Token → Gemini für Research

---

## 📖 Verwendung

### Partner finden

```python
# Auto-Detection
user_input = "Search for genetic mutations"
partner = detect_partner(user_input)
# → Returns: "pubmed"

# Manual
partner = get_partner_by_id("partner-006")
# → Returns: PubMed Registry
```

### Kommunikation starten

```python
# Direct API
ollama.generate(prompt="Draft email")

# Queue System
ollama.queue_job({
  "task": "bulk_categorize",
  "data": emails
})

# MCP Server
pubmed.search_articles("CRISPR therapy")
```

### Multi-Partner-Task

```python
# Complex Workflow
task = "Research + Create Presentation"

# 1. Research
results = pubmed.search_articles("topic")

# 2. Analyze
analysis = claude.analyze(results)

# 3. Design
presentation = canva.generate_design(
  type="presentation",
  content=analysis
)
```

---

## 🔄 Synchronisation

### Master ← Sub-Registries

**Strategie:** Master pulls from Sub
**Frequenz:** Boot + Manual Trigger

**Sync-Prozess:**
```python
def sync_master_registry():
    for sub_registry in get_all_sub_registries():
        data = load_json(sub_registry)
        update_master_entry(data["partner_id"], data)
    save_master_registry()
```

### Auto-Discovery

**Neue Partner automatisch erkennen:**
```python
def discover_new_partners():
    scan_locations = [
        "connected_AIs/",
        "connected_APIs/",
        "connected_services/",
        "connected_Tools/"
    ]
    for location in scan_locations:
        for registry in find("registry.json"):
            if not is_registered(registry):
                register_new_partner(registry)
```

---

## 📊 Statistiken

### Master Registry

```json
{
  "total_partners": 8,
  "active_partners": 5,
  "inactive_partners": 3,
  "sub_registries_active": 8,
  "total_registry_lines": 723
}
```

### Partner-Kategorien

```json
{
  "internal_system": 2,
  "local_ai": 1,
  "external_ai": 2,
  "apis": 1,
  "services": 1,
  "tools": 1
}
```

---

## 🛠️ Debugging

### Health-Checks

**Ollama:**
```bash
curl http:/localhost:11434/api/tags
# HTTP 200 → OK
```

**Google Drive:**
```python
google_drive_search(api_query="test")
# Results → OK
```

**PubMed:**
```python
pubmed.search_articles("test")
# Results → OK
```

### Logs

**Location:** `logs/communication_log.txt`

**Format:**
```
[2025-12-28 08:00] [USER] MessageBox scan: 16 files
[2025-12-28 08:05] [OLLAMA] Health check: OK
[2025-12-28 08:10] [PUBMED] Query: genetic mutations
```

---

## 🔮 Roadmap

### v2.2.0 (Planned)
- [ ] GPT-Integration
- [ ] Erweiterte Statistiken
- [ ] Performance-Metriken
- [ ] Machine Learning Partner-Selection

### v2.3.0 (Future)
- [ ] Predictive Routing
- [ ] Kommunikations-Patterns lernen
- [ ] Auto-Scaling für Bulk-Tasks

---

## 📚 Dokumentation

| Dokument | Pfad | Größe |
|----------|------|-------|
| Master Registry | master_communication_registry.json | 420+ Zeilen |
| Communication Executor | communication_executor.py | 678 Zeilen |
| Explorer Bridge | system-explorer/explorer_bridge.py | 364 Zeilen |
| Partner Profiles | profiles/COMMUNICATION_PROFILES.md | 350 Zeilen |
| Recognition System | profiles/RECOGNITION_SYSTEM.md | 393 Zeilen |
| CLI Tools Registry | cli_skills/tools/cli_tools_registry.json | 126 Zeilen |
| Gemini Workflow | gemini/DELEGATION_WORKFLOW.md | 178 Zeilen |

**Total Dokumentation:** ~2500+ Zeilen

---

**Version:** 2.1.0  
**Status:** ✅ PRODUCTION READY  
**Erstellt:** 2025-12-28  
**Erweitert:** 2025-12-31  
**Integriert:** Registry-Watcher, Boot-Prozess, Communication Executor  
**Partner:** 9 (6 active, 3 inactive)  
**CLI-Tools:** 12 registriert  
**Sub-Registries:** 9 (alle active)