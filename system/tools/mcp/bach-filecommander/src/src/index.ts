#!/usr/bin/env node
/**
 * BACH FileCommander MCP Server
 *
 * A comprehensive MCP server for filesystem access, process management,
 * interactive sessions, and async file search.
 *
 * Copyright (c) 2025-2026 Lukas (BACH). Licensed under MIT License.
 * See LICENSE file for details.
 *
 * @author Lukas (BACH)
 * @version 1.4.0
 * @license MIT
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import * as fs from "fs/promises";
import * as fsSync from "fs";
import * as path from "path";
import * as crypto from "crypto";
import * as os from "os";
import { exec, spawn } from "child_process";
import { promisify } from "util";

const execAsync = promisify(exec);

// ============================================================================
// Server Initialization
// ============================================================================

const server = new McpServer({
  name: "bach-filecommander-mcp",
  version: "1.4.1"
});

// ============================================================================
// Process Session Management (für interaktive Prozesse)
// ============================================================================

interface ProcessSession {
  id: string;
  process: ReturnType<typeof spawn>;
  command: string;
  args: string[];
  cwd: string;
  startTime: Date;
  output: string[];
  isRunning: boolean;
}

const processSessions: Map<string, ProcessSession> = new Map();
let sessionCounter = 0;

function generateSessionId(): string {
  return `session_${++sessionCounter}_${Date.now()}`;
}

// ============================================================================
// Async Search Management (für Hintergrund-Suchen)
// ============================================================================

interface SearchSession {
  id: string;
  directory: string;
  pattern: RegExp;
  patternString: string;
  results: string[];
  isRunning: boolean;
  startTime: Date;
  scannedDirs: number;
  abortController: AbortController;
}

const searchSessions: Map<string, SearchSession> = new Map();
let searchCounter = 0;

function generateSearchId(): string {
  return `search_${++searchCounter}_${Date.now()}`;
}

/**
 * Asynchrone rekursive Suche mit AbortController
 */
async function asyncSearchFiles(
  session: SearchSession,
  dirPath: string
): Promise<void> {
  if (!session.isRunning || session.abortController.signal.aborted) {
    return;
  }

  try {
    const entries = await fs.readdir(dirPath, { withFileTypes: true });
    session.scannedDirs++;

    for (const entry of entries) {
      if (!session.isRunning || session.abortController.signal.aborted) {
        return;
      }

      const fullPath = path.join(dirPath, entry.name);

      if (entry.isDirectory()) {
        // Skip system directories
        if (!['node_modules', '.git', '$RECYCLE.BIN', 'System Volume Information', 'Windows', 'Program Files', 'Program Files (x86)'].includes(entry.name)) {
          await asyncSearchFiles(session, fullPath);
        }
      } else if (session.pattern.test(entry.name)) {
        session.results.push(fullPath);
      }
    }
  } catch {
    // Ignore permission errors silently
  }
}

// ============================================================================
// Helper Functions
// ============================================================================

/**
 * Normalisiert Pfade für Windows/Unix Kompatibilität
 */
function normalizePath(inputPath: string): string {
  return path.normalize(inputPath);
}

/**
 * Prüft ob ein Pfad existiert
 */
async function pathExists(targetPath: string): Promise<boolean> {
  try {
    await fs.access(targetPath);
    return true;
  } catch {
    return false;
  }
}

/**
 * Formatiert Dateigröße menschenlesbar
 */
function formatFileSize(bytes: number): string {
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let unitIndex = 0;
  let size = bytes;
  
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024;
    unitIndex++;
  }
  
  return `${size.toFixed(2)} ${units[unitIndex]}`;
}

/**
 * Prüft ob ein Pfad Windows-Sonderzeichen enthält die Probleme machen
 */
function hasWindowsSpecialChars(inputPath: string): boolean {
  return /[&^%$#@!]/.test(inputPath);
}

/**
 * Escaped einen Pfad für PowerShell-Nutzung
 * Behandelt & und andere Sonderzeichen korrekt
 */
function escapeForPowerShell(inputPath: string): string {
  // In PowerShell: & ist der Call-Operator, muss in Quotes oder escaped werden
  // Backtick (`) ist das Escape-Zeichen in PowerShell
  return inputPath
    .replace(/`/g, '``')      // Backtick zuerst escapen
    .replace(/\$/g, '`$')     // Dollar-Zeichen
    .replace(/"/g, '`"')      // Anführungszeichen
    .replace(/'/g, "''");     // Single quotes verdoppeln
}

/**
 * Escaped einen Pfad für cmd.exe-Nutzung
 * Behandelt & ^ % und andere Sonderzeichen
 */
function escapeForCmd(inputPath: string): string {
  // In cmd.exe: ^ ist das Escape-Zeichen
  return inputPath
    .replace(/([&^%!<>|])/g, '^$1');  // Sonderzeichen mit ^ escapen
}

/**
 * Ermittelt den PowerShell-Pfad auf Windows
 * Fallback-Kette: pwsh -> powershell.exe im System32 -> cmd.exe
 */
function getWindowsShell(): string {
  const systemRoot = process.env.SystemRoot || 'C:\\Windows';
  const ps7Path = `${systemRoot}\\System32\\WindowsPowerShell\\v1.0\\powershell.exe`;

  // Prüfe ob PowerShell im System32 existiert
  try {
    if (fsSync.existsSync(ps7Path)) {
      return ps7Path;
    }
  } catch {
    // Ignore
  }

  // Fallback zu cmd.exe
  return `${systemRoot}\\System32\\cmd.exe`;
}

/**
 * Führt einen Befehl aus - auf Windows mit korrektem Escaping für Sonderzeichen
 * Erkennt automatisch & und andere problematische Zeichen in Pfaden
 */
async function executeCommand(
  command: string,
  options: { cwd?: string; timeout?: number } = {}
): Promise<{ stdout: string; stderr: string }> {
  const isWindows = process.platform === 'win32';
  const cwd = options.cwd;

  // Auf Windows bei Sonderzeichen im Pfad oder Befehl: Spezielles Handling
  const cwdHasSpecialChars = cwd && hasWindowsSpecialChars(cwd);
  const cmdHasSpecialChars = hasWindowsSpecialChars(command);

  if (isWindows && (cwdHasSpecialChars || cmdHasSpecialChars)) {
    const windowsShell = getWindowsShell();

    if (windowsShell.includes('powershell')) {
      // PowerShell: Nutze -LiteralPath für Pfade mit Sonderzeichen
      const escapedCwd = cwd ? escapeForPowerShell(cwd) : '';

      // Befehl für PowerShell vorbereiten
      // Bei Pfaden mit & den Call-Operator nutzen: & "pfad mit &"
      let psCommand: string;

      if (cwd) {
        psCommand = `Set-Location -LiteralPath '${escapedCwd}'; ${command}`;
      } else {
        psCommand = command;
      }

      // Wenn der Befehl selbst Pfade mit & enthält, diese in Quotes wrappen
      // Erkennt Muster wie: python "C:\path\with & special\script.py"
      psCommand = psCommand.replace(
        /(?<!["`'])([A-Za-z]:\\[^"'`\n]*&[^"'`\n]*?)(?=\s|$)/g,
        '"$1"'
      );

      return execAsync(`"${windowsShell}" -Command "${psCommand.replace(/"/g, '\\"')}"`, {
        timeout: options.timeout
      });
    } else {
      // cmd.exe: Escape mit ^
      const escapedCmd = escapeForCmd(command);
      const escapedCwd = cwd ? escapeForCmd(cwd) : undefined;

      return execAsync(escapedCmd, {
        ...options,
        cwd: escapedCwd || cwd,
        shell: windowsShell
      });
    }
  }

  return execAsync(command, options);
}
async function listDirectoryRecursive(
  dirPath: string, 
  maxDepth: number, 
  currentDepth: number = 0
): Promise<string[]> {
  const results: string[] = [];
  
  if (currentDepth > maxDepth) return results;
  
  const entries = await fs.readdir(dirPath, { withFileTypes: true });
  
  for (const entry of entries) {
    const fullPath = path.join(dirPath, entry.name);
    const indent = "  ".repeat(currentDepth);
    
    if (entry.isDirectory()) {
      results.push(`${indent}📁 ${entry.name}/`);
      if (currentDepth < maxDepth) {
        const subEntries = await listDirectoryRecursive(fullPath, maxDepth, currentDepth + 1);
        results.push(...subEntries);
      }
    } else {
      results.push(`${indent}📄 ${entry.name}`);
    }
  }
  
  return results;
}

/**
 * Rekursive Dateisuche
 */
async function searchFilesRecursive(
  dirPath: string,
  pattern: RegExp,
  maxResults: number,
  results: string[] = []
): Promise<string[]> {
  if (results.length >= maxResults) return results;
  
  try {
    const entries = await fs.readdir(dirPath, { withFileTypes: true });
    
    for (const entry of entries) {
      if (results.length >= maxResults) break;
      
      const fullPath = path.join(dirPath, entry.name);
      
      if (entry.isDirectory()) {
        // Skip system directories
        if (!['node_modules', '.git', '$RECYCLE.BIN', 'System Volume Information'].includes(entry.name)) {
          await searchFilesRecursive(fullPath, pattern, maxResults, results);
        }
      } else if (pattern.test(entry.name)) {
        results.push(fullPath);
      }
    }
  } catch {
    // Ignore permission errors
  }
  
  return results;
}

// ============================================================================
// Tool: Read File
// ============================================================================

server.registerTool(
  "fc_read_file",
  {
    title: "Datei lesen",
    description: `Liest den Inhalt einer Datei.

Args:
  - path (string): Vollständiger Pfad zur Datei
  - encoding (string, optional): Zeichenkodierung (default: utf-8)
  - max_lines (number, optional): Maximale Anzahl Zeilen (0 = alle)

Returns:
  - Dateiinhalt als Text
  - Bei Binärdateien: Base64-kodierter Inhalt

Beispiele:
  - path: "C:\\Users\\User\\test.txt"
  - path: "/home/user/config.json"`,
    inputSchema: {
      path: z.string().min(1).describe("Vollständiger Pfad zur Datei"),
      encoding: z.string().default("utf-8").describe("Zeichenkodierung"),
      max_lines: z.number().int().min(0).default(0).describe("Max Zeilen (0 = alle)")
    },
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false
    }
  },
  async (params) => {
    try {
      const filePath = normalizePath(params.path);
      
      if (!await pathExists(filePath)) {
        return {
          isError: true,
          content: [{ type: "text", text: `❌ Datei nicht gefunden: ${filePath}` }]
        };
      }
      
      const stats = await fs.stat(filePath);
      if (stats.isDirectory()) {
        return {
          isError: true,
          content: [{ type: "text", text: `❌ Pfad ist ein Verzeichnis: ${filePath}. Nutze fc_list_directory.` }]
        };
      }
      
      let content = await fs.readFile(filePath, params.encoding as BufferEncoding);
      
      if (params.max_lines > 0) {
        const lines = content.split('\n');
        content = lines.slice(0, params.max_lines).join('\n');
        if (lines.length > params.max_lines) {
          content += `\n\n... (${lines.length - params.max_lines} weitere Zeilen)`;
        }
      }
      
      return {
        content: [{ 
          type: "text", 
          text: `📄 **${path.basename(filePath)}** (${formatFileSize(stats.size)})\n\n${content}` 
        }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Fehler beim Lesen: ${errorMsg}` }]
      };
    }
  }
);

// ============================================================================
// Tool: Write File
// ============================================================================

server.registerTool(
  "fc_write_file",
  {
    title: "Datei schreiben",
    description: `Schreibt Inhalt in eine Datei. Erstellt die Datei falls nicht vorhanden.

Args:
  - path (string): Vollständiger Pfad zur Datei
  - content (string): Zu schreibender Inhalt
  - append (boolean, optional): An Datei anhängen statt überschreiben
  - create_dirs (boolean, optional): Fehlende Verzeichnisse erstellen

Returns:
  - Bestätigung mit Dateigröße

⚠️ ACHTUNG: Überschreibt existierende Dateien ohne Warnung wenn append=false!`,
    inputSchema: {
      path: z.string().min(1).describe("Vollständiger Pfad zur Datei"),
      content: z.string().describe("Zu schreibender Inhalt"),
      append: z.boolean().default(false).describe("An Datei anhängen"),
      create_dirs: z.boolean().default(true).describe("Fehlende Verzeichnisse erstellen")
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: true,
      idempotentHint: false,
      openWorldHint: false
    }
  },
  async (params) => {
    try {
      const filePath = normalizePath(params.path);
      const dirPath = path.dirname(filePath);
      
      if (params.create_dirs && !await pathExists(dirPath)) {
        await fs.mkdir(dirPath, { recursive: true });
      }
      
      if (params.append) {
        await fs.appendFile(filePath, params.content, "utf-8");
      } else {
        await fs.writeFile(filePath, params.content, "utf-8");
      }
      
      const stats = await fs.stat(filePath);
      const action = params.append ? "erweitert" : "geschrieben";
      
      return {
        content: [{ 
          type: "text", 
          text: `✅ Datei ${action}: ${filePath}\n📊 Größe: ${formatFileSize(stats.size)}` 
        }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Fehler beim Schreiben: ${errorMsg}` }]
      };
    }
  }
);

// ============================================================================
// Tool: List Directory
// ============================================================================

server.registerTool(
  "fc_list_directory",
  {
    title: "Verzeichnis auflisten",
    description: `Listet Dateien und Unterverzeichnisse auf.

Args:
  - path (string): Pfad zum Verzeichnis
  - depth (number, optional): Maximale Tiefe für rekursive Auflistung (default: 1)
  - show_hidden (boolean, optional): Versteckte Dateien anzeigen

Returns:
  - Formatierte Liste aller Einträge mit Icons (📁/📄)`,
    inputSchema: {
      path: z.string().min(1).describe("Pfad zum Verzeichnis"),
      depth: z.number().int().min(0).max(10).default(1).describe("Rekursionstiefe"),
      show_hidden: z.boolean().default(false).describe("Versteckte Dateien anzeigen")
    },
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false
    }
  },
  async (params) => {
    try {
      const dirPath = normalizePath(params.path);
      
      if (!await pathExists(dirPath)) {
        return {
          isError: true,
          content: [{ type: "text", text: `❌ Verzeichnis nicht gefunden: ${dirPath}` }]
        };
      }
      
      const stats = await fs.stat(dirPath);
      if (!stats.isDirectory()) {
        return {
          isError: true,
          content: [{ type: "text", text: `❌ Pfad ist keine Verzeichnis: ${dirPath}. Nutze fc_read_file.` }]
        };
      }
      
      const entries = await listDirectoryRecursive(dirPath, params.depth);
      
      // Filter hidden files if needed
      const filteredEntries = params.show_hidden 
        ? entries 
        : entries.filter(e => !e.trim().startsWith('📁 .') && !e.trim().startsWith('📄 .'));
      
      return {
        content: [{ 
          type: "text", 
          text: `📂 **${dirPath}**\n\n${filteredEntries.join('\n') || '(Verzeichnis ist leer)'}` 
        }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Fehler beim Auflisten: ${errorMsg}` }]
      };
    }
  }
);

// ============================================================================
// Tool: Create Directory
// ============================================================================

server.registerTool(
  "fc_create_directory",
  {
    title: "Verzeichnis erstellen",
    description: `Erstellt ein neues Verzeichnis (inkl. Elternverzeichnisse).

Args:
  - path (string): Pfad zum neuen Verzeichnis

Returns:
  - Bestätigung der Erstellung`,
    inputSchema: {
      path: z.string().min(1).describe("Pfad zum neuen Verzeichnis")
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false
    }
  },
  async (params) => {
    try {
      const dirPath = normalizePath(params.path);
      
      if (await pathExists(dirPath)) {
        return {
          content: [{ type: "text", text: `ℹ️ Verzeichnis existiert bereits: ${dirPath}` }]
        };
      }
      
      await fs.mkdir(dirPath, { recursive: true });
      
      return {
        content: [{ type: "text", text: `✅ Verzeichnis erstellt: ${dirPath}` }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Fehler beim Erstellen: ${errorMsg}` }]
      };
    }
  }
);

