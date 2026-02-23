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
import { t, setLanguage, getLanguage } from './i18n/index.js';
import type { Lang } from './i18n/index.js';
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
  version: "1.5.0"
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
    title: "Read File",
    description: `Reads the content of a file.

Args:
  - path (string): Full path to the file
  - encoding (string, optional): Character encoding (default: utf-8)
  - max_lines (number, optional): Maximum number of lines (0 = all)

Returns:
  - File content as text
  - For binary files: Base64-encoded content

Examples:
  - path: "C:\\Users\\User\\test.txt"
  - path: "/home/user/config.json"`,
    inputSchema: {
      path: z.string().min(1).describe("Full path to the file"),
      encoding: z.string().default("utf-8").describe("Character encoding"),
      max_lines: z.number().int().min(0).default(0).describe("Max lines (0 = all)")
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
          content: [{ type: "text", text: t().common.fileNotFound(filePath) }]
        };
      }

      const stats = await fs.stat(filePath);
      if (stats.isDirectory()) {
        return {
          isError: true,
          content: [{ type: "text", text: t().common.pathIsDirectoryUseListDir(filePath) }]
        };
      }

      let content = await fs.readFile(filePath, params.encoding as BufferEncoding);

      if (params.max_lines > 0) {
        const lines = content.split('\n');
        content = lines.slice(0, params.max_lines).join('\n');
        if (lines.length > params.max_lines) {
          content += t().fc_read_file.moreLines(lines.length - params.max_lines);
        }
      }

      return {
        content: [{
          type: "text",
          text: `${t().fc_read_file.fileHeader(path.basename(filePath), formatFileSize(stats.size))}\n\n${content}`
        }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: t().fc_read_file.readError(errorMsg) }]
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
    title: "Write File",
    description: `Writes content to a file. Creates the file if it does not exist.

Args:
  - path (string): Full path to the file
  - content (string): Content to write
  - append (boolean, optional): Append to file instead of overwriting
  - create_dirs (boolean, optional): Create missing directories

Returns:
  - Confirmation with file size

Warning: Overwrites existing files without warning when append=false!`,
    inputSchema: {
      path: z.string().min(1).describe("Full path to the file"),
      content: z.string().describe("Content to write"),
      append: z.boolean().default(false).describe("Append to file"),
      create_dirs: z.boolean().default(true).describe("Create missing directories")
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
      const action = params.append ? t().fc_write_file.actionAppended : t().fc_write_file.actionWritten;

      return {
        content: [{
          type: "text",
          text: `${t().fc_write_file.success(action, filePath)}\n${t().fc_write_file.sizeLabel(formatFileSize(stats.size))}`
        }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: t().fc_write_file.writeError(errorMsg) }]
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
    title: "List Directory",
    description: `Lists files and subdirectories.

Args:
  - path (string): Path to the directory
  - depth (number, optional): Maximum depth for recursive listing (default: 1)
  - show_hidden (boolean, optional): Show hidden files

Returns:
  - Formatted list of all entries with icons`,
    inputSchema: {
      path: z.string().min(1).describe("Path to the directory"),
      depth: z.number().int().min(0).max(10).default(1).describe("Recursion depth"),
      show_hidden: z.boolean().default(false).describe("Show hidden files")
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
          content: [{ type: "text", text: t().common.dirNotFound(dirPath) }]
        };
      }

      const stats = await fs.stat(dirPath);
      if (!stats.isDirectory()) {
        return {
          isError: true,
          content: [{ type: "text", text: t().common.pathIsNotDirUseReadFile(dirPath) }]
        };
      }

      const entries = await listDirectoryRecursive(dirPath, params.depth);

      // Filter hidden files if needed
      const filteredEntries = params.show_hidden
        ? entries
        : entries.filter(e => !e.trim().startsWith('\uD83D\uDCC1 .') && !e.trim().startsWith('\uD83D\uDCC4 .'));

      return {
        content: [{
          type: "text",
          text: `${t().fc_list_directory.dirHeader(dirPath)}\n\n${filteredEntries.join('\n') || t().fc_list_directory.emptyDir}`
        }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: t().fc_list_directory.listError(errorMsg) }]
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
    title: "Create Directory",
    description: `Creates a new directory (including parent directories).

Args:
  - path (string): Path to the new directory

Returns:
  - Confirmation of creation`,
    inputSchema: {
      path: z.string().min(1).describe("Path to the new directory")
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
          content: [{ type: "text", text: t().fc_create_directory.alreadyExists(dirPath) }]
        };
      }

      await fs.mkdir(dirPath, { recursive: true });

      return {
        content: [{ type: "text", text: t().fc_create_directory.created(dirPath) }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: t().fc_create_directory.createError(errorMsg) }]
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
    title: "Delete File",
    description: `Deletes a file.

Args:
  - path (string): Path to the file

Warning: Irreversible! No recycle bin.`,
    inputSchema: {
      path: z.string().min(1).describe("Path to the file")
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
          content: [{ type: "text", text: t().common.fileNotFound(filePath) }]
        };
      }

      const stats = await fs.stat(filePath);
      if (stats.isDirectory()) {
        return {
          isError: true,
          content: [{ type: "text", text: t().common.pathIsDirectoryUseDeleteDir }]
        };
      }

      await fs.unlink(filePath);

      return {
        content: [{ type: "text", text: t().fc_delete_file.deleted(filePath) }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: t().fc_delete_file.deleteError(errorMsg) }]
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
    title: "Delete Directory",
    description: `Deletes a directory.

Args:
  - path (string): Path to the directory
  - recursive (boolean): Delete non-empty directories too

Warning: With recursive=true ALL contents are irreversibly deleted!`,
    inputSchema: {
      path: z.string().min(1).describe("Path to the directory"),
      recursive: z.boolean().default(false).describe("Delete recursively")
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
          content: [{ type: "text", text: t().common.dirNotFound(dirPath) }]
        };
      }

      const stats = await fs.stat(dirPath);
      if (!stats.isDirectory()) {
        return {
          isError: true,
          content: [{ type: "text", text: t().common.pathIsNotDirectory(dirPath) }]
        };
      }

      await fs.rm(dirPath, { recursive: params.recursive });

      return {
        content: [{ type: "text", text: t().fc_delete_directory.deleted(dirPath) }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      if (errorMsg.includes('ENOTEMPTY')) {
        return {
          isError: true,
          content: [{ type: "text", text: t().fc_delete_directory.notEmpty }]
        };
      }
      return {
        isError: true,
        content: [{ type: "text", text: t().fc_delete_directory.deleteError(errorMsg) }]
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
    title: "Move/Rename",
    description: `Moves or renames a file/directory.

Args:
  - source (string): Source path
  - destination (string): Destination path

Examples:
  - Rename: source="test.txt", destination="test_new.txt"
  - Move: source="C:\\a\\test.txt", destination="C:\\b\\test.txt"`,
    inputSchema: {
      source: z.string().min(1).describe("Source path"),
      destination: z.string().min(1).describe("Destination path")
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
          content: [{ type: "text", text: t().common.sourceNotFound(sourcePath) }]
        };
      }

      // Create destination directory if needed
      const destDir = path.dirname(destPath);
      if (!await pathExists(destDir)) {
        await fs.mkdir(destDir, { recursive: true });
      }

      await fs.rename(sourcePath, destPath);

      return {
        content: [{ type: "text", text: t().fc_move.moved(sourcePath, destPath) }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: t().fc_move.moveError(errorMsg) }]
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
    title: "Copy",
    description: `Copies a file or directory.

Args:
  - source (string): Source path
  - destination (string): Destination path
  - recursive (boolean): Copy directories recursively`,
    inputSchema: {
      source: z.string().min(1).describe("Source path"),
      destination: z.string().min(1).describe("Destination path"),
      recursive: z.boolean().default(true).describe("Copy recursively")
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
          content: [{ type: "text", text: t().common.sourceNotFound(sourcePath) }]
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
        content: [{ type: "text", text: t().fc_copy.copied(sourcePath, destPath) }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: t().fc_copy.copyError(errorMsg) }]
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
    title: "File Information",
    description: `Shows detailed information about a file/directory.

Args:
  - path (string): Path to the file/directory

Returns:
  - Size, type, creation/modification date, permissions`,
    inputSchema: {
      path: z.string().min(1).describe("Path to the file/directory")
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
          content: [{ type: "text", text: t().common.pathNotFound(targetPath) }]
        };
      }

      const stats = await fs.stat(targetPath);
      const fileType = stats.isDirectory() ? t().fc_file_info.typeDirectory : stats.isFile() ? t().fc_file_info.typeFile : t().fc_file_info.typeOther;
      const locale = getLanguage() === 'de' ? 'de-DE' : 'en-US';

      const info = [
        t().fc_file_info.header(path.basename(targetPath)),
        ``,
        `| ${t().fc_file_info.propType} | ${fileType} |`,
        `|-------------|------|`,
        `| ${t().fc_file_info.propSize} | ${formatFileSize(stats.size)} |`,
        `| ${t().fc_file_info.propCreated} | ${stats.birthtime.toLocaleString(locale)} |`,
        `| ${t().fc_file_info.propModified} | ${stats.mtime.toLocaleString(locale)} |`,
        `| ${t().fc_file_info.propAccessed} | ${stats.atime.toLocaleString(locale)} |`,
        `| ${t().fc_file_info.propPath} | ${targetPath} |`
      ];

      return {
        content: [{ type: "text", text: info.join('\n') }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: t().common.errorGeneric(errorMsg) }]
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
    title: "Search Files",
    description: `Searches files by name/pattern in a directory.

Args:
  - directory (string): Start directory for the search
  - pattern (string): Search pattern (supports * and ? wildcards)
  - max_results (number, optional): Maximum results (default: 50)

Examples:
  - pattern: "*.txt" - All text files
  - pattern: "test*" - Files starting with "test"
  - pattern: "*.py" - All Python files`,
    inputSchema: {
      directory: z.string().min(1).describe("Start directory"),
      pattern: z.string().min(1).describe("Search pattern with wildcards"),
      max_results: z.number().int().min(1).max(500).default(50).describe("Max results")
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
          content: [{ type: "text", text: t().common.dirNotFound(dirPath) }]
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
          content: [{ type: "text", text: t().fc_search_files.noResults(params.pattern) }]
        };
      }

      const output = [
        t().fc_search_files.resultsHeader(params.pattern),
        t().fc_search_files.inDir(dirPath),
        `${t().fc_search_files.found(results.length)} ${results.length >= params.max_results ? t().fc_search_files.maxReached : ''}`,
        ``,
        ...results.map(r => `  \uD83D\uDCC4 ${r}`)
      ];

      return {
        content: [{ type: "text", text: output.join('\n') }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: t().fc_search_files.searchError(errorMsg) }]
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
    title: "Start Async Search",
    description: `Starts a background search. Claude can perform other tasks in the meantime.

Args:
  - directory (string): Start directory
  - pattern (string): Search pattern (wildcards: * and ?)

Returns:
  - Search ID for fc_get_search_results, fc_stop_search

Example:
  Start search: fc_start_search("C:\\Users", "*.pdf")
  Get results later: fc_get_search_results(search_id)`,
    inputSchema: {
      directory: z.string().min(1).describe("Start directory"),
      pattern: z.string().min(1).describe("Search pattern with wildcards")
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
          content: [{ type: "text", text: t().common.dirNotFound(dirPath) }]
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
          text: `${t().fc_start_search.started(searchId, dirPath, params.pattern)}\n\n${t().fc_start_search.useGetResults}`
        }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: t().fc_start_search.startError(errorMsg) }]
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
    title: "Get Search Results",
    description: `Retrieves results of a running or completed search.

Args:
  - search_id (string): Search ID from fc_start_search
  - offset (number, optional): Start offset for pagination
  - limit (number, optional): Maximum number of results (default: 50)

Returns:
  - Search status and found files`,
    inputSchema: {
      search_id: z.string().min(1).describe("Search ID"),
      offset: z.number().int().min(0).default(0).describe("Start offset"),
      limit: z.number().int().min(1).max(200).default(50).describe("Max results")
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
        content: [{ type: "text", text: `${t().fc_get_search_results.notFound(params.search_id)}\n\n${t().fc_get_search_results.useListSearches}` }]
      };
    }

    const status = session.isRunning ? t().fc_get_search_results.statusRunning : t().fc_get_search_results.statusDone;
    const runtime = Math.round((Date.now() - session.startTime.getTime()) / 1000);
    const totalResults = session.results.length;
    const paginatedResults = session.results.slice(params.offset, params.offset + params.limit);
    const hasMore = totalResults > params.offset + params.limit;

    const output = [
      t().fc_get_search_results.header(status),
      ``,
      `| | |`,
      `|---|---|`,
      `| ${t().fc_get_search_results.labelPattern} | ${session.patternString} |`,
      `| ${t().fc_get_search_results.labelDirectory} | ${session.directory} |`,
      `| ${t().fc_get_search_results.labelScannedDirs} | ${session.scannedDirs} |`,
      `| ${t().fc_get_search_results.labelFound(totalResults)} | |`,
      `| ${t().fc_get_search_results.labelRuntime(runtime)} | |`,
      ``,
      t().fc_get_search_results.resultsRange(params.offset + 1, Math.min(params.offset + params.limit, totalResults), totalResults),
      ``,
      ...paginatedResults.map(r => `  \uD83D\uDCC4 ${r}`)
    ];

    if (hasMore) {
      output.push(``, t().fc_get_search_results.moreResults(params.search_id, params.offset + params.limit));
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
    title: "Stop Search",
    description: `Stops a running background search.

Args:
  - search_id (string): Search ID`,
    inputSchema: {
      search_id: z.string().min(1).describe("Search ID")
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
        content: [{ type: "text", text: t().fc_stop_search.notFound(params.search_id) }]
      };
    }

    if (!session.isRunning) {
      return {
        content: [{ type: "text", text: t().fc_stop_search.alreadyDone(session.results.length) }]
      };
    }

    session.isRunning = false;
    session.abortController.abort();

    return {
      content: [{ type: "text", text: `${t().fc_stop_search.stopped(params.search_id)}\n${t().fc_stop_search.resultsSoFar(session.results.length)}` }]
    };
  }
);

