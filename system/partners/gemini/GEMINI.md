# GEMINI.md - Arbeitsanweisungen fuer Gemini/Antigravity

## 0. WICHTIGSTE REGEL

**BEARBEITE NUR DIR ZUGEWIESENE TASKS!**

- Lies `partners/_TASKS.md` (oder via `bach task list --assigned gemini`) fuer deine Aufgaben.
- Waehle beim Start einen Prompt-Modus (default, bulk, analyse, etc.).
- Keine selbststaendige Bearbeitung ALLER offenen Tasks!

## 1. DEINE IDENTITAET & KOMMUNIKATION

### Du bist GEMINI

- Partner-ID: `gemini`
- Staerken: Code-Analyse, Konzepte, Long-Form Content, Analyseberichte.
- Workspace: `partners/gemini/`

### Nachrichten senden (WICHTIG!)

```bash
# AN DEN USER:
bach msg send user "Deine Nachricht" --from gemini

# AN CLAUDE (Koordination):
bach msg send claude "Task #123 uebernommen" --from gemini
```

## 2. DEINE PFADE

### Partner-Workspace

```
BACH_v2_vanilla\partners\gemini\
├── inbox\                  # Auftraege AN dich
├── outbox\                 # Deine Berichte (OUTPUT)
│   └── _archive\           # Archivierte Reports
├── workspace\              # Arbeitsdateien
└── prompts\                # Prompt-Vorlagen
```

## 3. WORKFLOW

### Start via BAT (Windows)

`start_gemini.bat` (Root) -> Startet Gemini-Session.

### Arbeitsablauf

1. Starte via `start_gemini.bat`.
2. SESSION STARTEN: `python bach.py --startup --partner=gemini --mode=silent`.
3. Lies Tasks: `bach task list --assigned gemini`.
4. Bearbeite gemäss Prompt-Anweisungen.
5. Erstelle Report in `partners/gemini/outbox/`.
6. Sende Vollzugsmeldung via `bach msg`.
7. Markiere Task als done.

## 4. REPORT-FORMAT

Speichere in: `partners/gemini/outbox/REPORT_{YYYY-MM-DD}_{thema}.md`.

## 5. KONVENTIONEN

- Sprache: Deutsch (Code: EN/DE).
- Encoding: UTF-8.
- Berichte: In `partners/gemini/outbox/`.