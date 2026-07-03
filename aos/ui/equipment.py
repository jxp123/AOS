
from nicegui import ui
from aos.services.repository import Repository

def equipment_page():
    ui.label('Equipment').classes('text-h5')
    rows = Repository().list_equipment()
    ui.table(
        columns=[
            {'name': 'code', 'label': 'Code', 'field': 'code'},
            {'name': 'name', 'label': 'Name', 'field': 'name'},
            {'name': 'type', 'label': 'Type', 'field': 'type'},
            {'name': 'location', 'label': 'Location', 'field': 'location'},
            {'name': 'compatible', 'label': 'Compatible', 'field': 'compatible'},
            {'name': 'status', 'label': 'Status', 'field': 'status'},
            {'name': 'notes', 'label': 'Notes', 'field': 'notes'},
        ],
        rows=rows,
        row_key='code',
    ).classes('w-full')