// ============================================================================
// Tool: List Searches
// ============================================================================

server.registerTool(
  "fc_list_searches",
  {
    title: "List Searches",
    description: `Lists all active and completed background searches.`,
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
        content: [{ type: "text", text: `${t().fc_list_searches.noSearches}\n\n${t().fc_list_searches.useStartSearch}` }]
      };
    }

    const rows: string[] = [];

    for (const [id, session] of searchSessions) {
      const status = session.isRunning ? '\uD83D\uDD04' : '\u2705';
      const runtime = Math.round((Date.now() - session.startTime.getTime()) / 1000);
      rows.push(`| ${status} | \`${id}\` | ${session.patternString} | ${session.results.length} | ${runtime}s |`);
    }

    const output = [
      t().fc_list_searches.header(searchSessions.size),
      ``,
      `| ${t().fc_list_searches.colStatus} | ${t().fc_list_searches.colSearchId} | ${t().fc_list_searches.colPattern} | ${t().fc_list_searches.colResults} | ${t().fc_list_searches.colRuntime} |`,
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
    title: "Clear Search",
    description: `Removes a completed search from the list and frees memory.

Args:
  - search_id (string): Search ID (or "all" for all completed)`,
    inputSchema: {
      search_id: z.string().min(1).describe("Search ID or 'all'")
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
        content: [{ type: "text", text: t().fc_clear_search.cleared(count) }]
      };
    }

    const session = searchSessions.get(params.search_id);

    if (!session) {
      return {
        isError: true,
        content: [{ type: "text", text: t().fc_clear_search.notFound(params.search_id) }]
      };
    }

    if (session.isRunning) {
      return {
        isError: true,
        content: [{ type: "text", text: t().fc_clear_search.stillRunning }]
      };
    }

    searchSessions.delete(params.search_id);

    return {
      content: [{ type: "text", text: t().fc_clear_search.removed(params.search_id) }]
    };
  }
);

