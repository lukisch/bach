# Batch-Übersetzung mit Haiku (EN/DE/Multi-Language)

> **Ziel:** Systematische Übersetzung von BACH-Komponenten (help, wiki, skills) in mehrere Sprachen mit Claude Haiku (kostengünstig, schnell).

---

## Kontext & Anforderungen

### Warum Haiku?
- **Kostengünstig:** Batch-Übersetzung von 100+ Texten
- **Schnell:** Haiku ist der schnellste Claude-Modell
- **Ausreichend:** Übersetzungen brauchen keine Deep-Reasoning
- **Konsistent:** API-Calls sind reproduzierbar

### Anforderungen
- ✅ EN ist **Pflicht** für GitHub-Release (internationale Nutzer)
- ✅ DE ist **Standard** (Entwicklersprache)
- ✅ Weitere Sprachen optional (FR, ES, IT, etc.)
- ✅ Übersetzungen müssen in `lang_translations` Tabelle (bach.db)
- ✅ LangHandler muss dynamische Sprachen unterstützen (SQ062 ✅ erledigt)

---

## Phase 1: Vorbereitung (15 Min)

### 1.1 Inventar erstellen
```sql
-- Alle zu übersetzenden Texte identifizieren
SELECT category, key, COUNT(*)
FROM lang_translations
WHERE language = 'de'
GROUP BY category;
```

**Kategorien:**
- `help` - CLI-Hilfe-Texte (bach help <topic>)
- `wiki` - Wiki-Inhalte (generisch, nicht nutzerspezifisch)
- `skill` - Skill-Beschreibungen + Prompts
- `agent` - Agent-Beschreibungen
- `ui` - GUI-Labels (falls GUI mitgeliefert)

### 1.2 Scope festlegen
```
Kategorie    | DE (Quelle) | EN (Ziel) | Priorität
-------------|-------------|-----------|----------
help         | ~50 Texte   | 50        | KRITISCH
wiki         | ~30 Texte   | 30        | HOCH
skill        | ~40 Texte   | 40        | MITTEL
agent        | ~20 Texte   | 20        | MITTEL
ui           | ~15 Texte   | 15        | NIEDRIG
```

**Release-Blocker:** Nur `help` + `wiki` (EN) sind kritisch.

### 1.3 API-Zugriff prüfen
```bash
# Anthropic API Key vorhanden?
python -c "import os; print('OK' if os.getenv('ANTHROPIC_API_KEY') else 'FEHLT')"
```

---

## Phase 2: Batch-Script erstellen (30 Min)

### 2.1 Script-Struktur
```python
# tools/translate_batch.py
"""
Batch-Übersetzung von lang_translations via Claude Haiku API.

Usage:
  python translate_batch.py --source de --target en --category help
  python translate_batch.py --source de --target en --all
  python translate_batch.py --source de --target fr --category wiki
"""

import anthropic
from hub.tools.lang import LangHandler

def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """Übersetzt einen Text via Haiku API."""
    client = anthropic.Anthropic()

    prompt = f"""Translate the following text from {source_lang} to {target_lang}.
Keep markdown formatting, code blocks, and placeholders ({{variable}}) unchanged.
Output ONLY the translation, no explanations.

Text:
{text}
"""

    message = client.messages.create(
        model="claude-haiku-4-20250514",  # Haiku 4
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text.strip()

def batch_translate(source_lang: str, target_lang: str, category: str = None):
    """Übersetzt alle Texte einer Kategorie."""
    handler = LangHandler()

    # Texte laden
    if category:
        texts = handler.get_category_texts(source_lang, category)
    else:
        texts = handler.get_all_texts(source_lang)

    total = len(texts)
    print(f"[translate_batch] {total} Texte gefunden ({source_lang} → {target_lang})")

    for i, (key, text) in enumerate(texts.items(), 1):
        print(f"[{i}/{total}] {key}...", end=" ", flush=True)

        # Übersetzung durchführen
        try:
            translation = translate_text(text, source_lang, target_lang)
            handler.set_translation(target_lang, key, translation)
            print("✅")
        except Exception as e:
            print(f"❌ {e}")
            continue

    print(f"[translate_batch] Fertig! {i}/{total} übersetzt.")
```

