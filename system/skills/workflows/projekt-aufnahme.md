# Standardaufnahmeverfahren für neue Software-Projekte

**Version:** 1.0  
**Stand:** 2026-01-10

---

## Übersicht

Dieses Verfahren definiert, welche Schritte bei neu entdeckten Software-Ordnern durchzuführen sind, bevor sie in den Task-Manager aufgenommen werden.

```
┌─────────────────────────────────────────────────────────┐
│           STANDARDAUFNAHMEVERFAHREN                     │
├─────────────────────────────────────────────────────────┤
│  1. Feature-Analyse erstellen                           │
│  2. Code-Qualitätsprüfung (Standard-Tests)              │
│  3. AUFGABEN.txt erstellen                              │
│  4. Scanner erkennt → Task-Manager                      │
└─────────────────────────────────────────────────────────┘
```

---

## Phase 1: Feature-Analyse

**Zweck:** Verständnis des Tools, seiner Funktionen und des Entwicklungsstandes.

**Datei erstellen:** `Feature_Analyse_<ToolName>.md`

### Template

```markdown
# Feature-Analyse: <ToolName>

## Kurzbeschreibung
Ein kurzer Satz der beschreibt was das Tool macht.

---

## ✨ Highlights

| Feature | Beschreibung |
|---------|-------------|
| **Feature 1** | Beschreibung |
| **Feature 2** | Beschreibung |

---

## 🎯 Bewertung der Ausbaustufe

### Aktueller Stand: **<Status> (<X>%)**

Mögliche Status:
- Prototype (0-30%)
- Alpha (30-60%)
- Beta (60-85%)
- Production Ready (85-95%)
- Release (95-100%)

| Kategorie | Bewertung | Details |
|-----------|:---------:|---------|
| **Funktionsumfang** | ⭐⭐⭐ | |
| **UI/UX** | ⭐⭐⭐ | |
| **Stabilität** | ⭐⭐⭐ | |
| **Dokumentation** | ⭐⭐⭐ | |

---

## 🚀 Empfohlene Erweiterungen

### Priorität: Hoch
1. ...

### Priorität: Mittel
2. ...

### Priorität: Niedrig
3. ...

---

## 💻 Technische Details

Framework:      <Framework>
Dateigröße:     <X> Zeilen Python
Hauptdatei:     <main.py>

---
*Analyse erstellt: <Datum>*
```

---

## Phase 2: Code-Qualitätsprüfung

**Zweck:** Technische Qualität sicherstellen, bekannte Probleme identifizieren.

### Standard-Tests mit DEV_TOOLS

| Test | Tool | Befehl |
|------|------|--------|
| **Encoding** | c_encoding_fixer.py | `python c_encoding_fixer.py <datei>` |
| **Methoden-Analyse** | c_method_analyzer.py | `python c_method_analyzer.py <datei>` |
| **Einrückung** | c_indent_checker.py | `python c_indent_checker.py <datei>` |
| **Imports** | c_import_diagnose.py | `python c_import_diagnose.py <datei>` |

### Prüfpunkte

- [ ] Alle .py Dateien UTF-8 kodiert?
- [ ] Keine ungewöhnlich große Methoden (>100 Zeilen)?
- [ ] Konsistente Einrückung (Spaces vs Tabs)?
- [ ] Unused Imports entfernt?
- [ ] Docstrings vorhanden?

### Ergebnis dokumentieren

Probleme in AUFGABEN.txt unter "QUALITÄTSPRÜFUNG" eintragen.

---

## Phase 3: AUFGABEN.txt erstellen

**Zweck:** Offene Aufgaben strukturiert erfassen für Scanner-Erkennung.

**Datei erstellen:** `AUFGABEN.txt` im Projektordner

### Template

```
AUFGABEN - <ToolName> V<Version>
==============================
Status: <Status>
Stand: <Datum>

OFFENE AUFGABEN:
[ ] <Aufgabe 1> - Aufwand: <NIEDRIG|MITTEL|HOCH>
[ ] <Aufgabe 2> - Aufwand: <NIEDRIG|MITTEL|HOCH>

---
ERLEDIGT (Archiv):
- <Erledigte Aufgabe> (<Version>, <Datum>)
```

### Status-Werte

| Status | Bedeutung |
|--------|-----------|
| NEU ENTDECKT | Noch nicht analysiert |
| ANALYSE NÖTIG | Feature-Analyse läuft |
| QUALITÄTSPRÜFUNG | Code-Tests laufen |
| VALIDIERT & BEREIT | Bereit für Features |
| MVP | Minimum Viable Product |
| NUR KOMPILIEREN | Nur noch Kompilierung nötig |
| GESPERRT | Wartet auf User-Test/Entscheidung |

---

## Phase 4: Scanner-Integration

Nach Abschluss der Phasen 1-3:

1. **Scanner ausführen:** `python scanner.py`
2. **Prüfen:** TASKS_all.md enthält neue Aufgaben
3. **Kategorisierung prüfen:** Ordner in SINGLE/, TOOLS/, SUITEN/ korrekt?

### Automatische Onboarding-Tasks (NEU)

Der Scanner erkennt **automatisch neue Tools** beim Scan und erstellt System-Tasks:

| Task-ID | Aufgabe | Aufwand |
|---------|---------|---------|
| onb_*_1 | Feature-Analyse erstellen | mittel |
| onb_*_2 | Code-Qualitätsprüfung | niedrig |
| onb_*_3 | AUFGABEN.txt erstellen | niedrig |

Diese Tasks erscheinen in `system-tasks.json` mit Abhängigkeiten (2 hängt von 1 ab, 3 hängt von 2 ab).

---

## Schnell-Checkliste

```
□ 1. Feature_Analyse_<Name>.md erstellt
□ 2. c_method_analyzer.py auf Hauptdatei angewandt
□ 3. c_encoding_fixer.py geprüft
□ 4. AUFGABEN.txt erstellt mit Status
□ 5. Scanner ausgeführt
```

---

## Beispiel: Neues Tool "MyTool"

```bash
# 1. Feature-Analyse
→ Feature_Analyse_MyTool.md erstellen (siehe Template)

# 2. Code-Qualität
cd _BATCH\DEV_TOOLS
python c_method_analyzer.py "..\..\SINGLE\MyTool\main.py"
python c_encoding_fixer.py "..\..\SINGLE\MyTool\main.py"

# 3. AUFGABEN.txt
→ Im Tool-Ordner erstellen mit Status "QUALITÄTSPRÜFUNG"

# 4. Scanner
cd _BATCH
python scanner.py
```

---

## Verwandte Dokumente

- `DEV_TOOLS/README.md` - Tool-Dokumentation
- `SYSTEM/TASKS.md` - Task-Kategorien
- `SYSTEM/WORKFLOW.md` - Arbeitsabläufe

---

*Erstellt: 2026-01-10 | sys_224259*
