from nicegui import ui
from aos.engines.seasonal_engine import seasonal_tasks
def seasonal_page():
    ui.label('Seasonal Planner').classes('text-h5')
    season = seasonal_tasks()
    ui.label(f"Current phase: {season['phase']}")
    with ui.card():
        for task in season['tasks']:
            ui.label('• ' + task)
