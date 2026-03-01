# BACH Agents & Experts

**Generiert:** 2026-03-01 03:34
**Quelle:** bach.db (bach_agents, bach_experts)
**Generator:** `bach export mirrors` oder `python tools/agents_export.py`

---

## Boss-Agenten (Orchestrierer)

Boss-Agenten orchestrieren komplexe Workflows und delegieren an Experten.

---

## Experten (Spezialisierte Ausführer)

Experten führen spezifische Aufgaben aus und werden von Boss-Agenten delegiert.

---

## Status-Kategorien

- **FUNCTIONAL:** Voll funktionsfähig, produktionsbereit
- **PARTIAL:** Grundfunktionen vorhanden, aber unvollständig
- **SKELETON:** Struktur vorhanden, aber Implementierung fehlt weitgehend

---

## Charakter-Modell (ENT-41)

Jeder Boss-Agent hat eine `## Charakter` Section in seiner SKILL.md:
- **Ton:** Wie kommuniziert der Agent?
- **Schwerpunkt:** Woran orientiert er sich?
- **Haltung:** Welche Werte vertritt er?

Siehe: BACH_Dev/MASTERPLAN_PENDING.txt → SQ049 Agenten-Audit & Upgrade

---

## Arbeitsprinzipien

Alle Agenten folgen den globalen Arbeitsprinzipien aus Root-SKILL.md:
- Unterscheiden was eigen, was fremd
- Text ist Wahrheit
- Erst lesen, dann ändern
- Keine Duplikate erzeugen
- Flexibel auf User-Korrekturen reagieren

---

## Nutzung

```bash
# Boss-Agent starten (mit Partner-Delegation)
bach agent start bueroassistent --partner=claude-code

# Experten direkt aufrufen (falls erlaubt)
bach expert run bewerbungsexperte --task="Anschreiben für Stelle X"

# Agent-Liste anzeigen
bach agent list

# Expert-Liste anzeigen
bach expert list
```

---

## Datei-Synchronisation

Diese Datei wird automatisch generiert aus:
- `bach_agents` (Tabelle für Boss-Agenten)
- `bach_experts` (Tabelle für Experten)

**Trigger:**
- `bach --shutdown` (via finalize_on_idle)
- `bach export mirrors` (manuell)

**dist_type:** 1 (TEMPLATE) - resetbar, aber anpassbar

---

## Siehe auch

- **PARTNERS.md** - LLM-Partner und Delegation
- **USECASES.md** - Anwendungsfälle
- **WORKFLOWS.md** - 25 Protocol-Skills als Index
- **CHAINS.md** - Toolchains