// ============================================================================
// Tool: Safe Delete (Papierkorb)
// ============================================================================

server.registerTool(
  "fc_safe_delete",
  {
    title: "Safe Delete (Recycle Bin)",
    description: `Moves files/directories to recycle bin instead of deleting them.

Args:
  - path (string): Path to the file/directory

SAFE: Can be restored from the recycle bin!

Note: Uses Windows recycle bin or creates backup on other systems.`,
    inputSchema: {
      path: z.string().min(1).describe("Path to the file/directory")
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
          content: [{ type: "text", text: t().common.pathNotFound(targetPath) }]
        };
      }

      const stats = await fs.stat(targetPath);
      const itemType = stats.isDirectory() ? t().fc_safe_delete.typeDirectory : t().fc_safe_delete.typeFile;
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
            text: `${t().fc_safe_delete.movedToTrash}\n\n| | |\n|---|---|\n| ${t().fc_safe_delete.propType} | ${itemType} |\n| ${t().fc_safe_delete.propPath} | ${targetPath} |\n\n${t().fc_safe_delete.canRestore}`
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
            text: `${t().fc_safe_delete.movedToTrash}\n\n| | |\n|---|---|\n| ${t().fc_safe_delete.propType} | ${itemType} |\n| ${t().fc_safe_delete.propOriginal} | ${targetPath} |\n| ${t().fc_safe_delete.propTrash} | ${trashPath} |\n\n${t().fc_safe_delete.canRestore}`
          }]
        };
      }
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: t().fc_safe_delete.trashError(errorMsg) }]
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
    title: "Execute Command",
    description: `Executes a shell command and returns the output.

Args:
  - command (string): Command to execute
  - cwd (string, optional): Working directory
  - timeout (number, optional): Timeout in milliseconds (default: 30000)

Warning: Commands are executed with user privileges!

Examples:
  - command: "dir" (Windows)
  - command: "ls -la" (Unix)
  - command: "python --version"`,
    inputSchema: {
      command: z.string().min(1).describe("Command to execute"),
      cwd: z.string().optional().describe("Working directory"),
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

      const output: string[] = [t().fc_execute_command.commandLabel(params.command)];

      if (stdout.trim()) {
        output.push(`\n${t().fc_execute_command.outputLabel}\n\`\`\`\n${stdout.trim()}\n\`\`\``);
      }

      if (stderr.trim()) {
        output.push(`\n${t().fc_execute_command.stderrLabel}\n\`\`\`\n${stderr.trim()}\n\`\`\``);
      }

      if (!stdout.trim() && !stderr.trim()) {
        output.push(`\n${t().fc_execute_command.noOutput}`);
      }
      
      return {
        content: [{ type: "text", text: output.join('') }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: t().fc_execute_command.execError(errorMsg) }]
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
    title: "Start Process",
    description: `Starts a process in the background (non-blocking).

Args:
  - program (string): Program/Executable
  - args (array, optional): Arguments as array
  - cwd (string, optional): Working directory

Examples:
  - program: "notepad.exe", args: ["test.txt"]
  - program: "python", args: ["script.py"]
  - program: "code", args: ["."] (open VS Code)`,
    inputSchema: {
      program: z.string().min(1).describe("Program/Executable"),
      args: z.array(z.string()).default([]).describe("Arguments"),
      cwd: z.string().optional().describe("Working directory")
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
          text: `${t().fc_start_process.started(params.program, argsStr)}\n${t().fc_start_process.pidLabel(child.pid)}`
        }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: t().fc_start_process.startError(errorMsg) }]
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
    title: "Current Time",
    description: `Returns the current system time.

Returns:
  - Date, time, weekday, timezone`,
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
    const locale = getLanguage() === 'de' ? 'de-DE' : 'en-US';

    const output = [
      t().fc_get_time.header,
      ``,
      `| | |`,
      `|---|---|`,
      `| ${t().fc_get_time.labelDate} | ${now.toLocaleDateString(locale)} |`,
      `| ${t().fc_get_time.labelTime} | ${now.toLocaleTimeString(locale)} |`,
      `| ${t().fc_get_time.labelWeekday} | ${t().common.weekdays[now.getDay()]} |`,
      `| ${t().fc_get_time.labelISO} | ${now.toISOString()} |`,
      `| ${t().fc_get_time.labelTimezone} | ${Intl.DateTimeFormat().resolvedOptions().timeZone} |`
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
    title: "Read Multiple Files",
    description: `Reads multiple files at once and returns their contents.

Args:
  - paths (array): Array of file paths
  - max_lines_per_file (number, optional): Max lines per file (0 = all)

Returns:
  - Contents of all files with separators

Example:
  paths: ["C:\\config.json", "C:\\readme.md"]`,
    inputSchema: {
      paths: z.array(z.string().min(1)).min(1).max(20).describe("Array of file paths"),
      max_lines_per_file: z.number().int().min(0).default(0).describe("Max lines per file")
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
          results.push(`\n\u274C **${path.basename(normalizedPath)}** - ${t().fc_read_multiple_files.notFound}\n`);
          errorCount++;
          continue;
        }

        const stats = await fs.stat(normalizedPath);
        if (stats.isDirectory()) {
          results.push(`\n\u274C **${path.basename(normalizedPath)}** - ${t().fc_read_multiple_files.isDirectory}\n`);
          errorCount++;
          continue;
        }

        let content = await fs.readFile(normalizedPath, "utf-8");
        
        if (params.max_lines_per_file > 0) {
          const lines = content.split('\n');
          content = lines.slice(0, params.max_lines_per_file).join('\n');
          if (lines.length > params.max_lines_per_file) {
            content += `\n${t().fc_read_multiple_files.moreLines(lines.length - params.max_lines_per_file)}`;
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

    const summary = `${t().fc_read_multiple_files.summary(successCount, errorCount)}\n${'═'.repeat(60)}`;
    
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
    title: "Edit File (Lines)",
    description: `Edits a file line-based: replace, insert, or delete.

Args:
  - path (string): Path to the file
  - operation (string): "replace" | "insert" | "delete"
  - start_line (number): Start line (1-based)
  - end_line (number, optional): End line for replace/delete
  - content (string, optional): New content for replace/insert

Examples:
  - Replace lines 5-10: operation="replace", start_line=5, end_line=10, content="new text"
  - Insert after line 3: operation="insert", start_line=3, content="new line"
  - Delete lines 7-9: operation="delete", start_line=7, end_line=9`,
    inputSchema: {
      path: z.string().min(1).describe("Path to the file"),
      operation: z.enum(["replace", "insert", "delete"]).describe("Operation"),
      start_line: z.number().int().min(1).describe("Start line (1-based)"),
      end_line: z.number().int().min(1).optional().describe("End line"),
      content: z.string().optional().describe("New content")
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
          content: [{ type: "text", text: t().common.fileNotFound(filePath) }]
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
          content: [{ type: "text", text: t().fc_edit_file.invalidStartLine(params.start_line, totalLines) }]
        };
      }

      if (endIdx < startIdx || endIdx >= totalLines) {
        return {
          isError: true,
          content: [{ type: "text", text: t().fc_edit_file.invalidEndLine(params.end_line!) }]
        };
      }

      let newLines: string[];
      let actionDesc: string;

      switch (params.operation) {
        case "replace":
          if (!params.content) {
            return {
              isError: true,
              content: [{ type: "text", text: t().fc_edit_file.contentRequired('replace') }]
            };
          }
          const replacementLines = params.content.split('\n');
          newLines = [
            ...lines.slice(0, startIdx),
            ...replacementLines,
            ...lines.slice(endIdx + 1)
          ];
          actionDesc = t().fc_edit_file.replacedLines(params.start_line, endIdx + 1, replacementLines.length);
          break;

        case "insert":
          if (!params.content) {
            return {
              isError: true,
              content: [{ type: "text", text: t().fc_edit_file.contentRequired('insert') }]
            };
          }
          const insertLines = params.content.split('\n');
          newLines = [
            ...lines.slice(0, startIdx + 1),
            ...insertLines,
            ...lines.slice(startIdx + 1)
          ];
          actionDesc = t().fc_edit_file.insertedLines(insertLines.length, params.start_line);
          break;

        case "delete":
          newLines = [
            ...lines.slice(0, startIdx),
            ...lines.slice(endIdx + 1)
          ];
          actionDesc = t().fc_edit_file.deletedLines(params.start_line, endIdx + 1);
          break;

        default:
          return {
            isError: true,
            content: [{ type: "text", text: t().fc_edit_file.unknownOperation(params.operation) }]
          };
      }

      await fs.writeFile(filePath, newLines.join('\n'), "utf-8");

      return {
        content: [{
          type: "text",
          text: `${t().fc_edit_file.edited(path.basename(filePath))}\n\uD83D\uDCDD ${actionDesc}\n${t().fc_edit_file.lineChange(totalLines, newLines.length)}`
        }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: t().fc_edit_file.editError(errorMsg) }]
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
    title: "String Replace in File",
    description: `Replaces a unique string in a file with another.

Args:
  - path (string): Path to the file
  - old_str (string): String to replace (must occur exactly once)
  - new_str (string): New string (empty = delete)

Returns:
  - Confirmation with context

IMPORTANT: old_str must occur EXACTLY once in the file!
An error is returned for 0 or >1 occurrences.

Examples:
  - Rename function: old_str="def old_name", new_str="def new_name"
  - Add import: old_str="import os", new_str="import os\\nimport sys"
  - Delete line: old_str="# TODO: remove this\\n", new_str=""`,
    inputSchema: {
      path: z.string().min(1).describe("Path to the file"),
      old_str: z.string().min(1).describe("String to replace (must be unique)"),
      new_str: z.string().default("").describe("New string (empty = delete)")
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
          content: [{ type: "text", text: t().common.fileNotFound(filePath) }]
        };
      }

      const stats = await fs.stat(filePath);
      if (stats.isDirectory()) {
        return {
          isError: true,
          content: [{ type: "text", text: t().fc_str_replace.pathIsDirectory(filePath) }]
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
            text: `${t().fc_str_replace.notFoundInFile(path.basename(filePath))}\n\n${t().fc_str_replace.searchedFor}\n\`\`\`\n${params.old_str}\n\`\`\`\n\n${t().fc_str_replace.fileStart}\n\`\`\`\n${preview}\n\`\`\``
          }]
        };
      }

      if (occurrences > 1) {
        return {
          isError: true,
          content: [{
            type: "text",
            text: `${t().fc_str_replace.multipleOccurrences(occurrences)}\n\n${t().fc_str_replace.searchedFor}\n\`\`\`\n${params.old_str}\n\`\`\`\n\n${t().fc_str_replace.tip}`
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
      const lineInfo = lineChange === 0 ? t().fc_str_replace.sameLineCount :
                       lineChange > 0 ? t().fc_str_replace.addedLines(lineChange) : t().fc_str_replace.removedLines(lineChange);

      // Show context around the change
      const changeIndex = content.indexOf(params.old_str);
      const contextStart = Math.max(0, changeIndex - 50);
      const contextEnd = Math.min(content.length, changeIndex + params.old_str.length + 50);
      const beforeContext = content.substring(contextStart, changeIndex);
      const afterContext = content.substring(changeIndex + params.old_str.length, contextEnd);

      return {
        content: [{
          type: "text",
          text: `${t().fc_str_replace.replaced(path.basename(filePath))}\n\n| | |\n|---|---|\n| ${t().fc_str_replace.labelChange} | ${lineInfo} |\n| ${t().fc_str_replace.labelFile} | ${filePath} |\n\n${t().fc_str_replace.contextLabel}\n\`\`\`\n...${beforeContext}\u25B6${params.new_str}\u25C0${afterContext}...\n\`\`\``
        }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: t().fc_str_replace.replaceError(errorMsg) }]
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
    title: "List Processes",
    description: `Lists running system processes.

Args:
  - filter (string, optional): Filter by process name

Returns:
  - List of processes with PID, name, memory

Note: Uses 'tasklist' (Windows) or 'ps' (Unix)`,
    inputSchema: {
      filter: z.string().optional().describe("Filter by process name")
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
          content: [{ type: "text", text: t().fc_list_processes.noProcesses(params.filter) }]
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
          t().fc_list_processes.header(params.filter),
          ``,
          `| ${t().fc_list_processes.colName} | ${t().fc_list_processes.colPid} | ${t().fc_list_processes.colMemory} |`,
          `|------|-----|----------|`,
          ...processes.slice(0, 50)
        ].join('\n');
      } else {
        output = [
          t().fc_list_processes.header(params.filter),
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
        content: [{ type: "text", text: t().fc_list_processes.listError(errorMsg) }]
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
    title: "Kill Process",
    description: `Terminates a process by PID or name.

Args:
  - pid (number, optional): Process ID
  - name (string, optional): Process name
  - force (boolean): Force termination

Warning: May cause data loss!`,
    inputSchema: {
      pid: z.number().int().optional().describe("Process ID"),
      name: z.string().optional().describe("Process name"),
      force: z.boolean().default(false).describe("Force")
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
        content: [{ type: "text", text: t().fc_kill_process.pidOrNameRequired }]
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
          text: `${t().fc_kill_process.killed(target)}\n${stdout || stderr || ''}`.trim()
        }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: t().fc_kill_process.killError(errorMsg) }]
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
    title: "Start Interactive Session",
    description: `Starts an interactive process as a session (for fc_read_output and fc_send_input).

Args:
  - command (string): Command/Program
  - args (array, optional): Arguments
  - cwd (string, optional): Working directory

Returns:
  - Session ID for further interaction

Examples:
  - Python REPL: command="python"
  - Node REPL: command="node"
  - PowerShell: command="powershell"`,
    inputSchema: {
      command: z.string().min(1).describe("Command/Program"),
      args: z.array(z.string()).default([]).describe("Arguments"),
      cwd: z.string().optional().describe("Working directory")
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
        session.output.push(t().fc_start_session.processExited(code));
      });

      proc.on('error', (err) => {
        session.isRunning = false;
        session.output.push(t().fc_start_session.processError(err.message));
      });

      processSessions.set(sessionId, session);

      return {
        content: [{
          type: "text",
          text: `${t().fc_start_session.started(sessionId, `${params.command} ${params.args.join(' ')}`, proc.pid, cwd)}\n\n${t().fc_start_session.useReadAndSend}`
        }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: t().fc_start_session.startError(errorMsg) }]
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
    title: "Read Session Output",
    description: `Reads the output of a running session.

Args:
  - session_id (string): Session ID from fc_start_session
  - clear (boolean, optional): Clear output after reading

Returns:
  - Collected output since start/last clear`,
    inputSchema: {
      session_id: z.string().min(1).describe("Session ID"),
      clear: z.boolean().default(false).describe("Clear output")
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
        content: [{ type: "text", text: `${t().fc_read_output.notFound(params.session_id)}\n\n${t().fc_read_output.useListSessions}` }]
      };
    }

    const output = session.output.join('');
    const status = session.isRunning ? t().fc_read_output.statusRunning : t().fc_read_output.statusEnded;

    if (params.clear) {
      session.output = [];
    }

    return {
      content: [{
        type: "text",
        text: `${t().fc_read_output.header(status)}\n\`\`\`\n${output || t().fc_read_output.noOutput}\n\`\`\``
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
    title: "Send Input to Session",
    description: `Sends input to a running session.

Args:
  - session_id (string): Session ID
  - input (string): Input to send
  - newline (boolean, optional): Append newline (default: true)

Examples:
  - Python: input="print('Hello')"
  - Shell: input="ls -la"`,
    inputSchema: {
      session_id: z.string().min(1).describe("Session ID"),
      input: z.string().describe("Input to send"),
      newline: z.boolean().default(true).describe("Append newline")
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
        content: [{ type: "text", text: t().fc_send_input.notFound(params.session_id) }]
      };
    }

    if (!session.isRunning) {
      return {
        isError: true,
        content: [{ type: "text", text: t().fc_send_input.sessionEnded }]
      };
    }

    try {
      const inputText = params.newline ? params.input + '\n' : params.input;
      session.process.stdin?.write(inputText);

      return {
        content: [{
          type: "text",
          text: `${t().fc_send_input.sent(params.session_id)}\n\`\`\`\n${params.input}\n\`\`\`\n${t().fc_send_input.useReadOutput}`
        }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: t().fc_send_input.sendError(errorMsg) }]
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
    title: "List Sessions",
    description: `Lists all active and ended sessions.

Returns:
  - Table of all sessions with status`,
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
        content: [{ type: "text", text: `${t().fc_list_sessions.noSessions}\n\n${t().fc_list_sessions.useStartSession}` }]
      };
    }

    const rows: string[] = [];

    for (const [id, session] of processSessions) {
      const status = session.isRunning ? '\uD83D\uDFE2' : '\uD83D\uDD34';
      const runtime = Math.round((Date.now() - session.startTime.getTime()) / 1000);
      rows.push(`| ${status} | \`${id}\` | ${session.command} | ${session.process.pid || '-'} | ${runtime}s |`);
    }

    const output = [
      t().fc_list_sessions.header(processSessions.size),
      ``,
      `| ${t().fc_list_sessions.colStatus} | ${t().fc_list_sessions.colSessionId} | ${t().fc_list_sessions.colCommand} | ${t().fc_list_sessions.colPid} | ${t().fc_list_sessions.colRuntime} |`,
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
    title: "Close Session",
    description: `Terminates a running session and removes it from the list.

Args:
  - session_id (string): Session ID
  - force (boolean, optional): Force termination`,
    inputSchema: {
      session_id: z.string().min(1).describe("Session ID"),
      force: z.boolean().default(false).describe("Force")
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
        content: [{ type: "text", text: t().fc_close_session.notFound(params.session_id) }]
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
        content: [{ type: "text", text: t().fc_close_session.closed(params.session_id) }]
      };
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      return {
        isError: true,
        content: [{ type: "text", text: t().fc_close_session.closeError(errorMsg) }]
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
    title: "Fix JSON",
    description: `Automatically repairs common JSON errors.

Args:
  - path (string): Path to the JSON file
  - dry_run (boolean, optional): Only show problems, do not repair
  - create_backup (boolean, optional): Create backup before repair

Repairs: BOM, trailing commas, single quotes, comments, NUL bytes`,
    inputSchema: {
      path: z.string().min(1).describe("Path to the JSON file"),
      dry_run: z.boolean().default(false).describe("Only show problems"),
      create_backup: z.boolean().default(true).describe("Create backup")
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
        return { isError: true, content: [{ type: "text", text: t().common.fileNotFound(filePath) }] };
      }

      const rawContent = await fs.readFile(filePath, "utf-8");
      const fixes: string[] = [];
      let content = rawContent;

      // Remove BOM
      if (content.charCodeAt(0) === 0xFEFF) {
        content = content.slice(1);
        fixes.push(t().fc_fix_json.fixBom);
      }

      // Remove NUL bytes
      if (content.includes('\0')) {
        content = content.replace(/\0/g, '');
        fixes.push(t().fc_fix_json.fixNul);
      }

      // Remove single-line comments
      const c1 = content;
      content = content.replace(/^(\s*)\/\/.*$/gm, '');
      if (content !== c1) fixes.push(t().fc_fix_json.fixSingleLineComments);

      // Remove multi-line comments
      const c2 = content;
      content = content.replace(/\/\*[\s\S]*?\*\//g, '');
      if (content !== c2) fixes.push(t().fc_fix_json.fixMultiLineComments);

      // Fix trailing commas before } or ]
      const c3 = content;
      content = content.replace(/,(\s*[}\]])/g, '$1');
      if (content !== c3) fixes.push(t().fc_fix_json.fixTrailingCommas);

      // Fix single quotes to double quotes for keys and simple values
      const c4 = content;
      content = content.replace(/(\s*)'([^'\\]*(?:\\.[^'\\]*)*)'\s*:/g, '$1"$2":');
      content = content.replace(/:\s*'([^'\\]*(?:\\.[^'\\]*)*)'/g, ': "$1"');
      if (content !== c4) fixes.push(t().fc_fix_json.fixSingleQuotes);

      // Try to parse
      let isValid = false;
      let parseError = '';
      try { JSON.parse(content); isValid = true; } catch (e) { parseError = e instanceof Error ? e.message : String(e); }

      if (fixes.length === 0 && isValid) {
        return { content: [{ type: "text", text: t().fc_fix_json.alreadyValid(path.basename(filePath)) }] };
      }

      if (params.dry_run) {
        return {
          content: [{ type: "text", text: [
            t().fc_fix_json.analysisHeader(path.basename(filePath)), '',
            fixes.length > 0 ? t().fc_fix_json.foundProblems : t().fc_fix_json.noAutoFixable,
            ...fixes.map(f => `  - ${f}`), '',
            isValid ? t().fc_fix_json.afterFixValid : t().fc_fix_json.afterFixInvalid(parseError)
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
          t().fc_fix_json.repairedHeader(path.basename(filePath)), '',
          ...fixes.map(f => `  - ${f}`), '',
          isValid ? t().fc_fix_json.validJson : t().fc_fix_json.stillInvalid(parseError),
          params.create_backup ? t().fc_fix_json.backupCreated(`${filePath}.bak`) : ''
        ].join('\n') }]
      };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: t().common.errorGeneric(error instanceof Error ? error.message : String(error)) }] };
    }
  }
);

