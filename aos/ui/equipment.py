from nicegui import ui
from aos.services.repository import Repository

def equipment_page():
    ui.label('Equipment').classes('text-h5')
    repo = Repository()
    holder = ui.column().classes('w-full')

    def open_dialog(existing=None):
        with ui.dialog() as dialog, ui.card().classes('w-[700px]'):
            ui.label('Edit Equipment' if existing else 'Add Equipment').classes('text-h6')
            code = ui.input('Code', value=existing.get('code','') if existing else '').classes('w-full')
            name = ui.input('Name', value=existing.get('name','') if existing else '').classes('w-full')
            typ = ui.input('Type', value=existing.get('type','') if existing else '').classes('w-full')
            location = ui.input('Current Location', value=existing.get('location','') if existing else '').classes('w-full')
            compatible = ui.select(['National','14x12','Langstroth','Universal','Unknown'], label='Compatible With', value=existing.get('compatible','Unknown') if existing else 'Unknown').classes('w-full')
            status = ui.input('Status', value=existing.get('status','') if existing else '').classes('w-full')
            notes = ui.textarea('Notes', value=existing.get('notes','') if existing else '').classes('w-full')

            def save():
                if not code.value or not name.value:
                    ui.notify('Code and name are required', type='warning')
                    return
                data = {
                    'code': code.value.strip(),
                    'name': name.value.strip(),
                    'type': typ.value or '',
                    'current_location': location.value or '',
                    'compatible_with': compatible.value,
                    'status': status.value or '',
                    'notes': notes.value or '',
                }
                try:
                    if existing:
                        repo.update_equipment(existing['code'], data)
                    else:
                        repo.create_equipment(data)
                    ui.notify('Saved', type='positive')
                    dialog.close()
                    render()
                except Exception as e:
                    ui.notify(str(e), type='negative')
            with ui.row():
                ui.button('Save', on_click=save)
                ui.button('Cancel', on_click=dialog.close)
        dialog.open()

    def render():
        holder.clear()
        with holder:
            table = ui.table(
                columns=[
                    {'name':'code','label':'Code','field':'code'},
                    {'name':'name','label':'Name','field':'name'},
                    {'name':'type','label':'Type','field':'type'},
                    {'name':'location','label':'Location','field':'location'},
                    {'name':'compatible','label':'Compatible','field':'compatible'},
                    {'name':'status','label':'Status','field':'status'},
                    {'name':'notes','label':'Notes','field':'notes'},
                ],
                rows=repo.list_equipment(),
                row_key='code',
                selection='single',
            ).classes('w-full')
            def edit_selected():
                if not table.selected:
                    ui.notify('Select one row first', type='warning')
                    return
                open_dialog(table.selected[0])
            def delete_selected():
                if not table.selected:
                    ui.notify('Select one row first', type='warning')
                    return
                code = table.selected[0]['code']
                try:
                    repo.delete_equipment(code)
                    ui.notify('Deleted', type='positive')
                    render()
                except Exception as e:
                    ui.notify(str(e), type='negative')
            with ui.row():
                ui.button('Add Equipment', on_click=lambda: open_dialog())
                ui.button('Edit Selected', on_click=edit_selected)
                ui.button('Delete Selected', color='red', on_click=delete_selected)
                ui.button('Refresh', on_click=render)
    render()
