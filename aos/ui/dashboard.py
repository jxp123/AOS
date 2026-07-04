from nicegui import ui
from aos.config import APP_VERSION
from aos.engines.operations_engine import todays_work, shift_briefing
from aos.engines.task_engine import task_summary, generated_tasks
from aos.engines.advisor_engine import advisor_summary, advisor_recommendations
from aos.engines.seasonal_engine import seasonal_tasks
from aos.engines.inspection_scheduler import scheduler_summary, todays_plan


def page():
    ui.label('Morning Briefing').classes('text-h5')
    tasks = task_summary()
    advisor = advisor_summary()
    season = seasonal_tasks()
    schedule = scheduler_summary()

    with ui.row():
        for label, value in [
            ('Version', APP_VERSION),
            ('Overdue Inspections', schedule['overdue']),
            ('Due Today', schedule['due_today']),
            ('Due Soon', schedule['due_soon']),
            ('No Inspection Record', schedule['no_record']),
            ('High Tasks', tasks['high']),
        ]:
            with ui.card():
                ui.label(label)
                ui.label(str(value)).classes('text-h6')

    ui.label("Today\'s Inspection Plan").classes("text-h6")
    ui.label('Default rule: active hives and nucs should be inspected every 7 days unless a closer strategy applies.').classes('text-subtitle2')
    ui.table(
        columns=[
            {'name':'priority','label':'Priority','field':'priority'},
            {'name':'status','label':'Status','field':'status'},
            {'name':'code','label':'Colony/Nuc','field':'code'},
            {'name':'type','label':'Type','field':'type'},
            {'name':'equipment','label':'Equipment','field':'equipment'},
            {'name':'last_inspection','label':'Last Inspection','field':'last_inspection'},
            {'name':'days_since','label':'Days Since','field':'days_since'},
            {'name':'next_due','label':'Next Due','field':'next_due'},
            {'name':'strategy','label':'Strategy','field':'strategy'},
            {'name':'action','label':'Action','field':'action'},
        ],
        rows=todays_plan(),
        row_key='code',
    ).classes('w-full')

    ui.label('Top Tasks').classes('text-h6')
    ui.table(
        columns=[
            {'name':'priority','label':'Priority','field':'priority'},
            {'name':'colony_code','label':'Colony/Nuc','field':'colony_code'},
            {'name':'task_type','label':'Task','field':'task_type'},
            {'name':'recommendation','label':'Recommendation','field':'recommendation'},
        ],
        rows=generated_tasks()[:10],
        row_key='recommendation',
    ).classes('w-full')

    ui.label('Advisor').classes('text-h6')
    ui.table(
        columns=[
            {'name':'colony_code','label':'Colony/Nuc','field':'colony_code'},
            {'name':'priority','label':'Priority','field':'priority'},
            {'name':'risk','label':'Risk','field':'risk'},
            {'name':'confidence','label':'Confidence','field':'confidence'},
            {'name':'recommendation','label':'Recommendation','field':'recommendation'},
        ],
        rows=advisor_recommendations()[:10],
        row_key='colony_code',
    ).classes('w-full')
