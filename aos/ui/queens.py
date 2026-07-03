
from nicegui import ui
from aos.services.repository import Repository

def queens_page():
    ui.label('Queen Register').classes('text-h5')
    rows = Repository().list_queens()
    ui.table(
        columns=[
            {'name': 'code', 'label': 'Code', 'field': 'code'},
            {'name': 'name', 'label': 'Name', 'field': 'name'},
            {'name': 'line', 'label': 'Line', 'field': 'line'},
            {'name': 'source', 'label': 'Source', 'field': 'source'},
            {'name': 'current_colony', 'label': 'Current Colony', 'field': 'current_colony'},
            {'name': 'status', 'label': 'Status', 'field': 'status'},
            {'name': 'evidence', 'label': 'Evidence', 'field': 'evidence'},
            {'name': 'notes', 'label': 'Notes', 'field': 'notes'},
        ],
        rows=rows,
        row_key='code',
    ).classes('w-full')
