---
name: external-tools
metadata:
  version: 1.1.0
  last_updated: 2025-12-22
description: >
  Verwaltet externe KI-Tools und Dienste für intelligente Delegation.
  Inkl. Prompt-Generator System (Ollama generiert Prompts für €0).
---

# External Tools - Registry & Delegation

> **🔧 Erweitere Claudes Fähigkeiten durch externe Tools**

## Highlight: Prompt-Generator

```
┌─────────────────────────────────────────────────────────────┐
│  🧠 OLLAMA GENERIERT PROMPTS FÜR ANDERE TOOLS               │
│                                                             │
│  Claude (~50 Tok) → Ollama (€0) → Fertiger Prompt          │
│                                                             │
│  Ersparnis: 90-95% Claude-Tokens bei Delegationen!         │
└─────────────────────────────────────────────────────────────┘
```

## Registrierte Tools

### 💳 Aktive Abos

| Tool | Kosten | Limits | Best For |
|------|--------|--------|----------|
| **Claude Pro** | €17/Mo | Flatrate | Code, RecludOS, Hauptarbeit |
| **Gemini Advanced** | €22/Mo | Großzügig | Recherche, Faktencheck, Vision |
| **Copilot M365** | Im Abo | 60 Credits/Mo | Office-Dokumente, Excel, E-Mails |

### 💻 Lokal

| Tool | Kosten | Rolle |
|------|--------|-------|
| **Ollama** | €0 | 🌟 Prompt-Generator + lokale Inferenz |

### 🆓 Kostenlose APIs (Setup nötig)

| Tool | Limits | Best For |
|------|--------|----------|
| **Groq** | 14.400 req/Tag | Schnelle Antworten |
| **OpenRouter** | ~200 req/Tag | Fallback, Vielfalt |

## Zugriffs-Typen

| Typ | Beschreibung | Tools |
|-----|--------------|-------|
| `api_direct` | Claude ruft API selbst | Ollama, Groq |
| `user_delegated` | Task an User → User führt aus | Gemini, Copilot |
| `current_session` | Aktuelle Claude-Session | Claude Pro |

## Prompt-Generierung (Kernfeature)

**Problem:** Prompts für andere Tools schreiben kostet ~500-2000 Tokens.

**Lösung:** Ollama generiert Prompts für €0!

```
1. Claude beschreibt kurz: "Fasse Bericht zusammen, 5 Punkte"
2. Ollama generiert optimierten Prompt für Copilot/Gemini
3. Fertiger Prompt landet in inbox/ für User
```

### Token-Ersparnis

| Szenario | Ohne Ollama | Mit Ollama | Ersparnis |
|----------|-------------|------------|-----------|
| Einfache Delegation | ~500 Tok | ~50 Tok | 90% |
| Komplexe Aufgabe | ~2000 Tok | ~100 Tok | 95% |

## Task-Routing

| Aufgabe | 1. Wahl | 2. Wahl |
|---------|---------|---------|
| Prompt generieren | **Ollama** | Groq |
| Office-Dokumente | **Copilot** | - |
| Excel-Formeln | **Copilot** | Claude |
| E-Mail-Entwürfe | **Copilot** | - |
| Präsentationen | **Copilot** | Gemini |
| Lange Recherche | **Gemini** | Claude |
| Faktencheck | **Gemini** | Claude |
| Code schreiben | **Claude** | Groq |
| Zusammenfassung | **Ollama** | Copilot |

## Copilot M365 Details

**Limits:**
- 60 AI-Credits/Monat (jede Aktion = 1 Credit)
- 15 Deep Research/Monat
- 10 Min Vision/Tag

**Features:**
- Word: Zusammenfassen, Umschreiben, Entwürfe
- Excel: Formeln, Datenanalyse
- Outlook: E-Mail-Entwürfe, Thread-Zusammenfassung
- PowerPoint: Folien aus Text
- OneNote: Listen, Strukturierung

**Prompt-Stil:** Kurz & direkt, konkrete Zahlen, Imperative

## Befehle

| Befehl | Aktion |
|--------|--------|
| "Tools anzeigen" | Dashboard öffnen |
| "Copilot-Aufgabe" | Task für Copilot erstellen |
| "Gemini-Aufgabe" | Task für Gemini erstellen |
| "Tool hinzufügen" | Neues Tool registrieren |

## Dateien

| Datei | Zweck |
|-------|-------|
| SKILL.md | Diese Dokumentation |
| registry.json | Tool-Datenbank |
| tools-dashboard.html | Visuelle Übersicht |
| PROMPT_GENERATOR.md | Prompt-Generator Doku |
| COPILOT_TEMPLATE.md | Copilot-Vorlagen |
| GEMINI_TEMPLATE.md | Gemini-Vorlagen |

---

## Changelog

### v1.1.0 (2025-12-22)
- **NEU:** Copilot M365 registriert (60 Credits/Monat)
- **NEU:** Prompt-Generator System (Ollama generiert Prompts)
- **NEU:** COPILOT_TEMPLATE.md
- **NEU:** PROMPT_GENERATOR.md
- Dashboard erweitert

### v1.0.0 (2025-12-22)
- Initial: Registry-Struktur
- Gemini Advanced, Claude Pro, Ollama
- Free Tier: Groq, OpenRouter, HuggingFace