// ============================================================================
// Tool: Validate JSON
// ============================================================================

server.registerTool(
  "fc_validate_json",
  {
    title: "Validate JSON",
    description: `Validates a JSON file and shows detailed error information.

Args:
  - path (string): Path to the JSON file

Returns:
  - Validation status with line/column on errors`,
    inputSchema: {
      path: z.string().min(1).describe("Path to the JSON file")
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
        return { isError: true, content: [{ type: "text", text: t().common.fileNotFound(filePath) }] };
      }

      const content = await fs.readFile(filePath, "utf-8");
      const stats = await fs.stat(filePath);

      try {
        const parsed = JSON.parse(content);
        const keyCount = typeof parsed === 'object' && parsed !== null ? Object.keys(parsed).length : 0;
        const jsonType = Array.isArray(parsed) ? t().fc_validate_json.typeArray(parsed.length) : typeof parsed === 'object' && parsed !== null ? t().fc_validate_json.typeObject(keyCount) : typeof parsed;

        return {
          content: [{ type: "text", text: [
            t().fc_validate_json.validHeader(path.basename(filePath)), '',
            `| ${t().fc_validate_json.propType} | ${jsonType} |`, `|---|---|`,
            `| ${t().fc_validate_json.propSize} | ${formatFileSize(stats.size)} |`,
            `| ${t().fc_validate_json.propBom} | ${content.charCodeAt(0) === 0xFEFF ? t().fc_validate_json.propBomYes : t().fc_validate_json.propBomNo} |`,
            `| ${t().fc_validate_json.propEncoding} | UTF-8 |`
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
          lineInfo = `\n${t().fc_validate_json.errorPosition(line, col)}\n\n\`\`\`\n${contextLines.map((l, i) => `${Math.max(1, line - 2) + i}: ${l}`).join('\n')}\n\`\`\``;
        }

        return {
          content: [{ type: "text", text: `${t().fc_validate_json.invalidHeader(path.basename(filePath))}\n\n${t().fc_validate_json.errorLabel} ${errorMsg}${lineInfo}\n\n${t().fc_validate_json.useFcFixJson}` }]
        };
      }
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: t().common.errorGeneric(error instanceof Error ? error.message : String(error)) }] };
    }
  }
);

