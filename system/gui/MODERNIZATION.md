# GUI Modernisierung - Strategie

Stand: 2026-02-16

## Interface-Hierarchie (neu)

| Interface | Status | Zielgruppe | Prioritaet |
|-----------|--------|------------|------------|
| **Claude Code CLI** | AKTIV | LLM-Sessions, Entwickler | Hoch |
| **Telegram Bridge** | AKTIV | Mobil, Remote, Chat | Hoch |
| **Zeitgesteuerte Agents** | GEPLANT | Autonome Tages-Sessions | Mittel |
| **REST API (headless)** | AKTIV | Scripts, Integrationen | Mittel |
| **Web-Dashboard** | AKTIV | Monitoring, Status | Niedrig |
| **Prompt-Manager (PyQt6)** | LEGACY | Desktop-Power-User | Niedrig |

## Legacy: Prompt-Manager (gui/prompt_manager.py)

- Weiterhin nutzbar, keine aktive Weiterentwicklung
- PyQt6-Abhaengigkeit bleibt optional
- Nicht entfernt, da bestehende Nutzer ihn verwenden koennten
- Bei Start: Hinweis auf moderne Alternativen

## Primaer-Interfaces

### 1. Claude Code CLI (bach.py)
- Vollzugriff auf alle Handler via `bach` Befehle
- Library-API fuer LLMs (`bach_api`)
- Session-Management mit Startup/Shutdown
- Empfohlen fuer alle LLM-Interaktionen

### 2. Telegram Bridge (hub/_services/claude_bridge/)
- Chat-basierter Zugang zu BACH
- Permission-System (restricted/full)
- Worker fuer laengere Aufgaben
- Mobiler Zugang von ueberall

### 3. Zeitgesteuerte Agents (GEPLANT)
- Tages-Agent der morgens startet (via Task Scheduler/cron)
- Claude Code mit --continue fuer persistente Session
- Abend-Summary in BACH Memory
- Siehe: hub/daily_agent.py