### 2.2 Trockenlauf (Dry-Run)
```bash
# Nur 5 Texte zum Testen
python translate_batch.py --source de --target en --category help --limit 5 --dry-run
```

**Prüfen:**
- ✅ Markdown-Formatierung bleibt erhalten?
- ✅ Code-Blöcke unverändert?
- ✅ Platzhalter wie `{user}` bleiben?
- ✅ Ton/Stil passt (nicht zu formal/casual)?

---

## Phase 3: Batch-Übersetzung durchführen (1-2 Stunden)

### 3.1 Release-kritische Texte zuerst
```bash
# 1. help-Texte (EN Pflicht für Release)
python translate_batch.py --source de --target en --category help

# 2. wiki-Texte (EN Pflicht für Release)
python translate_batch.py --source de --target en --category wiki
```

### 3.2 Weitere Kategorien (optional)
```bash
# 3. skill-Texte (EN empfohlen)
python translate_batch.py --source de --target en --category skill

# 4. agent-Texte (EN empfohlen)
python translate_batch.py --source de --target en --category agent
```

### 3.3 Weitere Sprachen (nach Release)
```bash
# Französisch (Beispiel)
python translate_batch.py --source de --target fr --category help

# Spanisch (Beispiel)
python translate_batch.py --source de --target es --category help
```

---

## Phase 4: Qualitätssicherung (30 Min)

### 4.1 Stichproben prüfen
```python
# tools/check_translations.py
from hub.tools.lang import LangHandler

handler = LangHandler()

# 10 zufällige Übersetzungen prüfen
samples = handler.get_random_translations("en", n=10)
for key, de_text, en_text in samples:
    print(f"\n[{key}]")
    print(f"DE: {de_text[:100]}...")
    print(f"EN: {en_text[:100]}...")
    print("---")
```

**Prüfkriterien:**
- ✅ Technische Begriffe korrekt? (z.B. "Skill" bleibt "Skill", nicht "Fähigkeit")
- ✅ BACH-spezifische Terme erkannt? (Kernel, Hub, Bridge, Agent, Expert)
- ✅ Markdown korrekt? (Headlines, Listen, Code-Blöcke)
- ✅ Ton konsistent? (Nicht zu formal, nicht zu casual)

### 4.2 Vollständigkeit prüfen
```sql
-- Fehlende Übersetzungen finden
SELECT key, category
FROM lang_translations
WHERE language = 'de'
  AND key NOT IN (
    SELECT key FROM lang_translations WHERE language = 'en'
  );
```

### 4.3 Duplikate / Inkonsistenzen prüfen
```sql
-- Gleiche DE-Texte mit unterschiedlichen EN-Übersetzungen?
SELECT t1.text_de, GROUP_CONCAT(t2.text_en)
FROM lang_translations t1
JOIN lang_translations t2 ON t1.key = t2.key
WHERE t1.language = 'de' AND t2.language = 'en'
GROUP BY t1.text_de
HAVING COUNT(DISTINCT t2.text_en) > 1;
```

---

## Phase 5: Integration testen (15 Min)

### 5.1 CLI testen
```bash
# Sprache umschalten
bach lang set en

# help-Texte auf EN anzeigen
bach help skills
bach help agents
bach help wiki
```

### 5.2 Fallback-Logik testen
```bash
# Nicht existierende Sprache → Fallback zu EN/DE?
bach lang set fr
bach help skills  # Sollte FR anzeigen (falls vorhanden) oder EN/DE Fallback
```

### 5.3 GUI testen (falls relevant)
```bash
# GUI-Labels auf EN?
bach gui --lang en
```

---

## Phase 6: Dokumentation & Abschluss (15 Min)

### 6.1 Changelog aktualisieren
```markdown
## [v3.0.0-strawberry] - 2026-02-XX

### Added
- **Multi-Language Support:** BACH unterstützt jetzt EN/DE nativ.
  - 150+ Texte (help, wiki, skills) in EN verfügbar
  - Dynamisches Sprach-System (`bach lang set <code>`)
  - Weitere Sprachen erweiterbar via `bach lang add-language <code>`
```

### 6.2 README.md aktualisieren
```markdown
## 🌍 Languages

BACH supports:
- **English** (EN) - Full support (help, wiki, skills)
- **German** (DE) - Full support (native language)
- **French** (FR) - Partial (help only)
- **Spanish** (ES) - Partial (help only)

Change language:
\`\`\`bash
bach lang set en  # Switch to English
bach lang set de  # Switch to German
\`\`\`
```