// ============================================================================
// Tool: Delete File
// ============================================================================

server.registerTool(
  "fc_delete_file",
  {
    title: "Datei löschen",
    description: `Löscht eine Datei.

Args:
  - path (string): Pfad zur Datei

⚠️ ACHTUNG: Unwiderruflich! Keine Papierkorb-Funktion.`,
    inputSchema: {
      path: z.string().min(1).describe("Pfad zur Datei")
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: true,
      idempotentHint: true,
      openWorldHint: false
    }
  },
  async (params) => {
    try {
      const filePath = normalizePath(params.path);
      
      if (!await pathExists(filePath)) {
        return {
          isError: true,
          content: [{ type: "text", text: `❌ Datei nicht gefunden: ${filePath}` }]
        };
      }
      
      const stats = await fs.stat(filePath);
      if (stats.isDirectory()) {
        return {
          isError: true,
          content: [{ type: "text", text: `❌ Pfad ist ein Verzeichnis. Nutze fc_delete_directory.` }]
        };
      }
      
      await fs.unlink(filePath);
      
      return {
        content: [{ type: "text", text: `✅ Datei gelöscht: ${filePath}` }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Fehler beim Löschen: ${errorMsg}` }]
      };
    }
  }
);

// ============================================================================
// Tool: Delete Directory
// ============================================================================

server.registerTool(
  "fc_delete_directory",
  {
    title: "Verzeichnis löschen",
    description: `Löscht ein Verzeichnis.

Args:
  - path (string): Pfad zum Verzeichnis
  - recursive (boolean): Auch nicht-leere Verzeichnisse löschen

⚠️ ACHTUNG: Mit recursive=true werden ALLE Inhalte unwiderruflich gelöscht!`,
    inputSchema: {
      path: z.string().min(1).describe("Pfad zum Verzeichnis"),
      recursive: z.boolean().default(false).describe("Rekursiv löschen")
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: true,
      idempotentHint: true,
      openWorldHint: false
    }
  },
  async (params) => {
    try {
      const dirPath = normalizePath(params.path);
      
      if (!await pathExists(dirPath)) {
        return {
          isError: true,
          content: [{ type: "text", text: `❌ Verzeichnis nicht gefunden: ${dirPath}` }]
        };
      }
      
      const stats = await fs.stat(dirPath);
      if (!stats.isDirectory()) {
        return {
          isError: true,
          content: [{ type: "text", text: `❌ Pfad ist keine Verzeichnis. Nutze fc_delete_file.` }]
        };
      }
      
      await fs.rm(dirPath, { recursive: params.recursive });
      
      return {
        content: [{ type: "text", text: `✅ Verzeichnis gelöscht: ${dirPath}` }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      if (errorMsg.includes('ENOTEMPTY')) {
        return {
          isError: true,
          content: [{ type: "text", text: `❌ Verzeichnis nicht leer. Setze recursive=true zum Löschen aller Inhalte.` }]
        };
      }
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Fehler beim Löschen: ${errorMsg}` }]
      };
    }
  }
);

// ============================================================================
// Tool: Move/Rename
// ============================================================================

server.registerTool(
  "fc_move",
  {
    title: "Verschieben/Umbenennen",
    description: `Verschiebt oder benennt eine Datei/Verzeichnis um.

Args:
  - source (string): Quellpfad
  - destination (string): Zielpfad

Beispiele:
  - Umbenennen: source="test.txt", destination="test_neu.txt"
  - Verschieben: source="C:\\a\\test.txt", destination="C:\\b\\test.txt"`,
    inputSchema: {
      source: z.string().min(1).describe("Quellpfad"),
      destination: z.string().min(1).describe("Zielpfad")
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: true,
      idempotentHint: false,
      openWorldHint: false
    }
  },
  async (params) => {
    try {
      const sourcePath = normalizePath(params.source);
      const destPath = normalizePath(params.destination);
      
      if (!await pathExists(sourcePath)) {
        return {
          isError: true,
          content: [{ type: "text", text: `❌ Quelle nicht gefunden: ${sourcePath}` }]
        };
      }
      
      // Create destination directory if needed
      const destDir = path.dirname(destPath);
      if (!await pathExists(destDir)) {
        await fs.mkdir(destDir, { recursive: true });
      }
      
      await fs.rename(sourcePath, destPath);
      
      return {
        content: [{ type: "text", text: `✅ Verschoben:\n  📤 ${sourcePath}\n  📥 ${destPath}` }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Fehler beim Verschieben: ${errorMsg}` }]
      };
    }
  }
);

// ============================================================================
// Tool: Copy
// ============================================================================

server.registerTool(
  "fc_copy",
  {
    title: "Kopieren",
    description: `Kopiert eine Datei oder ein Verzeichnis.

Args:
  - source (string): Quellpfad
  - destination (string): Zielpfad
  - recursive (boolean): Verzeichnisse rekursiv kopieren`,
    inputSchema: {
      source: z.string().min(1).describe("Quellpfad"),
      destination: z.string().min(1).describe("Zielpfad"),
      recursive: z.boolean().default(true).describe("Rekursiv kopieren")
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: false,
      openWorldHint: false
    }
  },
  async (params) => {
    try {
      const sourcePath = normalizePath(params.source);
      const destPath = normalizePath(params.destination);
      
      if (!await pathExists(sourcePath)) {
        return {
          isError: true,
          content: [{ type: "text", text: `❌ Quelle nicht gefunden: ${sourcePath}` }]
        };
      }
      
      // Create destination directory if needed
      const destDir = path.dirname(destPath);
      if (!await pathExists(destDir)) {
        await fs.mkdir(destDir, { recursive: true });
      }
      
      const stats = await fs.stat(sourcePath);
      
      if (stats.isDirectory()) {
        await fs.cp(sourcePath, destPath, { recursive: params.recursive });
      } else {
        await fs.copyFile(sourcePath, destPath);
      }
      
      return {
        content: [{ type: "text", text: `✅ Kopiert:\n  📤 ${sourcePath}\n  📥 ${destPath}` }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Fehler beim Kopieren: ${errorMsg}` }]
      };
    }
  }
);

// ============================================================================
// Tool: File Info
// ============================================================================

server.registerTool(
  "fc_file_info",
  {
    title: "Datei-Informationen",
    description: `Zeigt detaillierte Informationen zu einer Datei/Verzeichnis.

Args:
  - path (string): Pfad zur Datei/Verzeichnis

Returns:
  - Größe, Typ, Erstellungs-/Änderungsdatum, Berechtigungen`,
    inputSchema: {
      path: z.string().min(1).describe("Pfad zur Datei/Verzeichnis")
    },
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false
    }
  },
  async (params) => {
    try {
      const targetPath = normalizePath(params.path);
      
      if (!await pathExists(targetPath)) {
        return {
          isError: true,
          content: [{ type: "text", text: `❌ Pfad nicht gefunden: ${targetPath}` }]
        };
      }
      
      const stats = await fs.stat(targetPath);
      const type = stats.isDirectory() ? "Verzeichnis" : stats.isFile() ? "Datei" : "Sonstiges";
      
      const info = [
        `📋 **Informationen: ${path.basename(targetPath)}**`,
        ``,
        `| Eigenschaft | Wert |`,
        `|-------------|------|`,
        `| Typ | ${type} |`,
        `| Größe | ${formatFileSize(stats.size)} |`,
        `| Erstellt | ${stats.birthtime.toLocaleString('de-DE')} |`,
        `| Geändert | ${stats.mtime.toLocaleString('de-DE')} |`,
        `| Zugegriffen | ${stats.atime.toLocaleString('de-DE')} |`,
        `| Pfad | ${targetPath} |`
      ];
      
      return {
        content: [{ type: "text", text: info.join('\n') }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Fehler: ${errorMsg}` }]
      };
    }
  }
);

// ============================================================================
// Tool: Search Files
// ============================================================================

server.registerTool(
  "fc_search_files",
  {
    title: "Dateien suchen",
    description: `Sucht Dateien nach Name/Muster in einem Verzeichnis.

Args:
  - directory (string): Startverzeichnis für die Suche
  - pattern (string): Suchmuster (unterstützt * und ? Wildcards)
  - max_results (number, optional): Maximale Ergebnisse (default: 50)

Beispiele:
  - pattern: "*.txt" - Alle Textdateien
  - pattern: "test*" - Dateien die mit "test" beginnen
  - pattern: "*.py" - Alle Python-Dateien`,
    inputSchema: {
      directory: z.string().min(1).describe("Startverzeichnis"),
      pattern: z.string().min(1).describe("Suchmuster mit Wildcards"),
      max_results: z.number().int().min(1).max(500).default(50).describe("Max Ergebnisse")
    },
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false
    }
  },
  async (params) => {
    try {
      const dirPath = normalizePath(params.directory);
      
      if (!await pathExists(dirPath)) {
        return {
          isError: true,
          content: [{ type: "text", text: `❌ Verzeichnis nicht gefunden: ${dirPath}` }]
        };
      }
      
      // Convert wildcard pattern to regex
      const regexPattern = params.pattern
        .replace(/[.+^${}()|[\]\\]/g, '\\$&')
        .replace(/\*/g, '.*')
        .replace(/\?/g, '.');
      const regex = new RegExp(`^${regexPattern}$`, 'i');
      
      const results = await searchFilesRecursive(dirPath, regex, params.max_results);
      
      if (results.length === 0) {
        return {
          content: [{ type: "text", text: `🔍 Keine Dateien gefunden für: "${params.pattern}"` }]
        };
      }
      
      const output = [
        `🔍 **Suchergebnisse für "${params.pattern}"**`,
        `📁 In: ${dirPath}`,
        `📊 Gefunden: ${results.length} ${results.length >= params.max_results ? `(Maximum erreicht)` : ''}`,
        ``,
        ...results.map(r => `  📄 ${r}`)
      ];
      
      return {
        content: [{ type: "text", text: output.join('\n') }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Fehler bei Suche: ${errorMsg}` }]
      };
    }
  }
);

// ============================================================================
// Tool: Start Async Search
// ============================================================================

