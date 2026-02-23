import type { Translations } from './types.js';

export const en: Translations = {
  // === Common ===
  common: {
    fileNotFound: (path) => `\u274C File not found: ${path}`,
    sourceFileNotFound: (path) => `\u274C Source file not found: ${path}`,
    pathNotFound: (path) => `\u274C Path not found: ${path}`,
    error: (msg) => `\u274C Error: ${msg}`,
    serverStarted: '\uD83D\uDE80 BACH CodeCommander MCP Server started',
  },

  // === Tool 1: cc_analyze_code ===
  cc_analyze_code: {
    header: (filename) => `\uD83D\uDD0D **Code Analysis: ${filename}**`,
    metricTotalLines: 'Total lines',
    metricCodeLines: 'Code lines',
    metricCommentLines: 'Comment lines',
    metricBlankLines: 'Blank lines',
    metricClasses: 'Classes',
    metricFunctions: 'Functions',
    metricImports: 'Imports',
    metricCyclomaticComplexity: 'Cyclomatic complexity',
    metricFileSize: 'File size',
    classesHeader: '**Classes:**',
    classInfo: (name, bases, startLine, endLine, methodCount) =>
      `  \uD83D\uDCE6 **${name}${bases}** (L.${startLine}-${endLine}, ${methodCount} methods)`,
    classMethods: (methods) => `    Methods: ${methods}`,
    functionsHeader: '**Functions:**',
    functionInfo: (asyncPrefix, name, params, startLine, endLine) =>
      `  \u2699\uFE0F ${asyncPrefix}**${name}**(${params}) (L.${startLine}-${endLine})`,
    importsHeader: (stdlibCount, thirdPartyCount, localCount) =>
      `**Imports:** ${stdlibCount} stdlib, ${thirdPartyCount} third-party, ${localCount} local`,
    thirdPartyList: (modules) => `  Third-party: ${modules}`,
  },

  // === Tool 2: cc_analyze_methods ===
  cc_analyze_methods: {
    header: (filename) => `\uD83D\uDD0D **Method Analysis: ${filename}**`,
    classNotFound: (name, available) =>
      `\u274C Class "${name}" not found. Available: ${available}`,
    inheritsFrom: (bases) => `Inherits from: ${bases}`,
    visibility: 'Visibility',
    complexity: 'Complexity',
    visibilityLabel: (visibility, complexity) =>
      `  Visibility: ${visibility} | Complexity: ${complexity}`,
    decorators: (decorators) => `  Decorators: ${decorators}`,
    calls: (calls) => `  Calls: ${calls}`,
    topLevelFunctions: '## Top-Level Functions',
  },

  // === Tool 3: cc_extract_classes ===
  cc_extract_classes: {
    header: (filename) => `\uD83D\uDD0D **Class Extraction: ${filename}**`,
    classInfo: (name, lineCount, methodCount) =>
      `\uD83D\uDCE6 **${name}** (${lineCount} lines, ${methodCount} methods)`,
    helperFunctions: 'HelperFunctions',
    helperFunctionsInfo: (lineCount) => `\u2699\uFE0F **Helper Functions** (${lineCount} lines)`,
    filesWritten: (count, dir) => `\u2705 ${count} files written to: ${dir}`,
    hintUseOutputDir: `\uD83D\uDCA1 Use output_dir to save the extracts as files.`,
  },

  // === Tool 4: cc_organize_imports ===
  cc_organize_imports: {
    header: (filename) => `\uD83D\uDD0D **Import Analysis: ${filename}**`,
    noImportsFound: (filename) => `\uD83D\uDD0D No imports found in ${filename}.`,
    categoryFuture: '__future__',
    categoryStdlib: 'stdlib',
    categoryThirdParty: 'third-party',
    categoryLocal: 'local',
    duplicatesRemoved: 'Duplicates removed',
    previewHeader: '**Preview (sorted & grouped):**',
    importsSaved: `\u2705 Imports organized and saved.`,
  },

  // === Tool 5: cc_diagnose_imports ===
  cc_diagnose_imports: {
    header: (filename) => `\uD83D\uDD0D **Import Diagnostics: ${filename}**`,
    totalImports: 'Total imports',
    issues: 'Issues',
    warnings: 'Warnings',
    issuesHeader: '**Issues:**',
    warningsHeader: '**Warnings:**',
    noIssues: '\u2705 No import issues found.',
    unusedImport: (line, name) => `L.${line}: \`${name}\` is imported but not used`,
    duplicateImport: (text) => `Duplicate: \`${text}\``,
    relativeImportsWarning: (count) =>
      `${count} relative imports found (potential circular import risk)`,
    importOrderWarning: (line) => `L.${line}: Import order not PEP 8 compliant`,
    hintOrganize: `\uD83D\uDCA1 Use \`cc_organize_imports\` for automatic sorting.`,
  },

  // === Tool 6: cc_fix_json ===
  cc_fix_json: {
    validJson: (filename) => `\u2705 ${filename} is valid JSON.`,
    analysisHeader: (filename) => `\uD83D\uDD0D **JSON Analysis: ${filename}**`,
    validAfterRepair: '\u2705 Valid after repair',
    stillInvalid: (error) => `\u26A0\uFE0F Still invalid: ${error}`,
    repairedHeader: (filename) => `\u2705 **JSON repaired: ${filename}**`,
    fixBomRemoved: 'BOM removed',
    fixNulRemoved: 'NUL bytes removed',
    fixCommentsRemoved: 'Comments removed',
    fixBlockCommentsRemoved: 'Block comments removed',
    fixTrailingCommas: 'Trailing commas removed',
    fixSingleQuotes: 'Single quotes fixed',
  },

  // === Tool 7: cc_validate_json ===
  cc_validate_json: {
    validHeader: (filename) => `\u2705 **Valid JSON: ${filename}**`,
    invalidHeader: (filename) => `\u274C **Invalid JSON: ${filename}**`,
    typeArray: (count) => `Array (${count} elements)`,
    typeObject: (count) => `Object (${count} keys)`,
    labelType: 'Type',
    labelSize: 'Size',
    labelBom: 'BOM',
    bomYes: '\u26A0\uFE0F Yes',
    bomNo: 'No',
    positionInfo: (line, col) => `\n**Position:** Line ${line}, Column ${col}`,
    errorLabel: (msg) => `**Error:** ${msg}`,
    hintFix: `\uD83D\uDCA1 Use \`cc_fix_json\` for automatic repair.`,
  },

  // === Tool 8: cc_fix_encoding ===
  cc_fix_encoding: {
    noErrors: (filename) => `\u2705 No encoding errors in ${filename}.`,
    analysisHeader: (filename) => `\uD83D\uDD0D **Encoding Analysis: ${filename}**`,
    repairedHeader: (filename) => `\u2705 **Encoding repaired: ${filename}**`,
  },

  // === Tool 9: cc_cleanup_file ===
  cc_cleanup_file: {
    alreadyClean: (filename) => `\u2705 ${filename} is already clean.`,
    previewHeader: (filename) => `\uD83D\uDD0D **Preview: ${filename}**`,
    cleanedHeader: (filename) => `\u2705 **Cleaned: ${filename}**`,
    fixBomRemoved: 'BOM removed',
    fixNulRemoved: 'NUL bytes removed',
    fixTrailingWhitespace: 'Trailing whitespace',
  },

  // === Tool 10: cc_convert_format ===
  cc_convert_format: {
    conversionHeader: (inputFormat, outputFormat) => `\u2705 **${inputFormat} \u2192 ${outputFormat}**`,
    csvMinRows: `\u274C CSV: at least header + 1 data row required.`,
    csvRequiresArray: `\u274C CSV export requires an array.`,
    iniRequiresObject: `\u274C INI export requires an object.`,
    labelSource: 'Source',
    labelTarget: 'Target',
    labelSize: 'Size',
  },

  // === Tool 11: cc_fix_umlauts ===
  cc_fix_umlauts: {
    noIssues: (filename) => `\u2705 No broken umlauts in ${filename}.`,
    analysisHeader: (filename) => `\uD83D\uDD0D **Umlaut Analysis: ${filename}**`,
    replacements: (count) => `${count} replacements:`,
    repairedHeader: (filename) => `\u2705 **Umlauts repaired: ${filename}**`,
  },

  // === Tool 12: cc_scan_emoji ===
  cc_scan_emoji: {
    noEmojis: (fileCount) => `\u2705 No emojis found in ${fileCount} files.`,
    scanHeader: (fileCount) => `\uD83D\uDD0D **Emoji Scan: ${fileCount} files**`,
    emojiTableEmoji: 'Emoji',
    emojiTableCount: 'Count',
    emojiTableCodepoint: 'Codepoint',
    occurrencesHeader: '**Occurrences (first 30):**',
    andMore: (count) => `  ... and ${count} more`,
  },

  // === Tool 13: cc_generate_licenses ===
  cc_generate_licenses: {
    noPackageFiles: (dir) => `\u274C No package.json or requirements.txt found in ${dir}.`,
    generatedHeader: (count) => `\u2705 **Licenses generated: ${count} packages**`,
    labelFile: 'File',
    labelFormat: 'Format',
    labelPackages: 'Packages',
  },

  // === Tool 14: cc_md_to_pdf ===
  cc_md_to_pdf: {
    conversionHeader: (filename) => `\u2705 **Markdown \u2192 HTML: ${filename}**`,
    labelSource: 'Source',
    labelTarget: 'Target',
    labelSize: 'Size',
    hintPrint: `\uD83D\uDCA1 Open the HTML file in a browser and print as PDF.`,
  },

  // === Tool 15: cc_set_language ===
  cc_set_language: {
    languageSet: (lang) => `Language set to: ${lang}`,
  },
};
