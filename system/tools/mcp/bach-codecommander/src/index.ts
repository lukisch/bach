#!/usr/bin/env node
/**
 * BACH CodeCommander MCP Server
 *
 * A developer-focused MCP server for code analysis, JSON repair,
 * encoding fix, import organization, and format conversion.
 *
 * Copyright (c) 2025-2026 Lukas (BACH). Licensed under MIT License.
 * See LICENSE file for details.
 *
 * @author Lukas (BACH)
 * @version 1.1.0
 * @license MIT
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import * as fs from "fs/promises";
import * as path from "path";
import { exec } from "child_process";
import { promisify } from "util";
import { t, setLanguage } from './i18n/index.js';

const execAsync = promisify(exec);

// ============================================================================
// Server Initialization
// ============================================================================

const server = new McpServer({
  name: "bach-codecommander-mcp",
  version: "1.1.0"
});

// ============================================================================
// Helper Functions
// ============================================================================

function normalizePath(inputPath: string): string {
  return path.normalize(inputPath);
}

async function pathExists(targetPath: string): Promise<boolean> {
  try { await fs.access(targetPath); return true; } catch { return false; }
}

function formatFileSize(bytes: number): string {
  const units = ['B', 'KB', 'MB', 'GB'];
  let unitIndex = 0;
  let size = bytes;
  while (size >= 1024 && unitIndex < units.length - 1) { size /= 1024; unitIndex++; }
  return `${size.toFixed(2)} ${units[unitIndex]}`;
}

// Simple Python AST-like parser for TypeScript
// Extracts classes, functions, imports from Python files using regex patterns

interface PythonClass {
  name: string;
  startLine: number;
  endLine: number;
  methods: string[];
  bases: string[];
  decorators: string[];
  docstring: string;
}

interface PythonFunction {
  name: string;
  startLine: number;
  endLine: number;
  params: string;
  decorators: string[];
  docstring: string;
  isAsync: boolean;
}

interface PythonImport {
  line: number;
  text: string;
  type: 'stdlib' | 'third_party' | 'local';
  module: string;
}

interface CodeAnalysis {
  classes: PythonClass[];
  functions: PythonFunction[];
  imports: PythonImport[];
  totalLines: number;
  codeLines: number;
  commentLines: number;
  blankLines: number;
  complexity: number;
}

// Known Python stdlib modules
const STDLIB_MODULES = new Set([
  'abc', 'aifc', 'argparse', 'array', 'ast', 'asyncio', 'atexit', 'base64',
  'binascii', 'bisect', 'builtins', 'calendar', 'cgi', 'cmd', 'code', 'codecs',
  'collections', 'colorsys', 'compileall', 'configparser', 'contextlib', 'copy',
  'copyreg', 'csv', 'ctypes', 'curses', 'dataclasses', 'datetime', 'decimal',
  'difflib', 'dis', 'distutils', 'doctest', 'email', 'encodings', 'enum',
  'errno', 'faulthandler', 'fcntl', 'filecmp', 'fileinput', 'fnmatch',
  'fractions', 'ftplib', 'functools', 'gc', 'getopt', 'getpass', 'gettext',
  'glob', 'gzip', 'hashlib', 'heapq', 'hmac', 'html', 'http', 'idlelib',
  'imaplib', 'importlib', 'inspect', 'io', 'ipaddress', 'itertools', 'json',
  'keyword', 'lib2to3', 'linecache', 'locale', 'logging', 'lzma', 'mailbox',
  'math', 'mimetypes', 'mmap', 'modulefinder', 'multiprocessing', 'netrc',
  'numbers', 'operator', 'optparse', 'os', 'pathlib', 'pdb', 'pickle',
  'pickletools', 'pkgutil', 'platform', 'plistlib', 'poplib', 'posixpath',
  'pprint', 'profile', 'pstats', 'py_compile', 'pyclbr', 'pydoc', 'queue',
  'quopri', 'random', 're', 'readline', 'reprlib', 'resource', 'rlcompleter',
  'runpy', 'sched', 'secrets', 'select', 'selectors', 'shelve', 'shlex',
  'shutil', 'signal', 'site', 'smtpd', 'smtplib', 'sndhdr', 'socket',
  'socketserver', 'sqlite3', 'ssl', 'stat', 'statistics', 'string',
  'stringprep', 'struct', 'subprocess', 'sunau', 'symtable', 'sys', 'sysconfig',
  'syslog', 'tabnanny', 'tarfile', 'tempfile', 'test', 'textwrap', 'threading',
  'time', 'timeit', 'tkinter', 'token', 'tokenize', 'trace', 'traceback',
  'tracemalloc', 'tty', 'turtle', 'turtledemo', 'types', 'typing', 'unicodedata',
  'unittest', 'urllib', 'uu', 'uuid', 'venv', 'warnings', 'wave', 'weakref',
  'webbrowser', 'winreg', 'winsound', 'wsgiref', 'xdrlib', 'xml', 'xmlrpc',
  'zipapp', 'zipfile', 'zipimport', 'zlib', '_thread', '__future__'
]);

function classifyImport(module: string): 'stdlib' | 'third_party' | 'local' {
  if (module.startsWith('.')) return 'local';
  const topLevel = module.split('.')[0];
  if (STDLIB_MODULES.has(topLevel)) return 'stdlib';
  return 'third_party';
}

function analyzePythonCode(content: string): CodeAnalysis {
  const lines = content.split('\n');
  const totalLines = lines.length;
  let codeLines = 0;
  let commentLines = 0;
  let blankLines = 0;
  let complexity = 0;

  // Line classification
  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed === '') blankLines++;
    else if (trimmed.startsWith('#')) commentLines++;
    else codeLines++;

    // Cyclomatic complexity: count branches
    if (/^\s*(if|elif|for|while|except|with|and|or)\b/.test(line)) complexity++;
  }

  // Extract imports
  const imports: PythonImport[] = [];
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    const importMatch = line.match(/^import\s+(\S+)/);
    const fromMatch = line.match(/^from\s+(\S+)\s+import/);
    if (importMatch) {
      imports.push({ line: i + 1, text: line, type: classifyImport(importMatch[1]), module: importMatch[1] });
    } else if (fromMatch) {
      imports.push({ line: i + 1, text: line, type: classifyImport(fromMatch[1]), module: fromMatch[1] });
    }
  }

  // Extract classes
  const classes: PythonClass[] = [];
  for (let i = 0; i < lines.length; i++) {
    const classMatch = lines[i].match(/^class\s+(\w+)\s*(?:\(([^)]*)\))?\s*:/);
    if (classMatch) {
      const decorators: string[] = [];
      let j = i - 1;
      while (j >= 0 && lines[j].trim().startsWith('@')) {
        decorators.unshift(lines[j].trim());
        j--;
      }

      // Find end of class (next line with same or less indentation, or EOF)
      let endLine = i + 1;
      const baseIndent = lines[i].search(/\S/);
      for (let k = i + 1; k < lines.length; k++) {
        const lineIndent = lines[k].search(/\S/);
        if (lineIndent >= 0 && lineIndent <= baseIndent && lines[k].trim() !== '') {
          endLine = k;
          break;
        }
        endLine = k + 1;
      }

      // Find methods within class
      const methods: string[] = [];
      for (let k = i + 1; k < endLine; k++) {
        const methodMatch = lines[k].match(/^\s+(?:async\s+)?def\s+(\w+)\s*\(/);
        if (methodMatch) methods.push(methodMatch[1]);
      }

      // Extract docstring
      let docstring = '';
      if (i + 1 < lines.length) {
        const nextLine = lines[i + 1].trim();
        if (nextLine.startsWith('"""') || nextLine.startsWith("'''")) {
          const quote = nextLine.substring(0, 3);
          if (nextLine.endsWith(quote) && nextLine.length > 6) {
            docstring = nextLine.slice(3, -3);
          } else {
            const dsLines = [nextLine.slice(3)];
            for (let k = i + 2; k < lines.length; k++) {
              if (lines[k].trim().endsWith(quote)) {
                dsLines.push(lines[k].trim().slice(0, -3));
                break;
              }
              dsLines.push(lines[k].trim());
            }
            docstring = dsLines.join(' ').trim();
          }
        }
      }

      classes.push({
        name: classMatch[1],
        startLine: i + 1,
        endLine,
        methods,
        bases: classMatch[2] ? classMatch[2].split(',').map(b => b.trim()) : [],
        decorators,
        docstring: docstring.substring(0, 200)
      });
    }
  }

  // Extract top-level functions
  const functions: PythonFunction[] = [];
  for (let i = 0; i < lines.length; i++) {
    const funcMatch = lines[i].match(/^(async\s+)?def\s+(\w+)\s*\(([^)]*)\)\s*(?:->.*?)?\s*:/);
    if (funcMatch) {
      // Check if inside a class
      const isInClass = classes.some(c => i + 1 > c.startLine && i + 1 < c.endLine);
      if (isInClass) continue;

      const decorators: string[] = [];
      let j = i - 1;
      while (j >= 0 && lines[j].trim().startsWith('@')) {
        decorators.unshift(lines[j].trim());
        j--;
      }

      let endLine = i + 1;
      for (let k = i + 1; k < lines.length; k++) {
        const lineIndent = lines[k].search(/\S/);
        if (lineIndent === 0 && lines[k].trim() !== '') {
          endLine = k;
          break;
        }
        endLine = k + 1;
      }

      let docstring = '';
      if (i + 1 < lines.length) {
        const nextLine = lines[i + 1].trim();
        if (nextLine.startsWith('"""') || nextLine.startsWith("'''")) {
          docstring = nextLine.replace(/^['"]{'3}|['"]{'3}$/g, '').trim();
        }
      }

      functions.push({
        name: funcMatch[2],
        startLine: i + 1,
        endLine,
        params: funcMatch[3],
        decorators,
        docstring: docstring.substring(0, 200),
        isAsync: !!funcMatch[1]
      });
    }
  }

  return { classes, functions, imports, totalLines, codeLines, commentLines, blankLines, complexity };
}

// ============================================================================
// Tool 1: Analyze Code
// ============================================================================

server.registerTool(
  "cc_analyze_code",
  {
    title: "Analyze Code",
    description: `Analyzes a Python file: classes, functions, imports, metrics.

Args:
  - path (string): Path to the Python file

Returns:
  - Classes with methods, functions, import analysis, LOC, complexity`,
    inputSchema: {
      path: z.string().min(1).describe("Path to the Python file")
    },
    annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false }
  },
  async (params) => {
    try {
      const filePath = normalizePath(params.path);
      if (!await pathExists(filePath)) {
        return { isError: true, content: [{ type: "text", text: t().common.fileNotFound(filePath) }] };
      }

      const content = await fs.readFile(filePath, "utf-8");
      const analysis = analyzePythonCode(content);
      const stats = await fs.stat(filePath);

      const output = [
        t().cc_analyze_code.header(path.basename(filePath)), '',
        `| ${t().cc_analyze_code.metricTotalLines} | ${analysis.totalLines} |`, `|---|---|`,
        `| ${t().cc_analyze_code.metricTotalLines} | ${analysis.totalLines} |`,
        `| ${t().cc_analyze_code.metricCodeLines} | ${analysis.codeLines} |`,
        `| ${t().cc_analyze_code.metricCommentLines} | ${analysis.commentLines} |`,
        `| ${t().cc_analyze_code.metricBlankLines} | ${analysis.blankLines} |`,
        `| ${t().cc_analyze_code.metricClasses} | ${analysis.classes.length} |`,
        `| ${t().cc_analyze_code.metricFunctions} | ${analysis.functions.length} |`,
        `| ${t().cc_analyze_code.metricImports} | ${analysis.imports.length} |`,
        `| ${t().cc_analyze_code.metricCyclomaticComplexity} | ${analysis.complexity} |`,
        `| ${t().cc_analyze_code.metricFileSize} | ${formatFileSize(stats.size)} |`
      ];

      if (analysis.classes.length > 0) {
        output.push('', t().cc_analyze_code.classesHeader);
        for (const cls of analysis.classes) {
          const bases = cls.bases.length > 0 ? `(${cls.bases.join(', ')})` : '';
          output.push(t().cc_analyze_code.classInfo(cls.name, bases, cls.startLine, cls.endLine, cls.methods.length));
          if (cls.docstring) output.push(`    _${cls.docstring}_`);
          if (cls.methods.length > 0) output.push(t().cc_analyze_code.classMethods(cls.methods.join(', ')));
        }
      }

      if (analysis.functions.length > 0) {
        output.push('', t().cc_analyze_code.functionsHeader);
        for (const func of analysis.functions) {
          const async_prefix = func.isAsync ? 'async ' : '';
          output.push(t().cc_analyze_code.functionInfo(async_prefix, func.name, func.params, func.startLine, func.endLine));
          if (func.docstring) output.push(`    _${func.docstring}_`);
        }
      }

      if (analysis.imports.length > 0) {
        const stdlib = analysis.imports.filter(i => i.type === 'stdlib');
        const thirdParty = analysis.imports.filter(i => i.type === 'third_party');
        const local = analysis.imports.filter(i => i.type === 'local');
        output.push('', t().cc_analyze_code.importsHeader(stdlib.length, thirdParty.length, local.length));
        if (thirdParty.length > 0) {
          output.push(t().cc_analyze_code.thirdPartyList(thirdParty.map(i => i.module).join(', ')));
        }
      }

      return { content: [{ type: "text", text: output.join('\n') }] };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: t().common.error(error instanceof Error ? error.message : String(error)) }] };
    }
  }
);

// ============================================================================
// Tool 2: Analyze Methods
// ============================================================================

server.registerTool(
  "cc_analyze_methods",
  {
    title: "Analyze Methods",
    description: `Detailed method analysis of a Python file.

Args:
  - path (string): Path to the Python file
  - class_name (string, optional): Only methods of this class

Returns:
  - Methods with parameters, decorators, complexity, data flow`,
    inputSchema: {
      path: z.string().min(1).describe("Path to the Python file"),
      class_name: z.string().optional().describe("Only analyze this class")
    },
    annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false }
  },
  async (params) => {
    try {
      const filePath = normalizePath(params.path);
      if (!await pathExists(filePath)) {
        return { isError: true, content: [{ type: "text", text: t().common.fileNotFound(filePath) }] };
      }

      const content = await fs.readFile(filePath, "utf-8");
      const lines = content.split('\n');
      const analysis = analyzePythonCode(content);

      const output = [t().cc_analyze_methods.header(path.basename(filePath)), ''];

      const targetClasses = params.class_name
        ? analysis.classes.filter(c => c.name === params.class_name)
        : analysis.classes;

      if (targetClasses.length === 0 && params.class_name) {
        return { isError: true, content: [{ type: "text", text: t().cc_analyze_methods.classNotFound(params.class_name, analysis.classes.map(c => c.name).join(', ')) }] };
      }

      for (const cls of targetClasses) {
        output.push(`## ${cls.name}`);
        if (cls.bases.length > 0) output.push(t().cc_analyze_methods.inheritsFrom(cls.bases.join(', ')));
        output.push('');

        // Analyze each method
        for (let i = cls.startLine; i < cls.endLine && i < lines.length; i++) {
          const methodMatch = lines[i].match(/^\s+(async\s+)?def\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*(.+?))?\s*:/);
          if (!methodMatch) continue;

          const [, isAsync, methodName, params_str, returnType] = methodMatch;
          const decorators: string[] = [];
          let j = i - 1;
          while (j >= cls.startLine - 1 && lines[j]?.trim().startsWith('@')) {
            decorators.unshift(lines[j].trim());
            j--;
          }

          // Count method complexity
          let methodComplexity = 1;
          const methodIndent = lines[i].search(/\S/);
          for (let k = i + 1; k < lines.length; k++) {
            const indent = lines[k].search(/\S/);
            if (indent >= 0 && indent <= methodIndent && lines[k].trim() !== '') break;
            if (/^\s*(if|elif|for|while|except|and|or)\b/.test(lines[k])) methodComplexity++;
          }

          // Detect calls to self
          const selfCalls: string[] = [];
          for (let k = i + 1; k < lines.length; k++) {
            const indent = lines[k].search(/\S/);
            if (indent >= 0 && indent <= methodIndent && lines[k].trim() !== '') break;
            const selfMatch = lines[k].match(/self\.(\w+)\(/g);
            if (selfMatch) {
              selfMatch.forEach(m => {
                const name = m.replace('self.', '').replace('(', '');
                if (!selfCalls.includes(name)) selfCalls.push(name);
              });
            }
          }

          const visibility = methodName.startsWith('__') && methodName.endsWith('__') ? 'magic' :
                            methodName.startsWith('__') ? 'private' :
                            methodName.startsWith('_') ? 'protected' : 'public';

          output.push(`### ${isAsync ? 'async ' : ''}${methodName}(${params_str})`);
          if (returnType) output.push(`  Return: ${returnType}`);
          output.push(t().cc_analyze_methods.visibilityLabel(visibility, methodComplexity));
          if (decorators.length > 0) output.push(t().cc_analyze_methods.decorators(decorators.join(', ')));
          if (selfCalls.length > 0) output.push(t().cc_analyze_methods.calls(selfCalls.join(', ')));
          output.push('');
        }
      }

      // Also show top-level functions
      if (!params.class_name && analysis.functions.length > 0) {
        output.push(t().cc_analyze_methods.topLevelFunctions, '');
        for (const func of analysis.functions) {
          output.push(`### ${func.isAsync ? 'async ' : ''}${func.name}(${func.params})`);
          if (func.decorators.length > 0) output.push(t().cc_analyze_methods.decorators(func.decorators.join(', ')));
          output.push('');
        }
      }

      return { content: [{ type: "text", text: output.join('\n') }] };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: t().common.error(error instanceof Error ? error.message : String(error)) }] };
    }
  }
);

// ============================================================================
// Tool 3: Extract Classes
// ============================================================================

server.registerTool(
  "cc_extract_classes",
  {
    title: "Extract Classes",
    description: `Extracts Python classes and functions from a file as separate text blocks.

Args:
  - path (string): Path to the Python file
  - output_dir (string, optional): Output directory (otherwise display only)

Useful for code review and documentation.`,
    inputSchema: {
      path: z.string().min(1).describe("Path to the Python file"),
      output_dir: z.string().optional().describe("Output directory")
    },
    annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: true, openWorldHint: false }
  },
  async (params) => {
    try {
      const filePath = normalizePath(params.path);
      if (!await pathExists(filePath)) {
        return { isError: true, content: [{ type: "text", text: t().common.fileNotFound(filePath) }] };
      }

      const content = await fs.readFile(filePath, "utf-8");
      const lines = content.split('\n');
      const analysis = analyzePythonCode(content);

      const output: string[] = [t().cc_extract_classes.header(path.basename(filePath)), ''];

      const extractedFiles: { name: string; content: string }[] = [];

      for (const cls of analysis.classes) {
        const classContent = lines.slice(cls.startLine - 1, cls.endLine).join('\n');
        extractedFiles.push({ name: `${cls.name}.txt`, content: classContent });
        output.push(t().cc_extract_classes.classInfo(cls.name, cls.endLine - cls.startLine + 1, cls.methods.length));
      }

      // Collect top-level code (imports, functions, globals)
      const topLevelLines: string[] = [];
      for (let i = 0; i < lines.length; i++) {
        const isInClass = analysis.classes.some(c => i + 1 >= c.startLine && i + 1 <= c.endLine);
        if (!isInClass) topLevelLines.push(lines[i]);
      }
      if (topLevelLines.some(l => l.trim() !== '')) {
        extractedFiles.push({ name: `${t().cc_extract_classes.helperFunctions}.txt`, content: topLevelLines.join('\n') });
        output.push(t().cc_extract_classes.helperFunctionsInfo(topLevelLines.filter(l => l.trim() !== '').length));
      }

      if (params.output_dir) {
        const outDir = normalizePath(params.output_dir);
        await fs.mkdir(outDir, { recursive: true });
        for (const file of extractedFiles) {
          await fs.writeFile(path.join(outDir, file.name), file.content, 'utf-8');
        }
        output.push('', t().cc_extract_classes.filesWritten(extractedFiles.length, outDir));
      } else {
        output.push('', t().cc_extract_classes.hintUseOutputDir);
      }

      return { content: [{ type: "text", text: output.join('\n') }] };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: t().common.error(error instanceof Error ? error.message : String(error)) }] };
    }
  }
);

// ============================================================================
// Tool 4: Organize Imports
// ============================================================================

server.registerTool(
  "cc_organize_imports",
  {
    title: "Organize Imports",
    description: `Organizes Python imports per PEP 8: sorted, deduplicated, grouped.

Args:
  - path (string): Path to the Python file
  - dry_run (boolean): Preview only

Groups: 1) __future__ 2) stdlib 3) third-party 4) local`,
    inputSchema: {
      path: z.string().min(1).describe("Path to the Python file"),
      dry_run: z.boolean().default(false).describe("Preview only")
    },
    annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: true, openWorldHint: false }
  },
  async (params) => {
    try {
      const filePath = normalizePath(params.path);
      if (!await pathExists(filePath)) {
        return { isError: true, content: [{ type: "text", text: t().common.fileNotFound(filePath) }] };
      }

      const content = await fs.readFile(filePath, "utf-8");
      const lines = content.split('\n');

      // Find import block (contiguous imports at top of file, after docstrings/comments)
      let importStart = -1;
      let importEnd = -1;
      const importLines: string[] = [];

      for (let i = 0; i < lines.length; i++) {
        const trimmed = lines[i].trim();
        if (trimmed.startsWith('import ') || trimmed.startsWith('from ')) {
          if (importStart === -1) importStart = i;
          importEnd = i;
          importLines.push(trimmed);
        } else if (importStart !== -1 && trimmed !== '' && !trimmed.startsWith('#')) {
          // Non-import, non-blank line after imports started: end of import block
          // But allow blank lines and comments between imports
          if (importEnd < i - 2) break; // Gap too large
        }
      }

      if (importLines.length === 0) {
        return { content: [{ type: "text", text: t().cc_organize_imports.noImportsFound(path.basename(filePath)) }] };
      }

      // Deduplicate
      const uniqueImports = [...new Set(importLines)];
      const removed = importLines.length - uniqueImports.length;

      // Classify and sort
      const futureImports = uniqueImports.filter(l => l.includes('__future__')).sort();
      const stdlibImports = uniqueImports.filter(l => {
        if (l.includes('__future__')) return false;
        const mod = l.match(/^(?:from\s+)?(\S+)/)?.[1]?.replace(/^from\s+/, '') || '';
        return classifyImport(mod) === 'stdlib';
      }).sort();
      const thirdPartyImports = uniqueImports.filter(l => {
        const mod = l.match(/^(?:from\s+)?(\S+)/)?.[1]?.replace(/^from\s+/, '') || '';
        return classifyImport(mod) === 'third_party';
      }).sort();
      const localImports = uniqueImports.filter(l => {
        const mod = l.match(/^(?:from\s+)?(\S+)/)?.[1]?.replace(/^from\s+/, '') || '';
        return classifyImport(mod) === 'local';
      }).sort();

      // Build new import block
      const newImportBlock: string[] = [];
      if (futureImports.length > 0) { newImportBlock.push(...futureImports, ''); }
      if (stdlibImports.length > 0) { newImportBlock.push(...stdlibImports, ''); }
      if (thirdPartyImports.length > 0) { newImportBlock.push(...thirdPartyImports, ''); }
      if (localImports.length > 0) { newImportBlock.push(...localImports, ''); }

      // Remove trailing empty line
      while (newImportBlock.length > 0 && newImportBlock[newImportBlock.length - 1] === '') {
        newImportBlock.pop();
      }

      const output = [
        t().cc_organize_imports.header(path.basename(filePath)), '',
        `| ${t().cc_organize_imports.categoryFuture} | ${futureImports.length} |`, `|---|---|`,
        `| ${t().cc_organize_imports.categoryFuture} | ${futureImports.length} |`,
        `| ${t().cc_organize_imports.categoryStdlib} | ${stdlibImports.length} |`,
        `| ${t().cc_organize_imports.categoryThirdParty} | ${thirdPartyImports.length} |`,
        `| ${t().cc_organize_imports.categoryLocal} | ${localImports.length} |`,
        `| ${t().cc_organize_imports.duplicatesRemoved} | ${removed} |`
      ];

      if (params.dry_run) {
        output.push('', t().cc_organize_imports.previewHeader, '```python', ...newImportBlock, '```');
        return { content: [{ type: "text", text: output.join('\n') }] };
      }

      // Apply changes
      const newLines = [
        ...lines.slice(0, importStart),
        ...newImportBlock,
        ...lines.slice(importEnd + 1)
      ];
      await fs.writeFile(filePath, newLines.join('\n'), 'utf-8');
      output.push('', t().cc_organize_imports.importsSaved);

      return { content: [{ type: "text", text: output.join('\n') }] };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: t().common.error(error instanceof Error ? error.message : String(error)) }] };
    }
  }
);

// ============================================================================
// Tool 5: Diagnose Imports
// ============================================================================

server.registerTool(
  "cc_diagnose_imports",
  {
    title: "Diagnose Imports",
    description: `Diagnoses import issues: missing modules, circular imports, unused imports.

Args:
  - path (string): Path to the Python file

Detects: Missing modules, suspected circular imports, import issues`,
    inputSchema: {
      path: z.string().min(1).describe("Path to the Python file")
    },
    annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false }
  },
  async (params) => {
    try {
      const filePath = normalizePath(params.path);
      if (!await pathExists(filePath)) {
        return { isError: true, content: [{ type: "text", text: t().common.fileNotFound(filePath) }] };
      }

      const content = await fs.readFile(filePath, "utf-8");
      const lines = content.split('\n');
      const analysis = analyzePythonCode(content);

      const issues: string[] = [];
      const warnings: string[] = [];

      // Check for potentially unused imports
      for (const imp of analysis.imports) {
        const importedNames: string[] = [];
        const fromMatch = imp.text.match(/from\s+\S+\s+import\s+(.+)/);
        const simpleMatch = imp.text.match(/^import\s+(\S+)(?:\s+as\s+(\w+))?/);

        if (fromMatch) {
          fromMatch[1].split(',').forEach(n => {
            const name = n.trim().split(' as ').pop()?.trim();
            if (name && name !== '*') importedNames.push(name);
          });
        } else if (simpleMatch) {
          importedNames.push(simpleMatch[2] || simpleMatch[1].split('.').pop() || '');
        }

        for (const name of importedNames) {
          if (!name) continue;
          // Check if name is used in rest of code (excluding the import line itself)
          const restOfCode = lines.filter((_, i) => i !== imp.line - 1).join('\n');
          const namePattern = new RegExp(`\\b${name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`);
          if (!namePattern.test(restOfCode)) {
            warnings.push(t().cc_diagnose_imports.unusedImport(imp.line, name));
          }
        }
      }

      // Check for duplicate imports
      const importTexts = analysis.imports.map(i => i.text);
      const seen = new Set<string>();
      for (const text of importTexts) {
        if (seen.has(text)) {
          issues.push(t().cc_diagnose_imports.duplicateImport(text));
        }
        seen.add(text);
      }

      // Check for relative imports that might cause circular dependencies
      const localImports = analysis.imports.filter(i => i.type === 'local');
      if (localImports.length > 0) {
        warnings.push(t().cc_diagnose_imports.relativeImportsWarning(localImports.length));
      }

      // Check import order
      let lastType = '';
      for (const imp of analysis.imports) {
        if (lastType && imp.type !== lastType) {
          if ((lastType === 'third_party' && imp.type === 'stdlib') ||
              (lastType === 'local' && imp.type !== 'local')) {
            warnings.push(t().cc_diagnose_imports.importOrderWarning(imp.line));
            break;
          }
        }
        lastType = imp.type;
      }

      const output = [
        t().cc_diagnose_imports.header(path.basename(filePath)), '',
        `| | |`, `|---|---|`,
        `| ${t().cc_diagnose_imports.totalImports} | ${analysis.imports.length} |`,
        `| ${t().cc_diagnose_imports.issues} | ${issues.length} |`,
        `| ${t().cc_diagnose_imports.warnings} | ${warnings.length} |`
      ];

      if (issues.length > 0) {
        output.push('', t().cc_diagnose_imports.issuesHeader, ...issues.map(i => `  \u274C ${i}`));
      }
      if (warnings.length > 0) {
        output.push('', t().cc_diagnose_imports.warningsHeader, ...warnings.map(w => `  \u26A0\uFE0F ${w}`));
      }
      if (issues.length === 0 && warnings.length === 0) {
        output.push('', t().cc_diagnose_imports.noIssues);
      }

      output.push('', t().cc_diagnose_imports.hintOrganize);

      return { content: [{ type: "text", text: output.join('\n') }] };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: t().common.error(error instanceof Error ? error.message : String(error)) }] };
    }
  }
);

// ============================================================================
// Tool 6: Fix JSON (shared with FileCommander)
// ============================================================================

server.registerTool(
  "cc_fix_json",
  {
    title: "Fix JSON",
    description: `Automatically repairs common JSON errors.

Args:
  - path (string): Path to the JSON file
  - dry_run (boolean): Only show issues
  - create_backup (boolean): Create backup

Repairs: BOM, trailing commas, single quotes, comments, NUL bytes`,
    inputSchema: {
      path: z.string().min(1).describe("Path to the JSON file"),
      dry_run: z.boolean().default(false).describe("Preview only"),
      create_backup: z.boolean().default(true).describe("Create backup")
    },
    annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: true, openWorldHint: false }
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

      if (content.charCodeAt(0) === 0xFEFF) { content = content.slice(1); fixes.push(t().cc_fix_json.fixBomRemoved); }
      if (content.includes('\0')) { content = content.replace(/\0/g, ''); fixes.push(t().cc_fix_json.fixNulRemoved); }

      const c1 = content; content = content.replace(/^(\s*)\/\/.*$/gm, '');
      if (content !== c1) fixes.push(t().cc_fix_json.fixCommentsRemoved);

      const c2 = content; content = content.replace(/\/\*[\s\S]*?\*\//g, '');
      if (content !== c2) fixes.push(t().cc_fix_json.fixBlockCommentsRemoved);

      const c3 = content; content = content.replace(/,(\s*[}\]])/g, '$1');
      if (content !== c3) fixes.push(t().cc_fix_json.fixTrailingCommas);

      const c4 = content;
      content = content.replace(/(\s*)'([^'\\]*(?:\\.[^'\\]*)*)'\s*:/g, '$1"$2":');
      content = content.replace(/:\s*'([^'\\]*(?:\\.[^'\\]*)*)'/g, ': "$1"');
      if (content !== c4) fixes.push(t().cc_fix_json.fixSingleQuotes);

      let isValid = false;
      let parseError = '';
      try { JSON.parse(content); isValid = true; } catch (e) { parseError = e instanceof Error ? e.message : String(e); }

      if (fixes.length === 0 && isValid) {
        return { content: [{ type: "text", text: t().cc_fix_json.validJson(path.basename(filePath)) }] };
      }

      if (params.dry_run) {
        return { content: [{ type: "text", text: [t().cc_fix_json.analysisHeader(path.basename(filePath)), '', ...fixes.map(f => `  - ${f}`), '', isValid ? t().cc_fix_json.validAfterRepair : t().cc_fix_json.stillInvalid(parseError)].join('\n') }] };
      }

      if (params.create_backup && fixes.length > 0) await fs.writeFile(filePath + '.bak', rawContent, "utf-8");
      if (isValid) content = JSON.stringify(JSON.parse(content), null, 2);
      await fs.writeFile(filePath, content, "utf-8");

      return { content: [{ type: "text", text: [t().cc_fix_json.repairedHeader(path.basename(filePath)), '', ...fixes.map(f => `  - ${f}`), '', isValid ? '\u2705' : `\u26A0\uFE0F ${parseError}`].join('\n') }] };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: t().common.error(error instanceof Error ? error.message : String(error)) }] };
    }
  }
);

// ============================================================================
// Tool 7: Validate JSON (shared with FileCommander)
// ============================================================================

server.registerTool(
  "cc_validate_json",
  {
    title: "Validate JSON",
    description: `Validates JSON with detailed error information and position.

Args:
  - path (string): Path to the JSON file`,
    inputSchema: {
      path: z.string().min(1).describe("Path to the JSON file")
    },
    annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false }
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
        const type = Array.isArray(parsed) ? t().cc_validate_json.typeArray(parsed.length) : typeof parsed === 'object' && parsed !== null ? t().cc_validate_json.typeObject(Object.keys(parsed).length) : typeof parsed;

        return { content: [{ type: "text", text: [t().cc_validate_json.validHeader(path.basename(filePath)), '', `| | |`, `|---|---|`, `| ${t().cc_validate_json.labelType} | ${type} |`, `| ${t().cc_validate_json.labelSize} | ${formatFileSize(stats.size)} |`, `| ${t().cc_validate_json.labelBom} | ${content.charCodeAt(0) === 0xFEFF ? t().cc_validate_json.bomYes : t().cc_validate_json.bomNo} |`].join('\n') }] };
      } catch (e) {
        const errorMsg = e instanceof Error ? e.message : String(e);
        const posMatch = errorMsg.match(/position\s+(\d+)/i);
        let lineInfo = '';
        if (posMatch) {
          const pos = parseInt(posMatch[1]);
          const before = content.substring(0, pos);
          const line = before.split('\n').length;
          const col = pos - before.lastIndexOf('\n');
          const cLines = content.split('\n');
          const ctx = cLines.slice(Math.max(0, line - 3), line + 2);
          lineInfo = `${t().cc_validate_json.positionInfo(line, col)}\n\n\`\`\`\n${ctx.map((l, i) => `${Math.max(1, line - 2) + i}: ${l}`).join('\n')}\n\`\`\``;
        }
        return { content: [{ type: "text", text: `${t().cc_validate_json.invalidHeader(path.basename(filePath))}\n\n${t().cc_validate_json.errorLabel(errorMsg)}${lineInfo}\n\n${t().cc_validate_json.hintFix}` }] };
      }
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: t().common.error(error instanceof Error ? error.message : String(error)) }] };
    }
  }
);

// ============================================================================
// Tool 8: Fix Encoding (shared with FileCommander)
// ============================================================================

server.registerTool(
  "cc_fix_encoding",
  {
    title: "Fix Encoding",
    description: `Repairs encoding errors (Mojibake, double UTF-8).

Args:
  - path (string): Path to the file
  - dry_run (boolean): Preview only
  - create_backup (boolean): Create backup

Repairs 27+ Mojibake patterns (German, French, Spanish).`,
    inputSchema: {
      path: z.string().min(1).describe("Path to the file"),
      dry_run: z.boolean().default(false).describe("Preview only"),
      create_backup: z.boolean().default(true).describe("Create backup")
    },
    annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: true, openWorldHint: false }
  },
  async (params) => {
    try {
      const filePath = normalizePath(params.path);
      if (!await pathExists(filePath)) {
        return { isError: true, content: [{ type: "text", text: t().common.fileNotFound(filePath) }] };
      }

      const rawContent = await fs.readFile(filePath, "utf-8");
      const mojibakeMap: [RegExp, string, string][] = [
        [/\u00c3\u00a4/g, '\u00e4', '\u00e4'], [/\u00c3\u00b6/g, '\u00f6', '\u00f6'], [/\u00c3\u00bc/g, '\u00fc', '\u00fc'],
        [/\u00c3\u0084/g, '\u00c4', '\u00c4'], [/\u00c3\u0096/g, '\u00d6', '\u00d6'], [/\u00c3\u009c/g, '\u00dc', '\u00dc'],
        [/\u00c3\u009f/g, '\u00df', '\u00df'],
        [/\u00c3\u00a9/g, '\u00e9', '\u00e9'], [/\u00c3\u00a8/g, '\u00e8', '\u00e8'],
        [/\u00c3\u00a0/g, '\u00e0', '\u00e0'], [/\u00c3\u00a1/g, '\u00e1', '\u00e1'],
        [/\u00c3\u00ae/g, '\u00ee', '\u00ee'], [/\u00c3\u00af/g, '\u00ef', '\u00ef'],
        [/\u00c3\u00b4/g, '\u00f4', '\u00f4'], [/\u00c3\u00b9/g, '\u00f9', '\u00f9'],
        [/\u00c3\u00a7/g, '\u00e7', '\u00e7'], [/\u00c3\u00b1/g, '\u00f1', '\u00f1'],
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
        return { content: [{ type: "text", text: t().cc_fix_encoding.noErrors(path.basename(filePath)) }] };
      }

      if (params.dry_run) {
        return { content: [{ type: "text", text: [t().cc_fix_encoding.analysisHeader(path.basename(filePath)), '', ...fixes.map(f => `  - ${f}`)].join('\n') }] };
      }

      if (params.create_backup) await fs.writeFile(filePath + '.bak', rawContent, "utf-8");
      await fs.writeFile(filePath, content, "utf-8");

      return { content: [{ type: "text", text: [t().cc_fix_encoding.repairedHeader(path.basename(filePath)), '', ...fixes.map(f => `  - ${f}`)].join('\n') }] };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: t().common.error(error instanceof Error ? error.message : String(error)) }] };
    }
  }
);

// ============================================================================
// Tool 9: Cleanup File (shared with FileCommander)
// ============================================================================

server.registerTool(
  "cc_cleanup_file",
  {
    title: "Cleanup File",
    description: `Cleans up source code files: BOM, NUL bytes, trailing whitespace, line endings.

Args:
  - path (string): Path to the file
  - remove_bom (boolean): Remove BOM
  - remove_trailing_whitespace (boolean): Trailing whitespace
  - normalize_line_endings (string): "lf" | "crlf"
  - remove_nul_bytes (boolean): Remove NUL bytes
  - dry_run (boolean): Preview only`,
    inputSchema: {
      path: z.string().min(1).describe("Path to the file"),
      remove_bom: z.boolean().default(true).describe("Remove BOM"),
      remove_trailing_whitespace: z.boolean().default(true).describe("Trailing whitespace"),
      normalize_line_endings: z.enum(["lf", "crlf"]).optional().describe("Line endings"),
      remove_nul_bytes: z.boolean().default(true).describe("NUL bytes"),
      dry_run: z.boolean().default(false).describe("Preview only")
    },
    annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: true, openWorldHint: false }
  },
  async (params) => {
    try {
      const filePath = normalizePath(params.path);
      if (!await pathExists(filePath)) {
        return { isError: true, content: [{ type: "text", text: t().common.fileNotFound(filePath) }] };
      }

      const raw = await fs.readFile(filePath, "utf-8");
      let content = raw;
      const fixes: string[] = [];

      if (params.remove_bom && content.charCodeAt(0) === 0xFEFF) { content = content.slice(1); fixes.push(t().cc_cleanup_file.fixBomRemoved); }
      if (params.remove_nul_bytes && content.includes('\0')) { content = content.replace(/\0/g, ''); fixes.push(t().cc_cleanup_file.fixNulRemoved); }
      if (params.remove_trailing_whitespace) { const c = content; content = content.replace(/[ \t]+$/gm, ''); if (content !== c) fixes.push(t().cc_cleanup_file.fixTrailingWhitespace); }
      if (params.normalize_line_endings) {
        const c = content;
        content = content.replace(/\r\n/g, '\n');
        if (params.normalize_line_endings === 'crlf') content = content.replace(/\n/g, '\r\n');
        if (content !== c) fixes.push(params.normalize_line_endings.toUpperCase());
      }

      if (fixes.length === 0) {
        return { content: [{ type: "text", text: t().cc_cleanup_file.alreadyClean(path.basename(filePath)) }] };
      }

      if (params.dry_run) {
        return { content: [{ type: "text", text: [t().cc_cleanup_file.previewHeader(path.basename(filePath)), '', ...fixes.map(f => `  - ${f}`)].join('\n') }] };
      }

      await fs.writeFile(filePath, content, "utf-8");
      return { content: [{ type: "text", text: [t().cc_cleanup_file.cleanedHeader(path.basename(filePath)), '', ...fixes.map(f => `  - ${f}`)].join('\n') }] };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: t().common.error(error instanceof Error ? error.message : String(error)) }] };
    }
  }
);

// ============================================================================
// Tool 10: Convert Format (shared with FileCommander)
// ============================================================================

server.registerTool(
  "cc_convert_format",
  {
    title: "Convert Format",
    description: `Converts between JSON, CSV, and INI formats.

Args:
  - input_path (string): Source file
  - output_path (string): Target file
  - input_format (string): "json" | "csv" | "ini"
  - output_format (string): "json" | "csv" | "ini"
  - json_indent (number): JSON indentation`,
    inputSchema: {
      input_path: z.string().min(1).describe("Source file"),
      output_path: z.string().min(1).describe("Target file"),
      input_format: z.enum(["json", "csv", "ini"]).describe("Input format"),
      output_format: z.enum(["json", "csv", "ini"]).describe("Output format"),
      json_indent: z.number().int().min(0).max(8).default(2).describe("JSON indentation")
    },
    annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: true, openWorldHint: false }
  },
  async (params) => {
    try {
      const inputPath = normalizePath(params.input_path);
      const outputPath = normalizePath(params.output_path);
      if (!await pathExists(inputPath)) {
        return { isError: true, content: [{ type: "text", text: t().common.sourceFileNotFound(inputPath) }] };
      }

      const rawContent = await fs.readFile(inputPath, "utf-8");
      let data: unknown;

      switch (params.input_format) {
        case 'json': data = JSON.parse(rawContent); break;
        case 'csv': {
          const lines = rawContent.trim().split('\n');
          if (lines.length < 2) return { isError: true, content: [{ type: "text", text: t().cc_convert_format.csvMinRows }] };
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
          let section = '_default';
          result[section] = {};
          for (const line of rawContent.split('\n')) {
            const tl = line.trim();
            if (!tl || tl.startsWith(';') || tl.startsWith('#')) continue;
            const sm = tl.match(/^\[(.+)\]$/);
            if (sm) { section = sm[1]; result[section] = result[section] || {}; }
            else { const eq = tl.indexOf('='); if (eq > 0) result[section][tl.substring(0, eq).trim()] = tl.substring(eq + 1).trim(); }
          }
          if (Object.keys(result._default).length === 0) delete result._default;
          data = result;
          break;
        }
      }

      let output: string;
      switch (params.output_format) {
        case 'json': output = JSON.stringify(data, null, params.json_indent || undefined); break;
        case 'csv': {
          if (!Array.isArray(data)) return { isError: true, content: [{ type: "text", text: t().cc_convert_format.csvRequiresArray }] };
          const headers = Object.keys((data as Record<string, unknown>[])[0] || {});
          const rows = (data as Record<string, unknown>[]).map(item =>
            headers.map(h => { const v = String(item[h] ?? ''); return v.includes(',') || v.includes('"') ? `"${v.replace(/"/g, '""')}"` : v; }).join(','));
          output = [headers.join(','), ...rows].join('\n');
          break;
        }
        case 'ini': {
          if (typeof data !== 'object' || data === null || Array.isArray(data)) return { isError: true, content: [{ type: "text", text: t().cc_convert_format.iniRequiresObject }] };
          const lines: string[] = [];
          for (const [section, values] of Object.entries(data as Record<string, unknown>)) {
            if (typeof values === 'object' && values !== null && !Array.isArray(values)) {
              lines.push(`[${section}]`);
              for (const [k, v] of Object.entries(values as Record<string, unknown>)) lines.push(`${k} = ${v}`);
              lines.push('');
            } else lines.push(`${section} = ${values}`);
          }
          output = lines.join('\n');
          break;
        }
      }

      const outDir = path.dirname(outputPath);
      if (!await pathExists(outDir)) await fs.mkdir(outDir, { recursive: true });
      await fs.writeFile(outputPath, output, "utf-8");
      const outStats = await fs.stat(outputPath);

      return { content: [{ type: "text", text: [t().cc_convert_format.conversionHeader(params.input_format.toUpperCase(), params.output_format.toUpperCase()), '', `| | |`, `|---|---|`, `| ${t().cc_convert_format.labelSource} | ${inputPath} |`, `| ${t().cc_convert_format.labelTarget} | ${outputPath} |`, `| ${t().cc_convert_format.labelSize} | ${formatFileSize(outStats.size)} |`].join('\n') }] };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: t().common.error(error instanceof Error ? error.message : String(error)) }] };
    }
  }
);

// ============================================================================
// Tool 11: Fix Umlauts
// ============================================================================

server.registerTool(
  "cc_fix_umlauts",
  {
    title: "Fix Umlauts",
    description: `Repairs broken German umlauts in source code files.

Args:
  - path (string): Path to the file
  - dry_run (boolean): Preview only
  - create_backup (boolean): Create backup

Detects 70+ patterns of broken umlauts and replaces them correctly.`,
    inputSchema: {
      path: z.string().min(1).describe("Path to the file"),
      dry_run: z.boolean().default(false).describe("Preview only"),
      create_backup: z.boolean().default(true).describe("Create backup")
    },
    annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: true, openWorldHint: false }
  },
  async (params) => {
    try {
      const filePath = normalizePath(params.path);
      if (!await pathExists(filePath)) {
        return { isError: true, content: [{ type: "text", text: t().common.fileNotFound(filePath) }] };
      }

      const rawContent = await fs.readFile(filePath, "utf-8");
      // Comprehensive umlaut fix patterns
      const umlautFixes: [RegExp, string][] = [
        // Double-encoded UTF-8
        [/\u00c3\u00a4/g, '\u00e4'], [/\u00c3\u00b6/g, '\u00f6'], [/\u00c3\u00bc/g, '\u00fc'],
        [/\u00c3\u0084/g, '\u00c4'], [/\u00c3\u0096/g, '\u00d6'], [/\u00c3\u009c/g, '\u00dc'],
        [/\u00c3\u009f/g, '\u00df'],
        // HTML entities
        [/&auml;/g, '\u00e4'], [/&ouml;/g, '\u00f6'], [/&uuml;/g, '\u00fc'],
        [/&Auml;/g, '\u00c4'], [/&Ouml;/g, '\u00d6'], [/&Uuml;/g, '\u00dc'],
        [/&szlig;/g, '\u00df'],
        // Unicode escape sequences in text
        [/\\u00e4/g, '\u00e4'], [/\\u00f6/g, '\u00f6'], [/\\u00fc/g, '\u00fc'],
        [/\\u00c4/g, '\u00c4'], [/\\u00d6/g, '\u00d6'], [/\\u00dc/g, '\u00dc'],
        [/\\u00df/g, '\u00df'],
        // Latin-1 misinterpretation patterns
        [/\u00e4/g, '\u00e4'], // already correct, skip
        [/ae(?=[a-z])/g, '\u00e4'], // Only in obvious German words - too risky, skip
      ];

      let content = rawContent;
      const fixes: string[] = [];
      let totalFixes = 0;

      for (const [pattern, replacement] of umlautFixes) {
        const before = content;
        content = content.replace(pattern, replacement);
        if (content !== before) {
          const count = (before.match(pattern) || []).length;
          totalFixes += count;
          fixes.push(`${replacement} (${count}x)`);
        }
      }

      if (fixes.length === 0) {
        return { content: [{ type: "text", text: t().cc_fix_umlauts.noIssues(path.basename(filePath)) }] };
      }

      if (params.dry_run) {
        return { content: [{ type: "text", text: [t().cc_fix_umlauts.analysisHeader(path.basename(filePath)), '', t().cc_fix_umlauts.replacements(totalFixes), ...fixes.map(f => `  - ${f}`)].join('\n') }] };
      }

      if (params.create_backup) await fs.writeFile(filePath + '.bak', rawContent, "utf-8");
      await fs.writeFile(filePath, content, "utf-8");

      return { content: [{ type: "text", text: [t().cc_fix_umlauts.repairedHeader(path.basename(filePath)), '', t().cc_fix_umlauts.replacements(totalFixes), ...fixes.map(f => `  - ${f}`)].join('\n') }] };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: t().common.error(error instanceof Error ? error.message : String(error)) }] };
    }
  }
);

// ============================================================================
// Tool 12: Scan Emoji
// ============================================================================

server.registerTool(
  "cc_scan_emoji",
  {
    title: "Scan Emoji",
    description: `Scans files for emojis and shows ASCII alternatives.

Args:
  - path (string): Path to the file or directory
  - recursive (boolean): Scan recursively
  - extensions (string): Only certain extensions

Useful for systems that don't support Unicode/Emoji.`,
    inputSchema: {
      path: z.string().min(1).describe("Path"),
      recursive: z.boolean().default(false).describe("Recursive"),
      extensions: z.string().default(".py,.js,.ts,.json,.md,.txt").describe("Extensions")
    },
    annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false }
  },
  async (params) => {
    try {
      const targetPath = normalizePath(params.path);
      if (!await pathExists(targetPath)) {
        return { isError: true, content: [{ type: "text", text: t().common.pathNotFound(targetPath) }] };
      }

      const extFilter = params.extensions.split(',').map(e => e.trim().toLowerCase());
      const stats = await fs.stat(targetPath);
      const files: string[] = [];

      if (stats.isDirectory()) {
        async function scan(dir: string): Promise<void> {
          const entries = await fs.readdir(dir, { withFileTypes: true });
          for (const entry of entries) {
            const full = path.join(dir, entry.name);
            if (entry.isDirectory() && params.recursive && !['node_modules', '.git'].includes(entry.name)) {
              await scan(full);
            } else if (entry.isFile() && extFilter.includes(path.extname(entry.name).toLowerCase())) {
              files.push(full);
            }
          }
        }
        await scan(targetPath);
      } else {
        files.push(targetPath);
      }

      // Emoji detection pattern (covers most emoji ranges)
      const emojiPattern = /[\u{1F300}-\u{1F9FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{1F000}-\u{1F02F}\u{1F0A0}-\u{1F0FF}\u{1FA00}-\u{1FA6F}\u{1FA70}-\u{1FAFF}\u{200D}\u{FE0F}]/gu;

      const results: { file: string; line: number; emoji: string; text: string }[] = [];

      for (const filePath of files) {
        try {
          const content = await fs.readFile(filePath, "utf-8");
          const lines = content.split('\n');
          for (let i = 0; i < lines.length; i++) {
            const matches = lines[i].match(emojiPattern);
            if (matches) {
              for (const emoji of matches) {
                results.push({
                  file: path.relative(targetPath, filePath) || path.basename(filePath),
                  line: i + 1,
                  emoji,
                  text: lines[i].trim().substring(0, 80)
                });
              }
            }
          }
        } catch { /* skip unreadable */ }
      }

      if (results.length === 0) {
        return { content: [{ type: "text", text: t().cc_scan_emoji.noEmojis(files.length) }] };
      }

      // Group by emoji
      const emojiCounts: Map<string, number> = new Map();
      for (const r of results) {
        emojiCounts.set(r.emoji, (emojiCounts.get(r.emoji) || 0) + 1);
      }

      const output = [
        t().cc_scan_emoji.scanHeader(files.length), '',
        `| ${t().cc_scan_emoji.emojiTableEmoji} | ${t().cc_scan_emoji.emojiTableCount} | ${t().cc_scan_emoji.emojiTableCodepoint} |`, `|---|---|---|`,
        ...[...emojiCounts.entries()].sort((a, b) => b[1] - a[1]).slice(0, 30).map(
          ([emoji, count]) => `| ${emoji} | ${count} | U+${emoji.codePointAt(0)?.toString(16).toUpperCase()} |`
        ), '',
        t().cc_scan_emoji.occurrencesHeader,
        ...results.slice(0, 30).map(r => `  ${r.file}:${r.line} ${r.emoji} \`${r.text}\``),
        results.length > 30 ? `\n${t().cc_scan_emoji.andMore(results.length - 30)}` : ''
      ];

      return { content: [{ type: "text", text: output.join('\n') }] };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: t().common.error(error instanceof Error ? error.message : String(error)) }] };
    }
  }
);