server.registerTool(
  "fc_start_search",
  {
    title: "Asynchrone Suche starten",
    description: `Startet eine Suche im Hintergrund. Claude kann währenddessen andere Aufgaben erledigen.

Args:
  - directory (string): Startverzeichnis
  - pattern (string): Suchmuster (Wildcards: * und ?)

Returns:
  - Search-ID für fc_get_search_results, fc_stop_search

Beispiel:
  Suche starten: fc_start_search("C:\\Users", "*.pdf")
  Später Ergebnisse holen: fc_get_search_results(search_id)`,
    inputSchema: {
      directory: z.string().min(1).describe("Startverzeichnis"),
      pattern: z.string().min(1).describe("Suchmuster mit Wildcards")
    },
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: false,
      openWorldHint: false
    }
  },
  async (params) => {
    try {
      const dirPath = normalizePath(params.directory);
      
      if (!await pathExists(dirPath)) {
        return {
          isError: true,
          content: [{ type: "text", text: `❌ Verzeichnis nicht gefunden: ${dirPath}` }]
        };
      }

      // Convert wildcard pattern to regex
      const regexPattern = params.pattern
        .replace(/[.+^${}()|[\]\\]/g, '\\$&')
        .replace(/\*/g, '.*')
        .replace(/\?/g, '.');
      const regex = new RegExp(`^${regexPattern}$`, 'i');

      const searchId = generateSearchId();
      const abortController = new AbortController();

      const session: SearchSession = {
        id: searchId,
        directory: dirPath,
        pattern: regex,
        patternString: params.pattern,
        results: [],
        isRunning: true,
        startTime: new Date(),
        scannedDirs: 0,
        abortController
      };

      searchSessions.set(searchId, session);

      // Start search in background (don't await)
      asyncSearchFiles(session, dirPath).then(() => {
        session.isRunning = false;
      }).catch(() => {
        session.isRunning = false;
      });

      return {
        content: [{ 
          type: "text", 
          text: `🔍 **Suche gestartet**\n\n| | |\n|---|---|\n| Search-ID | \`${searchId}\` |\n| Verzeichnis | ${dirPath} |\n| Muster | ${params.pattern} |\n\nNutze \`fc_get_search_results\` um Ergebnisse abzurufen.`
        }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Fehler beim Starten der Suche: ${errorMsg}` }]
      };
    }
  }
);

// ============================================================================
// Tool: Get Search Results
// ============================================================================

server.registerTool(
  "fc_get_search_results",
  {
    title: "Suchergebnisse abrufen",
    description: `Ruft Ergebnisse einer laufenden oder beendeten Suche ab.

Args:
  - search_id (string): Search-ID von fc_start_search
  - offset (number, optional): Ab welchem Ergebnis (für Paginierung)
  - limit (number, optional): Maximale Anzahl Ergebnisse (default: 50)

Returns:
  - Status der Suche und gefundene Dateien`,
    inputSchema: {
      search_id: z.string().min(1).describe("Search-ID"),
      offset: z.number().int().min(0).default(0).describe("Start-Offset"),
      limit: z.number().int().min(1).max(200).default(50).describe("Max Ergebnisse")
    },
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false
    }
  },
  async (params) => {
    const session = searchSessions.get(params.search_id);

    if (!session) {
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Suche nicht gefunden: ${params.search_id}\n\nNutze fc_list_searches für aktive Suchen.` }]
      };
    }

    const status = session.isRunning ? '🔄 Läuft' : '✅ Abgeschlossen';
    const runtime = Math.round((Date.now() - session.startTime.getTime()) / 1000);
    const totalResults = session.results.length;
    const paginatedResults = session.results.slice(params.offset, params.offset + params.limit);
    const hasMore = totalResults > params.offset + params.limit;

    const output = [
      `🔍 **Suchergebnisse** (${status})`,
      ``,
      `| | |`,
      `|---|---|`,
      `| Muster | ${session.patternString} |`,
      `| Verzeichnis | ${session.directory} |`,
      `| Gescannte Ordner | ${session.scannedDirs} |`,
      `| Gefunden | ${totalResults} Dateien |`,
      `| Laufzeit | ${runtime}s |`,
      ``,
      `**Ergebnisse ${params.offset + 1}-${Math.min(params.offset + params.limit, totalResults)} von ${totalResults}:**`,
      ``,
      ...paginatedResults.map(r => `  📄 ${r}`)
    ];

    if (hasMore) {
      output.push(``, `📌 Weitere Ergebnisse: \`fc_get_search_results("${params.search_id}", offset=${params.offset + params.limit})\``);
    }

    return {
      content: [{ type: "text", text: output.join('\n') }]
    };
  }
);

// ============================================================================
// Tool: Stop Search
// ============================================================================

server.registerTool(
  "fc_stop_search",
  {
    title: "Suche stoppen",
    description: `Stoppt eine laufende Hintergrund-Suche.

Args:
  - search_id (string): Search-ID`,
    inputSchema: {
      search_id: z.string().min(1).describe("Search-ID")
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false
    }
  },
  async (params) => {
    const session = searchSessions.get(params.search_id);

    if (!session) {
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Suche nicht gefunden: ${params.search_id}` }]
      };
    }

    if (!session.isRunning) {
      return {
        content: [{ type: "text", text: `ℹ️ Suche bereits beendet. ${session.results.length} Ergebnisse gefunden.` }]
      };
    }

    session.isRunning = false;
    session.abortController.abort();

    return {
      content: [{ type: "text", text: `⏹️ Suche gestoppt: ${params.search_id}\n📊 ${session.results.length} Ergebnisse bis hierhin gefunden.` }]
    };
  }
);

// ============================================================================
// Tool: List Searches
// ============================================================================

server.registerTool(
  "fc_list_searches",
  {
    title: "Aktive Suchen auflisten",
    description: `Listet alle aktiven und beendeten Hintergrund-Suchen auf.`,
    inputSchema: {},
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false
    }
  },
  async () => {
    if (searchSessions.size === 0) {
      return {
        content: [{ type: "text", text: `📋 Keine Suchen aktiv.\n\nStarte eine neue mit \`fc_start_search\`.` }]
      };
    }

    const rows: string[] = [];
    
    for (const [id, session] of searchSessions) {
      const status = session.isRunning ? '🔄' : '✅';
      const runtime = Math.round((Date.now() - session.startTime.getTime()) / 1000);
      rows.push(`| ${status} | \`${id}\` | ${session.patternString} | ${session.results.length} | ${runtime}s |`);
    }

    const output = [
      `📋 **Suchen** (${searchSessions.size})`,
      ``,
      `| Status | Search-ID | Muster | Ergebnisse | Laufzeit |`,
      `|--------|-----------|--------|------------|----------|`,
      ...rows
    ];

    return {
      content: [{ type: "text", text: output.join('\n') }]
    };
  }
);

// ============================================================================
// Tool: Clear Search
// ============================================================================

server.registerTool(
  "fc_clear_search",
  {
    title: "Suche entfernen",
    description: `Entfernt eine beendete Suche aus der Liste und gibt Speicher frei.

Args:
  - search_id (string): Search-ID (oder "all" für alle beendeten)`,
    inputSchema: {
      search_id: z.string().min(1).describe("Search-ID oder 'all'")
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false
    }
  },
  async (params) => {
    if (params.search_id === "all") {
      let count = 0;
      for (const [id, session] of searchSessions) {
        if (!session.isRunning) {
          searchSessions.delete(id);
          count++;
        }
      }
      return {
        content: [{ type: "text", text: `🧹 ${count} beendete Suchen entfernt.` }]
      };
    }

    const session = searchSessions.get(params.search_id);

    if (!session) {
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Suche nicht gefunden: ${params.search_id}` }]
      };
    }

    if (session.isRunning) {
      return {
        isError: true,
        content: [{ type: "text", text: `⚠️ Suche läuft noch. Nutze erst fc_stop_search.` }]
      };
    }

    searchSessions.delete(params.search_id);

    return {
      content: [{ type: "text", text: `✅ Suche entfernt: ${params.search_id}` }]
    };
  }
);

// ============================================================================
// Tool: Safe Delete (Papierkorb)
// ============================================================================

server.registerTool(
  "fc_safe_delete",
  {
    title: "Sicher löschen (Papierkorb)",
    description: `Verschiebt Dateien/Verzeichnisse in den Papierkorb statt sie zu löschen.

Args:
  - path (string): Pfad zur Datei/Verzeichnis

✅ SICHER: Kann aus dem Papierkorb wiederhergestellt werden!

Hinweis: Nutzt Windows-Papierkorb oder erstellt Backup auf anderen Systemen.`,
    inputSchema: {
      path: z.string().min(1).describe("Pfad zur Datei/Verzeichnis")
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,  // Nicht destructive weil wiederherstellbar!
      idempotentHint: true,
      openWorldHint: false
    }
  },
  async (params) => {
    try {
      const targetPath = normalizePath(params.path);
      
      if (!await pathExists(targetPath)) {
        return {
          isError: true,
          content: [{ type: "text", text: `❌ Pfad nicht gefunden: ${targetPath}` }]
        };
      }

      const stats = await fs.stat(targetPath);
      const itemType = stats.isDirectory() ? "Verzeichnis" : "Datei";
      const isWindows = process.platform === 'win32';
        // Windows: PowerShell mit VisualBasic für echten Papierkorb
      if (isWindows) {
        // Windows: PowerShell mit VisualBasic für echten Papierkorb
        const escapedPath = targetPath.replace(/'/g, "''");
        const deleteMethod = stats.isDirectory() ? 'DeleteDirectory' : 'DeleteFile';
        
        const psCommand = `Add-Type -AssemblyName Microsoft.VisualBasic; [Microsoft.VisualBasic.FileIO.FileSystem]::${deleteMethod}('${escapedPath}', 'OnlyErrorDialogs', 'SendToRecycleBin')`;

        const windowsShell = getWindowsShell();
        if (windowsShell.includes('powershell')) {
          await execAsync(`"${windowsShell}" -Command "${psCommand}"`);
        } else {
          // cmd.exe kann kein PowerShell - normales Löschen als Fallback
          if (stats.isDirectory()) {
            await fs.rm(targetPath, { recursive: true });
          } else {
            await fs.unlink(targetPath);
          }
        }
        return {
          content: [{ 
            type: "text", 
            text: `🗑️ **In Papierkorb verschoben**\n\n| | |\n|---|---|\n| Typ | ${itemType} |\n| Pfad | ${targetPath} |\n\n✅ Kann aus dem Papierkorb wiederhergestellt werden.`
          }]
        };
      } else {
        // Unix/Mac: Verschiebe in ~/.Trash oder erstelle Backup
        const trashDir = path.join(process.env.HOME || '/tmp', '.Trash');
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const baseName = path.basename(targetPath);
        const trashPath = path.join(trashDir, `${baseName}_${timestamp}`);

        try {
          await fs.access(trashDir);
        } catch {
          await fs.mkdir(trashDir, { recursive: true });
        }

        await fs.rename(targetPath, trashPath);

        return {
          content: [{ 
            type: "text", 
            text: `🗑️ **In Papierkorb verschoben**\n\n| | |\n|---|---|\n| Typ | ${itemType} |\n| Original | ${targetPath} |\n| Papierkorb | ${trashPath} |\n\n✅ Kann wiederhergestellt werden.`
          }]
        };
      }
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Fehler beim Verschieben in Papierkorb: ${errorMsg}` }]
      };
    }
  }
);

// ============================================================================
// Tool: Execute Command
// ============================================================================

server.registerTool(
  "fc_execute_command",
  {
    title: "Befehl ausführen",
    description: `Führt einen Shell-Befehl aus und gibt die Ausgabe zurück.

Args:
  - command (string): Auszuführender Befehl
  - cwd (string, optional): Arbeitsverzeichnis
  - timeout (number, optional): Timeout in Millisekunden (default: 30000)

⚠️ ACHTUNG: Befehle werden mit Benutzerrechten ausgeführt!

Beispiele:
  - command: "dir" (Windows)
  - command: "ls -la" (Unix)
  - command: "python --version"`,
    inputSchema: {
      command: z.string().min(1).describe("Auszuführender Befehl"),
      cwd: z.string().optional().describe("Arbeitsverzeichnis"),
      timeout: z.number().int().min(1000).max(300000).default(30000).describe("Timeout in ms")
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: true,
      idempotentHint: false,
      openWorldHint: true
    }
  },
  async (params) => {
    try {
      const options: { cwd?: string; timeout: number } = {
        timeout: params.timeout
      };
      
      if (params.cwd) {
        options.cwd = normalizePath(params.cwd);
      }
      const { stdout, stderr } = await executeCommand(params.command, options);
      
      const output: string[] = [`⚡ **Befehl:** \`${params.command}\``];
      
      if (stdout.trim()) {
        output.push(`\n**Ausgabe:**\n\`\`\`\n${stdout.trim()}\n\`\`\``);
      }
      
      if (stderr.trim()) {
        output.push(`\n**Fehlerausgabe:**\n\`\`\`\n${stderr.trim()}\n\`\`\``);
      }
      
      if (!stdout.trim() && !stderr.trim()) {
        output.push(`\n✅ Befehl ausgeführt (keine Ausgabe)`);
      }
      
      return {
        content: [{ type: "text", text: output.join('') }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Fehler bei Befehlsausführung:\n${errorMsg}` }]
      };
    }
  }
);

// ============================================================================
// Tool: Start Process
// ============================================================================

server.registerTool(
  "fc_start_process",
  {
    title: "Prozess starten",
    description: `Startet einen Prozess im Hintergrund (non-blocking).

Args:
  - program (string): Programm/Executable
  - args (array, optional): Argumente als Array
  - cwd (string, optional): Arbeitsverzeichnis

Beispiele:
  - program: "notepad.exe", args: ["test.txt"]
  - program: "python", args: ["script.py"]
  - program: "code", args: ["."] (VS Code öffnen)`,
    inputSchema: {
      program: z.string().min(1).describe("Programm/Executable"),
      args: z.array(z.string()).default([]).describe("Argumente"),
      cwd: z.string().optional().describe("Arbeitsverzeichnis")
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: false,
      openWorldHint: true
    }
  },
  async (params) => {
    try {
      const options: { cwd?: string; detached: boolean; stdio: 'ignore' } = {
        detached: true,
        stdio: 'ignore'
      };
      
      if (params.cwd) {
        options.cwd = normalizePath(params.cwd);
      }
      
      const child = spawn(params.program, params.args, options);
      child.unref();
      
      const argsStr = params.args.length > 0 ? ` ${params.args.join(' ')}` : '';
      
      return {
        content: [{ 
          type: "text", 
          text: `🚀 Prozess gestartet: ${params.program}${argsStr}\n📋 PID: ${child.pid}` 
        }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Fehler beim Starten: ${errorMsg}` }]
      };
    }
  }
);

// ============================================================================
// Tool: Get Current Time
// ============================================================================

server.registerTool(
  "fc_get_time",
  {
    title: "Aktuelle Zeit",
    description: `Gibt die aktuelle Systemzeit zurück.

Returns:
  - Datum, Uhrzeit, Wochentag, Zeitzone`,
    inputSchema: {},
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: false,
      openWorldHint: false
    }
  },
  async () => {
    const now = new Date();
    const days = ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag'];
    
    const output = [
      `🕐 **Aktuelle Systemzeit**`,
      ``,
      `| | |`,
      `|---|---|`,
      `| Datum | ${now.toLocaleDateString('de-DE')} |`,
      `| Uhrzeit | ${now.toLocaleTimeString('de-DE')} |`,
      `| Wochentag | ${days[now.getDay()]} |`,
      `| ISO | ${now.toISOString()} |`,
      `| Zeitzone | ${Intl.DateTimeFormat().resolvedOptions().timeZone} |`
    ];
    
    return {
      content: [{ type: "text", text: output.join('\n') }]
    };
  }
);

