# PoC-Bericht: Expert "steuer" zu Persona+Skill konvertieren

**Task:** #1069
**Datum:** 2026-03-12
**Status:** Phase 1 abgeschlossen (Konzept + Dateien)

---

## IST-Zustand (vor Konvertierung)

Der Expert "steuer" (Theodor) war ein **monolithischer Expert-Ordner** mit 40+ Dateien,
in dem alles vermischt war:

| Aspekt | Dateien | Problem |
|--------|---------|---------|
| Persona/Charakter | rolle.txt (32 Zeilen) | Minimal, kaum Persoenlichkeit |
| Agent-Definition | steuer-agent.txt (343 Zeilen) | Alles in einer Datei: Rolle, Workflow, DB, CLI |
| Skill-Definition | SKILL.md (150 Zeilen) | Mischt Persona-Infos mit Tool-Listen |
| Tools | 16 Python-Dateien | Kein klarer Skill-Scope |
| Workflows | 7 Markdown-Dateien | Direkt im Expert-Ordner |
| Config | _config.py, _paths.py | Expert-spezifisch |
| Doku | README.md (200 Zeilen) | Historische Tool-Uebersicht |

**Kern-Problem:** Wer (Theodor), Was (Steuer-Faehigkeiten) und Wie (Session-Config)
waren nicht trennbar. Ein anderer Agent konnte die Steuer-Tools nicht nutzen, ohne
den ganzen Expert zu laden.

## SOLL-Zustand (nach Konvertierung)

### Persona: THEODOR.md (`system/agents/personas/`)
- **Inhalt:** Charakter, Stil, Werte, Kommunikationsmuster
- **Referenziert:** Skills per Name (`skills: [steuererklaerung]`)
- **Enthaelt:** Runtime/Session-Config (model, max_turns, tools)
- **Neu:** Claude Code Agent-Export-Block
- **Version:** 2.0.0 (vorher: 1.0.0 auto-generiert)

### Skill: steuererklaerung (`system/skills/steuererklaerung/`)
- **Inhalt:** Alles was "Steuererklaerung" als Faehigkeit ausmacht
- **Tools:** 16 Kern-Tools + 2 Setup-Tools (physisch noch in _experts/steuer/)
- **Workflows:** 7 Workflow-Dateien (physisch noch in _experts/steuer/)
- **Daten:** Tabellen-Schema, Listen-System, Output-Dateien
- **Portabel:** Jede kompatible Persona kann den Skill laden
- **Anthropic-kompatibel:** YAML-Frontmatter, strukturierte Tool-Definitionen

### Session-Config (in Persona eingebettet)
- `runtime.model`: null (flexibel)
- `runtime.max_turns`: 25
- `runtime.tools`: [Bash, Read, Edit, Write, Glob, Grep]

## Was funktioniert hat

1. **Trennung ist konzeptionell sauber:** Die drei Ebenen (Persona/Skill/Session)
   lassen sich klar voneinander abgrenzen. Es gab keine Grenzfaelle wo unklar war,
   wohin etwas gehoert.

2. **Persona hat jetzt Substanz:** Die auto-generierte THEODOR.md (v1.0) hatte
   nur Platzhalter. Die neue v2.0 hat echte Persoenlichkeit, Kommunikationsmuster
   und ein konkretes Beispiel.

3. **Skill ist portabel:** Die SKILL.md beschreibt alles was noetig ist, um die
   Steuer-Faehigkeiten zu nutzen -- unabhaengig von der Persona.

4. **Rueckwaerts-kompatibel:** Keine bestehende Datei wurde geloescht oder
   geaendert (ausser THEODOR.md, die erweitert wurde). Der alte Expert-Ordner
   funktioniert weiterhin.

5. **Template-konform:** Beide Dateien folgen dem TEMPLATE_PERSONA.md Format.

## Was noch fehlt (naechste Schritte)

### Prio 1: Physische Migration
- [ ] Tools von `_experts/steuer/` nach `skills/steuererklaerung/tools/` kopieren
- [ ] Workflows von `_experts/steuer/` nach `skills/steuererklaerung/workflows/` kopieren
- [ ] `_config.py` und `_paths.py` auf neue Pfade anpassen
- [ ] Import-Pfade in allen Python-Dateien aktualisieren

### Prio 2: BACH-System-Integration
- [ ] `bach skill load steuererklaerung` implementieren
- [ ] `bach skill list` zeigt den neuen Skill
- [ ] Persona-Loader liest `skills:` aus THEODOR.md und laedt zugehoerige Skills
- [ ] Session-Config wird aus `runtime:` Block gelesen

### Prio 3: Weitere Experts konvertieren
- [ ] Muster von Theodor auf andere Experts uebertragen
- [ ] Gemeinsame Skills identifizieren (z.B. "pdf-verarbeitung" koennte
      von steuer UND literaturverwalter genutzt werden)

### Prio 4: Anthropic Agent-Export
- [ ] `bach agent export theodor --format claude-code` generiert .claude/agents/theodor.md
- [ ] Skills werden inline in den System-Prompt eingebettet

## Dateien

| Datei | Status | Aktion |
|-------|--------|--------|
| `system/agents/personas/THEODOR.md` | Erweitert | v1.0 -> v2.0 |
| `system/skills/steuererklaerung/SKILL.md` | Neu erstellt | Skill-Definition |
| `system/skills/steuererklaerung/POC_BERICHT.md` | Neu erstellt | Dieser Bericht |
| `system/agents/_experts/steuer/*` | Unveraendert | Funktioniert weiter |

## Fazit

Das Persona+Skill+Session-Modell funktioniert fuer den Steuer-Expert.
Die Trennung ist sauber und bringt echten Mehrwert:

- **Personas werden wiederverwendbar** (Theodor koennte auch "Buchhaltung" als Skill bekommen)
- **Skills werden portabel** (Bueroassistent koennte "steuererklaerung" direkt nutzen)
- **Session-Config wird flexibel** (gleiche Persona, verschiedene Models/Turn-Limits)

Der naechste logische Schritt ist die physische Tool-Migration und die
Integration in den `bach skill`-CLI-Befehl.

---
*PoC abgeschlossen: 2026-03-12 | BACH Task #1069*
