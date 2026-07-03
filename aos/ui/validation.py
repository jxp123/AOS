from nicegui import ui
from aos.engines.validation_engine import validation_summary
def validation_page():
    ui.label('Validation').classes('text-h5')
    summary=validation_summary()
    ui.label(f"Status: {summary['status']}")
    ui.label(summary['message'])
    ui.table(columns=[{'name':'severity','label':'Severity','field':'severity'},{'name':'item','label':'Item','field':'item'},{'name':'issue','label':'Issue','field':'issue'}], rows=summary['issues'], row_key='item').classes('w-full')
