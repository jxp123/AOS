from nicegui import ui
from aos.config import APP_VERSION
from aos.engines.task_engine import task_summary, generated_tasks
from aos.engines.advisor_engine import advisor_summary, advisor_recommendations
from aos.engines.seasonal_engine import seasonal_tasks
def page():
    ui.label('Morning Briefing').classes('text-h5'); tasks=task_summary(); advisor=advisor_summary(); season=seasonal_tasks()
    with ui.row():
        for label,value in [('Version',APP_VERSION),('Season',season['phase']),('High Tasks',tasks['high']),('Advisor High',advisor['high']),('Low Confidence',advisor['low_confidence'])]:
            with ui.card(): ui.label(label); ui.label(str(value)).classes('text-h6')
    ui.label('Top Tasks').classes('text-h6')
    ui.table(columns=[{'name':'priority','label':'Priority','field':'priority'},{'name':'colony_code','label':'Colony/Nuc','field':'colony_code'},{'name':'task_type','label':'Task','field':'task_type'},{'name':'recommendation','label':'Recommendation','field':'recommendation'}],rows=generated_tasks()[:10],row_key='recommendation').classes('w-full')
    ui.label('Advisor').classes('text-h6')
    ui.table(columns=[{'name':'colony_code','label':'Colony/Nuc','field':'colony_code'},{'name':'priority','label':'Priority','field':'priority'},{'name':'risk','label':'Risk','field':'risk'},{'name':'confidence','label':'Confidence','field':'confidence'},{'name':'recommendation','label':'Recommendation','field':'recommendation'}],rows=advisor_recommendations()[:10],row_key='colony_code').classes('w-full')
