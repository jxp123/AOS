from nicegui import ui
from aos.services.repository import Repository

def colonies_page():
    ui.label('Colonies and Nucs').classes('text-h5')
    ui.label('This screen and New Inspection dropdown both use Repository.list_apiary_entities().')
    ui.table(columns=[
        {'name':'code','label':'Code','field':'code','sortable':True},
        {'name':'name','label':'Name','field':'name','sortable':True},
        {'name':'type','label':'Type','field':'type'},
        {'name':'equipment','label':'Equipment','field':'equipment','sortable':True},
        {'name':'objective','label':'Objective','field':'objective'},
        {'name':'status','label':'Status','field':'status'},
        {'name':'notes','label':'Notes','field':'notes'},
    ], rows=Repository().list_apiary_entities(active_only=False), row_key='code').classes('w-full')
