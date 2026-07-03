from nicegui import ui
from aos.engines.advisor_engine import advisor_recommendations, advisor_summary

def ai_advisor_page():
    ui.label('AI Advisor').classes('text-h5')
    ui.label('Evidence-based advisor scaffold. This is deterministic for now; future versions can connect to an LLM.')

    summary = advisor_summary()
    with ui.row():
        with ui.card():
            ui.label('Total')
            ui.label(str(summary['total_recommendations'])).classes('text-h5')
        with ui.card():
            ui.label('High Priority')
            ui.label(str(summary['high_priority'])).classes('text-h5')
        with ui.card():
            ui.label('Low Confidence')
            ui.label(str(summary['low_confidence'])).classes('text-h5')

    ui.table(
        columns=[
            {'name':'colony_code','label':'Colony/Nuc','field':'colony_code'},
            {'name':'priority','label':'Priority','field':'priority'},
            {'name':'risk','label':'Risk','field':'risk'},
            {'name':'confidence','label':'Confidence','field':'confidence'},
            {'name':'confidence_band','label':'Band','field':'confidence_band'},
            {'name':'recommendation','label':'Recommendation','field':'recommendation'},
            {'name':'risk_reason','label':'Risk Reason','field':'risk_reason'},
            {'name':'evidence','label':'Evidence','field':'evidence'},
        ],
        rows=advisor_recommendations(),
        row_key='colony_code',
    ).classes('w-full')
