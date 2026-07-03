from nicegui import ui
from aos.services.repository import Repository
def page():
    ui.label('Colonies and Nucs').classes('text-h5'); repo=Repository(); holder=ui.column().classes('w-full')
    def dialog(existing=None):
        with ui.dialog() as d, ui.card().classes('w-[700px]'):
            code=ui.input('Code',value=existing.get('code','') if existing else '').classes('w-full'); name=ui.input('Name',value=existing.get('name','') if existing else '').classes('w-full'); ctype=ui.select(['Hive','Nuc'],label='Type',value=existing.get('type','Hive') if existing else 'Hive').classes('w-full'); equipment=ui.select(['National','14x12','Langstroth','Unknown'],label='Equipment',value=existing.get('equipment','Unknown') if existing else 'Unknown').classes('w-full'); objective=ui.input('Objective',value=existing.get('objective','') if existing else '').classes('w-full'); status=ui.select(['Active','Inactive','Archived'],label='Status',value=existing.get('status','Active') if existing else 'Active').classes('w-full'); notes=ui.textarea('Notes',value=existing.get('notes','') if existing else '').classes('w-full')
            def save():
                try:
                    data={'code':code.value.strip(),'name':name.value.strip(),'colony_type':ctype.value,'equipment':equipment.value,'objective':objective.value or '','status':status.value,'notes':notes.value or ''}
                    repo.update_colony(existing['code'],data) if existing else repo.create_colony(data); ui.notify('Saved',type='positive'); d.close(); render()
                except Exception as e: ui.notify(str(e),type='negative')
            with ui.row(): ui.button('Save',on_click=save); ui.button('Cancel',on_click=d.close)
        d.open()
    def render():
        holder.clear()
        with holder:
            table=ui.table(columns=[{'name':'code','label':'Code','field':'code'},{'name':'name','label':'Name','field':'name'},{'name':'type','label':'Type','field':'type'},{'name':'equipment','label':'Equipment','field':'equipment'},{'name':'objective','label':'Objective','field':'objective'},{'name':'status','label':'Status','field':'status'},{'name':'notes','label':'Notes','field':'notes'}],rows=repo.list_colonies(),row_key='code',selection='single').classes('w-full')
            def edit():
                if not table.selected: ui.notify('Select one row',type='warning'); return
                dialog(table.selected[0])
            def delete():
                if not table.selected: ui.notify('Select one row',type='warning'); return
                try: repo.delete_colony(table.selected[0]['code']); ui.notify('Deleted',type='positive'); render()
                except Exception as e: ui.notify(str(e),type='negative')
            with ui.row(): ui.button('Add',on_click=lambda:dialog()); ui.button('Edit',on_click=edit); ui.button('Delete',color='red',on_click=delete); ui.button('Refresh',on_click=render)
    render()
