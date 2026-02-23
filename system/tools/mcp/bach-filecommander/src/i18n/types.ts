/**
 * i18n type definitions for BACH FileCommander MCP Server
 */

export interface Translations {
  // ==================== Common ====================
  common: {
    fileNotFound: (path: string) => string;
    dirNotFound: (path: string) => string;
    pathNotFound: (path: string) => string;
    error: (msg: string) => string;
    errorGeneric: (msg: string) => string;
    pathIsDirectory: (path: string) => string;
    pathIsNotDirectory: (path: string) => string;
    pathIsDirectoryUseListDir: (path: string) => string;
    pathIsNotDirUseReadFile: (path: string) => string;
    pathIsDirectoryUseDeleteDir: string;
    sourceNotFound: (path: string) => string;
    weekdays: string[];
  };

  // ==================== fc_read_file ====================
  fc_read_file: {
    moreLines: (count: number) => string;
    fileHeader: (name: string, size: string) => string;
    readError: (msg: string) => string;
  };

  // ==================== fc_write_file ====================
  fc_write_file: {
    actionAppended: string;
    actionWritten: string;
    success: (action: string, path: string) => string;
    sizeLabel: (size: string) => string;
    writeError: (msg: string) => string;
  };

  // ==================== fc_list_directory ====================
  fc_list_directory: {
    dirHeader: (path: string) => string;
    emptyDir: string;
    listError: (msg: string) => string;
  };

  // ==================== fc_create_directory ====================
  fc_create_directory: {
    alreadyExists: (path: string) => string;
    created: (path: string) => string;
    createError: (msg: string) => string;
  };

  // ==================== fc_delete_file ====================
  fc_delete_file: {
    deleted: (path: string) => string;
    deleteError: (msg: string) => string;
  };

  // ==================== fc_delete_directory ====================
  fc_delete_directory: {
    deleted: (path: string) => string;
    notEmpty: string;
    deleteError: (msg: string) => string;
  };

  // ==================== fc_move ====================
  fc_move: {
    moved: (source: string, dest: string) => string;
    moveError: (msg: string) => string;
  };

  // ==================== fc_copy ====================
  fc_copy: {
    copied: (source: string, dest: string) => string;
    copyError: (msg: string) => string;
  };

  // ==================== fc_file_info ====================
  fc_file_info: {
    header: (name: string) => string;
    typeDirectory: string;
    typeFile: string;
    typeOther: string;
    propType: string;
    propSize: string;
    propCreated: string;
    propModified: string;
    propAccessed: string;
    propPath: string;
  };

  // ==================== fc_search_files ====================
  fc_search_files: {
    noResults: (pattern: string) => string;
    resultsHeader: (pattern: string) => string;
    inDir: (dir: string) => string;
    found: (count: number) => string;
    maxReached: string;
    searchError: (msg: string) => string;
  };

  // ==================== fc_start_search ====================
  fc_start_search: {
    started: (id: string, dir: string, pattern: string) => string;
    useGetResults: string;
    startError: (msg: string) => string;
  };

  // ==================== fc_get_search_results ====================
  fc_get_search_results: {
    notFound: (id: string) => string;
    useListSearches: string;
    statusRunning: string;
    statusDone: string;
    header: (status: string) => string;
    labelPattern: string;
    labelDirectory: string;
    labelScannedDirs: string;
    labelFound: (count: number) => string;
    labelRuntime: (seconds: number) => string;
    resultsRange: (from: number, to: number, total: number) => string;
    moreResults: (id: string, offset: number) => string;
  };

  // ==================== fc_stop_search ====================
  fc_stop_search: {
    notFound: (id: string) => string;
    alreadyDone: (count: number) => string;
    stopped: (id: string) => string;
    resultsSoFar: (count: number) => string;
  };

  // ==================== fc_list_searches ====================
  fc_list_searches: {
    noSearches: string;
    useStartSearch: string;
    header: (count: number) => string;
    colStatus: string;
    colSearchId: string;
    colPattern: string;
    colResults: string;
    colRuntime: string;
  };

