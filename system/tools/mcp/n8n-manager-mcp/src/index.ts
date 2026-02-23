#!/usr/bin/env node
/**
 * n8n Manager MCP Server
 *
 * MCP server for managing n8n workflows via AI assistants (Claude, Cursor, etc.).
 * Connects directly to n8n servers via REST API.
 *
 * @author Lukas Geiger
 * @version 0.1.0
 * @license MIT
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import * as fs from "fs/promises";
import * as fsSync from "fs";
import * as path from "path";
import { homedir } from "os";

// ============================================================================
// Types
// ============================================================================

interface N8nServer {
  name: string;
  url: string;
  apiKey: string;
  isDefault: boolean;
}

interface ServerConfig {
  servers: N8nServer[];
}

// ============================================================================
// Configuration
// ============================================================================

const CONFIG_DIR = path.join(homedir(), ".n8n-manager-mcp");
const CONFIG_FILE = path.join(CONFIG_DIR, "servers.json");

async function ensureConfigDir(): Promise<void> {
  try {
    await fs.mkdir(CONFIG_DIR, { recursive: true });
  } catch { /* exists */ }
}

async function loadConfig(): Promise<ServerConfig> {
  await ensureConfigDir();
  try {
    const data = await fs.readFile(CONFIG_FILE, "utf-8");
    return JSON.parse(data);
  } catch {
    return { servers: [] };
  }
}

async function saveConfig(config: ServerConfig): Promise<void> {
  await ensureConfigDir();
  await fs.writeFile(CONFIG_FILE, JSON.stringify(config, null, 2), "utf-8");
}

function getDefaultServer(config: ServerConfig): N8nServer | undefined {
  return config.servers.find(s => s.isDefault) || config.servers[0];
}

function getServerByName(config: ServerConfig, name: string): N8nServer | undefined {
  return config.servers.find(s => s.name === name);
}

// ============================================================================
// n8n API Client
// ============================================================================

async function n8nRequest(
  server: N8nServer,
  method: string,
  endpoint: string,
  body?: unknown
): Promise<{ ok: boolean; status: number; data: unknown }> {
  const url = `${server.url.replace(/\/$/, "")}/api/v1${endpoint}`;
  const headers: Record<string, string> = {
    "X-N8N-API-KEY": server.apiKey,
    "Content-Type": "application/json",
    "Accept": "application/json",
  };

  try {
    const opts: RequestInit = { method, headers };
    if (body && method !== "GET") {
      opts.body = JSON.stringify(body);
    }
    const resp = await fetch(url, opts);
    const data = resp.ok ? await resp.json().catch(() => ({})) : { error: await resp.text() };
    return { ok: resp.ok, status: resp.status, data };
  } catch (e: unknown) {
    const msg = e instanceof Error ? e.message : String(e);
    return { ok: false, status: 0, data: { error: msg } };
  }
}

// ============================================================================
// Server
// ============================================================================

const server = new McpServer({
  name: "n8n-manager-mcp",
  version: "0.1.0",
});

// ── Tool: n8n_list_workflows ─────────────────────────────────────────

server.tool(
  "n8n_list_workflows",
  "List all workflows on an n8n server. Returns workflow names, IDs, active status, and node counts.",
  {
    server_name: z.string().optional().describe("Server name from config. Uses default if omitted."),
    limit: z.number().optional().default(100).describe("Max number of workflows to return"),
  },
  async ({ server_name, limit }) => {
    const config = await loadConfig();
    const srv = server_name ? getServerByName(config, server_name) : getDefaultServer(config);
    if (!srv) return { content: [{ type: "text" as const, text: "Error: No server configured. Use n8n_add_server first." }] };

    const result = await n8nRequest(srv, "GET", `/workflows?limit=${limit}`);
    if (!result.ok) return { content: [{ type: "text" as const, text: `Error ${result.status}: ${JSON.stringify(result.data)}` }] };

    const workflows = (result.data as { data?: unknown[] })?.data || [];
    const lines = [`Workflows on ${srv.name} (${srv.url}):\n`];
    for (const wf of workflows as Array<{ id: string; name: string; active: boolean; nodes?: unknown[] }>) {
      const nodeCount = wf.nodes?.length || 0;
      const status = wf.active ? "ACTIVE" : "inactive";
      lines.push(`  [${wf.id}] ${wf.name} (${nodeCount} nodes, ${status})`);
    }
    if (workflows.length === 0) lines.push("  No workflows found.");

    return { content: [{ type: "text" as const, text: lines.join("\n") }] };
  }
);