// ============================================================================
// Tool: Cleanup File
// ============================================================================

server.registerTool(
  "fc_cleanup_file",
  {
    title: "Cleanup File",
    description: `Cleans up one or more files from common problems.

Args:
  - path (string): Path to file or directory
  - recursive (boolean, optional): Recursive for directories
  - extensions (string, optional): Filter file extensions (e.g. ".txt,.json,.py")
  - remove_bom (boolean): Remove UTF-8 BOM
  - remove_trailing_whitespace (boolean): Remove trailing whitespace
  - normalize_line_endings (string, optional): "lf" | "crlf" | null
  - remove_nul_bytes (boolean): Remove NUL bytes
  - dry_run (boolean): Preview only

Cleans: BOM, NUL bytes, trailing whitespace, line endings`,
    inputSchema: {
      path: z.string().min(1).describe("Path to file/directory"),
      recursive: z.boolean().default(false).describe("Recursive"),
      extensions: z.string().optional().describe("Filter extensions (.txt,.json)"),
      remove_bom: z.boolean().default(true).describe("Remove BOM"),
      remove_trailing_whitespace: z.boolean().default(true).describe("Trailing whitespace"),
      normalize_line_endings: z.enum(["lf", "crlf"]).optional().describe("Line endings"),
      remove_nul_bytes: z.boolean().default(true).describe("Remove NUL bytes"),
      dry_run: z.boolean().default(false).describe("Preview only")
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
        return { isError: true, content: [{ type: "text", text: t().common.pathNotFound(targetPath) }] };
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
        return { content: [{ type: "text", text: t().fc_cleanup_file.noCleanupNeeded(files.length) }] };
      }

      return {
        content: [{ type: "text", text: [
          `${params.dry_run ? t().fc_cleanup_file.previewHeader : t().fc_cleanup_file.cleanedHeader}: ${t().fc_cleanup_file.cleanedCount(totalFixed, files.length)}`, '',
          ...results
        ].join('\n') }]
      };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: t().common.errorGeneric(error instanceof Error ? error.message : String(error)) }] };
    }
  }
);

