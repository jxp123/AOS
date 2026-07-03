from nicegui import ui
from aos.engines.advisor_engine import advisor_recommendations,advisor_summary
def page():
    ui.label('Advisor').classes('text-h5'); s=advisor_summary()
    with ui.row():
        for k,v in s.items():
            with ui.card(): ui.label(k.title()); ui.label(str(v)).classes('text-h6')
    ui.table(columns=[{'name':'colony_code','label':'Colony','field':'colony_code'},{'name':'priority','label':'Priority','field':'priority'},{'name':'risk','label':'Risk','field':'risk'},{'name':'confidence','label':'Confidence','field':'confidence'},{'name':'recommendation','label':'Recommendation','field':'recommendation'},{'name':'risk_reason','label':'Reason','field':'risk_reason'}],rows=advisor_recommendations(),row_key='colony_code').classes('w-full')