  // ==================== fc_clear_search ====================
  fc_clear_search: {
    notFound: (id: string) => string;
    cleared: (count: number) => string;
    stillRunning: string;
    useStopFirst: string;
    removed: (id: string) => string;
  };

  // ==================== fc_safe_delete ====================
  fc_safe_delete: {
    typeDirectory: string;
    typeFile: string;
    movedToTrash: string;
    propType: string;
    propPath: string;
    propOriginal: string;
    propTrash: string;
    canRestore: string;
    trashError: (msg: string) => string;
  };

  // ==================== fc_execute_command ====================
  fc_execute_command: {
    commandLabel: (cmd: string) => string;
    outputLabel: string;
    stderrLabel: string;
    noOutput: string;
    execError: (msg: string) => string;
  };

  // ==================== fc_start_process ====================
  fc_start_process: {
    started: (program: string, args: string) => string;
    pidLabel: (pid: number | undefined) => string;
    startError: (msg: string) => string;
  };

  // ==================== fc_get_time ====================
  fc_get_time: {
    header: string;
    labelDate: string;
    labelTime: string;
    labelWeekday: string;
    labelISO: string;
    labelTimezone: string;
  };

  // ==================== fc_read_multiple_files ====================
  fc_read_multiple_files: {
    notFound: string;
    isDirectory: string;
    moreLines: (count: number) => string;
    summary: (success: number, errors: number) => string;
  };

  // ==================== fc_edit_file ====================
  fc_edit_file: {
    invalidStartLine: (line: number, total: number) => string;
    invalidEndLine: (line: number) => string;
    contentRequired: (op: string) => string;
    unknownOperation: (op: string) => string;
    replacedLines: (start: number, end: number, count: number) => string;
    insertedLines: (count: number, after: number) => string;
    deletedLines: (start: number, end: number) => string;
    edited: (name: string) => string;
    lineChange: (before: number, after: number) => string;
    editError: (msg: string) => string;
  };

  // ==================== fc_str_replace ====================
  fc_str_replace: {
    pathIsDirectory: (path: string) => string;
    notFoundInFile: (name: string) => string;
    searchedFor: string;
    fileStart: string;
    multipleOccurrences: (count: number) => string;
    mustBeUnique: string;
    tip: string;
    replaced: (name: string) => string;
    sameLineCount: string;
    addedLines: (count: number) => string;
    removedLines: (count: number) => string;
    labelChange: string;
    labelFile: string;
    contextLabel: string;
    replaceError: (msg: string) => string;
  };

  // ==================== fc_list_processes ====================
  fc_list_processes: {
    noProcesses: (filter?: string) => string;
    header: (filter?: string) => string;
    colName: string;
    colPid: string;
    colMemory: string;
    listError: (msg: string) => string;
  };

  // ==================== fc_kill_process ====================
  fc_kill_process: {
    pidOrNameRequired: string;
    killed: (target: string) => string;
    killError: (msg: string) => string;
  };

  // ==================== fc_start_session ====================
  fc_start_session: {
    started: (id: string, command: string, pid: number | undefined, cwd: string) => string;
    useReadAndSend: string;
    startError: (msg: string) => string;
    processExited: (code: number | null) => string;
    processError: (msg: string) => string;
  };

  // ==================== fc_read_output ====================
  fc_read_output: {
    notFound: (id: string) => string;
    useListSessions: string;
    statusRunning: string;
    statusEnded: string;
    header: (status: string) => string;
    noOutput: string;
  };

  // ==================== fc_send_input ====================
  fc_send_input: {
    notFound: (id: string) => string;
    sessionEnded: string;
    useStartSession: string;
    sent: (id: string) => string;
    useReadOutput: string;
    sendError: (msg: string) => string;
  };

  // ==================== fc_list_sessions ====================
  fc_list_sessions: {
    noSessions: string;
    useStartSession: string;
    header: (count: number) => string;
    colStatus: string;
    colSessionId: string;
    colCommand: string;
    colPid: string;
    colRuntime: string;
  };