// ============================================================================
// Tool: Read Multiple Files
// ============================================================================

server.registerTool(
  "fc_read_multiple_files",
  {
    title: "Mehrere Dateien lesen",
    description: `Liest mehrere Dateien auf einmal und gibt deren Inhalte zurück.

Args:
  - paths (array): Array von Dateipfaden
  - max_lines_per_file (number, optional): Max Zeilen pro Datei (0 = alle)

Returns:
  - Inhalte aller Dateien mit Trennzeichen

Beispiel:
  paths: ["C:\\config.json", "C:\\readme.md"]`,
    inputSchema: {
      paths: z.array(z.string().min(1)).min(1).max(20).describe("Array von Dateipfaden"),
      max_lines_per_file: z.number().int().min(0).default(0).describe("Max Zeilen pro Datei")
    },
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false
    }
  },
  async (params) => {
    const results: string[] = [];
    let successCount = 0;
    let errorCount = 0;

    for (const filePath of params.paths) {
      const normalizedPath = normalizePath(filePath);
      
      try {
        if (!await pathExists(normalizedPath)) {
          results.push(`\n❌ **${path.basename(normalizedPath)}** - Nicht gefunden\n`);
          errorCount++;
          continue;
        }

        const stats = await fs.stat(normalizedPath);
        if (stats.isDirectory()) {
          results.push(`\n❌ **${path.basename(normalizedPath)}** - Ist ein Verzeichnis\n`);
          errorCount++;
          continue;
        }

        let content = await fs.readFile(normalizedPath, "utf-8");
        
        if (params.max_lines_per_file > 0) {
          const lines = content.split('\n');
          content = lines.slice(0, params.max_lines_per_file).join('\n');
          if (lines.length > params.max_lines_per_file) {
            content += `\n... (${lines.length - params.max_lines_per_file} weitere Zeilen)`;
          }
        }

        results.push(`\n📄 **${normalizedPath}** (${formatFileSize(stats.size)})\n${'─'.repeat(60)}\n${content}\n`);
        successCount++;
      } catch (error) {
        const errorMsg = error instanceof Error ? error.message : String(error);
        results.push(`\n❌ **${path.basename(normalizedPath)}** - ${errorMsg}\n`);
        errorCount++;
      }
    }

    const summary = `📊 **Ergebnis:** ${successCount} gelesen, ${errorCount} Fehler\n${'═'.repeat(60)}`;
    
    return {
      content: [{ type: "text", text: summary + results.join('') }]
    };
  }
);

// ============================================================================
// Tool: Edit File (Zeilenbasiert)
// ============================================================================

server.registerTool(
  "fc_edit_file",
  {
    title: "Datei bearbeiten (Zeilen)",
    description: `Bearbeitet eine Datei zeilenbasiert: ersetzen, einfügen oder löschen.

Args:
  - path (string): Pfad zur Datei
  - operation (string): "replace" | "insert" | "delete"
  - start_line (number): Startzeile (1-basiert)
  - end_line (number, optional): Endzeile für replace/delete
  - content (string, optional): Neuer Inhalt für replace/insert

Beispiele:
  - Zeilen 5-10 ersetzen: operation="replace", start_line=5, end_line=10, content="neuer text"
  - Nach Zeile 3 einfügen: operation="insert", start_line=3, content="neue zeile"
  - Zeilen 7-9 löschen: operation="delete", start_line=7, end_line=9`,
    inputSchema: {
      path: z.string().min(1).describe("Pfad zur Datei"),
      operation: z.enum(["replace", "insert", "delete"]).describe("Operation"),
      start_line: z.number().int().min(1).describe("Startzeile (1-basiert)"),
      end_line: z.number().int().min(1).optional().describe("Endzeile"),
      content: z.string().optional().describe("Neuer Inhalt")
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: true,
      idempotentHint: false,
      openWorldHint: false
    }
  },
  async (params) => {
    try {
      const filePath = normalizePath(params.path);
      
      if (!await pathExists(filePath)) {
        return {
          isError: true,
          content: [{ type: "text", text: `❌ Datei nicht gefunden: ${filePath}` }]
        };
      }

      const originalContent = await fs.readFile(filePath, "utf-8");
      const lines = originalContent.split('\n');
      const totalLines = lines.length;

      const startIdx = params.start_line - 1;
      const endIdx = params.end_line ? params.end_line - 1 : startIdx;

      if (startIdx < 0 || startIdx >= totalLines) {
        return {
          isError: true,
          content: [{ type: "text", text: `❌ Startzeile ${params.start_line} ungültig. Datei hat ${totalLines} Zeilen.` }]
        };
      }

      if (endIdx < startIdx || endIdx >= totalLines) {
        return {
          isError: true,
          content: [{ type: "text", text: `❌ Endzeile ${params.end_line} ungültig.` }]
        };
      }

      let newLines: string[];
      let actionDesc: string;

      switch (params.operation) {
        case "replace":
          if (!params.content) {
            return {
              isError: true,
              content: [{ type: "text", text: `❌ 'content' erforderlich für replace-Operation.` }]
            };
          }
          const replacementLines = params.content.split('\n');
          newLines = [
            ...lines.slice(0, startIdx),
            ...replacementLines,
            ...lines.slice(endIdx + 1)
          ];
          actionDesc = `Zeilen ${params.start_line}-${endIdx + 1} ersetzt durch ${replacementLines.length} Zeilen`;
          break;

        case "insert":
          if (!params.content) {
            return {
              isError: true,
              content: [{ type: "text", text: `❌ 'content' erforderlich für insert-Operation.` }]
            };
          }
          const insertLines = params.content.split('\n');
          newLines = [
            ...lines.slice(0, startIdx + 1),
            ...insertLines,
            ...lines.slice(startIdx + 1)
          ];
          actionDesc = `${insertLines.length} Zeilen nach Zeile ${params.start_line} eingefügt`;
          break;

        case "delete":
          newLines = [
            ...lines.slice(0, startIdx),
            ...lines.slice(endIdx + 1)
          ];
          actionDesc = `Zeilen ${params.start_line}-${endIdx + 1} gelöscht`;
          break;

        default:
          return {
            isError: true,
            content: [{ type: "text", text: `❌ Unbekannte Operation: ${params.operation}` }]
          };
      }

      await fs.writeFile(filePath, newLines.join('\n'), "utf-8");

      return {
        content: [{ 
          type: "text", 
          text: `✅ **${path.basename(filePath)}** bearbeitet\n📝 ${actionDesc}\n📊 ${totalLines} → ${newLines.length} Zeilen` 
        }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Fehler beim Bearbeiten: ${errorMsg}` }]
      };
    }
  }
);

// ============================================================================
// Tool: String Replace in File
// ============================================================================

server.registerTool(
  "fc_str_replace",
  {
    title: "String in Datei ersetzen",
    description: `Ersetzt einen eindeutigen String in einer Datei durch einen anderen.

Args:
  - path (string): Pfad zur Datei
  - old_str (string): Zu ersetzender String (muss genau 1x vorkommen)
  - new_str (string): Neuer String (leer = löschen)

Returns:
  - Bestätigung mit Kontext

⚠️ WICHTIG: old_str muss EXAKT 1x in der Datei vorkommen!
Bei 0 oder >1 Vorkommen wird ein Fehler ausgegeben.

Beispiele:
  - Funktionsname ändern: old_str="def old_name", new_str="def new_name"
  - Import hinzufügen: old_str="import os", new_str="import os\\nimport sys"
  - Zeile löschen: old_str="# TODO: remove this\\n", new_str=""`,
    inputSchema: {
      path: z.string().min(1).describe("Pfad zur Datei"),
      old_str: z.string().min(1).describe("Zu ersetzender String (muss eindeutig sein)"),
      new_str: z.string().default("").describe("Neuer String (leer = löschen)")
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: true,
      idempotentHint: false,
      openWorldHint: false
    }
  },
  async (params) => {
    try {
      const filePath = normalizePath(params.path);
      
      if (!await pathExists(filePath)) {
        return {
          isError: true,
          content: [{ type: "text", text: `❌ Datei nicht gefunden: ${filePath}` }]
        };
      }

      const stats = await fs.stat(filePath);
      if (stats.isDirectory()) {
        return {
          isError: true,
          content: [{ type: "text", text: `❌ Pfad ist ein Verzeichnis: ${filePath}` }]
        };
      }

      const content = await fs.readFile(filePath, "utf-8");
      
      // Count occurrences
      const occurrences = content.split(params.old_str).length - 1;
      
      if (occurrences === 0) {
        // Show a snippet of the file to help debug
        const preview = content.length > 500 ? content.substring(0, 500) + "..." : content;
        return {
          isError: true,
          content: [{ 
            type: "text", 
            text: `❌ String nicht gefunden in ${path.basename(filePath)}.\n\n**Gesucht:**\n\`\`\`\n${params.old_str}\n\`\`\`\n\n**Datei-Anfang:**\n\`\`\`\n${preview}\n\`\`\``
          }]
        };
      }
      
      if (occurrences > 1) {
        return {
          isError: true,
          content: [{ 
            type: "text", 
            text: `❌ String kommt ${occurrences}x vor (muss eindeutig sein).\n\n**Gesucht:**\n\`\`\`\n${params.old_str}\n\`\`\`\n\n💡 Tipp: Erweitere den Suchstring um mehr Kontext.`
          }]
        };
      }

      // Perform replacement
      const newContent = content.replace(params.old_str, params.new_str);
      await fs.writeFile(filePath, newContent, "utf-8");

      // Calculate change info
      const oldLines = params.old_str.split('\n').length;
      const newLines = params.new_str.split('\n').length;
      const lineChange = newLines - oldLines;
      const lineInfo = lineChange === 0 ? "gleiche Zeilenanzahl" : 
                       lineChange > 0 ? `+${lineChange} Zeilen` : `${lineChange} Zeilen`;

      // Show context around the change
      const changeIndex = content.indexOf(params.old_str);
      const contextStart = Math.max(0, changeIndex - 50);
      const contextEnd = Math.min(content.length, changeIndex + params.old_str.length + 50);
      const beforeContext = content.substring(contextStart, changeIndex);
      const afterContext = content.substring(changeIndex + params.old_str.length, contextEnd);

      return {
        content: [{ 
          type: "text", 
          text: `✅ **${path.basename(filePath)}** - String ersetzt\n\n| | |\n|---|---|\n| Änderung | ${lineInfo} |\n| Datei | ${filePath} |\n\n**Kontext:**\n\`\`\`\n...${beforeContext}▶${params.new_str}◀${afterContext}...\n\`\`\``
        }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Fehler beim Ersetzen: ${errorMsg}` }]
      };
    }
  }
)

// ============================================================================
// Tool: List Processes
// ============================================================================

server.registerTool(
  "fc_list_processes",
  {
    title: "Prozesse auflisten",
    description: `Listet laufende Systemprozesse auf.

Args:
  - filter (string, optional): Filter nach Prozessname

Returns:
  - Liste der Prozesse mit PID, Name, Speicher

Hinweis: Nutzt 'tasklist' (Windows) oder 'ps' (Unix)`,
    inputSchema: {
      filter: z.string().optional().describe("Filter nach Prozessname")
    },
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: true
    }
  },
  async (params) => {
    try {
      const isWindows = process.platform === 'win32';
      let command: string;

      if (isWindows) {
        command = params.filter 
          ? `tasklist /FI "IMAGENAME eq ${params.filter}*" /FO CSV /NH`
          : `tasklist /FO CSV /NH`;
      } else {
        command = params.filter
          ? `ps aux | grep -i "${params.filter}" | grep -v grep`
          : `ps aux --sort=-%mem | head -50`;
      }

      const { stdout } = await execAsync(command);

      if (!stdout.trim()) {
        return {
          content: [{ type: "text", text: `🔍 Keine Prozesse gefunden${params.filter ? ` für "${params.filter}"` : ''}.` }]
        };
      }

      let output: string;

      if (isWindows) {
        // Parse CSV output from tasklist
        const lines = stdout.trim().split('\n').filter(l => l.trim());
        const processes = lines.map(line => {
          const parts = line.split('","').map(p => p.replace(/"/g, ''));
          return `| ${parts[0] || '-'} | ${parts[1] || '-'} | ${parts[4] || '-'} |`;
        });
        
        output = [
          `📋 **Laufende Prozesse**${params.filter ? ` (Filter: ${params.filter})` : ''}`,
          ``,
          `| Name | PID | Speicher |`,
          `|------|-----|----------|`,
          ...processes.slice(0, 50)
        ].join('\n');
      } else {
        output = [
          `📋 **Laufende Prozesse**${params.filter ? ` (Filter: ${params.filter})` : ''}`,
          ``,
          '```',
          stdout.trim(),
          '```'
        ].join('\n');
      }

      return {
        content: [{ type: "text", text: output }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Fehler beim Auflisten: ${errorMsg}` }]
      };
    }
  }
);

// ============================================================================
// Tool: Kill Process
// ============================================================================

server.registerTool(
  "fc_kill_process",
  {
    title: "Prozess beenden",
    description: `Beendet einen Prozess nach PID oder Name.

Args:
  - pid (number, optional): Prozess-ID
  - name (string, optional): Prozessname
  - force (boolean): Erzwungenes Beenden

⚠️ ACHTUNG: Kann zu Datenverlust führen!`,
    inputSchema: {
      pid: z.number().int().optional().describe("Prozess-ID"),
      name: z.string().optional().describe("Prozessname"),
      force: z.boolean().default(false).describe("Erzwingen")
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: true,
      idempotentHint: true,
      openWorldHint: true
    }
  },
  async (params) => {
    if (!params.pid && !params.name) {
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Entweder 'pid' oder 'name' muss angegeben werden.` }]
      };
    }

    try {
      const isWindows = process.platform === 'win32';
      let command: string;

      if (isWindows) {
        if (params.pid) {
          command = params.force 
            ? `taskkill /F /PID ${params.pid}`
            : `taskkill /PID ${params.pid}`;
        } else {
          command = params.force
            ? `taskkill /F /IM "${params.name}"`
            : `taskkill /IM "${params.name}"`;
        }
      } else {
        if (params.pid) {
          command = params.force 
            ? `kill -9 ${params.pid}`
            : `kill ${params.pid}`;
        } else {
          command = params.force
            ? `pkill -9 "${params.name}"`
            : `pkill "${params.name}"`;
        }
      }

      const { stdout, stderr } = await execAsync(command);
      const target = params.pid ? `PID ${params.pid}` : `"${params.name}"`;

      return {
        content: [{ 
          type: "text", 
          text: `✅ Prozess beendet: ${target}\n${stdout || stderr || ''}`.trim()
        }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Fehler beim Beenden: ${errorMsg}` }]
      };
    }
  }
);

// ============================================================================
// Tool: Start Interactive Process (Session)
// ============================================================================

server.registerTool(
  "fc_start_session",
  {
    title: "Interaktive Session starten",
    description: `Startet einen interaktiven Prozess als Session (für fc_read_output und fc_send_input).

Args:
  - command (string): Befehl/Programm
  - args (array, optional): Argumente
  - cwd (string, optional): Arbeitsverzeichnis

Returns:
  - Session-ID für weitere Interaktion

Beispiele:
  - Python REPL: command="python"
  - Node REPL: command="node"
  - PowerShell: command="powershell"`,
    inputSchema: {
      command: z.string().min(1).describe("Befehl/Programm"),
      args: z.array(z.string()).default([]).describe("Argumente"),
      cwd: z.string().optional().describe("Arbeitsverzeichnis")
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: false,
      openWorldHint: true
    }
  },
  async (params) => {
    try {
      const sessionId = generateSessionId();
      const cwd = params.cwd ? normalizePath(params.cwd) : process.cwd();

      const proc = spawn(params.command, params.args, {
        cwd,
        shell: true,
        stdio: ['pipe', 'pipe', 'pipe']
      });

      const session: ProcessSession = {
        id: sessionId,
        process: proc,
        command: params.command,
        args: params.args,
        cwd,
        startTime: new Date(),
        output: [],
        isRunning: true
      };

      // Capture output
      proc.stdout?.on('data', (data: Buffer) => {
        session.output.push(data.toString());
        // Keep only last 1000 lines
        if (session.output.length > 1000) {
          session.output = session.output.slice(-500);
        }
      });

      proc.stderr?.on('data', (data: Buffer) => {
        session.output.push(`[stderr] ${data.toString()}`);
      });

      proc.on('close', (code) => {
        session.isRunning = false;
        session.output.push(`\n[Prozess beendet mit Code ${code}]`);
      });

      proc.on('error', (err) => {
        session.isRunning = false;
        session.output.push(`\n[Fehler: ${err.message}]`);
      });

      processSessions.set(sessionId, session);

      return {
        content: [{ 
          type: "text", 
          text: `🚀 **Session gestartet**\n\n| | |\n|---|---|\n| Session-ID | \`${sessionId}\` |\n| Befehl | ${params.command} ${params.args.join(' ')} |\n| PID | ${proc.pid} |\n| Verzeichnis | ${cwd} |\n\nNutze \`fc_read_output\` und \`fc_send_input\` zur Interaktion.`
        }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Fehler beim Starten: ${errorMsg}` }]
      };
    }
  }
);

// ============================================================================
// Tool: Read Process Output
// ============================================================================

server.registerTool(
  "fc_read_output",
  {
    title: "Session-Output lesen",
    description: `Liest die Ausgabe einer laufenden Session.

Args:
  - session_id (string): Session-ID von fc_start_session
  - clear (boolean, optional): Output nach dem Lesen löschen

Returns:
  - Gesammelter Output seit Start/letztem Clear`,
    inputSchema: {
      session_id: z.string().min(1).describe("Session-ID"),
      clear: z.boolean().default(false).describe("Output löschen")
    },
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false
    }
  },
  async (params) => {
    const session = processSessions.get(params.session_id);

    if (!session) {
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Session nicht gefunden: ${params.session_id}\n\nNutze fc_list_sessions für aktive Sessions.` }]
      };
    }

    const output = session.output.join('');
    const status = session.isRunning ? '🟢 Läuft' : '🔴 Beendet';

    if (params.clear) {
      session.output = [];
    }

    return {
      content: [{ 
        type: "text", 
        text: `📤 **Session Output** (${status})\n\`\`\`\n${output || '(kein Output)'}\n\`\`\``
      }]
    };
  }
);