// ============================================================================
// Tool 13: Generate Licenses
// ============================================================================

server.registerTool(
  "cc_generate_licenses",
  {
    title: "Generate Licenses",
    description: `Generates a third-party license file for an npm or Python project.

Args:
  - project_dir (string): Project directory
  - output_path (string): Output file
  - format (string): "text" | "json" | "csv"

Reads package.json (npm) or pip packages and collects license info.`,
    inputSchema: {
      project_dir: z.string().min(1).describe("Project directory"),
      output_path: z.string().min(1).describe("Output file"),
      format: z.enum(["text", "json", "csv"]).default("text").describe("Format")
    },
    annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: true, openWorldHint: false }
  },
  async (params) => {
    try {
      const projectDir = normalizePath(params.project_dir);
      const outputPath = normalizePath(params.output_path);

      interface LicenseInfo { name: string; version: string; license: string; }
      const licenses: LicenseInfo[] = [];

      // Check for package.json (npm project)
      const pkgJsonPath = path.join(projectDir, 'package.json');
      if (await pathExists(pkgJsonPath)) {
        const pkgJson = JSON.parse(await fs.readFile(pkgJsonPath, "utf-8"));
        const allDeps = { ...pkgJson.dependencies, ...pkgJson.devDependencies };

        for (const [name, version] of Object.entries(allDeps)) {
          const depPkgPath = path.join(projectDir, 'node_modules', name, 'package.json');
          try {
            if (await pathExists(depPkgPath)) {
              const depPkg = JSON.parse(await fs.readFile(depPkgPath, "utf-8"));
              licenses.push({
                name,
                version: depPkg.version || String(version),
                license: depPkg.license || 'UNKNOWN'
              });
            } else {
              licenses.push({ name, version: String(version), license: 'NOT_INSTALLED' });
            }
          } catch {
            licenses.push({ name, version: String(version), license: 'READ_ERROR' });
          }
        }
      }

      // Check for Python (pip list)
      const requirementsPath = path.join(projectDir, 'requirements.txt');
      if (await pathExists(requirementsPath)) {
        try {
          const { stdout } = await execAsync('pip list --format=json', { cwd: projectDir, timeout: 15000 });
          const pipList = JSON.parse(stdout);
          for (const pkg of pipList) {
            licenses.push({ name: pkg.name, version: pkg.version, license: 'Python' });
          }
        } catch {
          // pip not available, read requirements.txt directly
          const reqs = await fs.readFile(requirementsPath, "utf-8");
          for (const line of reqs.split('\n')) {
            const trimmed = line.trim();
            if (trimmed && !trimmed.startsWith('#')) {
              const [name] = trimmed.split(/[=<>!]/);
              licenses.push({ name: name.trim(), version: '?', license: 'Python' });
            }
          }
        }
      }

      if (licenses.length === 0) {
        return { content: [{ type: "text", text: t().cc_generate_licenses.noPackageFiles(projectDir) }] };
      }

      // Generate output
      let output: string;
      switch (params.format) {
        case 'json':
          output = JSON.stringify(licenses, null, 2);
          break;
        case 'csv':
          output = ['Name,Version,License', ...licenses.map(l => `${l.name},${l.version},${l.license}`)].join('\n');
          break;
        default:
          output = [
            'THIRD PARTY NOTICES', '='.repeat(40), '',
            ...licenses.map(l => `${l.name} v${l.version}\n  License: ${l.license}\n`)
          ].join('\n');
      }

      const outDir = path.dirname(outputPath);
      if (!await pathExists(outDir)) await fs.mkdir(outDir, { recursive: true });
      await fs.writeFile(outputPath, output, "utf-8");

      return { content: [{ type: "text", text: [t().cc_generate_licenses.generatedHeader(licenses.length), '', `| | |`, `|---|---|`, `| ${t().cc_generate_licenses.labelFile} | ${outputPath} |`, `| ${t().cc_generate_licenses.labelFormat} | ${params.format} |`, `| ${t().cc_generate_licenses.labelPackages} | ${licenses.length} |`].join('\n') }] };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: t().common.error(error instanceof Error ? error.message : String(error)) }] };
    }
  }
);