// ── Tool: n8n_get_workflow ───────────────────────────────────────────

server.tool(
  "n8n_get_workflow",
  "Get detailed information about a specific n8n workflow including all nodes, connections, and settings.",
  {
    workflow_id: z.string().describe("n8n workflow ID"),
    server_name: z.string().optional().describe("Server name. Uses default if omitted."),
  },
  async ({ workflow_id, server_name }) => {
    const config = await loadConfig();
    const srv = server_name ? getServerByName(config, server_name) : getDefaultServer(config);
    if (!srv) return { content: [{ type: "text" as const, text: "Error: No server configured." }] };

    const result = await n8nRequest(srv, "GET", `/workflows/${workflow_id}`);
    if (!result.ok) return { content: [{ type: "text" as const, text: `Error ${result.status}: ${JSON.stringify(result.data)}` }] };

    return { content: [{ type: "text" as const, text: JSON.stringify(result.data, null, 2) }] };
  }
);

// ── Tool: n8n_create_workflow ────────────────────────────────────────

server.tool(
  "n8n_create_workflow",
  "Create a new n8n workflow. Provide the full workflow JSON including nodes and connections.",
  {
    name: z.string().describe("Workflow name"),
    nodes: z.array(z.object({
      type: z.string().describe("n8n node type, e.g. 'n8n-nodes-base.webhook'"),
      name: z.string().describe("Node display name"),
      parameters: z.record(z.unknown()).optional().describe("Node parameters"),
      position: z.array(z.number()).optional().describe("[x, y] position"),
    })).describe("Array of workflow nodes"),
    connections: z.array(z.object({
      from_node: z.string().describe("Source node name"),
      to_node: z.string().describe("Target node name"),
      from_output: z.number().optional().default(0),
      to_input: z.number().optional().default(0),
    })).optional().describe("Array of connections between nodes"),
    server_name: z.string().optional().describe("Server name. Uses default if omitted."),
    activate: z.boolean().optional().default(false).describe("Activate workflow after creation"),
  },
  async ({ name, nodes, connections, server_name, activate }) => {
    const config = await loadConfig();
    const srv = server_name ? getServerByName(config, server_name) : getDefaultServer(config);
    if (!srv) return { content: [{ type: "text" as const, text: "Error: No server configured." }] };

    // Build n8n workflow JSON
    const n8nNodes = nodes.map((n, i) => ({
      parameters: n.parameters || {},
      type: n.type,
      typeVersion: 1,
      position: n.position || [250 * i, 300],
      name: n.name,
    }));

    const n8nConnections: Record<string, { main: Array<Array<{ node: string; type: string; index: number }>> }> = {};
    if (connections) {
      for (const conn of connections) {
        if (!n8nConnections[conn.from_node]) {
          n8nConnections[conn.from_node] = { main: [[]] };
        }
        const main = n8nConnections[conn.from_node].main;
        while (main.length <= (conn.from_output || 0)) main.push([]);
        main[conn.from_output || 0].push({
          node: conn.to_node,
          type: "main",
          index: conn.to_input || 0,
        });
      }
    }

    const workflow = {
      name,
      nodes: n8nNodes,
      connections: n8nConnections,
      settings: { executionOrder: "v1" },
    };

    const result = await n8nRequest(srv, "POST", "/workflows", workflow);
    if (!result.ok) return { content: [{ type: "text" as const, text: `Error ${result.status}: ${JSON.stringify(result.data)}` }] };

    const created = result.data as { id?: string; name?: string };
    const createdId = created.id || "unknown";

    // Activate separately via PATCH (POST rejects 'active' field)
    if (activate && createdId !== "unknown") {
      const actResult = await n8nRequest(srv, "PATCH", `/workflows/${createdId}`, { active: true });
      if (!actResult.ok) {
        return { content: [{ type: "text" as const, text: `Workflow created (ID: ${createdId}) but activation failed: ${JSON.stringify(actResult.data)}` }] };
      }
    }

    return { content: [{ type: "text" as const, text: `Workflow created: "${created.name || name}" (ID: ${createdId})${activate ? " [ACTIVE]" : ""} on ${srv.name}` }] };
  }
);

