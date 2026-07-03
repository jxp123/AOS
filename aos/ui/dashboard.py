from nicegui import ui
from aos.engines.morning_engine import morning_briefing
from aos.engines.seasonal_engine import seasonal_tasks
from aos.core.settings import APP_VERSION
def dashboard_page():
    ui.label('Morning Briefing').classes('text-h5'); season=seasonal_tasks()
    with ui.card(): ui.label(f'AOS version: {APP_VERSION}'); ui.label(f"Seasonal phase: {season['phase']}")
    ui.table(columns=[{'name':'code','label':'Colony/Nuc','field':'code'},{'name':'priority','label':'Priority','field':'priority'},{'name':'risk','label':'Risk','field':'risk'},{'name':'score','label':'Score','field':'score'},{'name':'recommendation','label':'Recommendation','field':'recommendation'},{'name':'nuc_expansion','label':'Nuc Expansion','field':'nuc_expansion'}], rows=morning_briefing(), row_key='code').classes('w-full')
