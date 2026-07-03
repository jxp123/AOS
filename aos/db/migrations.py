from sqlalchemy import text
from aos.db.session import engine
from aos.core.settings import SCHEMA_VERSION

EXPECTED_COLUMNS = {
    'inspections': {
        'bee_coverage_frames': 'FLOAT DEFAULT 0',
    },
    'queens': {
        'temperament_score': 'FLOAT DEFAULT 0',
        'brood_score': 'FLOAT DEFAULT 0',
        'honey_score': 'FLOAT DEFAULT 0',
    },
}

def table_columns(table):
    with engine.connect() as conn:
        rows = conn.execute(text(f'PRAGMA table_info({table})')).fetchall()
    return {r[1] for r in rows}

def migration_check():
    missing = []
    with engine.connect() as conn:
        existing_tables = {r[0] for r in conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'")).fetchall()}
    for table, columns in EXPECTED_COLUMNS.items():
        if table not in existing_tables:
            missing.append({'table': table, 'column': '*table missing*', 'sql': 'created by SQLAlchemy on boot'})
            continue
        present = table_columns(table)
        for col, sql_type in columns.items():
            if col not in present:
                missing.append({'table': table, 'column': col, 'sql': f'ALTER TABLE {table} ADD COLUMN {col} {sql_type}'})
    return missing

def apply_safe_migrations():
    missing = migration_check()
    applied = []
    with engine.begin() as conn:
        for item in missing:
            if item['column'] == '*table missing*':
                continue
            conn.execute(text(item['sql']))
            applied.append(item)
        # update schema version
        try:
            conn.execute(text("INSERT OR REPLACE INTO system_meta (key, value) VALUES ('schema_version', :v)"), {'v': SCHEMA_VERSION})
        except Exception:
            pass
    return applied
