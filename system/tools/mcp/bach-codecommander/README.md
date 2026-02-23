# BACH CodeCommander MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![npm version](https://img.shields.io/npm/v/bach-codecommander-mcp.svg)](https://www.npmjs.com/package/bach-codecommander-mcp)
[![Node.js](https://img.shields.io/badge/node-%3E%3D18-brightgreen.svg)](https://nodejs.org/)

A developer-focused **Model Context Protocol (MCP) server** that gives AI assistants code analysis, JSON repair, encoding fix, import organization, and format conversion capabilities.

**14 tools** optimized for developers - the coding companion to [FileCommander](https://github.com/lukisch/bach-filecommander-mcp).

---

## Why CodeCommander?

While FileCommander handles filesystem operations, CodeCommander focuses on **code intelligence**:

- **Python Code Analysis** - AST-based class/method extraction, complexity metrics, import analysis
- **JSON Repair** - Fix broken JSON automatically (trailing commas, single quotes, BOM, comments)
- **Import Organization** - Sort and deduplicate Python imports per PEP 8
- **Encoding Fix** - Repair Mojibake and double-encoded UTF-8 (27+ patterns)
- **Umlaut Repair** - Fix broken German characters (70+ patterns)
- **Format Conversion** - Convert between JSON, CSV, and INI
- **Markdown Export** - Convert Markdown to professional HTML/PDF with code blocks, tables, nested lists, blockquotes
- **Cross-platform** - Works on Windows, macOS, and Linux

---

## Installation

### Prerequisites

- [Node.js](https://nodejs.org/) 18 or higher

### Option 1: Install from NPM

```bash
npm install -g bach-codecommander-mcp
```

### Option 2: Install from Source

```bash
git clone https://github.com/lukisch/bach-codecommander-mcp.git
cd bach-codecommander-mcp
npm install
npm run build
```

---

## Configuration

### Claude Desktop

Add to your `claude_desktop_config.json`:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

#### If installed globally via NPM:

```json
{
  "mcpServers": {
    "codecommander": {
      "command": "bach-codecommander"
    }
  }
}
```

#### If installed from source:

```json
{
  "mcpServers": {
    "codecommander": {
      "command": "node",
      "args": ["/absolute/path/to/bach-codecommander-mcp/dist/index.js"]
    }
  }
}
```

### Using Both Servers Together

FileCommander and CodeCommander are designed to work side by side:

```json
{
  "mcpServers": {
    "filecommander": {
      "command": "bach-filecommander"
    },
    "codecommander": {
      "command": "bach-codecommander"
    }
  }
}
```

---

## Tools Overview

### Code Analysis (3 tools)

| Tool | Description |
|------|-------------|
| `cc_analyze_code` | Full code analysis: classes, functions, imports, LOC, complexity |
| `cc_analyze_methods` | Detailed method analysis: params, decorators, visibility, data flow |
| `cc_extract_classes` | Extract Python classes/functions as separate text blocks |

### Import Management (2 tools)

| Tool | Description |
|------|-------------|
| `cc_organize_imports` | Sort & deduplicate Python imports per PEP 8 |
| `cc_diagnose_imports` | Detect unused imports, duplicates, circular import risks |

### JSON Tools (2 tools)

| Tool | Description |
|------|-------------|
| `cc_fix_json` | Repair broken JSON (BOM, trailing commas, comments, single quotes) |
| `cc_validate_json` | Validate JSON with detailed error position and context |

### Encoding & Text (3 tools)

| Tool | Description |
|------|-------------|
| `cc_fix_encoding` | Fix Mojibake / double-encoded UTF-8 (27+ patterns) |
| `cc_cleanup_file` | Remove BOM, NUL bytes, trailing whitespace, normalize line endings |
| `cc_fix_umlauts` | Repair broken German umlauts (70+ patterns, HTML entities, escapes) |

### Scanning (1 tool)

| Tool | Description |
|------|-------------|
| `cc_scan_emoji` | Scan files for emojis with codepoint info |

### Format & Documentation (2 tools)

| Tool | Description |
|------|-------------|
| `cc_convert_format` | Convert between JSON, CSV, and INI formats |
| `cc_generate_licenses` | Generate third-party license file (npm/pip) |

### Export (1 tool)

| Tool | Description |
|------|-------------|
| `cc_md_to_pdf` | Markdown to HTML: headers, code blocks, tables, nested lists, blockquotes, images, checkboxes |

**Total: 14 tools**

---

## Shared Tools

6 tools exist in both FileCommander and CodeCommander for convenience:

| FileCommander | CodeCommander | Function |
|---------------|---------------|----------|
| `fc_fix_json` | `cc_fix_json` | JSON repair |
| `fc_validate_json` | `cc_validate_json` | JSON validation |
| `fc_fix_encoding` | `cc_fix_encoding` | Encoding repair |
| `fc_cleanup_file` | `cc_cleanup_file` | File cleanup |
| `fc_convert_format` | `cc_convert_format` | Format conversion |
| `fc_md_to_html` | `cc_md_to_pdf` | Markdown to HTML export |

---

## Tool Prefix

All tools use the `cc_` prefix (CodeCommander) to avoid conflicts with FileCommander's `fc_` prefix and other MCP servers.

---

## Security

See [SECURITY.md](SECURITY.md) for detailed security information.

Key points:
- All file-modifying tools support `dry_run` mode
- Backup creation is enabled by default for destructive operations
- No built-in sandboxing - security is delegated to the MCP client
- Designed for local development use via stdio transport

---

## Development

```bash
npm install
npm run dev    # Watch mode
npm run build  # One-time build
npm start      # Start server
```

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for the full version history.

---

## License

[MIT](LICENSE) - Lukas (BACH)
