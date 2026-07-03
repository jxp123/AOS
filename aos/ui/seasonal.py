from nicegui import ui
from aos.engines.seasonal_engine import seasonal_tasks
def seasonal_page():
    ui.label('Seasonal Planner').classes('text-h5'); s=seasonal_tasks(); ui.label(f"Current phase: {s['phase']}")
    with ui.card():
        for task in s['tasks']: ui.label('• '+task)
