from nicegui import ui
from aos.core.bootstrap import boot_aos
from aos.ui.dashboard import dashboard_page
from aos.ui.colonies import colonies_page
from aos.ui.queens import queens_page
from aos.ui.equipment import equipment_page
from aos.ui.inspections import inspections_page
from aos.ui.genealogy import genealogy_page
from aos.ui.commit import commit_page
from aos.ui.validation import validation_page
from aos.ui.ai import ai_page

boot_aos()

@ui.page('/')
def index():
    ui.label('🐝 Apiary Operating System').classes('text-h4')
    ui.label('v0.7 Commit + Validation').classes('text-subtitle1')

    with ui.tabs().classes('w-full') as tabs:
        dashboard = ui.tab('Morning Briefing')
        colonies = ui.tab('Colonies')
        queens = ui.tab('Queens')
        equipment = ui.tab('Equipment')
        inspections = ui.tab('Inspections')
        genealogy = ui.tab('Genealogy')
        validation = ui.tab('Validation')
        commit = ui.tab('Commit Queue')
        ai = ui.tab('AI Export')

    with ui.tab_panels(tabs, value=dashboard).classes('w-full'):
        with ui.tab_panel(dashboard): dashboard_page()
        with ui.tab_panel(colonies): colonies_page()
        with ui.tab_panel(queens): queens_page()
        with ui.tab_panel(equipment): equipment_page()
        with ui.tab_panel(inspections): inspections_page()
        with ui.tab_panel(genealogy): genealogy_page()
        with ui.tab_panel(validation): validation_page()
        with ui.tab_panel(commit): commit_page()
        with ui.tab_panel(ai): ai_page()

ui.run(title='AOS', host='127.0.0.1', port=8000)