// ============================================================================
// Tool: Send Input to Process
// ============================================================================

server.registerTool(
  "fc_send_input",
  {
    title: "Input an Session senden",
    description: `Sendet Input an eine laufende Session.

Args:
  - session_id (string): Session-ID
  - input (string): Zu sendender Input
  - newline (boolean, optional): Zeilenumbruch anhängen (default: true)

Beispiele:
  - Python: input="print('Hello')"
  - Shell: input="ls -la"`,
    inputSchema: {
      session_id: z.string().min(1).describe("Session-ID"),
      input: z.string().describe("Zu sendender Input"),
      newline: z.boolean().default(true).describe("Zeilenumbruch anhängen")
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: false,
      openWorldHint: true
    }
  },
  async (params) => {
    const session = processSessions.get(params.session_id);

    if (!session) {
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Session nicht gefunden: ${params.session_id}` }]
      };
    }

    if (!session.isRunning) {
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Session ist beendet. Starte eine neue mit fc_start_session.` }]
      };
    }

    try {
      const inputText = params.newline ? params.input + '\n' : params.input;
      session.process.stdin?.write(inputText);

      return {
        content: [{ 
          type: "text", 
          text: `📥 Input gesendet an ${params.session_id}:\n\`\`\`\n${params.input}\n\`\`\`\nNutze \`fc_read_output\` um die Antwort zu lesen.`
        }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Fehler beim Senden: ${errorMsg}` }]
      };
    }
  }
);

// ============================================================================
// Tool: List Sessions
// ============================================================================

server.registerTool(
  "fc_list_sessions",
  {
    title: "Sessions auflisten",
    description: `Listet alle aktiven und beendeten Sessions auf.

Returns:
  - Tabelle aller Sessions mit Status`,
    inputSchema: {},
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false
    }
  },
  async () => {
    if (processSessions.size === 0) {
      return {
        content: [{ type: "text", text: `📋 Keine Sessions vorhanden.\n\nStarte eine neue mit \`fc_start_session\`.` }]
      };
    }

    const rows: string[] = [];
    
    for (const [id, session] of processSessions) {
      const status = session.isRunning ? '🟢' : '🔴';
      const runtime = Math.round((Date.now() - session.startTime.getTime()) / 1000);
      rows.push(`| ${status} | \`${id}\` | ${session.command} | ${session.process.pid || '-'} | ${runtime}s |`);
    }

    const output = [
      `📋 **Aktive Sessions** (${processSessions.size})`,
      ``,
      `| Status | Session-ID | Befehl | PID | Laufzeit |`,
      `|--------|------------|--------|-----|----------|`,
      ...rows
    ];

    return {
      content: [{ type: "text", text: output.join('\n') }]
    };
  }
);

// ============================================================================
// Tool: Close Session
// ============================================================================

server.registerTool(
  "fc_close_session",
  {
    title: "Session beenden",
    description: `Beendet eine laufende Session und entfernt sie aus der Liste.

Args:
  - session_id (string): Session-ID
  - force (boolean, optional): Erzwungenes Beenden`,
    inputSchema: {
      session_id: z.string().min(1).describe("Session-ID"),
      force: z.boolean().default(false).describe("Erzwingen")
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: true,
      idempotentHint: true,
      openWorldHint: false
    }
  },
  async (params) => {
    const session = processSessions.get(params.session_id);

    if (!session) {
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Session nicht gefunden: ${params.session_id}` }]
      };
    }

    try {
      if (session.isRunning) {
        if (params.force) {
          session.process.kill('SIGKILL');
        } else {
          session.process.kill('SIGTERM');
        }
      }

      processSessions.delete(params.session_id);

      return {
        content: [{ type: "text", text: `✅ Session beendet und entfernt: ${params.session_id}` }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: `❌ Fehler beim Beenden: ${errorMsg}` }]
      };
    }
  }
);

// ============================================================================
// Tool: Fix JSON
// ============================================================================

server.registerTool(
  "fc_fix_json",
  {
    title: "JSON reparieren",
    description: `Repariert häufige JSON-Fehler automatisch.

Args:
  - path (string): Pfad zur JSON-Datei
  - dry_run (boolean, optional): Nur Probleme anzeigen, nicht reparieren
  - create_backup (boolean, optional): Backup erstellen vor Reparatur

Repariert: BOM, Trailing Commas, Single Quotes, Kommentare, NUL-Bytes`,
    inputSchema: {
      path: z.string().min(1).describe("Pfad zur JSON-Datei"),
      dry_run: z.boolean().default(false).describe("Nur Probleme anzeigen"),
      create_backup: z.boolean().default(true).describe("Backup erstellen")
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false
    }
  },
  async (params) => {
    try {
      const filePath = normalizePath(params.path);
      if (!await pathExists(filePath)) {
        return { isError: true, content: [{ type: "text", text: `❌ Datei nicht gefunden: ${filePath}` }] };
      }

      const rawContent = await fs.readFile(filePath, "utf-8");
      const fixes: string[] = [];
      let content = rawContent;

      // Remove BOM
      if (content.charCodeAt(0) === 0xFEFF) {
        content = content.slice(1);
        fixes.push("UTF-8 BOM entfernt");
      }

      // Remove NUL bytes
      if (content.includes('\0')) {
        content = content.replace(/\0/g, '');
        fixes.push("NUL-Bytes entfernt");
      }

      // Remove single-line comments
      const c1 = content;
      content = content.replace(/^(\s*)\/\/.*$/gm, '');
      if (content !== c1) fixes.push("Einzeilige Kommentare entfernt");

      // Remove multi-line comments
      const c2 = content;
      content = content.replace(/\/\*[\s\S]*?\*\//g, '');
      if (content !== c2) fixes.push("Mehrzeilige Kommentare entfernt");

      // Fix trailing commas before } or ]
      const c3 = content;
      content = content.replace(/,(\s*[}\]])/g, '$1');
      if (content !== c3) fixes.push("Trailing Commas entfernt");

      // Fix single quotes to double quotes for keys and simple values
      const c4 = content;
      content = content.replace(/(\s*)'([^'\\]*(?:\\.[^'\\]*)*)'\s*:/g, '$1"$2":');
      content = content.replace(/:\s*'([^'\\]*(?:\\.[^'\\]*)*)'/g, ': "$1"');
      if (content !== c4) fixes.push("Single Quotes → Double Quotes");

      // Try to parse
      let isValid = false;
      let parseError = '';
      try { JSON.parse(content); isValid = true; } catch (e) { parseError = e instanceof Error ? e.message : String(e); }

      if (fixes.length === 0 && isValid) {
        return { content: [{ type: "text", text: `✅ ${path.basename(filePath)} ist bereits gültiges JSON.` }] };
      }

      if (params.dry_run) {
        return {
          content: [{ type: "text", text: [
            `🔍 **JSON-Analyse: ${path.basename(filePath)}**`, '',
            fixes.length > 0 ? `**Gefundene Probleme:**` : `Keine automatisch reparierbaren Probleme.`,
            ...fixes.map(f => `  - ${f}`), '',
            isValid ? `✅ Nach Reparatur: Gültiges JSON` : `⚠️ Nach Reparatur noch ungültig: ${parseError}`
          ].join('\n') }]
        };
      }

      if (params.create_backup && fixes.length > 0) {
        await fs.writeFile(filePath + '.bak', rawContent, "utf-8");
      }

      if (isValid) {
        content = JSON.stringify(JSON.parse(content), null, 2);
      }
      await fs.writeFile(filePath, content, "utf-8");

      return {
        content: [{ type: "text", text: [
          `✅ **JSON repariert: ${path.basename(filePath)}**`, '',
          ...fixes.map(f => `  - ${f}`), '',
          isValid ? `✅ Gültiges JSON` : `⚠️ Noch ungültig: ${parseError}`,
          params.create_backup ? `📋 Backup: ${filePath}.bak` : ''
        ].join('\n') }]
      };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: `❌ Fehler: ${error instanceof Error ? error.message : String(error)}` }] };
    }
  }
);

// ============================================================================
// Tool: Validate JSON
// ============================================================================

server.registerTool(
  "fc_validate_json",
  {
    title: "JSON validieren",
    description: `Validiert eine JSON-Datei und zeigt detaillierte Fehlerinformationen.

Args:
  - path (string): Pfad zur JSON-Datei

Returns:
  - Validierungsstatus mit Zeile/Spalte bei Fehlern`,
    inputSchema: {
      path: z.string().min(1).describe("Pfad zur JSON-Datei")
    },
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false
    }
  },
  async (params) => {
    try {
      const filePath = normalizePath(params.path);
      if (!await pathExists(filePath)) {
        return { isError: true, content: [{ type: "text", text: `❌ Datei nicht gefunden: ${filePath}` }] };
      }

      const content = await fs.readFile(filePath, "utf-8");
      const stats = await fs.stat(filePath);

      try {
        const parsed = JSON.parse(content);
        const keyCount = typeof parsed === 'object' && parsed !== null ? Object.keys(parsed).length : 0;
        const type = Array.isArray(parsed) ? `Array (${parsed.length} Elemente)` : typeof parsed === 'object' && parsed !== null ? `Objekt (${keyCount} Schlüssel)` : typeof parsed;

        return {
          content: [{ type: "text", text: [
            `✅ **Gültiges JSON: ${path.basename(filePath)}**`, '',
            `| Eigenschaft | Wert |`, `|---|---|`,
            `| Typ | ${type} |`,
            `| Größe | ${formatFileSize(stats.size)} |`,
            `| BOM | ${content.charCodeAt(0) === 0xFEFF ? '⚠️ Ja' : 'Nein'} |`,
            `| Encoding | UTF-8 |`
          ].join('\n') }]
        };
      } catch (e) {
        const errorMsg = e instanceof Error ? e.message : String(e);
        // Extract position from error message
        const posMatch = errorMsg.match(/position\s+(\d+)/i);
        let lineInfo = '';
        if (posMatch) {
          const pos = parseInt(posMatch[1]);
          const before = content.substring(0, pos);
          const line = before.split('\n').length;
          const col = pos - before.lastIndexOf('\n');
          const lines = content.split('\n');
          const contextLines = lines.slice(Math.max(0, line - 3), line + 2);
          lineInfo = `\n**Fehlerposition:** Zeile ${line}, Spalte ${col}\n\n\`\`\`\n${contextLines.map((l, i) => `${Math.max(1, line - 2) + i}: ${l}`).join('\n')}\n\`\`\``;
        }

        return {
          content: [{ type: "text", text: `❌ **Ungültiges JSON: ${path.basename(filePath)}**\n\n**Fehler:** ${errorMsg}${lineInfo}\n\n💡 Nutze \`fc_fix_json\` für automatische Reparatur.` }]
        };
      }
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: `❌ Fehler: ${error instanceof Error ? error.message : String(error)}` }] };
    }
  }
);

