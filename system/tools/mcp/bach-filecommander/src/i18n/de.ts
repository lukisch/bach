import type { Translations } from './types.js';

export const de: Translations = {
  // ==================== Common ====================
  common: {
    fileNotFound: (p) => `\u274C Datei nicht gefunden: ${p}`,
    dirNotFound: (p) => `\u274C Verzeichnis nicht gefunden: ${p}`,
    pathNotFound: (p) => `\u274C Pfad nicht gefunden: ${p}`,
    error: (msg) => `\u274C Fehler: ${msg}`,
    errorGeneric: (msg) => `\u274C Fehler: ${msg}`,
    pathIsDirectory: (p) => `\u274C Pfad ist ein Verzeichnis: ${p}`,
    pathIsNotDirectory: (p) => `\u274C Pfad ist keine Verzeichnis: ${p}`,
    pathIsDirectoryUseListDir: (p) => `\u274C Pfad ist ein Verzeichnis: ${p}. Nutze fc_list_directory.`,
    pathIsNotDirUseReadFile: (p) => `\u274C Pfad ist keine Verzeichnis: ${p}. Nutze fc_read_file.`,
    pathIsDirectoryUseDeleteDir: `\u274C Pfad ist ein Verzeichnis. Nutze fc_delete_directory.`,
    sourceNotFound: (p) => `\u274C Quelle nicht gefunden: ${p}`,
    weekdays: ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag'],
  },

  // ==================== fc_read_file ====================
  fc_read_file: {
    moreLines: (count) => `\n\n... (${count} weitere Zeilen)`,
    fileHeader: (name, size) => `\uD83D\uDCC4 **${name}** (${size})`,
    readError: (msg) => `\u274C Fehler beim Lesen: ${msg}`,
  },

  // ==================== fc_write_file ====================
  fc_write_file: {
    actionAppended: 'erweitert',
    actionWritten: 'geschrieben',
    success: (action, p) => `\u2705 Datei ${action}: ${p}`,
    sizeLabel: (size) => `\uD83D\uDCCA Gr\u00f6\u00dfe: ${size}`,
    writeError: (msg) => `\u274C Fehler beim Schreiben: ${msg}`,
  },

  // ==================== fc_list_directory ====================
  fc_list_directory: {
    dirHeader: (p) => `\uD83D\uDCC2 **${p}**`,
    emptyDir: '(Verzeichnis ist leer)',
    listError: (msg) => `\u274C Fehler beim Auflisten: ${msg}`,
  },

  // ==================== fc_create_directory ====================
  fc_create_directory: {
    alreadyExists: (p) => `\u2139\uFE0F Verzeichnis existiert bereits: ${p}`,
    created: (p) => `\u2705 Verzeichnis erstellt: ${p}`,
    createError: (msg) => `\u274C Fehler beim Erstellen: ${msg}`,
  },

  // ==================== fc_delete_file ====================
  fc_delete_file: {
    deleted: (p) => `\u2705 Datei gel\u00f6scht: ${p}`,
    deleteError: (msg) => `\u274C Fehler beim L\u00f6schen: ${msg}`,
  },

  // ==================== fc_delete_directory ====================
  fc_delete_directory: {
    deleted: (p) => `\u2705 Verzeichnis gel\u00f6scht: ${p}`,
    notEmpty: `\u274C Verzeichnis nicht leer. Setze recursive=true zum L\u00f6schen aller Inhalte.`,
    deleteError: (msg) => `\u274C Fehler beim L\u00f6schen: ${msg}`,
  },

  // ==================== fc_move ====================
  fc_move: {
    moved: (source, dest) => `\u2705 Verschoben:\n  \uD83D\uDCE4 ${source}\n  \uD83D\uDCE5 ${dest}`,
    moveError: (msg) => `\u274C Fehler beim Verschieben: ${msg}`,
  },

  // ==================== fc_copy ====================
  fc_copy: {
    copied: (source, dest) => `\u2705 Kopiert:\n  \uD83D\uDCE4 ${source}\n  \uD83D\uDCE5 ${dest}`,
    copyError: (msg) => `\u274C Fehler beim Kopieren: ${msg}`,
  },

  // ==================== fc_file_info ====================
  fc_file_info: {
    header: (name) => `\uD83D\uDCCB **Informationen: ${name}**`,
    typeDirectory: 'Verzeichnis',
    typeFile: 'Datei',
    typeOther: 'Sonstiges',
    propType: 'Typ',
    propSize: 'Gr\u00f6\u00dfe',
    propCreated: 'Erstellt',
    propModified: 'Ge\u00e4ndert',
    propAccessed: 'Zugegriffen',
    propPath: 'Pfad',
  },

  // ==================== fc_search_files ====================
  fc_search_files: {
    noResults: (pattern) => `\uD83D\uDD0D Keine Dateien gefunden f\u00fcr: "${pattern}"`,
    resultsHeader: (pattern) => `\uD83D\uDD0D **Suchergebnisse f\u00fcr "${pattern}"**`,
    inDir: (dir) => `\uD83D\uDCC1 In: ${dir}`,
    found: (count) => `\uD83D\uDCCA Gefunden: ${count}`,
    maxReached: '(Maximum erreicht)',
    searchError: (msg) => `\u274C Fehler bei Suche: ${msg}`,
  },

  // ==================== fc_start_search ====================
  fc_start_search: {
    started: (id, dir, pattern) => `\uD83D\uDD0D **Suche gestartet**\n\n| | |\n|---|---|\n| Search-ID | \`${id}\` |\n| Verzeichnis | ${dir} |\n| Muster | ${pattern} |`,
    useGetResults: `Nutze \`fc_get_search_results\` um Ergebnisse abzurufen.`,
    startError: (msg) => `\u274C Fehler beim Starten der Suche: ${msg}`,
  },

  // ==================== fc_get_search_results ====================
  fc_get_search_results: {
    notFound: (id) => `\u274C Suche nicht gefunden: ${id}`,
    useListSearches: `Nutze fc_list_searches f\u00fcr aktive Suchen.`,
    statusRunning: '\uD83D\uDD04 L\u00e4uft',
    statusDone: '\u2705 Abgeschlossen',
    header: (status) => `\uD83D\uDD0D **Suchergebnisse** (${status})`,
    labelPattern: 'Muster',
    labelDirectory: 'Verzeichnis',
    labelScannedDirs: 'Gescannte Ordner',
    labelFound: (count) => `${count} Dateien`,
    labelRuntime: (seconds) => `${seconds}s`,
    resultsRange: (from, to, total) => `**Ergebnisse ${from}-${to} von ${total}:**`,
    moreResults: (id, offset) => `\uD83D\uDCCC Weitere Ergebnisse: \`fc_get_search_results("${id}", offset=${offset})\``,
  },

  // ==================== fc_stop_search ====================
  fc_stop_search: {
    notFound: (id) => `\u274C Suche nicht gefunden: ${id}`,
    alreadyDone: (count) => `\u2139\uFE0F Suche bereits beendet. ${count} Ergebnisse gefunden.`,
    stopped: (id) => `\u23F9\uFE0F Suche gestoppt: ${id}`,
    resultsSoFar: (count) => `\uD83D\uDCCA ${count} Ergebnisse bis hierhin gefunden.`,
  },

  // ==================== fc_list_searches ====================
  fc_list_searches: {
    noSearches: `\uD83D\uDCCB Keine Suchen aktiv.`,
    useStartSearch: `Starte eine neue mit \`fc_start_search\`.`,
    header: (count) => `\uD83D\uDCCB **Suchen** (${count})`,
    colStatus: 'Status',
    colSearchId: 'Search-ID',
    colPattern: 'Muster',
    colResults: 'Ergebnisse',
    colRuntime: 'Laufzeit',
  },

  // ==================== fc_clear_search ====================
  fc_clear_search: {
    notFound: (id) => `\u274C Suche nicht gefunden: ${id}`,
    cleared: (count) => `\uD83E\uDDF9 ${count} beendete Suchen entfernt.`,
    stillRunning: `\u26A0\uFE0F Suche l\u00e4uft noch. Nutze erst fc_stop_search.`,
    useStopFirst: `Nutze erst fc_stop_search.`,
    removed: (id) => `\u2705 Suche entfernt: ${id}`,
  },

  // ==================== fc_safe_delete ====================
  fc_safe_delete: {
    typeDirectory: 'Verzeichnis',
    typeFile: 'Datei',
    movedToTrash: `\uD83D\uDDD1\uFE0F **In Papierkorb verschoben**`,
    propType: 'Typ',
    propPath: 'Pfad',
    propOriginal: 'Original',
    propTrash: 'Papierkorb',
    canRestore: `\u2705 Kann aus dem Papierkorb wiederhergestellt werden.`,
    trashError: (msg) => `\u274C Fehler beim Verschieben in Papierkorb: ${msg}`,
  },

  // ==================== fc_execute_command ====================
  fc_execute_command: {
    commandLabel: (cmd) => `\u26A1 **Befehl:** \`${cmd}\``,
    outputLabel: '**Ausgabe:**',
    stderrLabel: '**Fehlerausgabe:**',
    noOutput: `\u2705 Befehl ausgef\u00fchrt (keine Ausgabe)`,
    execError: (msg) => `\u274C Fehler bei Befehlsausf\u00fchrung:\n${msg}`,
  },

  // ==================== fc_start_process ====================
  fc_start_process: {
    started: (program, args) => `\uD83D\uDE80 Prozess gestartet: ${program}${args}`,
    pidLabel: (pid) => `\uD83D\uDCCB PID: ${pid}`,
    startError: (msg) => `\u274C Fehler beim Starten: ${msg}`,
  },

  // ==================== fc_get_time ====================
  fc_get_time: {
    header: `\uD83D\uDD50 **Aktuelle Systemzeit**`,
    labelDate: 'Datum',
    labelTime: 'Uhrzeit',
    labelWeekday: 'Wochentag',
    labelISO: 'ISO',
    labelTimezone: 'Zeitzone',
  },

  // ==================== fc_read_multiple_files ====================
  fc_read_multiple_files: {
    notFound: 'Nicht gefunden',
    isDirectory: 'Ist ein Verzeichnis',
    moreLines: (count) => `... (${count} weitere Zeilen)`,
    summary: (success, errors) => `\uD83D\uDCCA **Ergebnis:** ${success} gelesen, ${errors} Fehler`,
  },

  // ==================== fc_edit_file ====================
  fc_edit_file: {
    invalidStartLine: (line, total) => `\u274C Startzeile ${line} ung\u00fcltig. Datei hat ${total} Zeilen.`,
    invalidEndLine: (line) => `\u274C Endzeile ${line} ung\u00fcltig.`,
    contentRequired: (op) => `\u274C 'content' erforderlich f\u00fcr ${op}-Operation.`,
    unknownOperation: (op) => `\u274C Unbekannte Operation: ${op}`,
    replacedLines: (start, end, count) => `Zeilen ${start}-${end} ersetzt durch ${count} Zeilen`,
    insertedLines: (count, after) => `${count} Zeilen nach Zeile ${after} eingef\u00fcgt`,
    deletedLines: (start, end) => `Zeilen ${start}-${end} gel\u00f6scht`,
    edited: (name) => `\u2705 **${name}** bearbeitet`,
    lineChange: (before, after) => `\uD83D\uDCCA ${before} \u2192 ${after} Zeilen`,
    editError: (msg) => `\u274C Fehler beim Bearbeiten: ${msg}`,
  },

  // ==================== fc_str_replace ====================
  fc_str_replace: {
    pathIsDirectory: (p) => `\u274C Pfad ist ein Verzeichnis: ${p}`,
    notFoundInFile: (name) => `\u274C String nicht gefunden in ${name}.`,
    searchedFor: '**Gesucht:**',
    fileStart: '**Datei-Anfang:**',
    multipleOccurrences: (count) => `\u274C String kommt ${count}x vor (muss eindeutig sein).`,
    mustBeUnique: 'muss eindeutig sein',
    tip: `\uD83D\uDCA1 Tipp: Erweitere den Suchstring um mehr Kontext.`,
    replaced: (name) => `\u2705 **${name}** - String ersetzt`,
    sameLineCount: 'gleiche Zeilenanzahl',
    addedLines: (count) => `+${count} Zeilen`,
    removedLines: (count) => `${count} Zeilen`,
    labelChange: '\u00C4nderung',
    labelFile: 'Datei',
    contextLabel: '**Kontext:**',
    replaceError: (msg) => `\u274C Fehler beim Ersetzen: ${msg}`,
  },

  // ==================== fc_list_processes ====================
  fc_list_processes: {
    noProcesses: (filter) => `\uD83D\uDD0D Keine Prozesse gefunden${filter ? ` f\u00fcr "${filter}"` : ''}.`,
    header: (filter) => `\uD83D\uDCCB **Laufende Prozesse**${filter ? ` (Filter: ${filter})` : ''}`,
    colName: 'Name',
    colPid: 'PID',
    colMemory: 'Speicher',
    listError: (msg) => `\u274C Fehler beim Auflisten: ${msg}`,
  },

  // ==================== fc_kill_process ====================
  fc_kill_process: {
    pidOrNameRequired: `\u274C Entweder 'pid' oder 'name' muss angegeben werden.`,
    killed: (target) => `\u2705 Prozess beendet: ${target}`,
    killError: (msg) => `\u274C Fehler beim Beenden: ${msg}`,
  },

  // ==================== fc_start_session ====================
  fc_start_session: {
    started: (id, command, pid, cwd) => `\uD83D\uDE80 **Session gestartet**\n\n| | |\n|---|---|\n| Session-ID | \`${id}\` |\n| Befehl | ${command} |\n| PID | ${pid} |\n| Verzeichnis | ${cwd} |`,
    useReadAndSend: `Nutze \`fc_read_output\` und \`fc_send_input\` zur Interaktion.`,
    startError: (msg) => `\u274C Fehler beim Starten: ${msg}`,
    processExited: (code) => `\n[Prozess beendet mit Code ${code}]`,
    processError: (msg) => `\n[Fehler: ${msg}]`,
  },

  // ==================== fc_read_output ====================
  fc_read_output: {
    notFound: (id) => `\u274C Session nicht gefunden: ${id}`,
    useListSessions: `Nutze fc_list_sessions f\u00fcr aktive Sessions.`,
    statusRunning: '\uD83D\uDFE2 L\u00e4uft',
    statusEnded: '\uD83D\uDD34 Beendet',
    header: (status) => `\uD83D\uDCE4 **Session Output** (${status})`,
    noOutput: '(kein Output)',
  },

  // ==================== fc_send_input ====================
  fc_send_input: {
    notFound: (id) => `\u274C Session nicht gefunden: ${id}`,
    sessionEnded: `\u274C Session ist beendet. Starte eine neue mit fc_start_session.`,
    useStartSession: 'Starte eine neue mit fc_start_session.',
    sent: (id) => `\uD83D\uDCE5 Input gesendet an ${id}:`,
    useReadOutput: `Nutze \`fc_read_output\` um die Antwort zu lesen.`,
    sendError: (msg) => `\u274C Fehler beim Senden: ${msg}`,
  },

  // ==================== fc_list_sessions ====================
  fc_list_sessions: {
    noSessions: `\uD83D\uDCCB Keine Sessions vorhanden.`,
    useStartSession: `Starte eine neue mit \`fc_start_session\`.`,
    header: (count) => `\uD83D\uDCCB **Aktive Sessions** (${count})`,
    colStatus: 'Status',
    colSessionId: 'Session-ID',
    colCommand: 'Befehl',
    colPid: 'PID',
    colRuntime: 'Laufzeit',
  },

  // ==================== fc_close_session ====================
  fc_close_session: {
    notFound: (id) => `\u274C Session nicht gefunden: ${id}`,
    closed: (id) => `\u2705 Session beendet und entfernt: ${id}`,
    closeError: (msg) => `\u274C Fehler beim Beenden: ${msg}`,
  },

  // ==================== fc_fix_json ====================
  fc_fix_json: {
    alreadyValid: (name) => `\u2705 ${name} ist bereits g\u00fcltiges JSON.`,
    fixBom: 'UTF-8 BOM entfernt',
    fixNul: 'NUL-Bytes entfernt',
    fixSingleLineComments: 'Einzeilige Kommentare entfernt',
    fixMultiLineComments: 'Mehrzeilige Kommentare entfernt',
    fixTrailingCommas: 'Trailing Commas entfernt',
    fixSingleQuotes: 'Single Quotes \u2192 Double Quotes',
    analysisHeader: (name) => `\uD83D\uDD0D **JSON-Analyse: ${name}**`,
    foundProblems: '**Gefundene Probleme:**',
    noAutoFixable: 'Keine automatisch reparierbaren Probleme.',
    afterFixValid: `\u2705 Nach Reparatur: G\u00fcltiges JSON`,
    afterFixInvalid: (error) => `\u26A0\uFE0F Nach Reparatur noch ung\u00fcltig: ${error}`,
    repairedHeader: (name) => `\u2705 **JSON repariert: ${name}**`,
    validJson: `\u2705 G\u00fcltiges JSON`,
    stillInvalid: (error) => `\u26A0\uFE0F Noch ung\u00fcltig: ${error}`,
    backupCreated: (p) => `\uD83D\uDCCB Backup: ${p}`,
  },

  // ==================== fc_validate_json ====================
  fc_validate_json: {
    validHeader: (name) => `\u2705 **G\u00fcltiges JSON: ${name}**`,
    typeArray: (count) => `Array (${count} Elemente)`,
    typeObject: (count) => `Objekt (${count} Schl\u00fcssel)`,
    propType: 'Typ',
    propSize: 'Gr\u00f6\u00dfe',
    propBom: 'BOM',
    propBomYes: '\u26A0\uFE0F Ja',
    propBomNo: 'Nein',
    propEncoding: 'Encoding',
    invalidHeader: (name) => `\u274C **Ung\u00fcltiges JSON: ${name}**`,
    errorLabel: '**Fehler:**',
    errorPosition: (line, col) => `**Fehlerposition:** Zeile ${line}, Spalte ${col}`,
    useFcFixJson: `\uD83D\uDCA1 Nutze \`fc_fix_json\` f\u00fcr automatische Reparatur.`,
  },

  // ==================== fc_cleanup_file ====================
  fc_cleanup_file: {
    noCleanupNeeded: (count) => `\u2705 Keine Bereinigung n\u00f6tig. ${count} Dateien gepr\u00fcft.`,
    previewHeader: '\uD83D\uDD0D **Vorschau**',
    cleanedHeader: '\u2705 **Bereinigt**',
    cleanedCount: (fixed, total) => `${fixed}/${total} Dateien`,
  },

  // ==================== fc_fix_encoding ====================
  fc_fix_encoding: {
    noErrors: (name) => `\u2705 Keine Encoding-Fehler in ${name} gefunden.`,
    analysisHeader: (name) => `\uD83D\uDD0D **Encoding-Analyse: ${name}**`,
    foundMojibake: '**Gefundene Mojibake-Muster:**',
    repairedHeader: (name) => `\u2705 **Encoding repariert: ${name}**`,
    backupCreated: (p) => `\uD83D\uDCCB Backup: ${p}`,
  },

  // ==================== fc_folder_diff ====================
  fc_folder_diff: {
    firstSnapshot: (name) => `\uD83D\uDCF8 **Erster Snapshot erstellt: ${name}**`,
    labelFiles: 'Dateien',
    labelSnapshot: 'Snapshot',
    nextCallInfo: 'Beim n\u00e4chsten Aufruf werden \u00c4nderungen erkannt.',
    noChanges: (name, count) => `\u2705 Keine \u00c4nderungen in ${name}. ${count} Dateien gepr\u00fcft.`,
    diffHeader: (name) => `\uD83D\uDCCA **Verzeichnis-Diff: ${name}**`,
    catNew: 'Neue Dateien',
    catModified: 'Ge\u00e4ndert',
    catDeleted: 'Gel\u00f6scht',
    catUnchanged: 'Unver\u00e4ndert',
    newFiles: '**Neue Dateien:**',
    modifiedFiles: '**Ge\u00e4nderte Dateien:**',
    deletedFiles: '**Gel\u00f6schte Dateien:**',
    andMore: (count) => `... und ${count} weitere`,
  },

  // ==================== fc_batch_rename ====================
  fc_batch_rename: {
    noMatchingFiles: (dir) => `\uD83D\uDD0D Keine passenden Dateien in ${dir}`,
    noCommonPattern: (count) => `\uD83D\uDD0D Kein gemeinsames Muster erkannt bei ${count} Dateien.`,
    autoDetectHeader: (count) => `\uD83D\uDD0D **Auto-Detect: ${count} Dateien**`,
    detectedPatterns: (patterns) => `Erkannte Muster: ${patterns}`,
    suggestedRename: (prefix) => `**Vorgeschlagene Umbenennung (Prefix "${prefix}" entfernen):**`,
    andMore: (count) => `... und ${count} weitere`,
    useTip: (prefix) => `\uD83D\uDCA1 Nutze \`mode="remove_prefix", pattern="${prefix}", dry_run=false\` zum Ausf\u00fchren.`,
    patternRequired: (mode) => `\u274C 'pattern' erforderlich f\u00fcr Modus "${mode}".`,
    noFilesMatchPattern: (pattern) => `\uD83D\uDD0D Keine Dateien passen zum Muster "${pattern}".`,
    previewHeader: (count) => `\uD83D\uDD0D **Vorschau: ${count} Umbenennungen**`,
    setDryRunFalse: `\uD83D\uDCA1 Setze \`dry_run=false\` zum Ausf\u00fchren.`,
    renamed: (success, total) => `\u2705 **${success}/${total} Dateien umbenannt**`,
  },

  // ==================== fc_convert_format ====================
  fc_convert_format: {
    sourceNotFound: (p) => `\u274C Quelldatei nicht gefunden: ${p}`,
    csvNeedsRows: `\u274C CSV ben\u00f6tigt mindestens Header + 1 Datenzeile.`,
    csvNeedsArray: `\u274C CSV-Export erfordert ein JSON-Array von Objekten.`,
    iniNeedsObject: `\u274C INI-Export erfordert ein JSON-Objekt.`,
    converted: (from, to) => `\u2705 **Konvertiert: ${from} \u2192 ${to}**`,
    labelSource: 'Quelle',
    labelTarget: 'Ziel',
    labelSize: 'Gr\u00f6\u00dfe',
  },

  // ==================== fc_detect_duplicates ====================
  fc_detect_duplicates: {
    noDuplicates: (files, hashed) => `\u2705 Keine Duplikate gefunden. ${files} Dateien gepr\u00fcft, ${hashed} gehasht.`,
    header: `\uD83D\uDD0D **Duplikate gefunden**`,
    labelChecked: 'Gepr\u00fcfte Dateien',
    labelGroups: 'Duplikat-Gruppen',
    labelDuplicates: 'Duplikate gesamt',
    labelWasted: 'Verschwendeter Platz',
    groupHeader: (index, size) => `**Gruppe ${index}** (${size}):`,
    andMoreGroups: (count) => `... und ${count} weitere Gruppen`,
    useSafeDelete: `\uD83D\uDCA1 Nutze \`fc_safe_delete\` zum sicheren Entfernen von Duplikaten.`,
  },

  // ==================== fc_md_to_html ====================
  fc_md_to_html: {
    converted: (name) => `\u2705 **Markdown \u2192 HTML: ${name}**`,
    labelSource: 'Quelle',
    labelTarget: 'Ziel',
    labelSize: 'Gr\u00f6\u00dfe',
    openInBrowser: `\uD83D\uDCA1 \u00d6ffne die HTML-Datei im Browser und drucke als PDF.`,
  },

  // ==================== Server ====================
  server: {
    started: '\uD83D\uDE80 BACH FileCommander MCP Server gestartet',
    languageSet: (lang) => `Language set to: ${lang}`,
  },
};
