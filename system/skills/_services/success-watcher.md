---
name: success-watcher
metadata:
  version: 3.0.0
  last_updated: 2025-12-29
description: >
  Definiert und überwacht Erfolgskriterien für alle 6 Akteur-Kategorien.
  Misst Fitness von Skills, Aktionen und Delegationen.
  Kern-Skill für Delegations-Entscheidungen.
  Siehe auch: ACTORS_MODEL.md für vollständige Akteur-Dokumentation.
---

# Success Watcher - Erfolgsmetriken

> **🎯 Wer macht was wie gut?**
> 
> 📖 **Akteur-Dokumentation:** `main/main/main/system/boot/ACTORS_MODEL.md`

---

## Die Sechs Akteur-Kategorien (v2.0)

```
┌──────────────────────────────────────────────────────────────┐
│                     SUCCESS WATCHER                           │
│                                                               │
│  🌐 Online  ⚙️ Tools  💻 OS   🧠 Geist  🤖 AIs  👤 User     │
│     ↓         ↓       ↓        ↓        ↓       ↓           │
│  [Metrics] [Metrics] [Metrics] [Metrics] [Metrics] [Metrics] │
│                                                               │
│     └──────────┴────────┴────────┴────────┴────────┘         │
│                           ↓                                   │
│              GESAMTBILD & OPTIMIERUNG                         │
└──────────────────────────────────────────────────────────────┘
```

---

## Erfolgs-Dimensionen

### Basis-Metriken (alle Kategorien)

| Dimension | Gewicht | Messung |
|-----------|---------|---------|
| **Completion** | 40% | Wurde die Aufgabe erledigt? |
| **Efficiency** | 25% | Ressourcen-Verbrauch (Zeit/Token/CPU) |
| **Quality** | 25% | Ergebnis-Qualität |
| **Reliability** | 10% | Zuverlässigkeit/Fehlerrate |

### Fitness-Formel

```
Fitness = (completion × 0.4) + (efficiency × 0.25) + 
          (quality × 0.25) + (reliability × 0.1)
```

---

## Kategorie-Profile

### 🌐 Online-Tools
| Metrik | Typischer Wert |
|--------|----------------|
| Completion | 0.95 (meist funktioniert) |
| Efficiency | 1.0 (kostenlos) |
| Quality | 0.9 (spezialisiert) |
| Reliability | 0.8 (Netzwerk-abhängig) |

### ⚙️ Tools & Scripts
| Metrik | Typischer Wert |
|--------|----------------|
| Completion | 0.99 (deterministisch) |
| Efficiency | 1.0 (CPU minimal) |
| Quality | 1.0 (determinismus) |
| Reliability | 1.0 (keine Schwankung) |

### 💻 OS (inkl. Ollama)
| Metrik | Typischer Wert |
|--------|----------------|
| Completion | 0.95 |
| Efficiency | 1.0 (lokal = kostenlos) |
| Quality | 0.75 (weniger als Cloud-AI) |
| Reliability | 0.9 (Hardware-abhängig) |

### 🧠 Geist (Claude)
| Metrik | Typischer Wert |
|--------|----------------|
| Completion | 0.95 |
| Efficiency | 0.5 (Token-Kosten) |
| Quality | 0.95 |
| Reliability | 1.0 (immer verfügbar) |

### 🤖 Weitere AIs
| Metrik | Typischer Wert |
|--------|----------------|
| Completion | 0.9 |
| Efficiency | 0.7 (variabel) |
| Quality | 0.85 |
| Reliability | 0.85 |

### 👤 User
| Metrik | Typischer Wert |
|--------|----------------|
| Completion | 0.85 |
| Efficiency | 0.3 (Zeit = wertvoll) |
| Quality | 0.95 (Entscheidungen) |
| Reliability | 0.4 (nicht immer da) |

---

## Aufgaben-Typ → Kategorie Mapping

| Aufgaben-Typ | Beste Kategorie | Fitness-Grund |
|--------------|-----------------|---------------|
| Finale Entscheidung | 👤 User | Quality 1.0 |
| Komplexe Analyse | 🧠 Geist | Quality 0.95 |
| Batch-Operation | ⚙️ Scripts | Efficiency+Reliability 1.0 |
| Einfache Zusammenfassung | 💻 OS | Efficiency 1.0 |
| RAG-Suche | 💻 OS | Spezialisiert |
| QR-Code generieren | 🌐 Online | Spezialisiert |
| Excel-Makros | 🤖 Copilot | Office-Integration |
| Recherche (lang) | 🤖 Gemini | Token-frei, Kontext |
| UI-Interaktion | 👤 User | Nur User kann |

---

## Integration

| Skill | Datenfluss |
|-------|------------|
| **delegate** | ← Empfängt Fitness-Daten für Entscheidungen |
| **token-watcher** | → Liefert Geist-Effizienz |
| **learning-routines** | ← Empfängt Metriken für Optimierung |
| **process-watcher** | → Liefert Prozess-Outcomes |

---

## Dateien

| Datei | Zweck |
|-------|-------|
| success_tracker.py | Basis-Implementation |
| config.json | Gewichtungen, Schwellwerte |
| data/actor_performance.json | Performance-Historie |

---

## Befehle

| Befehl | Aktion |
|--------|--------|
| `python success_tracker.py status` | Fitness aller Kategorien |
| `python success_tracker.py log <kategorie> <task> <success>` | Task loggen |
| `python success_tracker.py recommend <task_type>` | Empfehlung |