// ============================================================================
// Tool: Cleanup File
// ============================================================================

server.registerTool(
  "fc_cleanup_file",
  {
    title: "Datei bereinigen",
    description: `Bereinigt eine oder mehrere Dateien von häufigen Problemen.

Args:
  - path (string): Pfad zu Datei oder Verzeichnis
  - recursive (boolean, optional): Bei Verzeichnis rekursiv
  - extensions (string, optional): Dateierweiterungen filtern (z.B. ".txt,.json,.py")
  - remove_bom (boolean): UTF-8 BOM entfernen
  - remove_trailing_whitespace (boolean): Trailing Whitespace entfernen
  - normalize_line_endings (string, optional): "lf" | "crlf" | null
  - remove_nul_bytes (boolean): NUL-Bytes entfernen
  - dry_run (boolean): Nur anzeigen

Bereinigt: BOM, NUL-Bytes, Trailing Whitespace, Line Endings`,
    inputSchema: {
      path: z.string().min(1).describe("Pfad zu Datei/Verzeichnis"),
      recursive: z.boolean().default(false).describe("Rekursiv"),
      extensions: z.string().optional().describe("Erweiterungen filtern (.txt,.json)"),
      remove_bom: z.boolean().default(true).describe("BOM entfernen"),
      remove_trailing_whitespace: z.boolean().default(true).describe("Trailing Whitespace"),
      normalize_line_endings: z.enum(["lf", "crlf"]).optional().describe("Line Endings"),
      remove_nul_bytes: z.boolean().default(true).describe("NUL-Bytes entfernen"),
      dry_run: z.boolean().default(false).describe("Nur anzeigen")
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false
    }
  },
  async (params) => {
    try {
      const targetPath = normalizePath(params.path);
      if (!await pathExists(targetPath)) {
        return { isError: true, content: [{ type: "text", text: `❌ Pfad nicht gefunden: ${targetPath}` }] };
      }

      const stats = await fs.stat(targetPath);
      const extFilter = params.extensions ? params.extensions.split(',').map(e => e.trim().toLowerCase()) : null;

      // Collect files
      const files: string[] = [];
      if (stats.isDirectory()) {
        async function collectFiles(dir: string): Promise<void> {
          const entries = await fs.readdir(dir, { withFileTypes: true });
          for (const entry of entries) {
            const full = path.join(dir, entry.name);
            if (entry.isDirectory() && params.recursive) {
              if (!['node_modules', '.git', '$RECYCLE.BIN'].includes(entry.name)) {
                await collectFiles(full);
              }
            } else if (entry.isFile()) {
              if (!extFilter || extFilter.includes(path.extname(entry.name).toLowerCase())) {
                files.push(full);
              }
            }
          }
        }
        await collectFiles(targetPath);
      } else {
        files.push(targetPath);
      }

      const results: string[] = [];
      let totalFixed = 0;

      for (const filePath of files) {
        try {
          const raw = await fs.readFile(filePath, "utf-8");
          let content = raw;
          const fixes: string[] = [];

          if (params.remove_bom && content.charCodeAt(0) === 0xFEFF) {
            content = content.slice(1);
            fixes.push("BOM");
          }
          if (params.remove_nul_bytes && content.includes('\0')) {
            content = content.replace(/\0/g, '');
            fixes.push("NUL");
          }
          if (params.remove_trailing_whitespace) {
            const c = content;
            content = content.replace(/[ \t]+$/gm, '');
            if (content !== c) fixes.push("Whitespace");
          }
          if (params.normalize_line_endings) {
            const c = content;
            content = content.replace(/\r\n/g, '\n');
            if (params.normalize_line_endings === 'crlf') {
              content = content.replace(/\n/g, '\r\n');
            }
            if (content !== c) fixes.push(params.normalize_line_endings.toUpperCase());
          }

          if (fixes.length > 0) {
            if (!params.dry_run) {
              await fs.writeFile(filePath, content, "utf-8");
            }
            results.push(`  ✅ ${path.relative(targetPath, filePath) || path.basename(filePath)} [${fixes.join(', ')}]`);
            totalFixed++;
          }
        } catch {
          // Skip binary/unreadable files
        }
      }

      if (totalFixed === 0) {
        return { content: [{ type: "text", text: `✅ Keine Bereinigung nötig. ${files.length} Dateien geprüft.` }] };
      }

      return {
        content: [{ type: "text", text: [
          `${params.dry_run ? '🔍 **Vorschau**' : '✅ **Bereinigt**'}: ${totalFixed}/${files.length} Dateien`, '',
          ...results
        ].join('\n') }]
      };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: `❌ Fehler: ${error instanceof Error ? error.message : String(error)}` }] };
    }
  }
);

// ============================================================================
// Tool: Fix Encoding
// ============================================================================

server.registerTool(
  "fc_fix_encoding",
  {
    title: "Encoding reparieren",
    description: `Erkennt und repariert Encoding-Fehler (Mojibake, doppeltes UTF-8).

Args:
  - path (string): Pfad zur Datei
  - dry_run (boolean): Nur Probleme anzeigen
  - create_backup (boolean): Backup erstellen

Repariert häufige Mojibake-Muster wie:
  - Ã¤ → ä, Ã¶ → ö, Ã¼ → ü
  - Ã„ → Ä, Ã– → Ö, Ãœ → Ü
  - ÃŸ → ß, â‚¬ → €`,
    inputSchema: {
      path: z.string().min(1).describe("Pfad zur Datei"),
      dry_run: z.boolean().default(false).describe("Nur anzeigen"),
      create_backup: z.boolean().default(true).describe("Backup erstellen")
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false
    }
  },
  async (params) => {
    try {
      const filePath = normalizePath(params.path);
      if (!await pathExists(filePath)) {
        return { isError: true, content: [{ type: "text", text: `❌ Datei nicht gefunden: ${filePath}` }] };
      }

      const rawContent = await fs.readFile(filePath, "utf-8");

      // Common Mojibake patterns (UTF-8 decoded as Latin-1 then re-encoded as UTF-8)
      const mojibakeMap: [RegExp, string, string][] = [
        [/Ã¤/g, 'ä', 'ä'], [/Ã¶/g, 'ö', 'ö'], [/Ã¼/g, 'ü', 'ü'],
        [/Ã„/g, 'Ä', 'Ä'], [/Ã–/g, 'Ö', 'Ö'], [/Ãœ/g, 'Ü', 'Ü'],
        [/ÃŸ/g, 'ß', 'ß'], [/â‚¬/g, '€', '€'],
        [/Ã©/g, 'é', 'é'], [/Ã¨/g, 'è', 'è'],
        [/Ã /g, 'à', 'à'], [/Ã¡/g, 'á', 'á'],
        [/Ã®/g, 'î', 'î'], [/Ã¯/g, 'ï', 'ï'],
        [/Ã´/g, 'ô', 'ô'], [/Ã¹/g, 'ù', 'ù'],
        [/Ã§/g, 'ç', 'ç'], [/Ã±/g, 'ñ', 'ñ'],
        [/\u00e2\u0080\u0093/g, '\u2013', 'en-dash'], [/\u00e2\u0080\u0094/g, '\u2014', 'em-dash'],
        [/\u00e2\u0080\u009c/g, '\u201C', 'left-dquote'], [/\u00e2\u0080\u009d/g, '\u201D', 'right-dquote'],
        [/\u00e2\u0080\u0098/g, '\u2018', 'left-squote'], [/\u00e2\u0080\u0099/g, '\u2019', 'right-squote'],
        [/\u00c2\u00a0/g, ' ', 'NBSP'], [/\u00c2\u00a9/g, '\u00A9', '\u00A9'],
        [/\u00c2\u00ae/g, '\u00AE', '\u00AE'], [/\u00c2\u00b0/g, '\u00B0', '\u00B0'],
      ];

      let content = rawContent;
      const fixes: string[] = [];

      for (const [pattern, replacement, label] of mojibakeMap) {
        const before = content;
        content = content.replace(pattern, replacement);
        if (content !== before) {
          const count = (before.match(pattern) || []).length;
          fixes.push(`${label} (${count}x)`);
        }
      }

      if (fixes.length === 0) {
        return { content: [{ type: "text", text: `✅ Keine Encoding-Fehler in ${path.basename(filePath)} gefunden.` }] };
      }

      if (params.dry_run) {
        return {
          content: [{ type: "text", text: [
            `🔍 **Encoding-Analyse: ${path.basename(filePath)}**`, '',
            `**Gefundene Mojibake-Muster:**`,
            ...fixes.map(f => `  - ${f}`)
          ].join('\n') }]
        };
      }

      if (params.create_backup) {
        await fs.writeFile(filePath + '.bak', rawContent, "utf-8");
      }
      await fs.writeFile(filePath, content, "utf-8");

      return {
        content: [{ type: "text", text: [
          `✅ **Encoding repariert: ${path.basename(filePath)}**`, '',
          ...fixes.map(f => `  - ${f}`),
          params.create_backup ? `\n📋 Backup: ${filePath}.bak` : ''
        ].join('\n') }]
      };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: `❌ Fehler: ${error instanceof Error ? error.message : String(error)}` }] };
    }
  }
);

// ============================================================================
// Tool: Folder Diff
// ============================================================================

server.registerTool(
  "fc_folder_diff",
  {
    title: "Verzeichnis-Änderungen erkennen",
    description: `Vergleicht den aktuellen Zustand eines Verzeichnisses mit einem gespeicherten Snapshot.

Args:
  - path (string): Pfad zum Verzeichnis
  - save_snapshot (boolean): Aktuellen Zustand als neuen Snapshot speichern
  - extensions (string, optional): Dateierweiterungen filtern

Erkennt: Neue Dateien, geänderte Dateien, gelöschte Dateien
Snapshots werden in %TEMP%/.fc_snapshots/ gespeichert.`,
    inputSchema: {
      path: z.string().min(1).describe("Pfad zum Verzeichnis"),
      save_snapshot: z.boolean().default(true).describe("Snapshot speichern"),
      extensions: z.string().optional().describe("Erweiterungen filtern")
    },
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false
    }
  },
  async (params) => {
    try {
      const dirPath = normalizePath(params.path);
      if (!await pathExists(dirPath)) {
        return { isError: true, content: [{ type: "text", text: `❌ Verzeichnis nicht gefunden: ${dirPath}` }] };
      }

      const extFilter = params.extensions ? params.extensions.split(',').map(e => e.trim().toLowerCase()) : null;
      const snapshotDir = path.join(os.tmpdir(), '.fc_snapshots');
      const snapshotId = crypto.createHash('md5').update(dirPath).digest('hex');
      const snapshotFile = path.join(snapshotDir, `${snapshotId}.json`);

      // Scan current state
      interface FileEntry { size: number; mtime: number; }
      const currentState: Record<string, FileEntry> = {};

      async function scanDir(dir: string): Promise<void> {
        try {
          const entries = await fs.readdir(dir, { withFileTypes: true });
          for (const entry of entries) {
            const full = path.join(dir, entry.name);
            if (entry.isDirectory()) {
              if (!['node_modules', '.git', '$RECYCLE.BIN'].includes(entry.name)) {
                await scanDir(full);
              }
            } else if (entry.isFile()) {
              if (!extFilter || extFilter.includes(path.extname(entry.name).toLowerCase())) {
                const stats = await fs.stat(full);
                const rel = path.relative(dirPath, full);
                currentState[rel] = { size: stats.size, mtime: stats.mtimeMs };
              }
            }
          }
        } catch { /* skip inaccessible dirs */ }
      }
      await scanDir(dirPath);

      // Load previous snapshot
      let previousState: Record<string, FileEntry> = {};
      let hasSnapshot = false;
      try {
        const data = await fs.readFile(snapshotFile, "utf-8");
        previousState = JSON.parse(data);
        hasSnapshot = true;
      } catch { /* no previous snapshot */ }

      // Compare
      const newFiles: string[] = [];
      const modifiedFiles: string[] = [];
      const deletedFiles: string[] = [];

      for (const [rel, entry] of Object.entries(currentState)) {
        if (!previousState[rel]) {
          newFiles.push(rel);
        } else if (entry.size !== previousState[rel].size || Math.abs(entry.mtime - previousState[rel].mtime) > 1000) {
          modifiedFiles.push(rel);
        }
      }
      for (const rel of Object.keys(previousState)) {
        if (!currentState[rel]) {
          deletedFiles.push(rel);
        }
      }

      // Save snapshot
      if (params.save_snapshot) {
        await fs.mkdir(snapshotDir, { recursive: true });
        await fs.writeFile(snapshotFile, JSON.stringify(currentState), "utf-8");
      }

      const totalFiles = Object.keys(currentState).length;
      const totalChanges = newFiles.length + modifiedFiles.length + deletedFiles.length;

      if (!hasSnapshot) {
        return {
          content: [{ type: "text", text: [
            `📸 **Erster Snapshot erstellt: ${path.basename(dirPath)}**`, '',
            `| | |`, `|---|---|`,
            `| Dateien | ${totalFiles} |`,
            `| Snapshot | ${snapshotFile} |`, '',
            `Beim nächsten Aufruf werden Änderungen erkannt.`
          ].join('\n') }]
        };
      }

      if (totalChanges === 0) {
        return { content: [{ type: "text", text: `✅ Keine Änderungen in ${path.basename(dirPath)}. ${totalFiles} Dateien geprüft.` }] };
      }

      const output = [
        `📊 **Verzeichnis-Diff: ${path.basename(dirPath)}**`, '',
        `| Kategorie | Anzahl |`, `|---|---|`,
        `| Neue Dateien | ${newFiles.length} |`,
        `| Geändert | ${modifiedFiles.length} |`,
        `| Gelöscht | ${deletedFiles.length} |`,
        `| Unverändert | ${totalFiles - newFiles.length - modifiedFiles.length} |`
      ];

      if (newFiles.length > 0) {
        output.push('', '**Neue Dateien:**', ...newFiles.slice(0, 50).map(f => `  🟢 ${f}`));
        if (newFiles.length > 50) output.push(`  ... und ${newFiles.length - 50} weitere`);
      }
      if (modifiedFiles.length > 0) {
        output.push('', '**Geänderte Dateien:**', ...modifiedFiles.slice(0, 50).map(f => `  🟡 ${f}`));
        if (modifiedFiles.length > 50) output.push(`  ... und ${modifiedFiles.length - 50} weitere`);
      }
      if (deletedFiles.length > 0) {
        output.push('', '**Gelöschte Dateien:**', ...deletedFiles.slice(0, 50).map(f => `  🔴 ${f}`));
        if (deletedFiles.length > 50) output.push(`  ... und ${deletedFiles.length - 50} weitere`);
      }

      return { content: [{ type: "text", text: output.join('\n') }] };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: `❌ Fehler: ${error instanceof Error ? error.message : String(error)}` }] };
    }
  }
);