// ── Tool: n8n_update_workflow ────────────────────────────────────────

server.tool(
  "n8n_update_workflow",
  "Update an existing n8n workflow. Send the full updated workflow JSON.",
  {
    workflow_id: z.string().describe("n8n workflow ID to update"),
    workflow_json: z.string().describe("Full workflow JSON as string"),
    server_name: z.string().optional().describe("Server name. Uses default if omitted."),
  },
  async ({ workflow_id, workflow_json, server_name }) => {
    const config = await loadConfig();
    const srv = server_name ? getServerByName(config, server_name) : getDefaultServer(config);
    if (!srv) return { content: [{ type: "text" as const, text: "Error: No server configured." }] };

    let data: unknown;
    try { data = JSON.parse(workflow_json); } catch (e) {
      return { content: [{ type: "text" as const, text: `Invalid JSON: ${e}` }] };
    }

    const result = await n8nRequest(srv, "PUT", `/workflows/${workflow_id}`, data);
    if (!result.ok) return { content: [{ type: "text" as const, text: `Error ${result.status}: ${JSON.stringify(result.data)}` }] };

    return { content: [{ type: "text" as const, text: `Workflow ${workflow_id} updated successfully on ${srv.name}` }] };
  }
);

// ── Tool: n8n_delete_workflow ────────────────────────────────────────

server.tool(
  "n8n_delete_workflow",
  "Delete a workflow from an n8n server. This action cannot be undone.",
  {
    workflow_id: z.string().describe("n8n workflow ID to delete"),
    server_name: z.string().optional().describe("Server name. Uses default if omitted."),
  },
  async ({ workflow_id, server_name }) => {
    const config = await loadConfig();
    const srv = server_name ? getServerByName(config, server_name) : getDefaultServer(config);
    if (!srv) return { content: [{ type: "text" as const, text: "Error: No server configured." }] };

    const result = await n8nRequest(srv, "DELETE", `/workflows/${workflow_id}`);
    if (!result.ok) return { content: [{ type: "text" as const, text: `Error ${result.status}: ${JSON.stringify(result.data)}` }] };

    return { content: [{ type: "text" as const, text: `Workflow ${workflow_id} deleted from ${srv.name}` }] };
  }
);

// ── Tool: n8n_activate_workflow ──────────────────────────────────────

server.tool(
  "n8n_activate_workflow",
  "Activate or deactivate an n8n workflow.",
  {
    workflow_id: z.string().describe("n8n workflow ID"),
    active: z.boolean().describe("true to activate, false to deactivate"),
    server_name: z.string().optional().describe("Server name. Uses default if omitted."),
  },
  async ({ workflow_id, active, server_name }) => {
    const config = await loadConfig();
    const srv = server_name ? getServerByName(config, server_name) : getDefaultServer(config);
    if (!srv) return { content: [{ type: "text" as const, text: "Error: No server configured." }] };

    const result = await n8nRequest(srv, "PATCH", `/workflows/${workflow_id}`, { active });
    if (!result.ok) return { content: [{ type: "text" as const, text: `Error ${result.status}: ${JSON.stringify(result.data)}` }] };

    return { content: [{ type: "text" as const, text: `Workflow ${workflow_id} ${active ? "activated" : "deactivated"} on ${srv.name}` }] };
  }
);

// ── Tool: n8n_list_executions ────────────────────────────────────────

