# Vendor: Externe Quellcode-Kopien

Kopien von externem Code, der in BACH-Services integriert wird.
Diese Dateien leben in BACH und werden hier gepflegt.

## Dateien

| Datei | Quelle | Zweck |
|-------|--------|-------|
| `redaction_detector.py` | DokuZentrum (`Software Entwicklung/SUITEN/DokuZentrum/core/redaction/detector.py`) | Regex+Fuzzy+Blacklist Erkennung sensibler Daten |
| `pdf_schwaerzer_pro.py` | PDFSchwärzer Pro (`Software Entwicklung/TOOLS/Docs/PDFSchwärzer Pro/PDF schwärzer pro V2.py`) | PDF-Schwärzung + AES-256 Encryption (pikepdf) + Format-Konvertierung |
| `anthropic_docx/` | github.com/anthropics/skills (skills/docx) | XML Pack/Unpack, Validate, Tracked Changes, Comments |
| `anthropic_pdf/` | github.com/anthropics/skills (skills/pdf) | PDF-Formular-Extraktion, Ausfuellung, Konvertierung |
| `anthropic_xlsx/` | github.com/anthropics/skills (skills/xlsx) | Excel Recalc, Office XML Pack/Unpack/Validate |

## Integration

Der `anonymizer_service.py` nutzt aus diesen Quellen:

- **Von redaction_detector.py:** `RedactionDetector` (Regex-Erkennung, Blacklist, Fuzzy-Matching), `RedactionApplier` (PDF-Schwärzung via PyMuPDF)
- **Von pdf_schwaerzer_pro.py:** AES-256 Encryption Pipeline (pikepdf, R=6), Format-Konvertierung (Word→PDF via win32com, Bild→PDF via PIL)

## Hybrid-Ansatz

```
detector.py Erkennung (stark)  +  PDFSchwärzer Pipeline (stark)
     ↓                                    ↓
Regex, Fuzzy, Blacklist          Redact → Temp → Encrypt → Finalize
     ↓                                    ↓
     └──────── anonymizer_service.py ──────┘
```

## Kopiert am

- 2026-01-27: redaction_detector.py, pdf_schwaerzer_pro.py (Session session_20260127_012318)
- 2026-02-06: anthropic_docx/, anthropic_pdf/, anthropic_xlsx/ (Commit a5bcdd7)
