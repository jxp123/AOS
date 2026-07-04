from nicegui import ui
from aos.bootstrap import boot_aos
from aos.config import APP_VERSION
from aos.ui import operations, dashboard,colonies,queens,equipment,inspections,guided,natural_language,tasks,advisor,knowledge_graph,weather,validation,exports,system,inspection_scheduler
boot_aos()
@ui.page('/')
def index():
    ui.label('🐝 Apiary Operating System').classes('text-h4'); ui.label(f'v{APP_VERSION} Clean Foundation').classes('text-subtitle1')
    with ui.tabs().classes('w-full') as tabs:
        t_dashboard=ui.tab('Morning Briefing'); t_scheduler=ui.tab('Inspection Scheduler'); t_nl=ui.tab('Natural Language'); t_guided=ui.tab('Guided Inspection'); t_tasks=ui.tab('Tasks'); t_advisor=ui.tab('Advisor'); t_colonies=ui.tab('Colonies'); t_queens=ui.tab('Queens'); t_equipment=ui.tab('Equipment'); t_inspections=ui.tab('Inspections'); t_graph=ui.tab('Knowledge Graph'); t_weather=ui.tab('Weather'); t_validation=ui.tab('Validation'); t_exports=ui.tab('Exports / Self-Test'); t_system=ui.tab('System')
    with ui.tab_panels(tabs,value=t_dashboard).classes('w-full'):
        with ui.tab_panel(t_operations): operations.page()
        with ui.tab_panel(t_dashboard): dashboard.page()
        with ui.tab_panel(t_scheduler): inspection_scheduler.page()
        with ui.tab_panel(t_nl): natural_language.page()
        with ui.tab_panel(t_guided): guided.page()
        with ui.tab_panel(t_tasks): tasks.page()
        with ui.tab_panel(t_advisor): advisor.page()
        with ui.tab_panel(t_colonies): colonies.page()
        with ui.tab_panel(t_queens): queens.page()
        with ui.tab_panel(t_equipment): equipment.page()
        with ui.tab_panel(t_inspections): inspections.page()
        with ui.tab_panel(t_graph): knowledge_graph.page()
        with ui.tab_panel(t_weather): weather.page()
        with ui.tab_panel(t_validation): validation.page()
        with ui.tab_panel(t_exports): exports.page()
        with ui.tab_panel(t_system): system.page()
ui.run(title='AOS',host='127.0.0.1',port=8000,reload=False)
