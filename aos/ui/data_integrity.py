from nicegui import ui
from aos.services.repository import Repository

def data_integrity_page():
    ui.label('Data Integrity').classes('text-h5')
    repo = Repository()
    result_holder = ui.column().classes('w-full')

    def render():
        result_holder.clear()
        data = repo.baseline_integrity()
        with result_holder:
            ui.label(f"Expected baseline colonies/nucs: {data['expected_colonies']}")
            ui.label(f"Current colony/nuc records: {data['actual_colonies']}")
            if not data['missing_colonies'] and not data['missing_queens'] and not data['missing_equipment']:
                ui.label('✅ No missing baseline records detected.')
            else:
                ui.label('⚠️ Missing baseline records detected.')
                ui.label('Missing Colonies / Nucs').classes('text-h6')
                ui.table(columns=[
                    {'name':'code','label':'Code','field':'code'},
                    {'name':'name','label':'Name','field':'name'},
                    {'name':'type','label':'Type','field':'type'},
                    {'name':'equipment','label':'Equipment','field':'equipment'},
                    {'name':'status','label':'Status','field':'status'},
                ], rows=data['missing_colonies'], row_key='code').classes('w-full')
                ui.label('Missing Queens').classes('text-h6')
                ui.table(columns=[
                    {'name':'code','label':'Code','field':'code'},
                    {'name':'name','label':'Name','field':'name'},
                    {'name':'line','label':'Line','field':'line'},
                    {'name':'current_colony','label':'Current Colony','field':'current_colony'},
                ], rows=data['missing_queens'], row_key='code').classes('w-full')
                ui.label('Missing Equipment').classes('text-h6')
                ui.table(columns=[
                    {'name':'code','label':'Code','field':'code'},
                    {'name':'name','label':'Name','field':'name'},
                    {'name':'type','label':'Type','field':'type'},
                    {'name':'location','label':'Location','field':'location'},
                ], rows=data['missing_equipment'], row_key='code').classes('w-full')

    def restore():
        added = repo.restore_missing_baseline()
        ui.notify(f"Restored missing baseline: {added}", type='positive')
        render()

    with ui.row():
        ui.button('Run Integrity Check', on_click=render)
        ui.button('Restore Missing Baseline Entities', on_click=restore)
    render()
