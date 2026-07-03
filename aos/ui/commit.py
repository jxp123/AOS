from nicegui import ui
from aos.services.repository import Repository

def commit_page():
    ui.label('Commit / Audit').classes('text-h5')
    rows = Repository().list_audit()
    ui.table(columns=[{'name':'date','label':'Date','field':'date'},{'name':'action','label':'Action','field':'action'},{'name':'entity_type','label':'Entity Type','field':'entity_type'},{'name':'entity_code','label':'Entity Code','field':'entity_code'},{'name':'details','label':'Details','field':'details'}], rows=rows, row_key='date').classes('w-full')
