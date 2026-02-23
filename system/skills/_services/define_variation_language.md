# Define Variation Language

> **Definiert wie Varianten sich unterscheiden können**

---

## Metadaten

| Feld | Wert |
|------|------|
| **Name** | define_variation_language |
| **Version** | 1.0.0 |
| **Parent** | control_variation |

---

## 🎯 Aufgabe

Übersetzt erkannte Probleme in konkrete Mutations-Strategien.

---

## 🗣️ Problem → Strategie Mapping

| Problem-Signal | Empfohlene Strategien |
|----------------|----------------------|
| Negatives Feedback | `simplify_instructions`, `add_examples` |
| Ausführungsfehler | `restructure_sections`, `add_error_handling` |
| Hoher Token-Verbrauch | `reduce_redundancy`, `simplify_instructions` |
| Unklarheit | `add_examples`, `improve_triggers` |
| Fehlende Funktion | `extend_functionality` |

---

## 📝 Mutations-Strategien im Detail

### `simplify_instructions`
```
ZIEL: Klarere, kürzere Anweisungen

TRANSFORMATIONEN:
- Lange Sätze → Kurze Punkte
- Passive → Aktive Formulierung
- Abstrakt → Konkret
- Mehrere Schritte → Zusammenfassen wo möglich
```

### `add_examples`
```
ZIEL: Konkrete Beispiele hinzufügen

TRANSFORMATIONEN:
- Abstrakte Regel → + 2-3 Beispiele
- Edge Cases dokumentieren
- Input/Output Paare zeigen
```

### `restructure_sections`
```
ZIEL: Bessere Organisation

TRANSFORMATIONEN:
- Reihenfolge optimieren (Wichtiges zuerst)
- Unter-Abschnitte hinzufügen
- Redundanzen zusammenführen
- Querverweise hinzufügen
```

### `reduce_redundancy`
```
ZIEL: Weniger Wiederholung

TRANSFORMATIONEN:
- Doppelte Infos entfernen
- Einmal definieren, dann referenzieren
- Tabellen statt wiederholter Text
```

### `optimize_triggers`
```
ZIEL: Bessere Erkennung

TRANSFORMATIONEN:
- Mehr Varianten von Trigger-Phrasen
- Synonyme hinzufügen
- Tippfehler-tolerant
```

### `add_error_handling`
```
ZIEL: Robuster bei Fehlern

TRANSFORMATIONEN:
- Edge Cases dokumentieren
- Fallback-Verhalten definieren
- Validierungs-Schritte hinzufügen
```

---

## 🎲 Strategie-Auswahl

### Automatisch (auto_select)
```
1. Problem-Typ analysieren
2. Mapping konsultieren
3. Erste passende Strategie wählen
4. Bei mehreren: Zufällig oder nach Priorität
```

### Manuell
```
User kann Strategie explizit angeben:
"Erstelle Variante von X mit mehr Beispielen"
→ Strategie: add_examples
```

---

## 📊 Kombinations-Regeln

```
ERLAUBT:
- simplify + reduce_redundancy
- add_examples + restructure_sections

VERMEIDEN:
- simplify + add_examples (widerspricht sich teils)
- Mehr als 2 Strategien gleichzeitig
```

---

*Dieser Prozess definiert die "Sprache" in der Varianten formuliert werden.*
