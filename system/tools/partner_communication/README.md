# Partner Communication Tools

**Status:** 80% BACH-ready, 1 Datei ausstehend  
**Version:** 0.3.0 (BACH-Migration)  
**Aktualisiert:** 2026-01-22 10:49

---

## Übersicht

Tools für Partner-Kommunikation, System-Erkennung, Software-Analyse und Message-Routing.
Portiert aus RecludOS für BACH-Integration.

---

## Dateien

| Datei | Zeilen | Funktion | Status |
|-------|--------|----------|--------|
| `communication.py` | 678 | Partner-Erkennung, Health-Checks, Message-Routing | ✅ BACH-ready |
| `system_explorer.py` | 458 | System Explorer - OS-Software-Erkennung | ✅ BACH-ready |
| `ai_compatible.py` | 200 | Analyse AI-kompatibler Software aus Registry | ✅ BACH-ready (2026-01-22) |
| `real_tools.py` | 198 | Analyse echter CLI-Tools (EXE/CMD/BAT) | ✅ BACH-ready (2026-01-22) |
| `_NEEDS_ADAPT_interaction_protocol.py` | 1225 | Instanz-zu-Instanz-Kommunikation, DNA-Tracking, Handshake | ⚠️ Pfade anpassen |

**Aktiv: 5 Tools, 2.759 Zeilen**

### Archiviert (2026-01-22)

| Datei | Grund | Pfad |
|-------|-------|------|
| `DEPRECATED_explorer_bridge.py` | Konzeptionell RecludOS-spezifisch, braucht DB-basierte Neuimplementierung | `_archive/` |
| `DEPRECATED_integration_tests.py` | Tests für archivierte RecludOS-Struktur | `_archive/` |

### Präfix-Bedeutung

- `_NEEDS_ADAPT_` = Funktional aber braucht BACH-Pfadanpassungen
- Ohne Präfix = BACH-ready, kann direkt verwendet werden

---

## Tool-Kategorien

### 1. Kern-Kommunikation

| Tool | Beschreibung |
|------|--------------|
| `communication.py` | Zentrale Partner-Erkennung und Message-Routing |
| `interaction_protocol.py` | Instanz-Handshake, DNA-Tracking zwischen BACH-Instanzen |
| `explorer_bridge.py` | Brücke zwischen CLI-Tools und Partner-System |

### 2. System-Analyse

| Tool | Beschreibung |
|------|--------------|
| `system.py` | Scannt OS nach installierter Software, erfasst AI-Kompatibilität |
| `ai_compatible.py` | Filtert AI-kompatible Software aus Registry |
| `real_tools.py` | Identifiziert echte CLI-Tools (EXE/CMD/BAT) für Delegation |

### 3. Testing

| Tool | Beschreibung |
|------|--------------|
| `integration_tests.py` | E2E-Tests: Instanz-Erkennung, Import, DNA-Update, Receipts |

---

## Erforderliche Anpassungen

### Pfade (alle Dateien)

```python
# ALT (RecludOS)
RECLUDOS_ROOT = SCRIPT_DIR.parents[4]
CONNECTIONS_DIR = RECLUDOS_ROOT / "main" / "connections"

# NEU (BACH)
BACH_ROOT = Path(__file__).parents[2]  # skills/tools/partner_communication -> BACH_v2_vanilla
PARTNERS_DIR = BACH_ROOT / "_partners"
DATA_DIR = BACH_ROOT / "data"
```

### Pro Tool

**communication.py:**
- `RECOGNITION_PATTERNS` erweitern für BACH-Partner
- `HEALTH_CHECKS` auf BACH-Endpoints anpassen
- Routing-Logik auf `partners/` Workspace umstellen

**interaction_protocol.py:**
- Identity-Pfade auf `data/bach.db` umstellen
- Inbox/Outbox auf `partners/` Struktur anpassen
- DNA-Tracking auf BACH-Tabellen abbilden

**system.py + ai_compatible.py + real_tools.py:**
- Registry-Pfad auf BACH-Struktur anpassen
- Output nach `data/` oder `partners/registry/`

**integration_tests.py:**
- Import-Pfade für BACH-Module korrigieren
- Test-Fixtures auf BACH-Struktur anpassen

---

## Integration mit BACH

### Datenbank-Tabellen

Die Tools sollten folgende BACH-Tabellen nutzen:

- `connections` - Partner-Endpoints
- `partner_recognition` - Capabilities, Zonen
- `delegation_rules` - Token-basierte Delegation
- `comm_messages` - Nachrichtenprotokoll

### Partner-Workspaces

```
partners/
├── _TASKS.md           # Zentrale Task-Zuweisung
├── claude/
│   ├── inbox/          # Eingehende Aufträge
│   ├── outbox/         # Berichte
│   └── workspace/      # Arbeitsdateien
├── gemini/
│   └── ...
└── ollama/
    └── ...
```

---

## CLI-Integration (geplant)

```bash
# System-Scan
bach partner scan              # Alle Software scannen
bach partner scan --ai-only    # Nur AI-kompatible

# Partner-Erkennung
bach partner detect "Search for gene mutations"

# Health-Checks
bach partner health
bach partner health ollama

# Message-Routing
bach partner route --to gemini --message "Research task"

# Tests
bach partner test              # Integration-Tests ausführen
```

---

## Migrations-Priorität

1. **Verbleibend:** `interaction_protocol.py` - Instanz-Handshake, DNA-Tracking (Task COMM_001)
2. **Archiviert:** `explorer_bridge.py`, `integration_tests.py` - RecludOS-spezifisch → Neuimplementierung wenn nötig

---

## Referenzen

- Skill-Definition: `skills/_services/communicate.md`
- Help: `skills/docs/docs/docs/help/partners.txt`, `skills/docs/docs/docs/help/connections.txt`
- Datenbank: `data/bach.db` (connections, partner_recognition)