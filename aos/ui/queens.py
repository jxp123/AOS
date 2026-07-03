from nicegui import ui
from aos.services.repository import Repository

def queens_page():
    ui.label('Queen Register').classes('text-h5')
    repo = Repository()
    holder = ui.column().classes('w-full')

    def render():
        holder.clear()
        with holder:
            table = ui.table(columns=[
                {'name':'code','label':'Code','field':'code'},
                {'name':'name','label':'Name','field':'name'},
                {'name':'line','label':'Line','field':'line'},
                {'name':'source','label':'Source','field':'source'},
                {'name':'current_colony','label':'Current Colony','field':'current_colony'},
                {'name':'status','label':'Status','field':'status'},
                {'name':'evidence','label':'Evidence','field':'evidence'},
                {'name':'notes','label':'Notes','field':'notes'},
            ], rows=repo.list_queens(), row_key='code', selection='single').classes('w-full')
            with ui.row():
                ui.button('Add', on_click=lambda: dialog())
                ui.button('Edit selected', on_click=lambda: edit(table))
                ui.button('Delete selected', color='red', on_click=lambda: delete(table))
                ui.button('Refresh', on_click=render)

    def dialog(existing=None):
        with ui.dialog() as d, ui.card().classes('w-[650px]'):
            ui.label('Edit Queen' if existing else 'Add Queen').classes('text-h6')
            code = ui.input('Code', value=existing.get('code','') if existing else '').classes('w-full')
            name = ui.input('Name', value=existing.get('name','') if existing else '').classes('w-full')
            line = ui.input('Line', value=existing.get('line','') if existing else '').classes('w-full')
            source = ui.input('Source', value=existing.get('source','') if existing else '').classes('w-full')
            current = ui.input('Current Colony', value=existing.get('current_colony','') if existing else '').classes('w-full')
            status = ui.input('Status', value=existing.get('status','Active') if existing else 'Active').classes('w-full')
            evidence = ui.select(['Confirmed','Inferred','Unknown'], label='Evidence', value=existing.get('evidence','Unknown') if existing else 'Unknown').classes('w-full')
            notes = ui.textarea('Notes', value=existing.get('notes','') if existing else '').classes('w-full')
            def save():
                data = {'code': code.value, 'name': name.value, 'line': line.value, 'source': source.value, 'current_colony_code': current.value, 'status': status.value, 'evidence_status': evidence.value, 'notes': notes.value or ''}
                try:
                    if existing: repo.update_queen(existing['code'], data)
                    else: repo.create_queen(data)
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
        repo.delete_queen(code); ui.notify('Deleted', type='positive'); render()

    render()