server.tool(
  "n8n_list_executions",
  "List recent workflow executions on an n8n server. Shows status, timing, and errors.",
  {
    workflow_id: z.string().optional().describe("Filter by workflow ID"),
    status: z.enum(["success", "error", "waiting"]).optional().describe("Filter by status"),
    limit: z.number().optional().default(20).describe("Max results"),
    server_name: z.string().optional().describe("Server name. Uses default if omitted."),
  },
  async ({ workflow_id, status, limit, server_name }) => {
    const config = await loadConfig();
    const srv = server_name ? getServerByName(config, server_name) : getDefaultServer(config);
    if (!srv) return { content: [{ type: "text" as const, text: "Error: No server configured." }] };

    let endpoint = `/executions?limit=${limit}`;
    if (workflow_id) endpoint += `&workflowId=${workflow_id}`;
    if (status) endpoint += `&status=${status}`;

    const result = await n8nRequest(srv, "GET", endpoint);
    if (!result.ok) return { content: [{ type: "text" as const, text: `Error ${result.status}: ${JSON.stringify(result.data)}` }] };

    const executions = (result.data as { data?: unknown[] })?.data || [];
    const lines = [`Recent executions on ${srv.name}:\n`];
    for (const ex of executions as Array<{ id: string; workflowId: string; status: string; startedAt: string; stoppedAt: string; workflowData?: { name: string } }>) {
      const name = ex.workflowData?.name || `WF#${ex.workflowId}`;
      const duration = ex.stoppedAt && ex.startedAt
        ? `${((new Date(ex.stoppedAt).getTime() - new Date(ex.startedAt).getTime()) / 1000).toFixed(1)}s`
        : "running";
      lines.push(`  [${ex.id}] ${name} -- ${ex.status.toUpperCase()} (${duration})`);
    }
    if (executions.length === 0) lines.push("  No executions found.");

    return { content: [{ type: "text" as const, text: lines.join("\n") }] };
  }
);

// ── Tool: n8n_add_server ─────────────────────────────────────────────

server.tool(
  "n8n_add_server",
  "Add or update an n8n server connection. The API key can be created in n8n under Settings > API.",
  {
    name: z.string().describe("Server name (e.g. 'production', 'staging')"),
    url: z.string().describe("n8n server URL (e.g. 'http://localhost:5678')"),
    api_key: z.string().describe("n8n API key (from Settings > API in n8n)"),
    is_default: z.boolean().optional().default(false).describe("Set as default server"),
  },
  async ({ name, url, api_key, is_default }) => {
    const config = await loadConfig();

    // Remove existing server with same name
    config.servers = config.servers.filter(s => s.name !== name);

    // If is_default, clear other defaults
    if (is_default) {
      config.servers.forEach(s => s.isDefault = false);
    }

    config.servers.push({ name, url: url.replace(/\/$/, ""), apiKey: api_key, isDefault: is_default || config.servers.length === 0 });
    await saveConfig(config);

    return { content: [{ type: "text" as const, text: `Server "${name}" added (${url}). ${is_default ? "Set as default." : ""}` }] };
  }
);

// ── Tool: n8n_list_servers ───────────────────────────────────────────

server.tool(
  "n8n_list_servers",
  "List all configured n8n server connections.",
  {},
  async () => {
    const config = await loadConfig();
    if (config.servers.length === 0) {
      return { content: [{ type: "text" as const, text: "No servers configured. Use n8n_add_server to add one." }] };
    }

    const lines = ["Configured n8n servers:\n"];
    for (const s of config.servers) {
      const def = s.isDefault ? " [DEFAULT]" : "";
      const keyHint = s.apiKey ? ` (key: ${s.apiKey.substring(0, 8)}...)` : " (no key)";
      lines.push(`  ${s.name}: ${s.url}${keyHint}${def}`);
    }

    return { content: [{ type: "text" as const, text: lines.join("\n") }] };
  }
);

// ── Tool: n8n_ping_server ────────────────────────────────────────────

server.tool(
  "n8n_ping_server",
  "Test the connection to an n8n server.",
  {
    server_name: z.string().optional().describe("Server name. Uses default if omitted."),
  },
  async ({ server_name }) => {
    const config = await loadConfig();
    const srv = server_name ? getServerByName(config, server_name) : getDefaultServer(config);
    if (!srv) return { content: [{ type: "text" as const, text: "Error: No server configured." }] };

    const start = Date.now();
    const result = await n8nRequest(srv, "GET", "/workflows?limit=1");
    const elapsed = Date.now() - start;

    if (result.ok) {
      return { content: [{ type: "text" as const, text: `Server "${srv.name}" (${srv.url}) is reachable. Response time: ${elapsed}ms` }] };
    } else {
      return { content: [{ type: "text" as const, text: `Server "${srv.name}" (${srv.url}) unreachable. Status: ${result.status}, Error: ${JSON.stringify(result.data)}` }] };
    }
  }
);

