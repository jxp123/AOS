from nicegui import ui
from aos.engines.task_engine import generated_tasks,task_summary
def page():
    ui.label('Tasks').classes('text-h5'); summary=task_summary()
    with ui.row():
        for k,v in summary.items():
            with ui.card(): ui.label(k.title()); ui.label(str(v)).classes('text-h6')
    ui.table(columns=[{'name':'date','label':'Date','field':'date'},{'name':'priority','label':'Priority','field':'priority'},{'name':'colony_code','label':'Colony','field':'colony_code'},{'name':'task_type','label':'Task','field':'task_type'},{'name':'reason','label':'Reason','field':'reason'},{'name':'recommendation','label':'Recommendation','field':'recommendation'}],rows=generated_tasks(),row_key='recommendation').classes('w-full')