// ============================================================================
// Tool: Fix Encoding
// ============================================================================

server.registerTool(
  "fc_fix_encoding",
  {
    title: "Fix Encoding",
    description: `Detects and repairs encoding errors (mojibake, double UTF-8).

Args:
  - path (string): Path to the file
  - dry_run (boolean): Only show problems
  - create_backup (boolean): Create backup

Repairs common mojibake patterns like:
  - Ã¤ -> ae, Ã¶ -> oe, Ã¼ -> ue (German umlauts)
  - ÃŸ -> ss, â‚¬ -> EUR`,
    inputSchema: {
      path: z.string().min(1).describe("Path to the file"),
      dry_run: z.boolean().default(false).describe("Preview only"),
      create_backup: z.boolean().default(true).describe("Create backup")
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
        return { isError: true, content: [{ type: "text", text: t().common.fileNotFound(filePath) }] };
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
        return { content: [{ type: "text", text: t().fc_fix_encoding.noErrors(path.basename(filePath)) }] };
      }

      if (params.dry_run) {
        return {
          content: [{ type: "text", text: [
            t().fc_fix_encoding.analysisHeader(path.basename(filePath)), '',
            t().fc_fix_encoding.foundMojibake,
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
          t().fc_fix_encoding.repairedHeader(path.basename(filePath)), '',
          ...fixes.map(f => `  - ${f}`),
          params.create_backup ? `\n${t().fc_fix_encoding.backupCreated(`${filePath}.bak`)}` : ''
        ].join('\n') }]
      };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: t().common.errorGeneric(error instanceof Error ? error.message : String(error)) }] };
    }
  }
);

