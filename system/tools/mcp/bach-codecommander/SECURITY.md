# Security Policy

## Overview

BACH CodeCommander MCP Server is a developer tool that analyzes and modifies source code files. It operates with the running user's filesystem permissions.

## Risk Assessment

### Medium Risk Tools
| Tool | Risk | Description |
|------|------|-------------|
| `cc_organize_imports` | Modifies source files | Changes Python import order |
| `cc_fix_json` | Modifies files | Repairs JSON content |
| `cc_fix_encoding` | Modifies files | Changes file encoding |
| `cc_cleanup_file` | Modifies files | Removes whitespace/BOM/NUL |
| `cc_fix_umlauts` | Modifies files | Replaces character sequences |
| `cc_md_to_pdf` | Creates files | Generates PDF output |

### Low Risk Tools (Read-Only)
| Tool | Description |
|------|-------------|
| `cc_analyze_code` | Reads and analyzes code |
| `cc_analyze_methods` | Reads and analyzes methods |
| `cc_extract_classes` | Reads and extracts class info |
| `cc_diagnose_imports` | Reads and diagnoses imports |
| `cc_validate_json` | Reads and validates JSON |
| `cc_scan_emoji` | Reads and scans for emojis |
| `cc_generate_licenses` | Reads installed packages |
| `cc_convert_format` | Reads input, writes output |

## Recommendations

- All file-modifying tools support `dry_run` and/or `create_backup` options
- Use `dry_run=true` to preview changes before applying
- Review changes before deploying to production
- This server is designed for local development use via stdio transport

## Reporting

Report security issues at https://github.com/lukisch/bach-codecommander-mcp/issues
