# BACH Partners

Automatisch generiert aus der Datenbank (delegation_rules, partner_recognition, interaction_protocols).

## Delegation Rules

BACH nutzt ein Zonen-Modell fuer Partner-Auswahl:

| Zone | Strategie | Bevorzugter Partner |
|------|-----------|-------------------|
| Zone 1 | Voller Zugang | Claude (beste Qualitaet) |
| Zone 2 | Moderat | Ollama (kostenguenstig) |
| Zone 3 | Konservativ | Ollama (nur lokal) |
| Zone 4 | Notfall | Minimaler Verbrauch |

## Partner-Typen

- **Claude**: Anthropic API (hoehere Qualitaet, kostet Tokens)
- **Ollama**: Lokale LLMs (kostenlos, offline-faehig)
- **Gemini**: Google API (Alternative)

---

<!--
  HINWEIS: Diese Datei ist ein Template.
  BACH generiert die vollstaendige Liste automatisch aus bach.db.
-->
