from nicegui import ui
from aos.engines.morning_engine import morning_briefing
from aos.engines.seasonal_engine import seasonal_tasks
from aos.engines.task_engine import task_summary
from aos.engines.advisor_engine import advisor_summary
from aos.core.settings import APP_VERSION

def dashboard_page():
    ui.label('Morning Briefing').classes('text-h5')
    season = seasonal_tasks()
    tasks = task_summary()
    advisor = advisor_summary()

    with ui.row():
        with ui.card():
            ui.label('AOS Version')
            ui.label(APP_VERSION).classes('text-h5')
        with ui.card():
            ui.label('Season')
            ui.label(season['phase']).classes('text-subtitle1')
        with ui.card():
            ui.label('High Priority Tasks')
            ui.label(str(tasks['high'])).classes('text-h5')
        with ui.card():
            ui.label('Advisor High Priority')
            ui.label(str(advisor['high_priority'])).classes('text-h5')
        with ui.card():
            ui.label('Low Confidence Advice')
            ui.label(str(advisor['low_confidence'])).classes('text-h5')

    ui.label('Seasonal tasks').classes('text-h6')
    with ui.card():
        for t in season['tasks']:
            ui.label('• ' + t)

    ui.label('Operational briefing').classes('text-h6')
    ui.label('Use Guided Inspection for new records: Draft → Validate → Stage → Commit.').classes('text-subtitle2')
    ui.table(
        columns=[
            {'name':'code','label':'Colony/Nuc','field':'code'},
            {'name':'priority','label':'Priority','field':'priority'},
            {'name':'risk','label':'Risk','field':'risk'},
            {'name':'score','label':'Score','field':'score'},
            {'name':'recommendation','label':'Recommendation','field':'recommendation'},
            {'name':'nuc_expansion','label':'Nuc Expansion','field':'nuc_expansion'},
        ],
        rows=morning_briefing(),
        row_key='code',
    ).classes('w-full')