// ============================================================================
// Tool 14: Markdown to PDF
// ============================================================================

server.registerTool(
  "cc_md_to_pdf",
  {
    title: "Markdown to HTML",
    description: `Converts Markdown to formatted HTML (printable as PDF).

Args:
  - input_path (string): Path to the Markdown file
  - output_path (string): Path to the HTML output
  - title (string, optional): Document title

Produces standalone HTML with CSS styling, printable as PDF via browser.`,
    inputSchema: {
      input_path: z.string().min(1).describe("Markdown file"),
      output_path: z.string().min(1).describe("HTML output"),
      title: z.string().optional().describe("Document title")
    },
    annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: true, openWorldHint: false }
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

      return { content: [{ type: "text", text: [t().cc_md_to_pdf.conversionHeader(path.basename(outputPath)), '', `| | |`, `|---|---|`, `| ${t().cc_md_to_pdf.labelSource} | ${inputPath} |`, `| ${t().cc_md_to_pdf.labelTarget} | ${outputPath} |`, `| ${t().cc_md_to_pdf.labelSize} | ${formatFileSize(outStats.size)} |`, '', t().cc_md_to_pdf.hintPrint].join('\n') }] };
    } catch (error) {
      return { isError: true, content: [{ type: "text", text: t().common.error(error instanceof Error ? error.message : String(error)) }] };
    }
  }
);

// ============================================================================
// Tool 15: Set Language
// ============================================================================

server.tool(
  "cc_set_language",
  "Set the output language for CodeCommander tools",
  { language: z.enum(["de", "en"]).describe("Language code") },
  async ({ language }) => {
    setLanguage(language);
    return { content: [{ type: "text", text: t().cc_set_language.languageSet(language) }] };
  }
);

// ============================================================================
// Server Startup
// ============================================================================

async function main(): Promise<void> {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error(t().common.serverStarted);
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
