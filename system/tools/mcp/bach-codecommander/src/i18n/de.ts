import type { Translations } from './types.js';

export const de: Translations = {
  // === Common ===
  common: {
    fileNotFound: (path) => `\u274C Datei nicht gefunden: ${path}`,
    sourceFileNotFound: (path) => `\u274C Quelldatei nicht gefunden: ${path}`,
    pathNotFound: (path) => `\u274C Pfad nicht gefunden: ${path}`,
    error: (msg) => `\u274C Fehler: ${msg}`,
    serverStarted: '\uD83D\uDE80 BACH CodeCommander MCP Server gestartet',
  },

  // === Tool 1: cc_analyze_code ===
  cc_analyze_code: {
    header: (filename) => `\uD83D\uDD0D **Code-Analyse: ${filename}**`,
    metricTotalLines: 'Zeilen gesamt',
    metricCodeLines: 'Code-Zeilen',
    metricCommentLines: 'Kommentar-Zeilen',
    metricBlankLines: 'Leerzeilen',
    metricClasses: 'Klassen',
    metricFunctions: 'Funktionen',
    metricImports: 'Imports',
    metricCyclomaticComplexity: 'Zyklomatische Komplexitaet',
    metricFileSize: 'Dateigroesse',
    classesHeader: '**Klassen:**',
    classInfo: (name, bases, startLine, endLine, methodCount) =>
      `  \uD83D\uDCE6 **${name}${bases}** (Z.${startLine}-${endLine}, ${methodCount} Methoden)`,
    classMethods: (methods) => `    Methoden: ${methods}`,
    functionsHeader: '**Funktionen:**',
    functionInfo: (asyncPrefix, name, params, startLine, endLine) =>
      `  \u2699\uFE0F ${asyncPrefix}**${name}**(${params}) (Z.${startLine}-${endLine})`,
    importsHeader: (stdlibCount, thirdPartyCount, localCount) =>
      `**Imports:** ${stdlibCount} stdlib, ${thirdPartyCount} third-party, ${localCount} lokal`,
    thirdPartyList: (modules) => `  Third-party: ${modules}`,
  },

  // === Tool 2: cc_analyze_methods ===
  cc_analyze_methods: {
    header: (filename) => `\uD83D\uDD0D **Methoden-Analyse: ${filename}**`,
    classNotFound: (name, available) =>
      `\u274C Klasse "${name}" nicht gefunden. Verfuegbar: ${available}`,
    inheritsFrom: (bases) => `Erbt von: ${bases}`,
    visibility: 'Sichtbarkeit',
    complexity: 'Komplexitaet',
    visibilityLabel: (visibility, complexity) =>
      `  Sichtbarkeit: ${visibility} | Komplexitaet: ${complexity}`,
    decorators: (decorators) => `  Dekoratoren: ${decorators}`,
    calls: (calls) => `  Ruft auf: ${calls}`,
    topLevelFunctions: '## Top-Level Funktionen',
  },

  // === Tool 3: cc_extract_classes ===
  cc_extract_classes: {
    header: (filename) => `\uD83D\uDD0D **Klassen-Extraktion: ${filename}**`,
    classInfo: (name, lineCount, methodCount) =>
      `\uD83D\uDCE6 **${name}** (${lineCount} Zeilen, ${methodCount} Methoden)`,
    helperFunctions: 'Hilfsfunktionen',
    helperFunctionsInfo: (lineCount) => `\u2699\uFE0F **Hilfsfunktionen** (${lineCount} Zeilen)`,
    filesWritten: (count, dir) => `\u2705 ${count} Dateien geschrieben nach: ${dir}`,
    hintUseOutputDir: `\uD83D\uDCA1 Nutze output_dir um die Extrakte als Dateien zu speichern.`,
  },

  // === Tool 4: cc_organize_imports ===
  cc_organize_imports: {
    header: (filename) => `\uD83D\uDD0D **Import-Analyse: ${filename}**`,
    noImportsFound: (filename) => `\uD83D\uDD0D Keine Imports in ${filename} gefunden.`,
    categoryFuture: '__future__',
    categoryStdlib: 'stdlib',
    categoryThirdParty: 'third-party',
    categoryLocal: 'lokal',
    duplicatesRemoved: 'Duplikate entfernt',
    previewHeader: '**Vorschau (sortiert & gruppiert):**',
    importsSaved: `\u2705 Imports organisiert und gespeichert.`,
  },

  // === Tool 5: cc_diagnose_imports ===
  cc_diagnose_imports: {
    header: (filename) => `\uD83D\uDD0D **Import-Diagnose: ${filename}**`,
    totalImports: 'Imports gesamt',
    issues: 'Probleme',
    warnings: 'Warnungen',
    issuesHeader: '**Probleme:**',
    warningsHeader: '**Warnungen:**',
    noIssues: '\u2705 Keine Import-Probleme gefunden.',
    unusedImport: (line, name) => `Z.${line}: \`${name}\` wird importiert aber nicht verwendet`,
    duplicateImport: (text) => `Duplikat: \`${text}\``,
    relativeImportsWarning: (count) =>
      `${count} relative Imports gefunden (potenzielle Circular-Import-Gefahr)`,
    importOrderWarning: (line) => `Z.${line}: Import-Reihenfolge nicht PEP 8 konform`,
    hintOrganize: `\uD83D\uDCA1 Nutze \`cc_organize_imports\` zum automatischen Sortieren.`,
  },

  // === Tool 6: cc_fix_json ===
  cc_fix_json: {
    validJson: (filename) => `\u2705 ${filename} ist gueltiges JSON.`,
    analysisHeader: (filename) => `\uD83D\uDD0D **JSON-Analyse: ${filename}**`,
    validAfterRepair: '\u2705 Gueltig nach Reparatur',
    stillInvalid: (error) => `\u26A0\uFE0F Noch ungueltig: ${error}`,
    repairedHeader: (filename) => `\u2705 **JSON repariert: ${filename}**`,
    fixBomRemoved: 'BOM entfernt',
    fixNulRemoved: 'NUL-Bytes entfernt',
    fixCommentsRemoved: 'Kommentare entfernt',
    fixBlockCommentsRemoved: 'Block-Kommentare entfernt',
    fixTrailingCommas: 'Trailing Commas entfernt',
    fixSingleQuotes: 'Single Quotes fixiert',
  },

  // === Tool 7: cc_validate_json ===
  cc_validate_json: {
    validHeader: (filename) => `\u2705 **Gueltiges JSON: ${filename}**`,
    invalidHeader: (filename) => `\u274C **Ungueltiges JSON: ${filename}**`,
    typeArray: (count) => `Array (${count} Elemente)`,
    typeObject: (count) => `Objekt (${count} Schluessel)`,
    labelType: 'Typ',
    labelSize: 'Groesse',
    labelBom: 'BOM',
    bomYes: '\u26A0\uFE0F Ja',
    bomNo: 'Nein',
    positionInfo: (line, col) => `\n**Position:** Zeile ${line}, Spalte ${col}`,
    errorLabel: (msg) => `**Fehler:** ${msg}`,
    hintFix: `\uD83D\uDCA1 Nutze \`cc_fix_json\` fuer automatische Reparatur.`,
  },

  // === Tool 8: cc_fix_encoding ===
  cc_fix_encoding: {
    noErrors: (filename) => `\u2705 Keine Encoding-Fehler in ${filename}.`,
    analysisHeader: (filename) => `\uD83D\uDD0D **Encoding-Analyse: ${filename}**`,
    repairedHeader: (filename) => `\u2705 **Encoding repariert: ${filename}**`,
  },

  // === Tool 9: cc_cleanup_file ===
  cc_cleanup_file: {
    alreadyClean: (filename) => `\u2705 ${filename} ist bereits sauber.`,
    previewHeader: (filename) => `\uD83D\uDD0D **Vorschau: ${filename}**`,
    cleanedHeader: (filename) => `\u2705 **Bereinigt: ${filename}**`,
    fixBomRemoved: 'BOM entfernt',
    fixNulRemoved: 'NUL-Bytes entfernt',
    fixTrailingWhitespace: 'Trailing Whitespace',
  },

  // === Tool 10: cc_convert_format ===
  cc_convert_format: {
    conversionHeader: (inputFormat, outputFormat) => `\u2705 **${inputFormat} \u2192 ${outputFormat}**`,
    csvMinRows: `\u274C CSV: mindestens Header + 1 Datenzeile noetig.`,
    csvRequiresArray: `\u274C CSV-Export erfordert ein Array.`,
    iniRequiresObject: `\u274C INI-Export erfordert ein Objekt.`,
    labelSource: 'Quelle',
    labelTarget: 'Ziel',
    labelSize: 'Groesse',
  },

  // === Tool 11: cc_fix_umlauts ===
  cc_fix_umlauts: {
    noIssues: (filename) => `\u2705 Keine kaputten Umlaute in ${filename}.`,
    analysisHeader: (filename) => `\uD83D\uDD0D **Umlaut-Analyse: ${filename}**`,
    replacements: (count) => `${count} Ersetzungen:`,
    repairedHeader: (filename) => `\u2705 **Umlaute repariert: ${filename}**`,
  },

  // === Tool 12: cc_scan_emoji ===
  cc_scan_emoji: {
    noEmojis: (fileCount) => `\u2705 Keine Emojis gefunden in ${fileCount} Dateien.`,
    scanHeader: (fileCount) => `\uD83D\uDD0D **Emoji-Scan: ${fileCount} Dateien**`,
    emojiTableEmoji: 'Emoji',
    emojiTableCount: 'Anzahl',
    emojiTableCodepoint: 'Codepoint',
    occurrencesHeader: '**Vorkommen (erste 30):**',
    andMore: (count) => `  ... und ${count} weitere`,
  },

  // === Tool 13: cc_generate_licenses ===
  cc_generate_licenses: {
    noPackageFiles: (dir) => `\u274C Kein package.json oder requirements.txt in ${dir} gefunden.`,
    generatedHeader: (count) => `\u2705 **Lizenzen generiert: ${count} Pakete**`,
    labelFile: 'Datei',
    labelFormat: 'Format',
    labelPackages: 'Pakete',
  },

  // === Tool 14: cc_md_to_pdf ===
  cc_md_to_pdf: {
    conversionHeader: (filename) => `\u2705 **Markdown \u2192 HTML: ${filename}**`,
    labelSource: 'Quelle',
    labelTarget: 'Ziel',
    labelSize: 'Groesse',
    hintPrint: `\uD83D\uDCA1 Oeffne die HTML-Datei im Browser und drucke als PDF.`,
  },

  // === Tool 15: cc_set_language ===
  cc_set_language: {
    languageSet: (lang) => `Sprache gesetzt auf: ${lang}`,
  },
};
