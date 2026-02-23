/**
 * i18n Type Definitions for BACH CodeCommander MCP Server
 */

export interface Translations {
  // === Common ===
  common: {
    fileNotFound: (path: string) => string;
    sourceFileNotFound: (path: string) => string;
    pathNotFound: (path: string) => string;
    error: (msg: string) => string;
    serverStarted: string;
  };

  // === Tool 1: cc_analyze_code ===
  cc_analyze_code: {
    header: (filename: string) => string;
    metricTotalLines: string;
    metricCodeLines: string;
    metricCommentLines: string;
    metricBlankLines: string;
    metricClasses: string;
    metricFunctions: string;
    metricImports: string;
    metricCyclomaticComplexity: string;
    metricFileSize: string;
    classesHeader: string;
    classInfo: (name: string, bases: string, startLine: number, endLine: number, methodCount: number) => string;
    classMethods: (methods: string) => string;
    functionsHeader: string;
    functionInfo: (asyncPrefix: string, name: string, params: string, startLine: number, endLine: number) => string;
    importsHeader: (stdlibCount: number, thirdPartyCount: number, localCount: number) => string;
    thirdPartyList: (modules: string) => string;
  };

  // === Tool 2: cc_analyze_methods ===
  cc_analyze_methods: {
    header: (filename: string) => string;
    classNotFound: (name: string, available: string) => string;
    inheritsFrom: (bases: string) => string;
    visibility: string;
    complexity: string;
    visibilityLabel: (visibility: string, complexity: number) => string;
    decorators: (decorators: string) => string;
    calls: (calls: string) => string;
    topLevelFunctions: string;
  };

  // === Tool 3: cc_extract_classes ===
  cc_extract_classes: {
    header: (filename: string) => string;
    classInfo: (name: string, lineCount: number, methodCount: number) => string;
    helperFunctions: string;
    helperFunctionsInfo: (lineCount: number) => string;
    filesWritten: (count: number, dir: string) => string;
    hintUseOutputDir: string;
  };

  // === Tool 4: cc_organize_imports ===
  cc_organize_imports: {
    header: (filename: string) => string;
    noImportsFound: (filename: string) => string;
    categoryFuture: string;
    categoryStdlib: string;
    categoryThirdParty: string;
    categoryLocal: string;
    duplicatesRemoved: string;
    previewHeader: string;
    importsSaved: string;
  };

  // === Tool 5: cc_diagnose_imports ===
  cc_diagnose_imports: {
    header: (filename: string) => string;
    totalImports: string;
    issues: string;
    warnings: string;
    issuesHeader: string;
    warningsHeader: string;
    noIssues: string;
    unusedImport: (line: number, name: string) => string;
    duplicateImport: (text: string) => string;
    relativeImportsWarning: (count: number) => string;
    importOrderWarning: (line: number) => string;
    hintOrganize: string;
  };

  // === Tool 6: cc_fix_json ===
  cc_fix_json: {
    validJson: (filename: string) => string;
    analysisHeader: (filename: string) => string;
    validAfterRepair: string;
    stillInvalid: (error: string) => string;
    repairedHeader: (filename: string) => string;
    fixBomRemoved: string;
    fixNulRemoved: string;
    fixCommentsRemoved: string;
    fixBlockCommentsRemoved: string;
    fixTrailingCommas: string;
    fixSingleQuotes: string;
  };

  // === Tool 7: cc_validate_json ===
  cc_validate_json: {
    validHeader: (filename: string) => string;
    invalidHeader: (filename: string) => string;
    typeArray: (count: number) => string;
    typeObject: (count: number) => string;
    labelType: string;
    labelSize: string;
    labelBom: string;
    bomYes: string;
    bomNo: string;
    positionInfo: (line: number, col: number) => string;
    errorLabel: (msg: string) => string;
    hintFix: string;
  };

  // === Tool 8: cc_fix_encoding ===
  cc_fix_encoding: {
    noErrors: (filename: string) => string;
    analysisHeader: (filename: string) => string;
    repairedHeader: (filename: string) => string;
  };

  // === Tool 9: cc_cleanup_file ===
  cc_cleanup_file: {
    alreadyClean: (filename: string) => string;
    previewHeader: (filename: string) => string;
    cleanedHeader: (filename: string) => string;
    fixBomRemoved: string;
    fixNulRemoved: string;
    fixTrailingWhitespace: string;
  };

  // === Tool 10: cc_convert_format ===
  cc_convert_format: {
    conversionHeader: (inputFormat: string, outputFormat: string) => string;
    csvMinRows: string;
    csvRequiresArray: string;
    iniRequiresObject: string;
    labelSource: string;
    labelTarget: string;
    labelSize: string;
  };

  // === Tool 11: cc_fix_umlauts ===
  cc_fix_umlauts: {
    noIssues: (filename: string) => string;
    analysisHeader: (filename: string) => string;
    replacements: (count: number) => string;
    repairedHeader: (filename: string) => string;
  };

  // === Tool 12: cc_scan_emoji ===
  cc_scan_emoji: {
    noEmojis: (fileCount: number) => string;
    scanHeader: (fileCount: number) => string;
    emojiTableEmoji: string;
    emojiTableCount: string;
    emojiTableCodepoint: string;
    occurrencesHeader: string;
    andMore: (count: number) => string;
  };

  // === Tool 13: cc_generate_licenses ===
  cc_generate_licenses: {
    noPackageFiles: (dir: string) => string;
    generatedHeader: (count: number) => string;
    labelFile: string;
    labelFormat: string;
    labelPackages: string;
  };

  // === Tool 14: cc_md_to_pdf ===
  cc_md_to_pdf: {
    conversionHeader: (filename: string) => string;
    labelSource: string;
    labelTarget: string;
    labelSize: string;
    hintPrint: string;
  };

  // === Tool 15: cc_set_language ===
  cc_set_language: {
    languageSet: (lang: string) => string;
  };
}
