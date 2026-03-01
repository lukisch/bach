# BACH Partners

Automatisch generiert aus der Datenbank (delegation_rules, partner_recognition, interaction_protocols).
Letzte Aktualisierung: 2026-03-01 22:28

## Delegation Rules

**Total:** 4 Regeln

### Zone: zone_1

- **zone_1_full_access** ⭐⭐⭐
  - Voller Zugang: Alle Partner verfuegbar, optimale Qualitaet
  - Preferred: Claude

### Zone: zone_2

- **zone_2_moderate** ⭐⭐⭐
  - Moderate Sparsamkeit: Bevorzuge kostenguenstige Partner
  - Preferred: Ollama

### Zone: zone_3

- **zone_3_conservative** ⭐⭐
  - Konservativ: Nur lokale Partner (Ollama) bevorzugt
  - Preferred: Ollama

### Zone: zone_4

- **zone_4_emergency** ⭐
  - Notfall: Nur Eskalation oder lokale Verarbeitung
  - Preferred: Human

## Partner Recognition

**Total:** 10 Partner

- **Claude** (api) ✓
  - Zone: zone_1 | Cost: $$$ | Priority: 100
  - Capabilities: ["general", "coding", "analysis", "writing"]

- **Ollama** (local) ✓
  - Zone: zone_3 | Cost: $ | Priority: 80
  - Capabilities: ["coding", "general"]

- **Gemini** (api) ✓
  - Zone: zone_1 | Cost: $$ | Priority: 70
  - Capabilities: ["general", "research", "coding"]

- **Copilot** (api) ✓
  - Zone: zone_2 | Cost: $$ | Priority: 60
  - Capabilities: ["coding", "completion"]

- **ChatGPT** (api) ✓
  - Zone: zone_1 | Cost: $$$ | Priority: 50
  - Capabilities: ["general", "writing"]

- **Perplexity** (api) ✓
  - Zone: zone_2 | Cost: $$ | Priority: 40
  - Capabilities: ["research", "search"]

- **Mistral** (api) ✓
  - Zone: zone_2 | Cost: $$ | Priority: 30
  - Capabilities: ["coding", "general"]

- **Anthropic-Local** (local) ✗
  - Zone: zone_4 | Cost: $ | Priority: 20
  - Capabilities: ["general"]

- **Custom-Agent** (local) ✗
  - Zone: zone_4 | Cost: $ | Priority: 10
  - Capabilities: ["custom"]

- **Human** (human) ✓
  - Zone: zone_4 | Cost: $ | Priority: 5
  - Capabilities: ["review", "decision", "escalation"]

## Interaction Protocols

**Total:** 10 Protokolle

### confirmation

#### receipt

Empfangsbestaetigung

- **Timeout:** 60s | **Retries:** 3 | **Priority:** 50

### delegation

#### task_delegation

Aufgabe an Partner delegieren

- **Timeout:** 300s | **Retries:** 3 | **Priority:** 90
- **Applicable Partners:** ["Claude", "Ollama", "Copilot"]

### discovery

#### compare

Vergleich: Was hat der Partner was ich nicht habe

- **Timeout:** 60s | **Retries:** 3 | **Priority:** 50

#### handshake

Gegenseitige Erkennung zwischen Instanzen

- **Timeout:** 60s | **Retries:** 3 | **Priority:** 50

### escalation

#### human_escalation

Eskalation an Benutzer

- **Timeout:** 60s | **Retries:** 3 | **Priority:** 50
- **Applicable Partners:** ["Human"]

### query

#### simple_query

Einfache Frage-Antwort

- **Timeout:** 30s | **Retries:** 2 | **Priority:** 100
- **Applicable Partners:** ["Claude", "Ollama", "Gemini", "ChatGPT", "Mistral"]

#### code_review

Code-Review anfordern

- **Timeout:** 120s | **Retries:** 2 | **Priority:** 80
- **Applicable Partners:** ["Claude", "Copilot", "ChatGPT"]

#### research_query

Recherche-Anfrage

- **Timeout:** 180s | **Retries:** 3 | **Priority:** 70
- **Applicable Partners:** ["Perplexity", "Claude", "Gemini"]

### transfer

#### request

Import-Anfrage an Partner

- **Timeout:** 60s | **Retries:** 3 | **Priority:** 50

#### transfer

Datenuebertragung zwischen Partnern

- **Timeout:** 60s | **Retries:** 3 | **Priority:** 50
