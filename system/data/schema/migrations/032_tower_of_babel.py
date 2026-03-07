"""
TOWER_OF_BABEL v3.7.1: Mehrsprachigkeit fuer Content-Tabellen

Fuehrt Schema-Migration durch und passt UNIQUE-Constraints an,
damit name+language zusammen unique sind (statt nur name).
"""
import sqlite3
from pathlib import Path


def migrate(db_path: str) -> tuple:
    """
    Fuehre TOWER_OF_BABEL Migration durch.

    Args:
        db_path: Pfad zur bach.db

    Returns:
        tuple (success, message)
    """
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # Pruefen ob language-Spalte bereits existiert
        cur.execute("PRAGMA table_info(bach_agents)")
        columns = [row[1] for row in cur.fetchall()]

        if 'language' in columns:
            # Spalte existiert, aber EN-Daten koennten fehlen
            en_count = cur.execute(
                "SELECT COUNT(*) FROM bach_agents WHERE language='en'"
            ).fetchone()[0]
            if en_count == 0:
                _insert_en_agents(cur)
                _insert_en_experts(cur)
                conn.commit()
                conn.close()
                return True, "TOWER_OF_BABEL: EN-Daten nachgetragen"
            conn.close()
            return True, "TOWER_OF_BABEL Migration bereits durchgefuehrt"

        # SQL-Datei ausfuehren (ALTER TABLE Statements)
        sql_path = Path(__file__).with_suffix('.sql')
        if sql_path.exists():
            sql = sql_path.read_text(encoding='utf-8')
            for statement in sql.split(';'):
                statement = statement.strip()
                if statement and not statement.startswith('--'):
                    try:
                        cur.execute(statement)
                    except sqlite3.OperationalError as e:
                        if 'duplicate column' not in str(e).lower():
                            raise

        # Unique-Index: name + language (ersetzt den alten name-only UNIQUE)
        # SQLite erlaubt kein DROP CONSTRAINT, daher neuen zusammengesetzten Index
        tables_with_name = ['bach_agents', 'bach_experts', 'skills']
        for table in tables_with_name:
            try:
                cur.execute(f"""
                    CREATE UNIQUE INDEX IF NOT EXISTS idx_{table}_name_language
                    ON {table}(name, language)
                """)
            except sqlite3.OperationalError:
                pass  # Index existiert bereits

        # Table-Rebuild: UNIQUE(name) -> UNIQUE(name, language)
        for table in tables_with_name:
            schema = cur.execute(
                f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table}'"
            ).fetchone()
            if schema and 'name TEXT UNIQUE' in schema[0]:
                new_schema = schema[0].replace(
                    f'CREATE TABLE {table}', f'CREATE TABLE {table}_new'
                ).replace('name TEXT UNIQUE NOT NULL', 'name TEXT NOT NULL')
                cur.execute(new_schema)
                cur.execute(f'INSERT INTO {table}_new SELECT * FROM {table}')
                cur.execute(f'DROP TABLE {table}')
                cur.execute(f'ALTER TABLE {table}_new RENAME TO {table}')
                cur.execute(
                    f'CREATE UNIQUE INDEX IF NOT EXISTS idx_{table}_name_language '
                    f'ON {table}(name, language)'
                )

        # EN-Duplikate fuer bach_agents
        _insert_en_agents(cur)
        _insert_en_experts(cur)

        conn.commit()
        conn.close()

        return True, "TOWER_OF_BABEL Migration erfolgreich: language-Spalte in 5 Tabellen + EN-Daten"

    except Exception as e:
        return False, f"TOWER_OF_BABEL Migration fehlgeschlagen: {e}"


def _insert_en_agents(cur):
    """Fuegt englische Agent-Beschreibungen ein."""
    agents_en = [
        ('persoenlicher-assistent', 'Personal Assistant',
         'Schedule management, research, organization'),
        ('gesundheitsassistent', 'Health Assistant',
         'Medical documentation and health management'),
        ('bueroassistent', 'Office Assistant',
         'Taxes, funding planning, documentation'),
        ('finanz-assistent', 'Finance Assistant',
         'Financial mails, subscriptions, insurances'),
        ('ati', 'Developer Agent (ATI)',
         'Specialized in tool monitoring and software development.'),
    ]
    for name, display_en, desc_en in agents_en:
        row = cur.execute(
            'SELECT type, category, skill_path, user_data_folder, parent_agent_id, '
            'is_active, priority, requires_setup, setup_completed, version, dashboard '
            'FROM bach_agents WHERE name=? AND language="de"', (name,)
        ).fetchone()
        if row:
            try:
                cur.execute(
                    'INSERT INTO bach_agents '
                    '(name, display_name, type, category, description, skill_path, '
                    'user_data_folder, parent_agent_id, is_active, priority, '
                    'requires_setup, setup_completed, version, dashboard, language) '
                    'VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,"en")',
                    (name, display_en, row[0], row[1], desc_en, row[2], row[3],
                     row[4], row[5], row[6], row[7], row[8], row[9], row[10])
                )
            except sqlite3.IntegrityError:
                pass


def _insert_en_experts(cur):
    """Fuegt englische Expert-Beschreibungen ein."""
    experts_en = [
        ('haushaltsmanagement', 'Household Management',
         'Household budgeting, inventory, shopping lists'),
        ('gesundheitsverwalter', 'Health Manager',
         'Medical reports, lab values, medications'),
        ('psycho-berater', 'Psycho Counselor',
         'Therapeutic conversations, session protocols'),
        ('steuer-agent', 'Tax Expert',
         'Tax receipts, work-related expenses'),
        ('foerderplaner', 'Funding Planner',
         'ICF funding planning, material research'),
        ('transkriptions-service', 'Transcription Service',
         'Transcribe audio files and conversations'),
        ('decision-briefing', 'Decision Briefing',
         'Central system for pending decisions and briefings'),
    ]
    for name, display_en, desc_en in experts_en:
        row = cur.execute(
            'SELECT agent_id, skill_path, domain, capabilities, is_active, '
            'requires_db, requires_files, version '
            'FROM bach_experts WHERE name=? AND language="de"', (name,)
        ).fetchone()
        if row:
            try:
                cur.execute(
                    'INSERT INTO bach_experts '
                    '(name, display_name, agent_id, description, skill_path, '
                    'domain, capabilities, is_active, requires_db, requires_files, '
                    'version, language) '
                    'VALUES (?,?,?,?,?,?,?,?,?,?,?,"en")',
                    (name, display_en, row[0], desc_en, row[1], row[2], row[3],
                     row[4], row[5], row[6], row[7])
                )
            except sqlite3.IntegrityError:
                pass


if __name__ == "__main__":
    import sys
    db = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).parent.parent / "bach.db")
    success, msg = migrate(db)
    print(f"{'OK' if success else 'FEHLER'}: {msg}")
