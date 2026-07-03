from nicegui import ui
from aos.services.repository import Repository
def colonies_page():
    ui.label('Colonies and Nucs').classes('text-h5')
    ui.table(columns=[{'name':'code','label':'Code','field':'code'},{'name':'name','label':'Name','field':'name'},{'name':'type','label':'Type','field':'type'},{'name':'equipment','label':'Equipment','field':'equipment'},{'name':'objective','label':'Objective','field':'objective'},{'name':'status','label':'Status','field':'status'},{'name':'notes','label':'Notes','field':'notes'}], rows=Repository().list_colonies(), row_key='code').classes('w-full')
