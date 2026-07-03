from nicegui import ui
from aos.services.repository import Repository
def page():
    ui.label('Equipment').classes('text-h5'); repo=Repository(); ui.table(columns=[{'name':'code','label':'Code','field':'code'},{'name':'name','label':'Name','field':'name'},{'name':'type','label':'Type','field':'type'},{'name':'location','label':'Location','field':'location'},{'name':'compatible','label':'Compatible','field':'compatible'},{'name':'status','label':'Status','field':'status'},{'name':'notes','label':'Notes','field':'notes'}],rows=repo.list_equipment(),row_key='code').classes('w-full')
    ui.label('Full add/edit/delete is available in Colonies; expanded CRUD for this screen remains in follow-up patch if needed.').classes('text-caption')
