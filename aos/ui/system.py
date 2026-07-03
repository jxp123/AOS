from nicegui import ui
from aos.config import APP_VERSION,SCHEMA_VERSION,DB_PATH,EXPORT_DIR,BACKUP_DIR,LOG_DIR
from aos.services.repository import Repository
def page():
    ui.label('System').classes('text-h5'); meta=Repository().system_meta()
    with ui.card():
        ui.label(f'AOS version: {APP_VERSION}'); ui.label(f'Schema version: {SCHEMA_VERSION}'); ui.label(f"DB schema meta: {meta.get('schema_version','Unknown')}"); ui.label(f'Database: {DB_PATH}'); ui.label(f'Exports: {EXPORT_DIR}'); ui.label(f'Backups: {BACKUP_DIR}'); ui.label(f'Logs: {LOG_DIR}')
