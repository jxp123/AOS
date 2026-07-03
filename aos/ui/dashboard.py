from nicegui import ui
from aos.engines.morning_engine import morning_briefing
def dashboard_page():
    ui.label('Morning Briefing').classes('text-h5')
    ui.table(columns=[{'name':'code','label':'Colony/Nuc','field':'code'},{'name':'priority','label':'Priority','field':'priority'},{'name':'risk','label':'Risk','field':'risk'},{'name':'score','label':'Score','field':'score'},{'name':'recommendation','label':'Recommendation','field':'recommendation'}], rows=morning_briefing(), row_key='code').classes('w-full')