// ── Tool: n8n_remove_server ──────────────────────────────────────────

server.tool(
  "n8n_remove_server",
  "Remove an n8n server from the configuration.",
  {
    server_name: z.string().describe("Name of the server to remove"),
  },
  async ({ server_name }) => {
    const config = await loadConfig();
    const before = config.servers.length;
    config.servers = config.servers.filter(s => s.name !== server_name);

    if (config.servers.length === before) {
      return { content: [{ type: "text" as const, text: `Server "${server_name}" not found.` }] };
    }

    // Ensure a default exists
    if (config.servers.length > 0 && !config.servers.some(s => s.isDefault)) {
      config.servers[0].isDefault = true;
    }

    await saveConfig(config);
    return { content: [{ type: "text" as const, text: `Server "${server_name}" removed.` }] };
  }
);

// ── Tool: n8n_export_workflow ────────────────────────────────────────

server.tool(
  "n8n_export_workflow",
  "Export a workflow from an n8n server as JSON. Returns the complete workflow definition that can be imported into another n8n instance.",
  {
    workflow_id: z.string().describe("n8n workflow ID to export"),
    server_name: z.string().optional().describe("Server name. Uses default if omitted."),
  },
  async ({ workflow_id, server_name }) => {
    const config = await loadConfig();
    const srv = server_name ? getServerByName(config, server_name) : getDefaultServer(config);
    if (!srv) return { content: [{ type: "text" as const, text: "Error: No server configured." }] };

    const result = await n8nRequest(srv, "GET", `/workflows/${workflow_id}`);
    if (!result.ok) return { content: [{ type: "text" as const, text: `Error ${result.status}: ${JSON.stringify(result.data)}` }] };

    // Clean export (remove server-specific fields that n8n rejects on POST)
    const wf = result.data as Record<string, unknown>;
    delete wf.id;
    delete wf.tags;
    delete wf.active;
    delete wf.createdAt;
    delete wf.updatedAt;
    delete wf.versionId;

    return { content: [{ type: "text" as const, text: JSON.stringify(wf, null, 2) }] };
  }
);

// ── Tool: n8n_import_workflow ────────────────────────────────────────

server.tool(
  "n8n_import_workflow",
  "Import a workflow JSON onto an n8n server. Takes a full n8n workflow JSON and creates it on the server.",
  {
    workflow_json: z.string().describe("Complete n8n workflow JSON as string"),
    server_name: z.string().optional().describe("Target server name. Uses default if omitted."),
    activate: z.boolean().optional().default(false).describe("Activate after import"),
  },
  async ({ workflow_json, server_name, activate }) => {
    const config = await loadConfig();
    const srv = server_name ? getServerByName(config, server_name) : getDefaultServer(config);
    if (!srv) return { content: [{ type: "text" as const, text: "Error: No server configured." }] };

    let data: Record<string, unknown>;
    try { data = JSON.parse(workflow_json); } catch (e) {
      return { content: [{ type: "text" as const, text: `Invalid JSON: ${e}` }] };
    }

    // Ensure required fields
    if (!data.nodes || !data.connections) {
      return { content: [{ type: "text" as const, text: "Invalid workflow: missing 'nodes' or 'connections'" }] };
    }

    // Strip fields that n8n rejects on POST /workflows
    for (const key of ["id", "tags", "active", "createdAt", "updatedAt", "versionId"]) {
      delete data[key];
    }

    const result = await n8nRequest(srv, "POST", "/workflows", data);
    if (!result.ok) return { content: [{ type: "text" as const, text: `Error ${result.status}: ${JSON.stringify(result.data)}` }] };

    const created = result.data as { id?: string; name?: string };
    const createdId = created.id || "unknown";

    // Activate separately via PATCH (POST rejects 'active' field)
    if (activate && createdId !== "unknown") {
      const actResult = await n8nRequest(srv, "PATCH", `/workflows/${createdId}`, { active: true });
      if (!actResult.ok) {
        return { content: [{ type: "text" as const, text: `Workflow imported (ID: ${createdId}) but activation failed: ${JSON.stringify(actResult.data)}` }] };
      }
    }

    return { content: [{ type: "text" as const, text: `Workflow imported: "${created.name}" (ID: ${createdId})${activate ? " [ACTIVE]" : ""} on ${srv.name}` }] };
  }
);

