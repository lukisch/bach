# Epstein-Methode: Wissensindexierung

**Protokoll-ID:** `epstein_wissensindexierung`
**Version:** 1.0.0
**Datum:** 2026-02-21
**Status:** PRODUKTIV
**Kategorie:** Wissensmanagement, Dokumentation, LLM-Training

---

## Zweck

Die Epstein-Methode ist ein 4-stufiger Prozess zur systematischen Indexierung, Aufbereitung und Zusammenfassung großer Wissensbestände. Benannt nach dem Wissenschaftler der die Methode entwickelte.

**Kernidee:** Große Dokumente werden in handliche Chunks zerlegt, semantisch indexiert und mit LLM-generierten Zusammenfassungen angereichert. Das Ergebnis ist durchsuchbares, strukturiertes Wissen.

---

## Die 4 Stufen

### Stufe 1: INDEXIEREN
**Ziel:** Alle Wissensquellen erfassen und in eine durchsuchbare Datenbank aufnehmen.

**Schritte:**
1. **Quellen sammeln:** Alle .md, .txt, .py, .sql, .json Dateien aus definierten Verzeichnissen scannen
2. **Metadaten extrahieren:**
   - Pfad, Dateiname, Dateigröße
   - Erstellungs-/Änderungsdatum
   - SHA256-Hash (Duplikats-Erkennung)
3. **Tags generieren:** Aus Pfadstruktur automatisch Tags ableiten (ProFiler-Pattern)
   - Beispiel: `system/hub/upgrade.py` → Tags: `system`, `hub`, `upgrade`, `python`
4. **In DB schreiben:** `search_index` Tabelle befüllen

**Werkzeuge:**
- `tools/unified_search.py` (UnifiedSearch Engine)
- `tools/document_indexer.py` (falls vorhanden)

**Resultat:** Zentrale `search_index` Tabelle mit allen Dokumenten, inkl. Volltext + Tags.

---

### Stufe 2: ZERTEILEN
**Ziel:** Große Dokumente in handliche, überlappende Chunks aufteilen.

**Schritte:**
1. **Chunk-Größe festlegen:** 400 Tokens (ca. 300 Wörter)
2. **Overlap definieren:** 80 Tokens (20% Overlap für Kontext-Erhaltung)
3. **Dokument tokenisieren:** Einfache Wort-basierte Tokenisierung (Approximation)
4. **Chunks erstellen:** Sliding-Window-Ansatz mit Overlap
5. **Chunks speichern:** In `document_chunks` Tabelle (falls vorhanden) oder als JSON

**Werkzeuge:**
- `tools/document_chunker.py` (DocumentChunker Klasse)

**Resultat:** Jedes Dokument wird in N Chunks zerlegt (z.B. 10-Seiten-Doku → 25 Chunks).

**Warum Overlap?**
- Verhindert dass Sätze/Absätze an Chunk-Grenzen "zerrissen" werden
- Ermöglicht bessere semantische Suche (Context-Bleeding)

---

### Stufe 3: ZUSAMMENFASSEN
**Ziel:** Für jeden Chunk eine LLM-generierte Zusammenfassung erstellen.

**Schritte:**
1. **LLM-Modell wählen:** Haiku (schnell, günstig) oder Sonnet (präzise)
2. **Prompt-Template:**
   ```
   Fasse den folgenden Text-Chunk in 2-3 Sätzen zusammen.
   Fokus: Kernaussage, wichtigste Konzepte, technische Details.

   ---
   {chunk_text}
   ---

   Zusammenfassung:
   ```
3. **Batch-Processing:** Alle Chunks sequentiell durch LLM jagen (Rate-Limits beachten!)
4. **Zusammenfassungen speichern:** Als `summary` Feld in `document_chunks` Tabelle

**Werkzeuge:**
- Claude API (via `bach_api` oder direkt)
- Batch-Script (TODO: `tools/summarize_chunks.py`)

**Resultat:** Jeder Chunk hat eine prägnante Zusammenfassung (50-150 Tokens).

**Nutzen:**
- Schneller Überblick ohne ganzen Chunk lesen
- Bessere semantische Suche (Zusammenfassung als Suchindex)
- Training-Daten für Fine-Tuning (Chunk → Summary Paare)

---

### Stufe 4: PROTOKOLLIEREN
**Ziel:** Den Prozess wiederverwendbar und dokumentiert machen.

**Schritte:**
1. **Prozess-Log:** Welche Quellen wurden indexiert? Wann? Wie viele Chunks?
2. **Statistiken:** Anzahl Dokumente, Chunks, durchschnittliche Chunk-Größe, LLM-Kosten
3. **Fehler-Handling:** Welche Dateien konnten nicht verarbeitet werden? Warum?
4. **Versionierung:** DB-Schema-Version, Protokoll-Version, verwendetes LLM-Modell
5. **Reproduzierbarkeit:** Alle Parameter (chunk_size, overlap, Modell, Prompt) dokumentieren

**Werkzeuge:**
- `system_logs` Tabelle (BACH-intern)
- Separates `epstein_runs` Tabelle (TODO)

**Resultat:** Jede Indexierungs-Runde ist nachvollziehbar, wiederholbar und evaluierbar.

