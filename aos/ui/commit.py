from nicegui import ui
from aos.services.repository import Repository
from aos.engines.commit_engine import validate_pending_commits, commit_all_pending
def commit_page():
    ui.label('Commit Queue').classes('text-h5'); repo=Repository(); payload=ui.textarea('Stage new pending change').classes('w-full')
    def stage(): repo.create_pending_commit('Manual Note','System','AOS',payload.value or ''); ui.notify('Pending change staged',type='positive')
    def validate(): s=validate_pending_commits(); ui.notify(s['message'],type='warning' if s['status']=='WARN' else 'positive')
    def commit(): r=commit_all_pending(); ui.notify(r['message'],type='positive' if r['status']=='COMMITTED' else 'negative')
    with ui.row(): ui.button('Stage Note',on_click=stage); ui.button('Validate Queue',on_click=validate); ui.button('Commit Pending',on_click=commit)
    ui.table(columns=[{'name':'id','label':'ID','field':'id'},{'name':'date','label':'Date','field':'date'},{'name':'event_type','label':'Event','field':'event_type'},{'name':'entity_code','label':'Entity','field':'entity_code'},{'name':'payload','label':'Payload','field':'payload'},{'name':'status','label':'Status','field':'status'}], rows=repo.list_pending_commits(), row_key='id').classes('w-full')