// ============================================================================
// Tool: Folder Diff
// ============================================================================

server.registerTool(
  "fc_folder_diff",
  {
    title: "Folder Diff",
    description: `Compares the current state of a directory with a saved snapshot.

Args:
  - path (string): Path to the directory
  - save_snapshot (boolean): Save current state as new snapshot
  - extensions (string, optional): Filter file extensions

Detects: New files, modified files, deleted files
Snapshots are saved in %TEMP%/.fc_snapshots/`,
    inputSchema: {
      path: z.string().min(1).describe("Path to the directory"),
      save_snapshot: z.boolean().default(true).describe("Save snapshot"),
      extensions: z.string().optional().describe("Filter extensions")
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
        return { isError: true, content: [{ type: "text", text: t().common.dirNotFound(dirPath) }] };
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
            t().fc_folder_diff.firstSnapshot(path.basename(dirPath)), '',
            `| | |`, `|---|---|`,
            `| ${t().fc_folder_diff.labelFiles} | ${totalFiles} |`,
            `| ${t().fc_folder_diff.labelSnapshot} | ${snapshotFile} |`, '',
            t().fc_folder_diff.nextCallInfo
          ].join('\n') }]
        };
      }

      if (totalChanges === 0) {
        return { content: [{ type: "text", text: t().fc_folder_diff.noChanges(path.basename(dirPath), totalFiles) }] };
      }

      const output = [
        t().fc_folder_diff.diffHeader(path.basename(dirPath)), '',
        `| | |`, `|---|---|`,
        `| ${t().fc_folder_diff.catNew} | ${newFiles.length} |`,
        `| ${t().fc_folder_diff.catModified} | ${modifiedFiles.length} |`,
        `| ${t().fc_folder_diff.catDeleted} | ${deletedFiles.length} |`,
        `| ${t().fc_folder_diff.catUnchanged} | ${totalFiles - newFiles.length - modifiedFiles.length} |`
      ];

      if (newFiles.length > 0) {
        output.push('', t().fc_folder_diff.newFiles, ...newFiles.slice(0, 50).map(f => `  \uD83D\uDFE2 ${f}`));
        if (newFiles.length > 50) output.push(`  ${t().fc_folder_diff.andMore(newFiles.length - 50)}`);
      }
      if (modifiedFiles.length > 0) {
        output.push('', t().fc_folder_diff.modifiedFiles, ...modifiedFiles.slice(0, 50).map(f => `  \uD83D\uDFE1 ${f}`));
        if (modifiedFiles.length > 50) output.push(`  ${t().fc_folder_diff.andMore(modifiedFiles.length - 50)}`);
      }
      if (deletedFiles.length > 0) {
        output.push('', t().fc_folder_diff.deletedFiles, ...deletedFiles.slice(0, 50).map(f => `  \uD83D\uDD34 ${f}`));
        if (deletedFiles.length > 50) output.push(`  ${t().fc_folder_diff.andMore(deletedFiles.length - 50)}`);
      }

      return { content: [{ type: "text", text: output.join('\n') }] };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: t().common.errorGeneric(error instanceof Error ? error.message : String(error)) }] };
    }
  }
);

// ============================================================================
// Tool: Batch Rename
// ============================================================================

server.registerTool(
  "fc_batch_rename",
  {
    title: "Batch Rename",
    description: `Renames files by pattern: remove prefix/suffix, replace, or auto-detect.

Args:
  - directory (string): Directory with the files
  - mode (string): "remove_prefix" | "remove_suffix" | "replace" | "auto_detect"
  - pattern (string, optional): Text to remove/replace
  - replacement (string, optional): Replacement text (for replace mode)
  - extensions (string, optional): Filter by extensions
  - dry_run (boolean): Preview only

Examples:
  - Remove prefix: mode="remove_prefix", pattern="backup_"
  - Auto-detect: mode="auto_detect" detects common prefixes`,
    inputSchema: {
      directory: z.string().min(1).describe("Directory"),
      mode: z.enum(["remove_prefix", "remove_suffix", "replace", "auto_detect"]).describe("Mode"),
      pattern: z.string().optional().describe("Text to remove/replace"),
      replacement: z.string().default("").describe("Replacement text"),
      extensions: z.string().optional().describe("Filter extensions"),
      dry_run: z.boolean().default(true).describe("Preview only")
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
        return { isError: true, content: [{ type: "text", text: t().common.dirNotFound(dirPath) }] };
      }

      const extFilter = params.extensions ? params.extensions.split(',').map(e => e.trim().toLowerCase()) : null;
      const entries = await fs.readdir(dirPath, { withFileTypes: true });
      const files = entries.filter(e => e.isFile() && (!extFilter || extFilter.includes(path.extname(e.name).toLowerCase())));

      if (files.length === 0) {
        return { content: [{ type: "text", text: t().fc_batch_rename.noMatchingFiles(dirPath) }] };
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
          return { content: [{ type: "text", text: t().fc_batch_rename.noCommonPattern(files.length) }] };
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
            t().fc_batch_rename.autoDetectHeader(files.length), '',
            t().fc_batch_rename.detectedPatterns(detections.join(', ')), '',
            renames.length > 0 ? t().fc_batch_rename.suggestedRename(commonPrefix) : '',
            ...renames.slice(0, 30).map(r => `  ${r.old} \u2192 ${r.new}`),
            renames.length > 30 ? `  ${t().fc_batch_rename.andMore(renames.length - 30)}` : '', '',
            t().fc_batch_rename.useTip(commonPrefix)
          ].join('\n') }]
        };
      }

      if (!params.pattern) {
        return { isError: true, content: [{ type: "text", text: t().fc_batch_rename.patternRequired(params.mode) }] };
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
        return { content: [{ type: "text", text: t().fc_batch_rename.noFilesMatchPattern(params.pattern) }] };
      }

      if (params.dry_run) {
        return {
          content: [{ type: "text", text: [
            t().fc_batch_rename.previewHeader(renames.length), '',
            ...renames.map(r => `  ${r.old} \u2192 ${r.new}`), '',
            t().fc_batch_rename.setDryRunFalse
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
          t().fc_batch_rename.renamed(successCount, renames.length),
          ...errors.map(e => `  \u274C ${e}`)
        ].join('\n') }]
      };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: t().common.errorGeneric(error instanceof Error ? error.message : String(error)) }] };
    }
  }
);

