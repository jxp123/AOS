from nicegui import ui
from aos.engines.task_engine import generated_tasks, task_summary

def tasks_page():
    ui.label('Tasks').classes('text-h5')
    summary = task_summary()
    with ui.row():
        for key, value in summary.items():
            with ui.card():
                ui.label(key.title())
                ui.label(str(value)).classes('text-h5')

    ui.table(
        columns=[
            {'name':'date','label':'Date','field':'date'},
            {'name':'priority','label':'Priority','field':'priority'},
            {'name':'colony_code','label':'Colony/Nuc','field':'colony_code'},
            {'name':'task_type','label':'Task','field':'task_type'},
            {'name':'reason','label':'Reason','field':'reason'},
            {'name':'recommendation','label':'Recommendation','field':'recommendation'},
            {'name':'evidence','label':'Evidence','field':'evidence'},
        ],
        rows=generated_tasks(),
        row_key='recommendation',
    ).classes('w-full')
