from nicegui import ui
from aos.services.repository import Repository
def queens_page():
    ui.label('Queen Register').classes('text-h5')
    ui.table(columns=[{'name':'code','label':'Code','field':'code'},{'name':'name','label':'Name','field':'name'},{'name':'line','label':'Line','field':'line'},{'name':'current_colony','label':'Colony','field':'current_colony'},{'name':'status','label':'Status','field':'status'},{'name':'temperament_score','label':'Temperament','field':'temperament_score'},{'name':'brood_score','label':'Brood','field':'brood_score'},{'name':'honey_score','label':'Honey','field':'honey_score'}], rows=Repository().list_queens(), row_key='code').classes('w-full')
