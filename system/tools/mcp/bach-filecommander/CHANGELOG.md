# Changelog

All notable changes to this project will be documented in this file.

## [1.4.1] - 2026-02-14

### Fixed
- `fc_md_to_html` completely rewritten: line-by-line parser instead of regex chain
- Added: nested lists, ordered lists, blockquotes, checkboxes, badge images, standalone images
- Added: bold+italic combo (`***text***`), proper `<thead>/<tbody>` tables
- Professional CSS: dark code blocks, colored headers, print-ready layout

## [1.4.0] - 2026-02-14

### Added
- `fc_fix_json` - Repair common JSON errors (BOM, trailing commas, single quotes, comments, NUL bytes)
- `fc_validate_json` - Validate JSON with detailed error position and context
- `fc_cleanup_file` - Clean files: remove BOM, NUL bytes, trailing whitespace, normalize line endings
- `fc_fix_encoding` - Fix Mojibake and double-encoded UTF-8 (27+ patterns for German, French, Spanish)
- `fc_folder_diff` - Track directory changes (new/modified/deleted files) with snapshots
- `fc_batch_rename` - Pattern-based batch renaming (prefix/suffix removal, replace, auto-detect)
- `fc_convert_format` - Convert between JSON, CSV, and INI formats
- `fc_detect_duplicates` - Find duplicate files using SHA-256 hashing with size pre-filter
- `fc_md_to_html` - Convert Markdown to styled HTML (printable as PDF via browser)
- Total tools: 38

## [1.3.0] - 2026-02-14

### Changed
- Project prepared for public open-source release
- README rewritten in English for international audience
- Added LICENSE (MIT), SECURITY.md, CONTRIBUTING.md
- Package metadata updated for NPM publishing

## [1.2.1] - 2025-01-05

### Added
- `fc_str_replace` - String replacement tool with unique-match validation
- Total tools: 29

### Fixed
- `fc_safe_delete` PowerShell escaping for paths with special characters
- `&` character handling in Windows paths (PowerShell fallback)

## [1.2.0] - 2025-01-05

### Added
- Async Search system (5 tools): `fc_start_search`, `fc_get_search_results`, `fc_stop_search`, `fc_list_searches`, `fc_clear_search`
- `fc_safe_delete` - Moves files to Recycle Bin (Windows) or Trash (macOS/Linux) instead of permanent deletion

## [1.1.0] - 2025-01-05

### Added
- `fc_read_multiple_files` - Read multiple files in one call
- `fc_edit_file` - Line-based file editing (replace/insert/delete)
- `fc_list_processes` - List running system processes
- `fc_kill_process` - Terminate processes by PID or name
- Interactive Sessions (4 tools): `fc_start_session`, `fc_read_output`, `fc_send_input`, `fc_close_session`

## [1.0.0] - 2025-01-05

### Added
- Initial release with 13 filesystem tools
- File operations: read, write, list, create directory, delete, move, copy, file info, search
- Process execution: `fc_execute_command`, `fc_start_process`
- System: `fc_get_time`
