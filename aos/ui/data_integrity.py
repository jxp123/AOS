from nicegui import ui
from aos.services.repository import Repository
def data_integrity_page():
    ui.label('Data Integrity').classes('text-h5'); repo=Repository(); holder=ui.column().classes('w-full')
    def render():
        holder.clear(); data=repo.baseline_integrity()
        with holder:
            ui.label(f"Expected baseline colonies/nucs: {data['expected_colonies']}")
            ui.label(f"Current colony/nuc records: {data['actual_colonies']}")
            ui.table(columns=[{'name':'code','label':'Code','field':'code'},{'name':'name','label':'Name','field':'name'},{'name':'type','label':'Type','field':'type'},{'name':'equipment','label':'Equipment','field':'equipment'}], rows=data['missing_colonies'], row_key='code').classes('w-full')
            ui.table(columns=[{'name':'code','label':'Queen Code','field':'code'},{'name':'name','label':'Name','field':'name'},{'name':'line','label':'Line','field':'line'}], rows=data['missing_queens'], row_key='code').classes('w-full')
    def restore():
        added=repo.restore_missing_baseline(); ui.notify(f'Restored: {added}', type='positive'); render()
    with ui.row(): ui.button('Run Integrity Check', on_click=render); ui.button('Restore Missing Baseline Entities', on_click=restore)
    render()
