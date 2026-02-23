# Provenance: anthropic_docx

- **Source:** https://github.com/anthropics/skills
- **Path:** `skills/docx/scripts/`
- **Commit:** a5bcdd7
- **Date:** 2026-02-06
- **License:** Apache 2.0

## Contents

Word/DOCX manipulation tools:
- `accept_changes.py` - Accept tracked changes in DOCX
- `comment.py` - Add/manage comments in DOCX
- `office/` - Pack/unpack/validate Office XML formats
  - `pack.py` - Pack directory to DOCX/PPTX/XLSX
  - `unpack.py` - Unpack DOCX/PPTX/XLSX to directory
  - `validate.py` - Validate Office XML against schemas
  - `soffice.py` - LibreOffice integration
  - `helpers/` - Merge runs, simplify redlines
  - `schemas/` - ECMA/ISO/Microsoft XSD schemas
  - `validators/` - Format-specific validators (docx, pptx, redlining)
- `templates/` - XML templates for comments

## Modifications

None. Verbatim copy from upstream.
