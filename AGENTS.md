# BACH Agents & Experts

**Generiert:** 2026-03-01 22:28
**Quelle:** bach.db (bach_agents, bach_experts)
**Generator:** `bach export mirrors` oder `python tools/agents_export.py`

---

## Boss-Agenten (Orchestrierer)

Boss-Agenten orchestrieren komplexe Workflows und delegieren an Experten.

### Entwickler Agent (ATI)
- **Name:** ati
- **Typ:** Expert
- **Kategorie:** None
- **Pfad:** `None`
- **Status:** active
- **Version:** 1.2.0
- **Beschreibung:** Spezialisiert auf Tool-Ueberwachung und Software-Entwicklung.

### Bueroassistent
- **Name:** bueroassistent
- **Typ:** boss
- **Kategorie:** beruflich
- **Pfad:** `agents/bueroassistent.txt`
- **Status:** active
- **Version:** 1.0.0
- **Beschreibung:** Steuern, Foerderplanung, Dokumentation

### Finanzassistent
- **Name:** finanz-assistent
- **Typ:** assistant
- **Kategorie:** beruflich
- **Pfad:** `None`
- **Status:** active
- **Version:** 1.0.0
- **Beschreibung:** Financial Mails, Abos, Versicherungen

### Gesundheitsassistent
- **Name:** gesundheitsassistent
- **Typ:** boss
- **Kategorie:** privat
- **Pfad:** `agents/gesundheitsassistent.txt`
- **Status:** active
- **Version:** 1.0.0
- **Beschreibung:** Medizinische Dokumentation und Gesundheitsverwaltung

### Persoenlicher Assistent
- **Name:** persoenlicher-assistent
- **Typ:** boss
- **Kategorie:** privat
- **Pfad:** `agents/persoenlicher-assistent.txt`
- **Status:** active
- **Version:** 1.0.0
- **Beschreibung:** Terminverwaltung, Recherche, Organisation

---

## Experten (Spezialisierte Ausführer)

Experten führen spezifische Aufgaben aus und werden von Boss-Agenten delegiert.

### Abo-Service
- **Name:** aboservice
- **Domain:** finanzen
- **Pfad:** `None`
- **Status:** active
- **Version:** 1.0.0

### Bewerbungsexperte
- **Name:** bewerbungsexperte
- **Domain:** karriere
- **Pfad:** `None`
- **Status:** active
- **Version:** 1.0.0

### Daten-Analyse
- **Name:** data-analysis
- **Domain:** analytik
- **Pfad:** `None`
- **Status:** active
- **Version:** 1.0.0

### Decision-Briefing
- **Name:** decision-briefing
- **Domain:** None
- **Pfad:** `agents\_experts\decision-briefing\CONCEPT.md`
- **Status:** active
- **Version:** 1.0.0
- **Beschreibung:** Der Decision-Briefing-Experte ist das zentrale System für ausstehende Entscheidungen und User-Aufgaben in BACH. Er:

### Finanz-Mails
- **Name:** financial_mail
- **Domain:** finanzen
- **Pfad:** `None`
- **Status:** active
- **Version:** 1.0.0

### Foerderplaner
- **Name:** foerderplaner
- **Domain:** paedagogik
- **Pfad:** `agents/_experts/foerderplaner/`
- **Status:** active
- **Version:** 1.0.0
- **Beschreibung:** ICF-Foerderplanung, Material-Recherche

### Gesundheitsverwalter
- **Name:** gesundheitsverwalter
- **Domain:** gesundheit
- **Pfad:** `agents/_experts/gesundheitsverwalter/`
- **Status:** active
- **Version:** 1.0.0
- **Beschreibung:** Arztberichte, Laborwerte, Medikamente

### Haushaltsmanagement
- **Name:** haushaltsmanagement
- **Domain:** haushalt
- **Pfad:** `agents/_experts/haushaltsmanagement/`
- **Status:** active
- **Version:** 1.0.0
- **Beschreibung:** Haushaltsbuch, Inventar, Einkaufslisten

### Health-Import
- **Name:** health_import
- **Domain:** gesundheit
- **Pfad:** `None`
- **Status:** active
- **Version:** 1.0.0

### Termin-Optimierer
- **Name:** mr_tiktak
- **Domain:** zeit
- **Pfad:** `None`
- **Status:** active
- **Version:** 1.0.0

### Psycho-Berater
- **Name:** psycho-berater
- **Domain:** psychologie
- **Pfad:** `agents/_experts/psycho-berater/`
- **Status:** active
- **Version:** 1.0.0
- **Beschreibung:** Therapeutische Gespraeche, Sitzungsprotokolle

### Bericht-Generator
- **Name:** report_generator
- **Domain:** dokumentation
- **Pfad:** `None`
- **Status:** active
- **Version:** 1.0.0

### Steuer-Experte
- **Name:** steuer-agent
- **Domain:** finanzen
- **Pfad:** `agents/_experts/steuer/`
- **Status:** active
- **Version:** 1.0.0
- **Beschreibung:** Steuerbelege, Werbungskosten

### Transkriptions-Service
- **Name:** transkriptions-service
- **Domain:** medien
- **Pfad:** `agents/_experts/transkriptions-service/`
- **Status:** active
- **Version:** 1.0.0
- **Beschreibung:** Audiodateien und Gespraeche transkribieren, Sprecher erkennen, bereinigen, exportieren

### Wiki-Lernhilfe
- **Name:** wikiquizzer
- **Domain:** bildung
- **Pfad:** `None`
- **Status:** active
- **Version:** 1.0.0

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
