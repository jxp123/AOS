from nicegui import ui
from aos.core.bootstrap import boot_aos
from aos.core.settings import APP_VERSION
from aos.ui.dashboard import dashboard_page
from aos.ui.colonies import colonies_page
from aos.ui.queens import queens_page
from aos.ui.equipment import equipment_page
from aos.ui.inspections import inspections_page
from aos.ui.guided_inspection import guided_inspection_page
from aos.ui.natural_language_intake import natural_language_intake_page
from aos.ui.genealogy import genealogy_page
from aos.ui.knowledge_graph import knowledge_graph_page
from aos.ui.weather import weather_page
from aos.ui.seasonal import seasonal_page
from aos.ui.validation import validation_page
from aos.ui.tasks import tasks_page
from aos.ui.ai_advisor import ai_advisor_page
from aos.ui.data_integrity import data_integrity_page
from aos.ui.migrations import migrations_page
from aos.ui.commit import commit_page
from aos.ui.import_export import import_export_page
from aos.ui.ai import ai_page
from aos.ui.system import system_page

boot_aos()

@ui.page('/')
def index():
    ui.label('🐝 Apiary Operating System').classes('text-h4')
    ui.label(f'v{APP_VERSION} Migration-Safe Update').classes('text-subtitle1')

    with ui.tabs().classes('w-full') as tabs:
        dashboard = ui.tab('Morning Briefing')
        colonies = ui.tab('Colonies')
        queens = ui.tab('Queens')
        equipment = ui.tab('Equipment')
        natural_language = ui.tab('Natural Language Intake')
        guided_inspection = ui.tab('Guided Inspection')
        inspections = ui.tab('Inspections')
        genealogy = ui.tab('Genealogy')
        knowledge_graph = ui.tab('Knowledge Graph')
        weather = ui.tab('Weather / Forage')
        seasonal = ui.tab('Seasonal Planner')
        tasks = ui.tab('Tasks')
        ai_advisor = ui.tab('AI Advisor')
        validation = ui.tab('Validation')
        integrity = ui.tab('Data Integrity')
        migrations = ui.tab('Migrations')
        commit = ui.tab('Commit Queue')
        io = ui.tab('Import / Export')
        ai = ui.tab('AI Export')
        system = ui.tab('System')

    with ui.tab_panels(tabs, value=dashboard).classes('w-full'):
        with ui.tab_panel(dashboard): dashboard_page()
        with ui.tab_panel(colonies): colonies_page()
        with ui.tab_panel(queens): queens_page()
        with ui.tab_panel(equipment): equipment_page()
        with ui.tab_panel(natural_language): natural_language_intake_page()
        with ui.tab_panel(guided_inspection): guided_inspection_page()
        with ui.tab_panel(inspections): inspections_page()
        with ui.tab_panel(genealogy): genealogy_page()
        with ui.tab_panel(knowledge_graph): knowledge_graph_page()
        with ui.tab_panel(weather): weather_page()
        with ui.tab_panel(seasonal): seasonal_page()
        with ui.tab_panel(tasks): tasks_page()
        with ui.tab_panel(ai_advisor): ai_advisor_page()
        with ui.tab_panel(validation): validation_page()
        with ui.tab_panel(integrity): data_integrity_page()
        with ui.tab_panel(migrations): migrations_page()
        with ui.tab_panel(commit): commit_page()
        with ui.tab_panel(io): import_export_page()
        with ui.tab_panel(ai): ai_page()
        with ui.tab_panel(system): system_page()

ui.run(title='AOS', host='127.0.0.1', port=8000, reload=False)
