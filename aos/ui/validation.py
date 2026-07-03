from nicegui import ui
from aos.engines.validation_engine import validation_summary
from aos.services.repository import Repository
def page():
    ui.label('Validation / Data Integrity').classes('text-h5'); repo=Repository(); holder=ui.column().classes('w-full')
    def render():
        holder.clear(); v=validation_summary(); b=repo.baseline_integrity()
        with holder:
            ui.label(f"Status: {v['status']} — {v['message']}")
            ui.table(columns=[{'name':'severity','label':'Severity','field':'severity'},{'name':'item','label':'Item','field':'item'},{'name':'issue','label':'Issue','field':'issue'}],rows=v['issues'],row_key='item').classes('w-full')
            ui.label(f"Expected colonies/nucs: {b['expected_colonies']} | Actual: {b['actual_colonies']}")
            ui.table(columns=[{'name':'code','label':'Code','field':'code'},{'name':'name','label':'Name','field':'name'},{'name':'type','label':'Type','field':'type'}],rows=b['missing_colonies'],row_key='code').classes('w-full')
    def restore(): added=repo.restore_missing_baseline(); ui.notify(f'Restored: {added}',type='positive'); render()
    with ui.row(): ui.button('Run Check',on_click=render); ui.button('Restore Missing Baseline',on_click=restore)
    render()
