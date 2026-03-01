# EXPERTE: Press (Pressemitteilungen & Positionspapiere)

## Status: AKTIV
Version: 1.0.0
Erstellt: 2026-02-19
Parent-Agent: production

---

## 1. Ueberblick

Der Press-Experte erstellt professionelle Dokumente via LaTeX:
- **Pressemitteilungen** - fuer Medien und Oeffentlichkeit
- **Positionspapiere** - fuer akademische/politische Kontexte

Features:
- LaTeX-Templates mit Logo-Platzhalter
- PDF-Kompilierung via pdflatex/xelatex
- Email-Versand ueber das bestehende Notify-System
- Versionierung und Archivierung in der DB

## 2. Voraussetzungen

- MiKTeX (pdflatex/xelatex) installiert
- LaTeX-Pakete: geometry, fancyhdr, graphicx, hyperref, babel

## 3. Befehle

```
bach press create --type pressemitteilung --title "..." [--body "..."]
bach press create --type positionspapier --title "..." [--body "..."]
bach press templates                    Verfuegbare Templates
bach press list                         Alle Dokumente
bach press show <id>                    Dokument anzeigen
bach press send <id> --to <email>       Per Email versenden
bach press config [--logo <path>] [--author "..."]  Konfiguration
```

## 4. Datenbank

Tabelle: `press_documents`
- doc_type, title, body, metadata_json, pdf_path, status, sent_to, sent_at

## 5. Templates

- `pressemitteilung.tex` - Professionelles Pressemitteilungs-Layout
- `positionspapier.tex` - Akademisches Layout mit Inhaltsverzeichnis
