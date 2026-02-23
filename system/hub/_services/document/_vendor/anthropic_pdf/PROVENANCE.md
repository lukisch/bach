# Provenance: anthropic_pdf

- **Source:** https://github.com/anthropics/skills
- **Path:** `skills/pdf/scripts/`
- **Commit:** a5bcdd7
- **Date:** 2026-02-06
- **License:** Apache 2.0

## Contents

PDF manipulation tools:
- `check_bounding_boxes.py` - Validate PDF bounding box coordinates
- `check_fillable_fields.py` - Check if PDF has fillable form fields
- `convert_pdf_to_images.py` - Convert PDF pages to PNG images
- `create_validation_image.py` - Create visual validation overlay
- `extract_form_field_info.py` - Extract detailed field metadata
- `extract_form_structure.py` - Extract form structure (labels, lines, checkboxes)
- `fill_fillable_fields.py` - Fill PDF form fields programmatically
- `fill_pdf_form_with_annotations.py` - Fill non-fillable PDFs via annotations

## Dependencies

- `pypdf` - PDF reading/writing
- `pdfplumber` - PDF structure extraction
- `pdf2image` - PDF to image conversion (requires poppler)

## Modifications

None. Verbatim copy from upstream.
