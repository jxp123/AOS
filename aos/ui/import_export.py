from nicegui import ui
from aos.exporters.excel_export import export_excel
from aos.importers.excel_import import import_colonies_from_excel
from aos.utils.backup import backup_database, list_backups
from aos.core.settings import IMPORT_DIR
def import_export_page():
    ui.label('Import / Export / Backups').classes('text-h5')
    def do_export(): path=export_excel(); ui.notify(f'Exported {path}',type='positive')
    def do_backup(): path=backup_database(); ui.notify(f'Backup created: {path}',type='positive')
    with ui.row(): ui.button('Export AOS to Excel',on_click=do_export); ui.button('Create Manual Backup',on_click=do_backup)
    filename=ui.input('Import filename in imports folder').classes('w-96')
    def do_import():
        try: count=import_colonies_from_excel(IMPORT_DIR / filename.value); ui.notify(f'Processed {count} colonies',type='positive')
        except Exception as e: ui.notify(str(e),type='negative')
    ui.button('Import Colonies Sheet',on_click=do_import)
    ui.table(columns=[{'name':'file','label':'Backup file','field':'file'}], rows=[{'file':x} for x in list_backups()], row_key='file').classes('w-full')
