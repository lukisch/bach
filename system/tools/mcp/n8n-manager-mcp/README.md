# n8n Manager MCP Server

[![npm](https://img.shields.io/npm/v/n8n-manager-mcp.svg)](https://www.npmjs.com/package/n8n-manager-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MCP (Model Context Protocol) server for managing n8n workflows via AI assistants like Claude, Cursor, and Windsurf.

## Features

- **13 Tools** for complete n8n workflow management
- List, create, update, delete, and activate/deactivate workflows
- Multi-server support (connect to multiple n8n instances)
- Export/Import workflows between servers
- View execution history and status
- Built-in node catalog with descriptions
- Zero dependencies on Python -- connects directly to n8n REST API

## Installation

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "n8n-manager": {
      "command": "npx",
      "args": ["-y", "n8n-manager-mcp"]
    }
  }
}
```

### Claude Code

```bash
claude mcp add --scope user n8n-manager npx -y n8n-manager-mcp
```

### Manual

```bash
npm install -g n8n-manager-mcp
```

## Quick Start

After installation, use these commands in your AI assistant:

1. **Add your n8n server:**
   > "Add my n8n server at http://localhost:5678 with API key abc123"

2. **List workflows:**
   > "Show me all workflows on my n8n server"

3. **Create a workflow:**
   > "Create an n8n workflow that triggers on a webhook, fetches data from an API, and sends a Slack message"

4. **Check executions:**
   > "Show me the last 10 workflow executions"

## Available Tools

| Tool | Description |
|------|-------------|
| `n8n_list_workflows` | List all workflows on a server |
| `n8n_get_workflow` | Get workflow details (nodes, connections) |
| `n8n_create_workflow` | Create a new workflow from nodes + connections |
| `n8n_update_workflow` | Update an existing workflow |
| `n8n_delete_workflow` | Delete a workflow |
| `n8n_activate_workflow` | Activate or deactivate a workflow |
| `n8n_list_executions` | List recent executions with status |
| `n8n_export_workflow` | Export workflow as importable JSON |
| `n8n_import_workflow` | Import workflow JSON onto a server |
| `n8n_add_server` | Add/update n8n server connection |
| `n8n_list_servers` | List configured servers |
| `n8n_ping_server` | Test server connection |
| `n8n_remove_server` | Remove a server |
| `n8n_describe_nodes` | Browse available n8n node types |

## Configuration

Server connections are stored in `~/.n8n-manager-mcp/servers.json`.

## Related

- [n8n-workflow-manager](https://github.com/lukisch/n8n-workflow-manager) -- Full web UI + REST API for n8n workflow management (Python)
- [n8n](https://n8n.io/) -- The workflow automation platform

## License

MIT