// ============================================================================
// Tool: Batch Rename
// ============================================================================

server.registerTool(
  "fc_batch_rename",
  {
    title: "Batch-Umbenennung",
    description: `Benennt Dateien nach Muster um: Prefix/Suffix entfernen, ersetzen, oder Pattern.

Args:
  - directory (string): Verzeichnis mit den Dateien
  - mode (string): "remove_prefix" | "remove_suffix" | "replace" | "auto_detect"
  - pattern (string, optional): Zu entfernender/ersetzender Text
  - replacement (string, optional): Ersetzungstext (für replace-Modus)
  - extensions (string, optional): Nur bestimmte Erweiterungen
  - dry_run (boolean): Nur Vorschau

Beispiele:
  - Prefix entfernen: mode="remove_prefix", pattern="backup_"
  - Auto-Detect: mode="auto_detect" erkennt gemeinsame Prefixe`,
    inputSchema: {
      directory: z.string().min(1).describe("Verzeichnis"),
      mode: z.enum(["remove_prefix", "remove_suffix", "replace", "auto_detect"]).describe("Modus"),
      pattern: z.string().optional().describe("Zu entfernender/ersetzender Text"),
      replacement: z.string().default("").describe("Ersetzungstext"),
      extensions: z.string().optional().describe("Erweiterungen filtern"),
      dry_run: z.boolean().default(true).describe("Nur Vorschau")
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: true,
      idempotentHint: false,
      openWorldHint: false
    }
  },
  async (params) => {
    try {
      const dirPath = normalizePath(params.directory);
      if (!await pathExists(dirPath)) {
        return { isError: true, content: [{ type: "text", text: `❌ Verzeichnis nicht gefunden: ${dirPath}` }] };
      }

      const extFilter = params.extensions ? params.extensions.split(',').map(e => e.trim().toLowerCase()) : null;
      const entries = await fs.readdir(dirPath, { withFileTypes: true });
      const files = entries.filter(e => e.isFile() && (!extFilter || extFilter.includes(path.extname(e.name).toLowerCase())));

      if (files.length === 0) {
        return { content: [{ type: "text", text: `🔍 Keine passenden Dateien in ${dirPath}` }] };
      }

      const renames: { old: string; new: string }[] = [];

      if (params.mode === 'auto_detect') {
        // Find common prefix
        const names = files.map(f => f.name);
        let commonPrefix = names[0] || '';
        for (let i = 1; i < names.length; i++) {
          while (!names[i].startsWith(commonPrefix) && commonPrefix.length > 0) {
            commonPrefix = commonPrefix.slice(0, -1);
          }
        }
        // Find common suffix (before extension)
        const stems = files.map(f => path.parse(f.name).name);
        let commonSuffix = stems[0] || '';
        for (let i = 1; i < stems.length; i++) {
          while (!stems[i].endsWith(commonSuffix) && commonSuffix.length > 0) {
            commonSuffix = commonSuffix.slice(1);
          }
        }

        const detections: string[] = [];
        if (commonPrefix.length >= 3) detections.push(`Prefix: "${commonPrefix}"`);
        if (commonSuffix.length >= 3) detections.push(`Suffix: "${commonSuffix}"`);

        if (detections.length === 0) {
          return { content: [{ type: "text", text: `🔍 Kein gemeinsames Muster erkannt bei ${files.length} Dateien.` }] };
        }

        // Use prefix if found
        if (commonPrefix.length >= 3) {
          for (const f of files) {
            const newName = f.name.slice(commonPrefix.length);
            if (newName.length > 0) {
              renames.push({ old: f.name, new: newName });
            }
          }
        }

        return {
          content: [{ type: "text", text: [
            `🔍 **Auto-Detect: ${files.length} Dateien**`, '',
            `Erkannte Muster: ${detections.join(', ')}`, '',
            renames.length > 0 ? `**Vorgeschlagene Umbenennung (Prefix "${commonPrefix}" entfernen):**` : '',
            ...renames.slice(0, 30).map(r => `  ${r.old} → ${r.new}`),
            renames.length > 30 ? `  ... und ${renames.length - 30} weitere` : '', '',
            `💡 Nutze \`mode="remove_prefix", pattern="${commonPrefix}", dry_run=false\` zum Ausführen.`
          ].join('\n') }]
        };
      }

      if (!params.pattern) {
        return { isError: true, content: [{ type: "text", text: `❌ 'pattern' erforderlich für Modus "${params.mode}".` }] };
      }

      for (const f of files) {
        let newName: string;
        switch (params.mode) {
          case 'remove_prefix':
            newName = f.name.startsWith(params.pattern) ? f.name.slice(params.pattern.length) : f.name;
            break;
          case 'remove_suffix': {
            const parsed = path.parse(f.name);
            newName = parsed.name.endsWith(params.pattern) ? parsed.name.slice(0, -params.pattern.length) + parsed.ext : f.name;
            break;
          }
          case 'replace':
            newName = f.name.replace(new RegExp(params.pattern.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), params.replacement);
            break;
          default:
            newName = f.name;
        }

        if (newName !== f.name && newName.length > 0) {
          renames.push({ old: f.name, new: newName });
        }
      }

      if (renames.length === 0) {
        return { content: [{ type: "text", text: `🔍 Keine Dateien passen zum Muster "${params.pattern}".` }] };
      }

      if (params.dry_run) {
        return {
          content: [{ type: "text", text: [
            `🔍 **Vorschau: ${renames.length} Umbenennungen**`, '',
            ...renames.map(r => `  ${r.old} → ${r.new}`), '',
            `💡 Setze \`dry_run=false\` zum Ausführen.`
          ].join('\n') }]
        };
      }

      let successCount = 0;
      const errors: string[] = [];
      for (const r of renames) {
        try {
          await fs.rename(path.join(dirPath, r.old), path.join(dirPath, r.new));
          successCount++;
        } catch (e) {
          errors.push(`${r.old}: ${e instanceof Error ? e.message : String(e)}`);
        }
      }

      return {
        content: [{ type: "text", text: [
          `✅ **${successCount}/${renames.length} Dateien umbenannt**`,
          ...errors.map(e => `  ❌ ${e}`)
        ].join('\n') }]
      };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: `❌ Fehler: ${error instanceof Error ? error.message : String(error)}` }] };
    }
  }
);

// ============================================================================
// Tool: Convert Format
// ============================================================================

server.registerTool(
  "fc_convert_format",
  {
    title: "Format konvertieren",
    description: `Konvertiert Dateien zwischen verschiedenen Formaten.

Args:
  - input_path (string): Pfad zur Quelldatei
  - output_path (string): Pfad zur Zieldatei
  - input_format (string): "json" | "csv" | "ini"
  - output_format (string): "json" | "csv" | "ini"
  - json_indent (number, optional): Einrückung für JSON (default: 2)

Unterstützte Konvertierungen:
  - JSON ↔ CSV (bei Arrays von Objekten)
  - JSON ↔ INI (bei flachen Objekten/Sektionen)
  - JSON pretty-print / minify`,
    inputSchema: {
      input_path: z.string().min(1).describe("Quelldatei"),
      output_path: z.string().min(1).describe("Zieldatei"),
      input_format: z.enum(["json", "csv", "ini"]).describe("Eingabeformat"),
      output_format: z.enum(["json", "csv", "ini"]).describe("Ausgabeformat"),
      json_indent: z.number().int().min(0).max(8).default(2).describe("JSON Einrückung")
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false
    }
  },
  async (params) => {
    try {
      const inputPath = normalizePath(params.input_path);
      const outputPath = normalizePath(params.output_path);
      if (!await pathExists(inputPath)) {
        return { isError: true, content: [{ type: "text", text: `❌ Quelldatei nicht gefunden: ${inputPath}` }] };
      }

      const rawContent = await fs.readFile(inputPath, "utf-8");
      let data: unknown;

      // Parse input
      switch (params.input_format) {
        case 'json':
          data = JSON.parse(rawContent);
          break;
        case 'csv': {
          const lines = rawContent.trim().split('\n');
          if (lines.length < 2) {
            return { isError: true, content: [{ type: "text", text: `❌ CSV benötigt mindestens Header + 1 Datenzeile.` }] };
          }
          const headers = lines[0].split(',').map(h => h.trim().replace(/^"|"$/g, ''));
          data = lines.slice(1).map(line => {
            const vals = line.split(',').map(v => v.trim().replace(/^"|"$/g, ''));
            const obj: Record<string, string> = {};
            headers.forEach((h, i) => { obj[h] = vals[i] || ''; });
            return obj;
          });
          break;
        }
        case 'ini': {
          const result: Record<string, Record<string, string>> = {};
          let currentSection = '_default';
          result[currentSection] = {};
          for (const line of rawContent.split('\n')) {
            const trimmed = line.trim();
            if (!trimmed || trimmed.startsWith(';') || trimmed.startsWith('#')) continue;
            const sectionMatch = trimmed.match(/^\[(.+)\]$/);
            if (sectionMatch) {
              currentSection = sectionMatch[1];
              result[currentSection] = result[currentSection] || {};
            } else {
              const eqIdx = trimmed.indexOf('=');
              if (eqIdx > 0) {
                const key = trimmed.substring(0, eqIdx).trim();
                const val = trimmed.substring(eqIdx + 1).trim();
                result[currentSection][key] = val;
              }
            }
          }
          // Remove empty default section
          if (Object.keys(result._default).length === 0) delete result._default;
          data = result;
          break;
        }
      }

      // Generate output
      let output: string;
      switch (params.output_format) {
        case 'json':
          output = JSON.stringify(data, null, params.json_indent || undefined);
          break;
        case 'csv': {
          if (!Array.isArray(data)) {
            return { isError: true, content: [{ type: "text", text: `❌ CSV-Export erfordert ein JSON-Array von Objekten.` }] };
          }
          const headers = Object.keys(data[0] || {});
          const rows = data.map((item: Record<string, unknown>) =>
            headers.map(h => {
              const val = String(item[h] ?? '');
              return val.includes(',') || val.includes('"') ? `"${val.replace(/"/g, '""')}"` : val;
            }).join(',')
          );
          output = [headers.join(','), ...rows].join('\n');
          break;
        }
        case 'ini': {
          if (typeof data !== 'object' || data === null || Array.isArray(data)) {
            return { isError: true, content: [{ type: "text", text: `❌ INI-Export erfordert ein JSON-Objekt.` }] };
          }
          const lines: string[] = [];
          for (const [section, values] of Object.entries(data as Record<string, unknown>)) {
            if (typeof values === 'object' && values !== null && !Array.isArray(values)) {
              lines.push(`[${section}]`);
              for (const [key, val] of Object.entries(values as Record<string, unknown>)) {
                lines.push(`${key} = ${val}`);
              }
              lines.push('');
            } else {
              lines.push(`${section} = ${values}`);
            }
          }
          output = lines.join('\n');
          break;
        }
      }

      // Ensure output directory exists
      const outDir = path.dirname(outputPath);
      if (!await pathExists(outDir)) {
        await fs.mkdir(outDir, { recursive: true });
      }

      await fs.writeFile(outputPath, output, "utf-8");
      const outStats = await fs.stat(outputPath);

      return {
        content: [{ type: "text", text: [
          `✅ **Konvertiert: ${params.input_format.toUpperCase()} → ${params.output_format.toUpperCase()}**`, '',
          `| | |`, `|---|---|`,
          `| Quelle | ${inputPath} |`,
          `| Ziel | ${outputPath} |`,
          `| Größe | ${formatFileSize(outStats.size)} |`
        ].join('\n') }]
      };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: `❌ Fehler: ${error instanceof Error ? error.message : String(error)}` }] };
    }
  }
);

