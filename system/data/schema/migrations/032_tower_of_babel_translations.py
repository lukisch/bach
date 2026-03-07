"""
TOWER_OF_BABEL v3.7.1: Basis-Uebersetzungen fuer Help-Texte und Fehlermeldungen.

Fuegt englische Uebersetzungen fuer die haeufigsten Handler-Strings ein.
"""
import sqlite3
from pathlib import Path

# Format: (key, namespace, de_value, en_value)
TRANSLATIONS = [
    # === Task Handler ===
    ("task_add_desc", "help", "Task hinzufuegen", "Add task"),
    ("task_list_desc", "help", "Tasks auflisten", "List tasks"),
    ("task_done_desc", "help", "Task(s) als erledigt markieren", "Mark task(s) as done"),
    ("task_show_desc", "help", "Task-Details anzeigen", "Show task details"),
    ("task_delete_desc", "help", "Task(s) loeschen", "Delete task(s)"),
    ("task_block_desc", "help", "Task(s) blockieren", "Block task(s)"),
    ("task_unblock_desc", "help", "Task(s) entblocken", "Unblock task(s)"),
    ("task_priority_desc", "help", "Prioritaet aendern", "Change priority"),
    ("task_created", "cli", "Task erstellt", "Task created"),
    ("task_not_found", "error", "Task nicht gefunden", "Task not found"),
    ("no_tasks_found", "cli", "Keine Tasks gefunden", "No tasks found"),
    ("task_done_msg", "cli", "Task erledigt", "Task completed"),
    ("task_deleted", "cli", "Task geloescht", "Task deleted"),
    ("task_blocked", "cli", "Task blockiert", "Task blocked"),
    ("task_unblocked", "cli", "Task entblockt", "Task unblocked"),
    ("task_priority_set", "cli", "Prioritaet gesetzt", "Priority set"),
    ("task_title_missing", "error", "Titel fehlt", "Title missing"),

    # === Wiki Handler ===
    ("wiki_folder_not_found", "error", "Wiki-Ordner nicht gefunden", "Wiki folder not found"),
    ("article_not_found", "error", "Artikel nicht gefunden", "Article not found"),
    ("did_you_mean", "cli", "Meintest du", "Did you mean"),
    ("search_results", "cli", "Treffer", "Results"),
    ("no_results", "cli", "Keine Treffer", "No results"),

    # === Agent Handler ===
    ("db_not_found", "error", "Datenbank nicht gefunden", "Database not found"),
    ("boss_agents", "cli", "BOSS-AGENTEN", "BOSS AGENTS"),
    ("experts", "cli", "EXPERTEN", "EXPERTS"),
    ("legend", "cli", "Legende", "Legend"),
    ("details", "cli", "Details", "Details"),
    ("active", "cli", "aktiv", "active"),
    ("inactive", "cli", "inaktiv", "inactive"),

    # === Skills Handler ===
    ("skills_dir_not_found", "error", "Skills-Verzeichnis nicht gefunden", "Skills directory not found"),
    ("skill_not_found", "error", "Skill nicht gefunden", "Skill not found"),
    ("export_features", "cli", "Export-Features", "Export features"),
    ("dependencies", "cli", "Abhaengigkeiten", "Dependencies"),

    # === Docs Handler ===
    ("docs_dir_not_found", "error", "Docs-Verzeichnis nicht gefunden", "Docs directory not found"),
    ("doc_not_found", "error", "Dokument nicht gefunden", "Document not found"),
    ("documentation", "cli", "DOKUMENTATION", "DOCUMENTATION"),
    ("guides", "cli", "Guides", "Guides"),
    ("generated_with", "cli", "Generiert mit", "Generated with"),
    ("unknown_target", "error", "Unbekanntes Ziel", "Unknown target"),
    ("available", "cli", "Verfuegbar", "Available"),

    # === Allgemein ===
    ("success", "cli", "Erfolg", "Success"),
    ("error_generic", "error", "Fehler", "Error"),
    ("warning", "cli", "Warnung", "Warning"),
    ("not_found", "error", "nicht gefunden", "not found"),
    ("already_exists", "error", "existiert bereits", "already exists"),
    ("saved", "cli", "gespeichert", "saved"),
    ("deleted", "cli", "geloescht", "deleted"),
    ("updated", "cli", "aktualisiert", "updated"),
    ("created", "cli", "erstellt", "created"),
    ("count", "cli", "Anzahl", "Count"),
    ("category", "cli", "Kategorie", "Category"),
    ("name_label", "cli", "Name", "Name"),
    ("description_label", "cli", "Beschreibung", "Description"),
    ("status", "cli", "Status", "Status"),
    ("version_label", "cli", "Version", "Version"),
    ("overview", "cli", "Ueberblick", "Overview"),

    # === Setup Handler ===
    ("setup_lang_desc", "help", "Root-Dokumente auf Sprache umschalten", "Switch root documents to language"),
    ("setup_check_desc", "help", "Pruefe ob alle Abhaengigkeiten konfiguriert sind", "Check if all dependencies are configured"),
    ("all_ok", "cli", "Alles OK", "All OK"),
    ("some_checks_failed", "cli", "Einige Checks fehlgeschlagen", "Some checks failed"),
]


def migrate(db_path: str) -> tuple:
    """Fuegt Basis-Uebersetzungen ein."""
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        inserted = 0
        skipped = 0

        for key, namespace, de_value, en_value in TRANSLATIONS:
            for lang, value in [("de", de_value), ("en", en_value)]:
                try:
                    cur.execute("""
                        INSERT INTO languages_translations
                            (key, namespace, language, value, is_verified, source, created_at)
                        VALUES (?, ?, ?, ?, 1, 'tower_of_babel', datetime('now'))
                    """, (key, namespace, lang, value))
                    inserted += 1
                except sqlite3.IntegrityError:
                    skipped += 1

        conn.commit()
        conn.close()
        return True, f"TOWER_OF_BABEL Translations: {inserted} eingefuegt, {skipped} uebersprungen (bereits vorhanden)"

    except Exception as e:
        return False, f"Translation-Migration fehlgeschlagen: {e}"


if __name__ == "__main__":
    import sys
    db = sys.argv[1] if len(sys.argv) > 1 else str(
        Path(__file__).parent.parent / "bach.db"
    )
    success, msg = migrate(db)
    print(f"{'OK' if success else 'FEHLER'}: {msg}")
