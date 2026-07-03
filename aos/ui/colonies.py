from nicegui import ui
from aos.services.repository import Repository

def colonies_page():
    ui.label('Colonies and Nucs').classes('text-h5')
    repo = Repository()
    holder = ui.column().classes('w-full')

    def open_dialog(existing=None):
        with ui.dialog() as dialog, ui.card().classes('w-[700px]'):
            ui.label('Edit Colony/Nuc' if existing else 'Add Colony/Nuc').classes('text-h6')
            code = ui.input('Code', value=existing.get('code','') if existing else '').classes('w-full')
            name = ui.input('Name', value=existing.get('name','') if existing else '').classes('w-full')
            colony_type = ui.select(['Hive','Nuc'], label='Type', value=existing.get('type','Hive') if existing else 'Hive').classes('w-full')
            equipment = ui.select(['National','14x12','Langstroth','Unknown'], label='Equipment', value=existing.get('equipment','Unknown') if existing else 'Unknown').classes('w-full')
            objective = ui.input('Objective', value=existing.get('objective','') if existing else '').classes('w-full')
            status = ui.select(['Active','Inactive','Archived'], label='Status', value=existing.get('status','Active') if existing else 'Active').classes('w-full')
            notes = ui.textarea('Notes', value=existing.get('notes','') if existing else '').classes('w-full')

            def save():
                if not code.value or not name.value:
                    ui.notify('Code and name are required', type='warning')
                    return
                data = {
                    'code': code.value.strip(),
                    'name': name.value.strip(),
                    'colony_type': colony_type.value,
                    'equipment': equipment.value,
                    'objective': objective.value or '',
                    'status': status.value,
                    'notes': notes.value or '',
                }
                try:
                    if existing:
                        repo.update_colony(existing['code'], data)
                    else:
                        repo.create_colony(data)
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
            rows = repo.list_colonies()
            table = ui.table(
                columns=[
                    {'name':'code','label':'Code','field':'code','sortable':True},
                    {'name':'name','label':'Name','field':'name','sortable':True},
                    {'name':'type','label':'Type','field':'type'},
                    {'name':'equipment','label':'Equipment','field':'equipment'},
                    {'name':'objective','label':'Objective','field':'objective'},
                    {'name':'status','label':'Status','field':'status'},
                    {'name':'notes','label':'Notes','field':'notes'},
                ],
                rows=rows,
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
                    repo.delete_colony(code)
                    ui.notify('Deleted', type='positive')
                    render()
                except Exception as e:
                    ui.notify(str(e), type='negative')
            with ui.row():
                ui.button('Add Colony/Nuc', on_click=lambda: open_dialog())
                ui.button('Edit Selected', on_click=edit_selected)
                ui.button('Delete Selected', color='red', on_click=delete_selected)
                ui.button('Refresh', on_click=render)
    render()
