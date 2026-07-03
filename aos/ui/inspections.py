from nicegui import ui
from datetime import date
from aos.services.repository import Repository

def inspections_page():
    ui.label('Inspections').classes('text-h5')
    repo = Repository()
    with ui.card().classes('w-full'):
        ui.label('New Inspection').classes('text-h6')
        entities = repo.list_apiary_entities(active_only=True)
        options = {f"{e['code']} — {e['name']} ({e['type']}, {e['equipment']})": e['id'] for e in entities}
        colony_select = ui.select(options, label='Colony / Nuc').classes('w-96')
        inspection_date = ui.input('Date', value=str(date.today())).classes('w-48')
        inspection_type = ui.select(['Brood','Management','Queen Event','External Check'], label='Inspection Type', value='Brood').classes('w-48')
        queen_seen = ui.checkbox('Queen seen')
        eggs_seen = ui.checkbox('Eggs seen')
        larvae_seen = ui.checkbox('Larvae seen')
        queen_cells = ui.number('Queen cells', value=0, min=0).classes('w-48')
        brood_frames = ui.number('Brood frames', value=0, min=0, step=0.5).classes('w-48')
        stores_frames = ui.number('Stores frames', value=0, min=0, step=0.5).classes('w-48')
        temperament = ui.select(['Calm','OK','Defensive','Aggressive','Unknown'], label='Temperament', value='Unknown').classes('w-48')
        notes = ui.textarea('Notes').classes('w-full')
        def save():
            if not colony_select.value:
                ui.notify('Select a colony/nuc from central apiary entity list.', type='warning'); return
            repo.create_inspection({
                'colony_id': colony_select.value, 'date': inspection_date.value, 'inspection_type': inspection_type.value,
                'queen_seen': bool(queen_seen.value), 'eggs_seen': bool(eggs_seen.value), 'larvae_seen': bool(larvae_seen.value),
                'queen_cells': int(queen_cells.value or 0), 'brood_frames': float(brood_frames.value or 0),
                'stores_frames': float(stores_frames.value or 0), 'temperament': temperament.value, 'notes': notes.value or '',
            })
            ui.notify('Inspection saved', type='positive')
        ui.button('Save Inspection', on_click=save)
    ui.separator()
    ui.label('Inspection Log').classes('text-h6')
    ui.table(columns=[
        {'name':'date','label':'Date','field':'date'},
        {'name':'colony','label':'Colony/Nuc','field':'colony'},
        {'name':'inspection_type','label':'Type','field':'inspection_type'},
        {'name':'queen_seen','label':'Queen','field':'queen_seen'},
        {'name':'eggs_seen','label':'Eggs','field':'eggs_seen'},
        {'name':'queen_cells','label':'Q Cells','field':'queen_cells'},
        {'name':'brood_frames','label':'Brood','field':'brood_frames'},
        {'name':'stores_frames','label':'Stores','field':'stores_frames'},
        {'name':'notes','label':'Notes','field':'notes'},
    ], rows=repo.list_inspections(), row_key='date').classes('w-full')