  // ==================== fc_close_session ====================
  fc_close_session: {
    notFound: (id: string) => string;
    closed: (id: string) => string;
    closeError: (msg: string) => string;
  };

  // ==================== fc_fix_json ====================
  fc_fix_json: {
    alreadyValid: (name: string) => string;
    fixBom: string;
    fixNul: string;
    fixSingleLineComments: string;
    fixMultiLineComments: string;
    fixTrailingCommas: string;
    fixSingleQuotes: string;
    analysisHeader: (name: string) => string;
    foundProblems: string;
    noAutoFixable: string;
    afterFixValid: string;
    afterFixInvalid: (error: string) => string;
    repairedHeader: (name: string) => string;
    validJson: string;
    stillInvalid: (error: string) => string;
    backupCreated: (path: string) => string;
  };

  // ==================== fc_validate_json ====================
  fc_validate_json: {
    validHeader: (name: string) => string;
    typeArray: (count: number) => string;
    typeObject: (count: number) => string;
    propType: string;
    propSize: string;
    propBom: string;
    propBomYes: string;
    propBomNo: string;
    propEncoding: string;
    invalidHeader: (name: string) => string;
    errorLabel: string;
    errorPosition: (line: number, col: number) => string;
    useFcFixJson: string;
  };

  // ==================== fc_cleanup_file ====================
  fc_cleanup_file: {
    noCleanupNeeded: (count: number) => string;
    previewHeader: string;
    cleanedHeader: string;
    cleanedCount: (fixed: number, total: number) => string;
  };

  // ==================== fc_fix_encoding ====================
  fc_fix_encoding: {
    noErrors: (name: string) => string;
    analysisHeader: (name: string) => string;
    foundMojibake: string;
    repairedHeader: (name: string) => string;
    backupCreated: (path: string) => string;
  };

  // ==================== fc_folder_diff ====================
  fc_folder_diff: {
    firstSnapshot: (name: string) => string;
    labelFiles: string;
    labelSnapshot: string;
    nextCallInfo: string;
    noChanges: (name: string, count: number) => string;
    diffHeader: (name: string) => string;
    catNew: string;
    catModified: string;
    catDeleted: string;
    catUnchanged: string;
    newFiles: string;
    modifiedFiles: string;
    deletedFiles: string;
    andMore: (count: number) => string;
  };

  // ==================== fc_batch_rename ====================
  fc_batch_rename: {
    noMatchingFiles: (dir: string) => string;
    noCommonPattern: (count: number) => string;
    autoDetectHeader: (count: number) => string;
    detectedPatterns: (patterns: string) => string;
    suggestedRename: (prefix: string) => string;
    andMore: (count: number) => string;
    useTip: (prefix: string) => string;
    patternRequired: (mode: string) => string;
    noFilesMatchPattern: (pattern: string) => string;
    previewHeader: (count: number) => string;
    setDryRunFalse: string;
    renamed: (success: number, total: number) => string;
  };

  // ==================== fc_convert_format ====================
  fc_convert_format: {
    sourceNotFound: (path: string) => string;
    csvNeedsRows: string;
    csvNeedsArray: string;
    iniNeedsObject: string;
    converted: (from: string, to: string) => string;
    labelSource: string;
    labelTarget: string;
    labelSize: string;
  };

  // ==================== fc_detect_duplicates ====================
  fc_detect_duplicates: {
    noDuplicates: (files: number, hashed: number) => string;
    header: string;
    labelChecked: string;
    labelGroups: string;
    labelDuplicates: string;
    labelWasted: string;
    groupHeader: (index: number, size: string) => string;
    andMoreGroups: (count: number) => string;
    useSafeDelete: string;
  };

  // ==================== fc_md_to_html ====================
  fc_md_to_html: {
    converted: (name: string) => string;
    labelSource: string;
    labelTarget: string;
    labelSize: string;
    openInBrowser: string;
  };

  // ==================== Server ====================
  server: {
    started: string;
    languageSet: (lang: string) => string;
  };
}
