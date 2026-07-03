from nicegui import ui
from aos.services.repository import Repository

def genealogy_page():
    ui.label('Genealogy').classes('text-h5')
    rows = Repository().list_genealogy()
    ui.table(columns=[{'name':'date','label':'Date','field':'date'},{'name':'type','label':'Event','field':'type'},{'name':'source','label':'Source','field':'source'},{'name':'target','label':'Target','field':'target'},{'name':'queen','label':'Queen','field':'queen'},{'name':'details','label':'Details','field':'details'}], rows=rows, row_key='code' if rows and 'code' in rows[0] else 'date').classes('w-full')
