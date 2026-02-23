# Changelog

All notable changes to this project will be documented in this file.

## [1.0.1] - 2026-02-14

### Fixed
- `cc_md_to_pdf` completely rewritten: line-by-line parser instead of regex chain
- Added: nested lists, ordered lists, blockquotes, checkboxes, badge images, standalone images
- Added: bold+italic combo (`***text***`), proper `<thead>/<tbody>` tables
- Professional CSS: dark code blocks, colored headers, print-ready layout

## [1.0.0] - 2026-02-14

### Added
- Initial release with 14 developer-focused tools
- Code Analysis: `cc_analyze_code`, `cc_analyze_methods`, `cc_extract_classes`
- Import Management: `cc_organize_imports`, `cc_diagnose_imports`
- JSON Tools: `cc_fix_json`, `cc_validate_json`
- Encoding & Text: `cc_fix_encoding`, `cc_cleanup_file`, `cc_fix_umlauts`, `cc_scan_emoji`
- Format Conversion: `cc_convert_format`
- Documentation: `cc_generate_licenses`, `cc_md_to_pdf`