// ── Tool: n8n_describe_nodes ─────────────────────────────────────────

server.tool(
  "n8n_describe_nodes",
  "Get information about common n8n node types. Useful for understanding which nodes to use when building workflows.",
  {
    category: z.enum(["trigger", "action", "logic", "transform", "ai", "all"]).optional().default("all").describe("Filter by category"),
  },
  async ({ category }) => {
    const catalog = [
      { type: "n8n-nodes-base.manualTrigger", name: "Manual Trigger", cat: "trigger", desc: "Start workflow manually from n8n UI" },
      { type: "n8n-nodes-base.scheduleTrigger", name: "Schedule Trigger", cat: "trigger", desc: "Cron-based scheduling. Params: rule.interval[].field='cronExpression', expression='0 9 * * *'" },
      { type: "n8n-nodes-base.webhook", name: "Webhook", cat: "trigger", desc: "HTTP webhook endpoint. Params: path='/my-hook', httpMethod='POST'" },
      { type: "n8n-nodes-base.emailTrigger", name: "Email Trigger (IMAP)", cat: "trigger", desc: "Trigger on new emails via IMAP" },
      { type: "n8n-nodes-base.httpRequest", name: "HTTP Request", cat: "action", desc: "Make HTTP requests. Params: url, method, headers, body" },
      { type: "n8n-nodes-base.emailSend", name: "Send Email", cat: "action", desc: "Send emails via SMTP. Params: fromEmail, toEmail, subject, text" },
      { type: "n8n-nodes-base.slack", name: "Slack", cat: "action", desc: "Send messages to Slack channels" },
      { type: "n8n-nodes-base.telegram", name: "Telegram", cat: "action", desc: "Send messages via Telegram bot" },
      { type: "n8n-nodes-base.googleSheets", name: "Google Sheets", cat: "action", desc: "Read/write Google Sheets data" },
      { type: "n8n-nodes-base.if", name: "IF", cat: "logic", desc: "Conditional routing. Two outputs: true (index 0) and false (index 1)" },
      { type: "n8n-nodes-base.switch", name: "Switch", cat: "logic", desc: "Multi-path routing based on conditions" },
      { type: "n8n-nodes-base.merge", name: "Merge", cat: "logic", desc: "Merge data from multiple branches" },
      { type: "n8n-nodes-base.set", name: "Set", cat: "transform", desc: "Set/modify data fields" },
      { type: "n8n-nodes-base.code", name: "Code", cat: "transform", desc: "Execute custom JavaScript. Params: jsCode='return items;'" },
      { type: "n8n-nodes-base.splitInBatches", name: "Split In Batches", cat: "transform", desc: "Process items in batches" },
      { type: "n8n-nodes-base.aggregate", name: "Aggregate", cat: "transform", desc: "Aggregate multiple items into one" },
      { type: "@n8n/n8n-nodes-langchain.agent", name: "AI Agent", cat: "ai", desc: "LangChain-based AI agent with tools" },
      { type: "@n8n/n8n-nodes-langchain.chainLlm", name: "LLM Chain", cat: "ai", desc: "Simple LLM chain for text generation" },
      { type: "@n8n/n8n-nodes-langchain.openAi", name: "OpenAI", cat: "ai", desc: "Direct OpenAI API integration" },
    ];

    const filtered = category === "all" ? catalog : catalog.filter(n => n.cat === category);
    const lines = [`n8n Node Types (${category}):\n`];
    for (const n of filtered) {
      lines.push(`  [${n.cat.toUpperCase()}] ${n.type}`);
      lines.push(`    Name: ${n.name}`);
      lines.push(`    ${n.desc}\n`);
    }

    return { content: [{ type: "text" as const, text: lines.join("\n") }] };
  }
);

// ============================================================================
// Start Server
// ============================================================================

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