---

## Anwendungsfälle

1. **BACH Selbst-Dokumentation:**
   - Alle System-Dateien indexieren → Chunks → Zusammenfassungen
   - LLM kann "BACH-Wissen" abrufen ohne 5000+ Dateien zu lesen

2. **User-Projekt-Indexierung:**
   - User hat eigenes Software-Projekt → Epstein-Methode anwenden
   - LLM bekommt strukturiertes Projekt-Wissen

3. **Wiki/Docs-Generierung:**
   - Chunks + Summaries → Automatisch Wiki-Seiten generieren
   - Hierarchie: Dokument → Kapitel (= Chunk-Gruppen) → Absätze (= Chunks)

4. **Semantische Code-Suche:**
   - Code-Chunks mit Zusammenfassungen → "Finde alle Funktionen die X machen"
   - Hybrid-Suche: FTS5 (Keywords) + Embedding (Semantik) + Summary (Kontext)

5. **Training-Daten-Extraktion:**
   - Chunk/Summary-Paare als Fine-Tuning-Daten für eigenes Modell
   - "Lerne BACH-Kontext" → Spezialisiertes Mini-Modell

---

## Technische Details

### DB-Schema (Beispiel)

```sql
-- search_index: Bereits vorhanden (SQ064)
CREATE TABLE IF NOT EXISTS search_index (
    id INTEGER PRIMARY KEY,
    source_type TEXT,  -- 'file', 'wiki', 'memory', ...
    source_id TEXT,    -- Dateiname, Wiki-ID, ...
    path TEXT,
    title TEXT,
    content TEXT,      -- Volltext
    hash TEXT UNIQUE,  -- SHA256
    tags TEXT,         -- Komma-separiert
    word_count INTEGER,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- document_chunks: NEU (für Stufe 2+3)
CREATE TABLE IF NOT EXISTS document_chunks (
    id INTEGER PRIMARY KEY,
    search_index_id INTEGER,  -- FK zu search_index
    chunk_number INTEGER,     -- 0-basiert
    chunk_text TEXT,          -- Chunk-Inhalt
    chunk_tokens INTEGER,     -- Token-Anzahl
    summary TEXT,             -- LLM-Zusammenfassung (Stufe 3)
    created_at TIMESTAMP,
    FOREIGN KEY (search_index_id) REFERENCES search_index(id)
);

-- epstein_runs: NEU (für Stufe 4)
CREATE TABLE IF NOT EXISTS epstein_runs (
    id INTEGER PRIMARY KEY,
    started_at TIMESTAMP,
    finished_at TIMESTAMP,
    chunk_size INTEGER,
    overlap INTEGER,
    llm_model TEXT,           -- z.B. "haiku-3.5"
    llm_cost_usd REAL,        -- Geschätzte Kosten
    documents_indexed INTEGER,
    chunks_created INTEGER,
    chunks_summarized INTEGER,
    errors_count INTEGER,
    status TEXT,              -- 'running', 'completed', 'failed'
    log TEXT                  -- Fehler/Warnungen
);
```

### Parameter-Empfehlungen

| Parameter      | Empfohlen       | Begründung                                   |
|----------------|-----------------|----------------------------------------------|
| chunk_size     | 400 Tokens      | ~300 Wörter, passt in LLM-Context-Window     |
| overlap        | 80 Tokens       | 20% Overlap, erhält Kontext                  |
| LLM-Modell     | Haiku 3.5       | Schnell + günstig für Zusammenfassungen      |
| Batch-Größe    | 100 Chunks      | Rate-Limits beachten (z.B. 50 req/min)       |
| Prompt-Länge   | 50-100 Tokens   | Kurz halten → mehr Chunks pro Request        |

---

## CLI-Integration (TODO)

```bash
# Stufe 1: Indexieren
bach knowledge index <verzeichnis>

# Stufe 2: Chunken
bach knowledge chunk --chunk-size 400 --overlap 80

# Stufe 3: Zusammenfassen
bach knowledge summarize --model haiku --batch-size 100

# Alle Stufen in einem
bach knowledge epstein <verzeichnis> --all

# Status anzeigen
bach knowledge status
```

---

## Verwandte Protokolle

- `unified_search.md` — Semantische Suche (FTS5 + sqlite-vec)
- `translate_haiku.md` — LLM-Batch-Processing mit Haiku
- `document_indexing.md` — Allgemeine Dokumenten-Indexierung

---

## Changelog

**v1.0.0** (2026-02-21)
- Initial-Version
- 4 Stufen definiert (Indexieren, Zerteilen, Zusammenfassen, Protokollieren)
- DB-Schema entworfen
- CLI-Integration skizziert

---

## Nächste Schritte

1. **Stufe 3 implementieren:** `tools/summarize_chunks.py` schreiben
2. **CLI-Handler:** `hub/knowledge.py` (KnowledgeHandler)
3. **DB-Schema anlegen:** `document_chunks` + `epstein_runs` Tabellen
4. **Erste Test-Runde:** BACH-System selbst indexieren (5000+ Dateien)
5. **Evaluierung:** Qualität der Zusammenfassungen prüfen, ggf. Prompt anpassen

---

**Ende Protokoll**
