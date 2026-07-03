from nicegui import ui
from aos.services.repository import Repository
def page():
    ui.label('Queen Register').classes('text-h5'); repo=Repository(); ui.table(columns=[{'name':'code','label':'Code','field':'code'},{'name':'name','label':'Name','field':'name'},{'name':'line','label':'Line','field':'line'},{'name':'current_colony','label':'Current Colony','field':'current_colony'},{'name':'status','label':'Status','field':'status'},{'name':'evidence','label':'Evidence','field':'evidence'},{'name':'notes','label':'Notes','field':'notes'}],rows=repo.list_queens(),row_key='code').classes('w-full')
    ui.label('Full add/edit/delete is available in Colonies; expanded CRUD for this screen remains in follow-up patch if needed.').classes('text-caption')
