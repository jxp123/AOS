from nicegui import ui
from aos.exporters.ai_export import export_ai_state

def ai_page():
    ui.label('AI Workflow').classes('text-h5')
    def do_export():
        path = export_ai_state()
        ui.notify(f'Exported: {path}', type='positive')
    ui.button('Export AI State JSON', on_click=do_export)
