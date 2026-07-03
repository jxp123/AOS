
from nicegui import ui
from aos.services.repository import Repository

def inspections_page():
    ui.label('Inspection Log').classes('text-h5')
    rows = Repository().list_inspections()
    ui.table(
        columns=[
            {'name': 'date', 'label': 'Date', 'field': 'date'},
            {'name': 'colony', 'label': 'Colony', 'field': 'colony'},
            {'name': 'inspection_type', 'label': 'Type', 'field': 'inspection_type'},
            {'name': 'queen_seen', 'label': 'Queen', 'field': 'queen_seen'},
            {'name': 'eggs_seen', 'label': 'Eggs', 'field': 'eggs_seen'},
            {'name': 'queen_cells', 'label': 'Q Cells', 'field': 'queen_cells'},
            {'name': 'brood_frames', 'label': 'Brood', 'field': 'brood_frames'},
            {'name': 'stores_frames', 'label': 'Stores', 'field': 'stores_frames'},
            {'name': 'notes', 'label': 'Notes', 'field': 'notes'},
        ],
        rows=rows,
        row_key='date',
    ).classes('w-full')
    ui.label('Inspection entry form will be rebuilt through services in v0.6.1.')
