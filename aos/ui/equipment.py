from nicegui import ui
from aos.services.repository import Repository

def equipment_page():
    ui.label('Equipment').classes('text-h5')
    repo = Repository()
    holder = ui.column().classes('w-full')

    def render():
        holder.clear()
        with holder:
            table = ui.table(columns=[
                {'name':'code','label':'Code','field':'code'},
                {'name':'name','label':'Name','field':'name'},
                {'name':'type','label':'Type','field':'type'},
                {'name':'location','label':'Location','field':'location'},
                {'name':'compatible','label':'Compatible','field':'compatible'},
                {'name':'status','label':'Status','field':'status'},
                {'name':'notes','label':'Notes','field':'notes'},
            ], rows=repo.list_equipment(), row_key='code', selection='single').classes('w-full')
            with ui.row():
                ui.button('Add', on_click=lambda: dialog())
                ui.button('Edit selected', on_click=lambda: edit(table))
                ui.button('Delete selected', color='red', on_click=lambda: delete(table))
                ui.button('Refresh', on_click=render)

    def dialog(existing=None):
        with ui.dialog() as d, ui.card().classes('w-[650px]'):
            ui.label('Edit Equipment' if existing else 'Add Equipment').classes('text-h6')
            code = ui.input('Code', value=existing.get('code','') if existing else '').classes('w-full')
            name = ui.input('Name', value=existing.get('name','') if existing else '').classes('w-full')
            typ = ui.input('Type', value=existing.get('type','') if existing else '').classes('w-full')
            location = ui.input('Current Location', value=existing.get('location','') if existing else '').classes('w-full')
            compatible = ui.select(['National','14x12','Langstroth','Universal','Unknown'], label='Compatible With', value=existing.get('compatible','Unknown') if existing else 'Unknown').classes('w-full')
            status = ui.input('Status', value=existing.get('status','') if existing else '').classes('w-full')
            notes = ui.textarea('Notes', value=existing.get('notes','') if existing else '').classes('w-full')
            def save():
                data = {'code': code.value, 'name': name.value, 'type': typ.value, 'current_location': location.value, 'compatible_with': compatible.value, 'status': status.value, 'notes': notes.value or ''}
                try:
                    if existing: repo.update_equipment(existing['code'], data)
                    else: repo.create_equipment(data)
                    ui.notify('Saved', type='positive'); d.close(); render()
                except Exception as e: ui.notify(str(e), type='negative')
            with ui.row():
                ui.button('Save', on_click=save)
                ui.button('Cancel', on_click=d.close)
        d.open()

    def edit(table):
        if not table.selected: ui.notify('Select one row first', type='warning'); return
        dialog(table.selected[0])
    def delete(table):
        if not table.selected: ui.notify('Select one row first', type='warning'); return
        code = table.selected[0]['code']
        repo.delete_equipment(code); ui.notify('Deleted', type='positive'); render()

    render()