// ============================================================================
// Tool: Convert Format
// ============================================================================

server.registerTool(
  "fc_convert_format",
  {
    title: "Convert Format",
    description: `Converts files between different formats.

Args:
  - input_path (string): Path to source file
  - output_path (string): Path to target file
  - input_format (string): "json" | "csv" | "ini"
  - output_format (string): "json" | "csv" | "ini"
  - json_indent (number, optional): JSON indentation (default: 2)

Supported conversions:
  - JSON <-> CSV (for arrays of objects)
  - JSON <-> INI (for flat objects/sections)
  - JSON pretty-print / minify`,
    inputSchema: {
      input_path: z.string().min(1).describe("Source file"),
      output_path: z.string().min(1).describe("Target file"),
      input_format: z.enum(["json", "csv", "ini"]).describe("Input format"),
      output_format: z.enum(["json", "csv", "ini"]).describe("Output format"),
      json_indent: z.number().int().min(0).max(8).default(2).describe("JSON indentation")
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
        return { isError: true, content: [{ type: "text", text: t().fc_convert_format.sourceNotFound(inputPath) }] };
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
            return { isError: true, content: [{ type: "text", text: t().fc_convert_format.csvNeedsRows }] };
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
            return { isError: true, content: [{ type: "text", text: t().fc_convert_format.csvNeedsArray }] };
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
            return { isError: true, content: [{ type: "text", text: t().fc_convert_format.iniNeedsObject }] };
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
          t().fc_convert_format.converted(params.input_format.toUpperCase(), params.output_format.toUpperCase()), '',
          `| | |`, `|---|---|`,
          `| ${t().fc_convert_format.labelSource} | ${inputPath} |`,
          `| ${t().fc_convert_format.labelTarget} | ${outputPath} |`,
          `| ${t().fc_convert_format.labelSize} | ${formatFileSize(outStats.size)} |`
        ].join('\n') }]
      };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: t().common.errorGeneric(error instanceof Error ? error.message : String(error)) }] };
    }
  }
);

// ============================================================================
// Tool: Detect Duplicates
// ============================================================================

server.registerTool(
  "fc_detect_duplicates",
  {
    title: "Detect Duplicates",
    description: `Finds file duplicates in a directory using SHA-256 hashes.

Args:
  - directory (string): Directory to scan
  - recursive (boolean): Search recursively
  - extensions (string, optional): Filter by extensions
  - min_size (number, optional): Minimum size in bytes (default: 1)
  - max_size (number, optional): Maximum size in bytes

Returns:
  - Groups of duplicates with paths and sizes`,
    inputSchema: {
      directory: z.string().min(1).describe("Directory"),
      recursive: z.boolean().default(true).describe("Recursive"),
      extensions: z.string().optional().describe("Filter extensions"),
      min_size: z.number().int().min(0).default(1).describe("Minimum size in bytes"),
      max_size: z.number().int().optional().describe("Maximum size in bytes")
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
        return { isError: true, content: [{ type: "text", text: t().common.dirNotFound(dirPath) }] };
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
          content: [{ type: "text", text: t().fc_detect_duplicates.noDuplicates(files.length, hashedCount) }]
        };
      }

      const output = [
        t().fc_detect_duplicates.header, '',
        `| | |`, `|---|---|`,
        `| ${t().fc_detect_duplicates.labelChecked} | ${files.length} |`,
        `| ${t().fc_detect_duplicates.labelGroups} | ${duplicates.length} |`,
        `| ${t().fc_detect_duplicates.labelDuplicates} | ${totalDuplicateFiles} |`,
        `| ${t().fc_detect_duplicates.labelWasted} | ${formatFileSize(totalWastedSpace)} |`
      ];

      for (let i = 0; i < Math.min(duplicates.length, 20); i++) {
        const group = duplicates[i];
        output.push('', t().fc_detect_duplicates.groupHeader(i + 1, formatFileSize(group.size)));
        for (const p of group.paths) {
          output.push(`  \uD83D\uDCC4 ${path.relative(dirPath, p)}`);
        }
      }

      if (duplicates.length > 20) {
        output.push('', t().fc_detect_duplicates.andMoreGroups(duplicates.length - 20));
      }

      output.push('', t().fc_detect_duplicates.useSafeDelete);

      return { content: [{ type: "text", text: output.join('\n') }] };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: t().common.errorGeneric(error instanceof Error ? error.message : String(error)) }] };
    }
  }
);

// ============================================================================
// Tool: Markdown to HTML
// ============================================================================

server.registerTool(
  "fc_md_to_html",
  {
    title: "Markdown to HTML",
    description: `Converts Markdown to formatted HTML (printable as PDF).

Args:
  - input_path (string): Path to Markdown file
  - output_path (string): Path to HTML output
  - title (string, optional): Document title

Generates standalone HTML with CSS styling, printable as PDF via browser.`,
    inputSchema: {
      input_path: z.string().min(1).describe("Markdown file"),
      output_path: z.string().min(1).describe("HTML output"),
      title: z.string().optional().describe("Document title")
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
        return { isError: true, content: [{ type: "text", text: t().common.fileNotFound(inputPath) }] };
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
          t().fc_md_to_html.converted(path.basename(outputPath)), '',
          `| | |`, `|---|---|`,
          `| ${t().fc_md_to_html.labelSource} | ${inputPath} |`,
          `| ${t().fc_md_to_html.labelTarget} | ${outputPath} |`,
          `| ${t().fc_md_to_html.labelSize} | ${formatFileSize(outStats.size)} |`, '',
          t().fc_md_to_html.openInBrowser
        ].join('\n') }]
      };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: t().common.errorGeneric(error instanceof Error ? error.message : String(error)) }] };
    }
  }
);

// ============================================================================
// Tool: Set Language
// ============================================================================

server.tool(
  "fc_set_language",
  "Set the output language for FileCommander tools",
  { language: z.enum(["de", "en"]).describe("Language code") },
  async ({ language }) => {
    setLanguage(language as Lang);
    return { content: [{ type: "text", text: t().server.languageSet(language) }] };
  }
);

// ============================================================================
// Server Startup
// ============================================================================

async function main(): Promise<void> {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error(t().server.started);
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
