# EXPERTE: Literaturverwalter

## Status: AKTIV
Version: 1.0.0
Erstellt: 2026-03-01 (INT01: LitZentrum Integration)
Parent-Agent: persoenlicher-assistent

---

## 1. Ueberblick

Der Literaturverwalter unterstuetzt bei der wissenschaftlichen Literaturarbeit:
- **Quellenverwaltung** - Buecher, Artikel, Konferenzen, Websites erfassen und verwalten
- **Zitate sammeln** - Direkte/indirekte Zitate mit Seitenreferenzen
- **Zitation** - 5 Stile: APA (7th), MLA (9th), Chicago, DIN 1505-2, Harvard
- **BibTeX-Export** - Fuer LaTeX-Workflows
- **Zusammenfassungen** - Kapitel- oder Gesamt-Zusammenfassungen pro Quelle

Portiert aus LitZentrum Standalone (ordner-basiert -> SQLite).

---

## 2. Datenbank-Integration

### Tabellen in bach.db

| Tabelle | Beschreibung |
|---------|--------------|
| `lit_sources` | Quellen (Buecher, Artikel, etc.) mit Metadaten |
| `lit_quotes` | Zitate aus Quellen (direkt, indirekt, Paraphrase) |
| `lit_tasks` | Aufgaben pro Quelle oder projektweit |
| `lit_summaries` | Zusammenfassungen (manuell oder KI-generiert) |

### Beispiel-Queries

```sql
-- Alle ungelesenen Quellen
SELECT id, title, authors, year FROM lit_sources
WHERE read_status = 'unread' ORDER BY year DESC;

-- Zitate zu einer Quelle
SELECT q.text, q.page, q.quote_type, q.comment
FROM lit_quotes q
WHERE q.source_id = 1 ORDER BY q.page;

-- Quellen mit den meisten Zitaten
SELECT s.title, COUNT(q.id) as quote_count
FROM lit_sources s
LEFT JOIN lit_quotes q ON q.source_id = s.id
GROUP BY s.id ORDER BY quote_count DESC LIMIT 10;

-- Zusammenfassungen eines bestimmten Typs
SELECT s.title, sum.content
FROM lit_summaries sum
JOIN lit_sources s ON s.id = sum.source_id
WHERE sum.summary_type = 'abstract';
```

---

## 3. CLI-Befehle

```bash
# Quellen verwalten
bach literatur add "Titel" --author "Name" --year 2024
bach literatur list [--type article|book] [--status unread|read]
bach literatur search "Begriff"
bach literatur show <id>
bach literatur edit <id> --title "Neu" --status reading
bach literatur delete <id>

# Zitate
bach literatur quote <source_id> "Zitat-Text" --page 42
bach literatur quotes <source_id>

# Zitation & Export
bach literatur cite <id> --style apa|mla|chicago|din|harvard --page N
bach literatur export --all --out refs.bib

# Zusammenfassungen
bach literatur summary <source_id> "Text" --type full|chapter
bach literatur summary <source_id>   # anzeigen

# Statistik
bach literatur stats
```

---

## 4. Zitationsstile

| Stil | Standard | Beispiel (Inline) |
|------|----------|-------------------|
| APA | 7th Ed. | (Smith, 2024, S. 42) |
| MLA | 9th Ed. | (Smith 42) |
| Chicago | Notes-Bib | (Smith 2024, 42) |
| DIN | 1505-2 | [Smith 2024, S. 42] |
| Harvard | - | (Smith, 2024, p. 42) |

---

## 5. Quelltypen

- `article` - Zeitschriftenartikel (Standard)
- `book` - Buch
- `chapter` - Buchkapitel
- `thesis` - Dissertation/Abschlussarbeit
- `conference` - Konferenzbeitrag
- `website` - Webseite
- `other` - Sonstige

---

## 6. Integration mit Parent-Agent

Der Persoenliche Assistent kann:
- Ungelesene Quellen im Morgenbriefing erwaehnen
- Zitate fuer aktuelle Projekte vorschlagen
- BibTeX-Export bei Bedarf generieren
- Zusammenfassungen mit KI erstellen lassen

---

## 7. Abhaengigkeiten

```
sqlite3 (stdlib)
json (stdlib)
```

Keine externen Dependencies erforderlich.

---

## 8. Roadmap

### Phase 1 (DONE - INT01, v3.3.0)
- [x] DB-Schema (Migration 026)
- [x] Citation Formatter (5 Stile + BibTeX)
- [x] CLI-Handler (13 Operationen)
- [x] Expert-Profil + Tests

### Phase 2 (PLANNED)
- [ ] DOI-Lookup (Metadaten automatisch abrufen)
- [ ] BibTeX-Import (aus .bib Dateien)
- [ ] PDF-Integration (Pfade verwalten, Vorschau)
- [ ] KI-Zusammenfassungen (Ollama/Claude)
