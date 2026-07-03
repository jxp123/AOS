
from nicegui import ui
from aos.services.repository import Repository

def colonies_page():
    ui.label('Colonies').classes('text-h5')
    repo = Repository()
    rows = repo.list_colonies()
    ui.table(
        columns=[
            {'name': 'code', 'label': 'Code', 'field': 'code', 'sortable': True},
            {'name': 'name', 'label': 'Name', 'field': 'name', 'sortable': True},
            {'name': 'type', 'label': 'Type', 'field': 'type'},
            {'name': 'equipment', 'label': 'Equipment', 'field': 'equipment', 'sortable': True},
            {'name': 'objective', 'label': 'Objective', 'field': 'objective'},
            {'name': 'status', 'label': 'Status', 'field': 'status'},
            {'name': 'notes', 'label': 'Notes', 'field': 'notes'},
        ],
        rows=rows,
        row_key='code',
    ).classes('w-full')
    ui.label('CRUD editing will be re-added on top of the repository layer in v0.6.1.')