// ============================================================================
// Tool: Detect Duplicates
// ============================================================================

server.registerTool(
  "fc_detect_duplicates",
  {
    title: "Duplikate erkennen",
    description: `Findet Datei-Duplikate in einem Verzeichnis anhand von SHA-256 Hashes.

Args:
  - directory (string): Verzeichnis zum Scannen
  - recursive (boolean): Rekursiv suchen
  - extensions (string, optional): Nur bestimmte Erweiterungen
  - min_size (number, optional): Mindestgröße in Bytes (default: 1)
  - max_size (number, optional): Maximale Größe in Bytes

Returns:
  - Gruppen von Duplikaten mit Pfaden und Größen`,
    inputSchema: {
      directory: z.string().min(1).describe("Verzeichnis"),
      recursive: z.boolean().default(true).describe("Rekursiv"),
      extensions: z.string().optional().describe("Erweiterungen filtern"),
      min_size: z.number().int().min(0).default(1).describe("Mindestgröße in Bytes"),
      max_size: z.number().int().optional().describe("Maximale Größe in Bytes")
    },
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false
    }
  },
  async (params) => {
    try {
      const dirPath = normalizePath(params.directory);
      if (!await pathExists(dirPath)) {
        return { isError: true, content: [{ type: "text", text: `❌ Verzeichnis nicht gefunden: ${dirPath}` }] };
      }

      const extFilter = params.extensions ? params.extensions.split(',').map(e => e.trim().toLowerCase()) : null;

      // Collect files with sizes
      const files: { path: string; size: number }[] = [];
      async function collectFiles(dir: string): Promise<void> {
        try {
          const entries = await fs.readdir(dir, { withFileTypes: true });
          for (const entry of entries) {
            const full = path.join(dir, entry.name);
            if (entry.isDirectory() && params.recursive) {
              if (!['node_modules', '.git', '$RECYCLE.BIN'].includes(entry.name)) {
                await collectFiles(full);
              }
            } else if (entry.isFile()) {
              if (!extFilter || extFilter.includes(path.extname(entry.name).toLowerCase())) {
                const stats = await fs.stat(full);
                if (stats.size >= params.min_size && (!params.max_size || stats.size <= params.max_size)) {
                  files.push({ path: full, size: stats.size });
                }
              }
            }
          }
        } catch { /* skip inaccessible */ }
      }
      await collectFiles(dirPath);

      // Group by size first (quick filter)
      const sizeGroups: Map<number, string[]> = new Map();
      for (const f of files) {
        const group = sizeGroups.get(f.size) || [];
        group.push(f.path);
        sizeGroups.set(f.size, group);
      }

      // Hash only files with matching sizes
      const hashGroups: Map<string, { paths: string[]; size: number }> = new Map();
      let hashedCount = 0;

      for (const [size, paths] of sizeGroups) {
        if (paths.length < 2) continue;

        for (const filePath of paths) {
          try {
            const content = await fs.readFile(filePath);
            const hash = crypto.createHash('sha256').update(content).digest('hex');
            hashedCount++;

            const group = hashGroups.get(hash) || { paths: [], size };
            group.paths.push(filePath);
            hashGroups.set(hash, group);
          } catch { /* skip unreadable */ }
        }
      }

      // Filter to actual duplicates
      const duplicates = [...hashGroups.values()].filter(g => g.paths.length > 1);
      const totalDuplicateFiles = duplicates.reduce((sum, g) => sum + g.paths.length - 1, 0);
      const totalWastedSpace = duplicates.reduce((sum, g) => sum + g.size * (g.paths.length - 1), 0);

      if (duplicates.length === 0) {
        return {
          content: [{ type: "text", text: `✅ Keine Duplikate gefunden. ${files.length} Dateien geprüft, ${hashedCount} gehasht.` }]
        };
      }

      const output = [
        `🔍 **Duplikate gefunden**`, '',
        `| | |`, `|---|---|`,
        `| Geprüfte Dateien | ${files.length} |`,
        `| Duplikat-Gruppen | ${duplicates.length} |`,
        `| Duplikate gesamt | ${totalDuplicateFiles} |`,
        `| Verschwendeter Platz | ${formatFileSize(totalWastedSpace)} |`
      ];

      for (let i = 0; i < Math.min(duplicates.length, 20); i++) {
        const group = duplicates[i];
        output.push('', `**Gruppe ${i + 1}** (${formatFileSize(group.size)}):`);
        for (const p of group.paths) {
          output.push(`  📄 ${path.relative(dirPath, p)}`);
        }
      }

      if (duplicates.length > 20) {
        output.push('', `... und ${duplicates.length - 20} weitere Gruppen`);
      }

      output.push('', `💡 Nutze \`fc_safe_delete\` zum sicheren Entfernen von Duplikaten.`);

      return { content: [{ type: "text", text: output.join('\n') }] };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: `❌ Fehler: ${error instanceof Error ? error.message : String(error)}` }] };
    }
  }
);

// ============================================================================
// Tool: Markdown to HTML
// ============================================================================

server.registerTool(
  "fc_md_to_html",
  {
    title: "Markdown zu HTML",
    description: `Konvertiert Markdown zu formatiertem HTML (druckbar als PDF).

Args:
  - input_path (string): Pfad zur Markdown-Datei
  - output_path (string): Pfad zur HTML-Ausgabe
  - title (string, optional): Dokumenttitel

Erzeugt eigenstaendiges HTML mit CSS-Styling, druckbar als PDF ueber den Browser.`,
    inputSchema: {
      input_path: z.string().min(1).describe("Markdown-Datei"),
      output_path: z.string().min(1).describe("HTML-Ausgabe"),
      title: z.string().optional().describe("Dokumenttitel")
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false
    }
  },
  async (params) => {
    try {
      const inputPath = normalizePath(params.input_path);
      const outputPath = normalizePath(params.output_path);
      if (!await pathExists(inputPath)) {
        return { isError: true, content: [{ type: "text", text: `❌ Datei nicht gefunden: ${inputPath}` }] };
      }

      const md = await fs.readFile(inputPath, "utf-8");
      const title = params.title || path.basename(inputPath, '.md');

      // --- Inline formatting ---
      const inlineFmt = (text: string): string => {
        text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
        text = text.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
        text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        text = text.replace(/(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)/g, '<em>$1</em>');
        text = text.replace(/\[!\[([^\]]*)\]\(([^)]+)\)\]\(([^)]+)\)/g, '<a href="$3"><img src="$2" alt="$1"></a>');
        text = text.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1">');
        text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
        text = text.replace(/\[x\]/gi, '&#9745;');
        text = text.replace(/\[ \]/g, '&#9744;');
        return text;
      };

      // --- Table parser ---
      const parseTable = (tableLines: string[]): string => {
        if (tableLines.length < 2) return `<p>${inlineFmt(tableLines[0])}</p>`;
        const rows = tableLines.map(tl => tl.replace(/^\||\|$/g, '').split('|').map(c => c.trim()));
        let out = '<table>\n<thead>\n<tr>';
        for (const cell of rows[0]) out += `<th>${inlineFmt(cell)}</th>`;
        out += '</tr>\n</thead>\n<tbody>\n';
        for (let r = 2; r < rows.length; r++) {
          out += '<tr>';
          for (const cell of rows[r]) out += `<td>${inlineFmt(cell)}</td>`;
          out += '</tr>\n';
        }
        out += '</tbody>\n</table>';
        return out;
      };

      // --- List parser (nested, ordered + unordered) ---
      const parseList = (allLines: string[], start: number): [string, number] => {
        const result: string[] = [];
        const stack: string[] = [];
        let li = start;
        while (li < allLines.length) {
          const lline = allLines[li].trimEnd();
          const lm = lline.match(/^(\s*)([-*]|\d+\.)\s+(.+)$/);
          if (!lm) break;
          const indent = lm[1].length;
          const marker = lm[2];
          const content = inlineFmt(lm[3]);
          const tag = /^\d/.test(marker) ? 'ol' : 'ul';
          const depth = Math.floor(indent / 2);
          while (stack.length > depth + 1) result.push(`</${stack.pop()}>`);
          while (stack.length <= depth) { result.push(`<${tag}>`); stack.push(tag); }
          result.push(`<li>${content}</li>`);
          li++;
        }
        while (stack.length > 0) result.push(`</${stack.pop()}>`);
        return [result.join('\n'), li];
      };

      // --- Line-by-line parser ---
      const lines = md.split('\n');
      const parts: string[] = [];
      let i = 0;
      const n = lines.length;

      while (i < n) {
        const line = lines[i].trimEnd();

        // Fenced code block
        if (line.trimStart().startsWith('```')) {
          const lang = line.trim().slice(3).trim();
          const codeLines: string[] = [];
          i++;
          while (i < n && !lines[i].trimEnd().trimStart().startsWith('```')) {
            codeLines.push(lines[i].trimEnd().replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'));
            i++;
          }
          i++;
          parts.push(`<pre><code class="language-${lang}">${codeLines.join('\n')}</code></pre>`);
          continue;
        }

        // Table
        if (line.includes('|') && line.trim().startsWith('|') && line.trim().endsWith('|')) {
          const tableLines: string[] = [];
          while (i < n && lines[i].includes('|') && lines[i].trim().startsWith('|')) {
            tableLines.push(lines[i].trim());
            i++;
          }
          parts.push(parseTable(tableLines));
          continue;
        }

        // Blockquote
        if (line.startsWith('>')) {
          const bqLines: string[] = [];
          while (i < n && lines[i].trimEnd().startsWith('>')) {
            bqLines.push(inlineFmt(lines[i].trimEnd().replace(/^>\s*/, '')));
            i++;
          }
          parts.push(`<blockquote><p>${bqLines.join('<br>')}</p></blockquote>`);
          continue;
        }

        // Empty line
        if (line.trim() === '') { i++; continue; }

        // Horizontal rule
        if (/^(-{3,}|={3,}|\*{3,})$/.test(line.trim())) { parts.push('<hr>'); i++; continue; }

        // Header
        const hm = line.match(/^(#{1,6})\s+(.+)$/);
        if (hm) {
          const lvl = hm[1].length;
          parts.push(`<h${lvl}>${inlineFmt(hm[2])}</h${lvl}>`);
          i++;
          continue;
        }

        // List (ordered or unordered)
        if (/^(\s*)([-*]|\d+\.)\s+/.test(line)) {
          const [listHtml, nextI] = parseList(lines, i);
          parts.push(listHtml);
          i = nextI;
          continue;
        }

        // Normal paragraph
        parts.push(`<p>${inlineFmt(line)}</p>`);
        i++;
      }

      const html = parts.join('\n');

      const fullHtml = `<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <title>${title}</title>
  <style>
    body { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; line-height: 1.7; color: #2c3e50; font-size: 11pt; }
    h1 { color: #1a252f; border-bottom: 3px solid #3498db; padding-bottom: 12px; font-size: 22pt; }
    h2 { color: #2c3e50; border-bottom: 1px solid #bdc3c7; padding-bottom: 6px; margin-top: 28px; font-size: 16pt; }
    h3 { color: #34495e; margin-top: 22px; font-size: 13pt; }
    h4 { color: #7f8c8d; margin-top: 18px; font-size: 11pt; font-style: italic; }
    p { margin: 8px 0; }
    code { background: #f0f3f5; padding: 2px 6px; border-radius: 4px; font-family: 'Cascadia Code', Consolas, 'Courier New', monospace; font-size: 0.9em; color: #c0392b; }
    pre { background: #1e1e2e; color: #cdd6f4; padding: 16px 20px; border-radius: 8px; overflow-x: auto; font-size: 9.5pt; line-height: 1.5; margin: 14px 0; }
    pre code { background: none; color: inherit; padding: 0; font-size: inherit; }
    blockquote { border-left: 4px solid #3498db; margin: 16px 0; padding: 10px 20px; background: #f8f9fa; color: #555; border-radius: 0 6px 6px 0; }
    blockquote p { margin: 4px 0; }
    table { border-collapse: collapse; width: 100%; margin: 16px 0; font-size: 10pt; }
    th { background: #2c3e50; color: white; padding: 10px 14px; text-align: left; font-weight: 600; }
    td { border: 1px solid #ddd; padding: 8px 14px; }
    tr:nth-child(even) { background: #f8f9fa; }
    ul, ol { margin: 6px 0; padding-left: 24px; }
    li { margin: 4px 0; }
    hr { border: none; border-top: 1px solid #e0e0e0; margin: 24px 0; }
    a { color: #2980b9; text-decoration: none; }
    a:hover { text-decoration: underline; }
    img { max-width: 100%; }
    @media print { body { max-width: none; margin: 0; } @page { margin: 2cm 2.5cm; size: A4; } }
  </style>
</head>
<body>
${html}
</body>
</html>`;

      const outDir = path.dirname(outputPath);
      if (!await pathExists(outDir)) await fs.mkdir(outDir, { recursive: true });
      await fs.writeFile(outputPath, fullHtml, "utf-8");
      const outStats = await fs.stat(outputPath);

      return {
        content: [{ type: "text", text: [
          `✅ **Markdown → HTML: ${path.basename(outputPath)}**`, '',
          `| | |`, `|---|---|`,
          `| Quelle | ${inputPath} |`,
          `| Ziel | ${outputPath} |`,
          `| Größe | ${formatFileSize(outStats.size)} |`, '',
          `💡 Öffne die HTML-Datei im Browser und drucke als PDF.`
        ].join('\n') }]
      };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: `❌ Fehler: ${error instanceof Error ? error.message : String(error)}` }] };
    }
  }
);

// ============================================================================
// Server Startup
// ============================================================================

async function main(): Promise<void> {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("🚀 BACH FileCommander MCP Server gestartet");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