### 6.3 SKILL.md / CLAUDE.md aktualisieren
```markdown
## Language Settings

BACH's default language is German (DE), but English (EN) is fully supported.

Use `bach lang set <code>` to switch languages.
Available: de, en, fr (partial), es (partial)
```

---

## Troubleshooting

### Problem: API-Rate-Limit
**Symptom:** `RateLimitError` nach 50+ Requests
**Lösung:**
```python
import time
time.sleep(1)  # 1 Sekunde Pause zwischen Requests
```

### Problem: Formatierung kaputt
**Symptom:** Markdown-Syntax falsch übersetzt (z.B. `**bold**` → `** fett **`)
**Lösung:** Prompt anpassen:
```
CRITICAL: Keep markdown syntax EXACTLY as is.
Examples:
- **bold** must stay **bold** (no spaces!)
- `code` must stay `code`
- [link](url) must stay [link](url)
```

### Problem: Technische Begriffe falsch
**Symptom:** "Skill" → "Fähigkeit", "Agent" → "Vertreter"
**Lösung:** Glossar im Prompt:
```
Technical terms to keep unchanged:
- Skill, Agent, Expert, Hub, Bridge, Kernel
- BACH (system name), Strawberry (release name)
- Task, Session, Context, Memory
```

### Problem: Zu formell / zu casual
**Symptom:** EN klingt zu steif ("Please utilize") oder zu locker ("Yo, just use")
**Lösung:** Ton-Vorgabe im Prompt:
```
Tone: Professional but friendly, like technical documentation.
Not too formal, not too casual. Similar to GitHub READMEs.
```

---

## Kosten-Schätzung

**Annahmen:**
- 150 Texte à 500 Token (Durchschnitt)
- Haiku 4: $0.30 / 1M Input-Token, $1.50 / 1M Output-Token
- Input: 150 × 500 + Prompts ~100k Token
- Output: 150 × 500 ~75k Token

**Rechnung:**
```
Input:  100k Token × $0.30/1M = $0.03
Output:  75k Token × $1.50/1M = $0.11
Total: ~$0.14 (14 Cent)
```

**Praktisch:** Mit Fehler-Retries und Qualitätsprüfungen ~$0.50 (50 Cent) für volle EN-Übersetzung.

---

## Checkliste

```markdown
## Batch-Übersetzung: DE → EN

### Vorbereitung
- [ ] Inventar erstellt (Kategorien + Anzahl)
- [ ] Scope festgelegt (help + wiki = Release-kritisch)
- [ ] API-Key geprüft (ANTHROPIC_API_KEY)
- [ ] Script erstellt (translate_batch.py)

### Durchführung
- [ ] Trockenlauf erfolgreich (5 Texte)
- [ ] help-Texte übersetzt (EN)
- [ ] wiki-Texte übersetzt (EN)
- [ ] skill-Texte übersetzt (EN, optional)
- [ ] agent-Texte übersetzt (EN, optional)

### Qualitätssicherung
- [ ] 10 Stichproben manuell geprüft
- [ ] Vollständigkeit geprüft (SQL-Check)
- [ ] Duplikate/Inkonsistenzen geprüft
- [ ] Markdown-Formatierung korrekt
- [ ] Technische Begriffe korrekt

### Integration
- [ ] CLI getestet (bach lang set en)
- [ ] help-Texte angezeigt (EN)
- [ ] Fallback-Logik getestet
- [ ] GUI getestet (falls relevant)

### Dokumentation
- [ ] CHANGELOG.md aktualisiert
- [ ] README.md aktualisiert (Languages-Sektion)
- [ ] SKILL.md / CLAUDE.md aktualisiert
```

---

## Nächste Schritte (nach Release)

1. **Community-Übersetzungen:** Nutzer können via PR weitere Sprachen beitragen
2. **Qualität verbessern:** Haiku → Sonnet für wichtige Texte (höhere Qualität)
3. **Automatisierung:** GitHub Action für automatische Übersetzung bei neuen DE-Texten
4. **Multilinguale Wiki:** Separate Wiki-Seiten pro Sprache

---

*Erstellt: 2026-02-19 | BACH v3.0.0-strawberry | SQ062*
