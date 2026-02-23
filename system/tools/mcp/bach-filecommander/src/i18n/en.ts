import type { Translations } from './types.js';

export const en: Translations = {
  // ==================== Common ====================
  common: {
    fileNotFound: (p) => `\u274C File not found: ${p}`,
    dirNotFound: (p) => `\u274C Directory not found: ${p}`,
    pathNotFound: (p) => `\u274C Path not found: ${p}`,
    error: (msg) => `\u274C Error: ${msg}`,
    errorGeneric: (msg) => `\u274C Error: ${msg}`,
    pathIsDirectory: (p) => `\u274C Path is a directory: ${p}`,
    pathIsNotDirectory: (p) => `\u274C Path is not a directory: ${p}`,
    pathIsDirectoryUseListDir: (p) => `\u274C Path is a directory: ${p}. Use fc_list_directory.`,
    pathIsNotDirUseReadFile: (p) => `\u274C Path is not a directory: ${p}. Use fc_read_file.`,
    pathIsDirectoryUseDeleteDir: `\u274C Path is a directory. Use fc_delete_directory.`,
    sourceNotFound: (p) => `\u274C Source not found: ${p}`,
    weekdays: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
  },

  // ==================== fc_read_file ====================
  fc_read_file: {
    moreLines: (count) => `\n\n... (${count} more lines)`,
    fileHeader: (name, size) => `\uD83D\uDCC4 **${name}** (${size})`,
    readError: (msg) => `\u274C Error reading file: ${msg}`,
  },

  // ==================== fc_write_file ====================
  fc_write_file: {
    actionAppended: 'appended',
    actionWritten: 'written',
    success: (action, p) => `\u2705 File ${action}: ${p}`,
    sizeLabel: (size) => `\uD83D\uDCCA Size: ${size}`,
    writeError: (msg) => `\u274C Error writing file: ${msg}`,
  },

  // ==================== fc_list_directory ====================
  fc_list_directory: {
    dirHeader: (p) => `\uD83D\uDCC2 **${p}**`,
    emptyDir: '(Directory is empty)',
    listError: (msg) => `\u274C Error listing directory: ${msg}`,
  },

  // ==================== fc_create_directory ====================
  fc_create_directory: {
    alreadyExists: (p) => `\u2139\uFE0F Directory already exists: ${p}`,
    created: (p) => `\u2705 Directory created: ${p}`,
    createError: (msg) => `\u274C Error creating directory: ${msg}`,
  },

  // ==================== fc_delete_file ====================
  fc_delete_file: {
    deleted: (p) => `\u2705 File deleted: ${p}`,
    deleteError: (msg) => `\u274C Error deleting file: ${msg}`,
  },

  // ==================== fc_delete_directory ====================
  fc_delete_directory: {
    deleted: (p) => `\u2705 Directory deleted: ${p}`,
    notEmpty: `\u274C Directory not empty. Set recursive=true to delete all contents.`,
    deleteError: (msg) => `\u274C Error deleting directory: ${msg}`,
  },

  // ==================== fc_move ====================
  fc_move: {
    moved: (source, dest) => `\u2705 Moved:\n  \uD83D\uDCE4 ${source}\n  \uD83D\uDCE5 ${dest}`,
    moveError: (msg) => `\u274C Error moving: ${msg}`,
  },

  // ==================== fc_copy ====================
  fc_copy: {
    copied: (source, dest) => `\u2705 Copied:\n  \uD83D\uDCE4 ${source}\n  \uD83D\uDCE5 ${dest}`,
    copyError: (msg) => `\u274C Error copying: ${msg}`,
  },

  // ==================== fc_file_info ====================
  fc_file_info: {
    header: (name) => `\uD83D\uDCCB **Information: ${name}**`,
    typeDirectory: 'Directory',
    typeFile: 'File',
    typeOther: 'Other',
    propType: 'Type',
    propSize: 'Size',
    propCreated: 'Created',
    propModified: 'Modified',
    propAccessed: 'Accessed',
    propPath: 'Path',
  },

  // ==================== fc_search_files ====================
  fc_search_files: {
    noResults: (pattern) => `\uD83D\uDD0D No files found for: "${pattern}"`,
    resultsHeader: (pattern) => `\uD83D\uDD0D **Search results for "${pattern}"**`,
    inDir: (dir) => `\uD83D\uDCC1 In: ${dir}`,
    found: (count) => `\uD83D\uDCCA Found: ${count}`,
    maxReached: '(maximum reached)',
    searchError: (msg) => `\u274C Search error: ${msg}`,
  },

  // ==================== fc_start_search ====================
  fc_start_search: {
    started: (id, dir, pattern) => `\uD83D\uDD0D **Search started**\n\n| | |\n|---|---|\n| Search ID | \`${id}\` |\n| Directory | ${dir} |\n| Pattern | ${pattern} |`,
    useGetResults: `Use \`fc_get_search_results\` to retrieve results.`,
    startError: (msg) => `\u274C Error starting search: ${msg}`,
  },

  // ==================== fc_get_search_results ====================
  fc_get_search_results: {
    notFound: (id) => `\u274C Search not found: ${id}`,
    useListSearches: `Use fc_list_searches for active searches.`,
    statusRunning: '\uD83D\uDD04 Running',
    statusDone: '\u2705 Completed',
    header: (status) => `\uD83D\uDD0D **Search results** (${status})`,
    labelPattern: 'Pattern',
    labelDirectory: 'Directory',
    labelScannedDirs: 'Scanned directories',
    labelFound: (count) => `${count} files`,
    labelRuntime: (seconds) => `${seconds}s`,
    resultsRange: (from, to, total) => `**Results ${from}-${to} of ${total}:**`,
    moreResults: (id, offset) => `\uD83D\uDCCC More results: \`fc_get_search_results("${id}", offset=${offset})\``,
  },

  // ==================== fc_stop_search ====================
  fc_stop_search: {
    notFound: (id) => `\u274C Search not found: ${id}`,
    alreadyDone: (count) => `\u2139\uFE0F Search already completed. ${count} results found.`,
    stopped: (id) => `\u23F9\uFE0F Search stopped: ${id}`,
    resultsSoFar: (count) => `\uD83D\uDCCA ${count} results found so far.`,
  },

  // ==================== fc_list_searches ====================
  fc_list_searches: {
    noSearches: `\uD83D\uDCCB No active searches.`,
    useStartSearch: `Start a new one with \`fc_start_search\`.`,
    header: (count) => `\uD83D\uDCCB **Searches** (${count})`,
    colStatus: 'Status',
    colSearchId: 'Search ID',
    colPattern: 'Pattern',
    colResults: 'Results',
    colRuntime: 'Runtime',
  },

  // ==================== fc_clear_search ====================
  fc_clear_search: {
    notFound: (id) => `\u274C Search not found: ${id}`,
    cleared: (count) => `\uD83E\uDDF9 ${count} completed searches removed.`,
    stillRunning: `\u26A0\uFE0F Search is still running. Use fc_stop_search first.`,
    useStopFirst: `Use fc_stop_search first.`,
    removed: (id) => `\u2705 Search removed: ${id}`,
  },

  // ==================== fc_safe_delete ====================
  fc_safe_delete: {
    typeDirectory: 'Directory',
    typeFile: 'File',
    movedToTrash: `\uD83D\uDDD1\uFE0F **Moved to recycle bin**`,
    propType: 'Type',
    propPath: 'Path',
    propOriginal: 'Original',
    propTrash: 'Recycle Bin',
    canRestore: `\u2705 Can be restored from the recycle bin.`,
    trashError: (msg) => `\u274C Error moving to recycle bin: ${msg}`,
  },

  // ==================== fc_execute_command ====================
  fc_execute_command: {
    commandLabel: (cmd) => `\u26A1 **Command:** \`${cmd}\``,
    outputLabel: '**Output:**',
    stderrLabel: '**Error output:**',
    noOutput: `\u2705 Command executed (no output)`,
    execError: (msg) => `\u274C Command execution error:\n${msg}`,
  },

  // ==================== fc_start_process ====================
  fc_start_process: {
    started: (program, args) => `\uD83D\uDE80 Process started: ${program}${args}`,
    pidLabel: (pid) => `\uD83D\uDCCB PID: ${pid}`,
    startError: (msg) => `\u274C Error starting process: ${msg}`,
  },

  // ==================== fc_get_time ====================
  fc_get_time: {
    header: `\uD83D\uDD50 **Current system time**`,
    labelDate: 'Date',
    labelTime: 'Time',
    labelWeekday: 'Weekday',
    labelISO: 'ISO',
    labelTimezone: 'Timezone',
  },

  // ==================== fc_read_multiple_files ====================
  fc_read_multiple_files: {
    notFound: 'Not found',
    isDirectory: 'Is a directory',
    moreLines: (count) => `... (${count} more lines)`,
    summary: (success, errors) => `\uD83D\uDCCA **Result:** ${success} read, ${errors} errors`,
  },

  // ==================== fc_edit_file ====================
  fc_edit_file: {
    invalidStartLine: (line, total) => `\u274C Start line ${line} invalid. File has ${total} lines.`,
    invalidEndLine: (line) => `\u274C End line ${line} invalid.`,
    contentRequired: (op) => `\u274C 'content' required for ${op} operation.`,
    unknownOperation: (op) => `\u274C Unknown operation: ${op}`,
    replacedLines: (start, end, count) => `Lines ${start}-${end} replaced with ${count} lines`,
    insertedLines: (count, after) => `${count} lines inserted after line ${after}`,
    deletedLines: (start, end) => `Lines ${start}-${end} deleted`,
    edited: (name) => `\u2705 **${name}** edited`,
    lineChange: (before, after) => `\uD83D\uDCCA ${before} \u2192 ${after} lines`,
    editError: (msg) => `\u274C Error editing file: ${msg}`,
  },

  // ==================== fc_str_replace ====================
  fc_str_replace: {
    pathIsDirectory: (p) => `\u274C Path is a directory: ${p}`,
    notFoundInFile: (name) => `\u274C String not found in ${name}.`,
    searchedFor: '**Searched for:**',
    fileStart: '**File start:**',
    multipleOccurrences: (count) => `\u274C String occurs ${count}x (must be unique).`,
    mustBeUnique: 'must be unique',
    tip: `\uD83D\uDCA1 Tip: Extend the search string with more context.`,
    replaced: (name) => `\u2705 **${name}** - String replaced`,
    sameLineCount: 'same line count',
    addedLines: (count) => `+${count} lines`,
    removedLines: (count) => `${count} lines`,
    labelChange: 'Change',
    labelFile: 'File',
    contextLabel: '**Context:**',
    replaceError: (msg) => `\u274C Error replacing string: ${msg}`,
  },

  // ==================== fc_list_processes ====================
  fc_list_processes: {
    noProcesses: (filter) => `\uD83D\uDD0D No processes found${filter ? ` for "${filter}"` : ''}.`,
    header: (filter) => `\uD83D\uDCCB **Running processes**${filter ? ` (Filter: ${filter})` : ''}`,
    colName: 'Name',
    colPid: 'PID',
    colMemory: 'Memory',
    listError: (msg) => `\u274C Error listing processes: ${msg}`,
  },

  // ==================== fc_kill_process ====================
  fc_kill_process: {
    pidOrNameRequired: `\u274C Either 'pid' or 'name' must be specified.`,
    killed: (target) => `\u2705 Process terminated: ${target}`,
    killError: (msg) => `\u274C Error terminating process: ${msg}`,
  },

  // ==================== fc_start_session ====================
  fc_start_session: {
    started: (id, command, pid, cwd) => `\uD83D\uDE80 **Session started**\n\n| | |\n|---|---|\n| Session ID | \`${id}\` |\n| Command | ${command} |\n| PID | ${pid} |\n| Directory | ${cwd} |`,
    useReadAndSend: `Use \`fc_read_output\` and \`fc_send_input\` to interact.`,
    startError: (msg) => `\u274C Error starting session: ${msg}`,
    processExited: (code) => `\n[Process exited with code ${code}]`,
    processError: (msg) => `\n[Error: ${msg}]`,
  },

  // ==================== fc_read_output ====================
  fc_read_output: {
    notFound: (id) => `\u274C Session not found: ${id}`,
    useListSessions: `Use fc_list_sessions for active sessions.`,
    statusRunning: '\uD83D\uDFE2 Running',
    statusEnded: '\uD83D\uDD34 Ended',
    header: (status) => `\uD83D\uDCE4 **Session Output** (${status})`,
    noOutput: '(no output)',
  },

  // ==================== fc_send_input ====================
  fc_send_input: {
    notFound: (id) => `\u274C Session not found: ${id}`,
    sessionEnded: `\u274C Session has ended. Start a new one with fc_start_session.`,
    useStartSession: 'Start a new one with fc_start_session.',
    sent: (id) => `\uD83D\uDCE5 Input sent to ${id}:`,
    useReadOutput: `Use \`fc_read_output\` to read the response.`,
    sendError: (msg) => `\u274C Error sending input: ${msg}`,
  },

  // ==================== fc_list_sessions ====================
  fc_list_sessions: {
    noSessions: `\uD83D\uDCCB No sessions available.`,
    useStartSession: `Start a new one with \`fc_start_session\`.`,
    header: (count) => `\uD83D\uDCCB **Active sessions** (${count})`,
    colStatus: 'Status',
    colSessionId: 'Session ID',
    colCommand: 'Command',
    colPid: 'PID',
    colRuntime: 'Runtime',
  },

  // ==================== fc_close_session ====================
  fc_close_session: {
    notFound: (id) => `\u274C Session not found: ${id}`,
    closed: (id) => `\u2705 Session terminated and removed: ${id}`,
    closeError: (msg) => `\u274C Error closing session: ${msg}`,
  },

  // ==================== fc_fix_json ====================
  fc_fix_json: {
    alreadyValid: (name) => `\u2705 ${name} is already valid JSON.`,
    fixBom: 'UTF-8 BOM removed',
    fixNul: 'NUL bytes removed',
    fixSingleLineComments: 'Single-line comments removed',
    fixMultiLineComments: 'Multi-line comments removed',
    fixTrailingCommas: 'Trailing commas removed',
    fixSingleQuotes: 'Single quotes \u2192 double quotes',
    analysisHeader: (name) => `\uD83D\uDD0D **JSON analysis: ${name}**`,
    foundProblems: '**Found problems:**',
    noAutoFixable: 'No automatically fixable problems.',
    afterFixValid: `\u2705 After repair: Valid JSON`,
    afterFixInvalid: (error) => `\u26A0\uFE0F After repair still invalid: ${error}`,
    repairedHeader: (name) => `\u2705 **JSON repaired: ${name}**`,
    validJson: `\u2705 Valid JSON`,
    stillInvalid: (error) => `\u26A0\uFE0F Still invalid: ${error}`,
    backupCreated: (p) => `\uD83D\uDCCB Backup: ${p}`,
  },

  // ==================== fc_validate_json ====================
  fc_validate_json: {
    validHeader: (name) => `\u2705 **Valid JSON: ${name}**`,
    typeArray: (count) => `Array (${count} elements)`,
    typeObject: (count) => `Object (${count} keys)`,
    propType: 'Type',
    propSize: 'Size',
    propBom: 'BOM',
    propBomYes: '\u26A0\uFE0F Yes',
    propBomNo: 'No',
    propEncoding: 'Encoding',
    invalidHeader: (name) => `\u274C **Invalid JSON: ${name}**`,
    errorLabel: '**Error:**',
    errorPosition: (line, col) => `**Error position:** Line ${line}, Column ${col}`,
    useFcFixJson: `\uD83D\uDCA1 Use \`fc_fix_json\` for automatic repair.`,
  },

  // ==================== fc_cleanup_file ====================
  fc_cleanup_file: {
    noCleanupNeeded: (count) => `\u2705 No cleanup needed. ${count} files checked.`,
    previewHeader: '\uD83D\uDD0D **Preview**',
    cleanedHeader: '\u2705 **Cleaned**',
    cleanedCount: (fixed, total) => `${fixed}/${total} files`,
  },

  // ==================== fc_fix_encoding ====================
  fc_fix_encoding: {
    noErrors: (name) => `\u2705 No encoding errors found in ${name}.`,
    analysisHeader: (name) => `\uD83D\uDD0D **Encoding analysis: ${name}**`,
    foundMojibake: '**Found mojibake patterns:**',
    repairedHeader: (name) => `\u2705 **Encoding repaired: ${name}**`,
    backupCreated: (p) => `\uD83D\uDCCB Backup: ${p}`,
  },

  // ==================== fc_folder_diff ====================
  fc_folder_diff: {
    firstSnapshot: (name) => `\uD83D\uDCF8 **First snapshot created: ${name}**`,
    labelFiles: 'Files',
    labelSnapshot: 'Snapshot',
    nextCallInfo: 'Changes will be detected on the next call.',
    noChanges: (name, count) => `\u2705 No changes in ${name}. ${count} files checked.`,
    diffHeader: (name) => `\uD83D\uDCCA **Directory diff: ${name}**`,
    catNew: 'New files',
    catModified: 'Modified',
    catDeleted: 'Deleted',
    catUnchanged: 'Unchanged',
    newFiles: '**New files:**',
    modifiedFiles: '**Modified files:**',
    deletedFiles: '**Deleted files:**',
    andMore: (count) => `... and ${count} more`,
  },

  // ==================== fc_batch_rename ====================
  fc_batch_rename: {
    noMatchingFiles: (dir) => `\uD83D\uDD0D No matching files in ${dir}`,
    noCommonPattern: (count) => `\uD83D\uDD0D No common pattern detected in ${count} files.`,
    autoDetectHeader: (count) => `\uD83D\uDD0D **Auto-detect: ${count} files**`,
    detectedPatterns: (patterns) => `Detected patterns: ${patterns}`,
    suggestedRename: (prefix) => `**Suggested rename (remove prefix "${prefix}"):**`,
    andMore: (count) => `... and ${count} more`,
    useTip: (prefix) => `\uD83D\uDCA1 Use \`mode="remove_prefix", pattern="${prefix}", dry_run=false\` to execute.`,
    patternRequired: (mode) => `\u274C 'pattern' required for mode "${mode}".`,
    noFilesMatchPattern: (pattern) => `\uD83D\uDD0D No files match pattern "${pattern}".`,
    previewHeader: (count) => `\uD83D\uDD0D **Preview: ${count} renames**`,
    setDryRunFalse: `\uD83D\uDCA1 Set \`dry_run=false\` to execute.`,
    renamed: (success, total) => `\u2705 **${success}/${total} files renamed**`,
  },

  // ==================== fc_convert_format ====================
  fc_convert_format: {
    sourceNotFound: (p) => `\u274C Source file not found: ${p}`,
    csvNeedsRows: `\u274C CSV needs at least a header + 1 data row.`,
    csvNeedsArray: `\u274C CSV export requires a JSON array of objects.`,
    iniNeedsObject: `\u274C INI export requires a JSON object.`,
    converted: (from, to) => `\u2705 **Converted: ${from} \u2192 ${to}**`,
    labelSource: 'Source',
    labelTarget: 'Target',
    labelSize: 'Size',
  },

  // ==================== fc_detect_duplicates ====================
  fc_detect_duplicates: {
    noDuplicates: (files, hashed) => `\u2705 No duplicates found. ${files} files checked, ${hashed} hashed.`,
    header: `\uD83D\uDD0D **Duplicates found**`,
    labelChecked: 'Files checked',
    labelGroups: 'Duplicate groups',
    labelDuplicates: 'Total duplicates',
    labelWasted: 'Wasted space',
    groupHeader: (index, size) => `**Group ${index}** (${size}):`,
    andMoreGroups: (count) => `... and ${count} more groups`,
    useSafeDelete: `\uD83D\uDCA1 Use \`fc_safe_delete\` to safely remove duplicates.`,
  },

  // ==================== fc_md_to_html ====================
  fc_md_to_html: {
    converted: (name) => `\u2705 **Markdown \u2192 HTML: ${name}**`,
    labelSource: 'Source',
    labelTarget: 'Target',
    labelSize: 'Size',
    openInBrowser: `\uD83D\uDCA1 Open the HTML file in a browser and print as PDF.`,
  },

  // ==================== Server ====================
  server: {
    started: '\uD83D\uDE80 BACH FileCommander MCP Server started',
    languageSet: (lang) => `Language set to: ${lang}`,
  },
};
