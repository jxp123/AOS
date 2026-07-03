from nicegui import ui
from aos.core.settings import APP_VERSION, DB_PATH, EXPORT_DIR, IMPORT_DIR, BACKUP_DIR, LOG_DIR
from aos.services.repository import Repository
def system_page():
    ui.label('System').classes('text-h5'); meta=Repository().system_meta()
    with ui.card():
        ui.label(f'AOS version: {APP_VERSION}'); ui.label(f'Schema version: {meta.get("schema_version","Unknown")}'); ui.label(f'Database: {DB_PATH}'); ui.label(f'Exports: {EXPORT_DIR}'); ui.label(f'Imports: {IMPORT_DIR}'); ui.label(f'Backups: {BACKUP_DIR}'); ui.label(f'Logs: {LOG_DIR}')
