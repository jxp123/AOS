from nicegui import ui
from aos.services.repository import Repository
from aos.services.knowledge_graph_service import KnowledgeGraphService

def knowledge_graph_page():
    ui.label('Knowledge Graph').classes('text-h5')
    repo = Repository()
    kg = KnowledgeGraphService()

    with ui.card().classes('w-full'):
        ui.label('Graph Summary').classes('text-h6')
        summary = kg.graph_summary()
        with ui.row():
            for key, value in summary.items():
                with ui.card():
                    ui.label(key.replace('_', ' ').title())
                    ui.label(str(value)).classes('text-h5')

    def seed():
        added = kg.seed_graph_from_existing_data()
        ui.notify(f'Knowledge graph seeded. Relationships added: {added}', type='positive')
        render_relationships()

    ui.button('Seed / Refresh Knowledge Graph From Existing Data', on_click=seed)

    ui.separator()

    ui.label('Colony Timeline').classes('text-h6')
    colonies = repo.list_colonies()
    colony_options = {f"{c['code']} — {c['name']}": c['code'] for c in colonies}
    selected_colony = ui.select(colony_options, label='Select colony/nuc').classes('w-96')
    timeline_holder = ui.column().classes('w-full')

    def show_timeline():
        timeline_holder.clear()
        if not selected_colony.value:
            ui.notify('Select a colony/nuc first', type='warning')
            return
        events = kg.colony_timeline(selected_colony.value)
        with timeline_holder:
            ui.label(f'Timeline for {selected_colony.value}').classes('text-h6')
            ui.table(
                columns=[
                    {'name':'date','label':'Date','field':'date'},
                    {'name':'type','label':'Type','field':'type'},
                    {'name':'title','label':'Title','field':'title'},
                    {'name':'details','label':'Details','field':'details'},
                ],
                rows=events,
                row_key='title',
            ).classes('w-full')

    ui.button('Show Colony Timeline', on_click=show_timeline)
    timeline_holder

    ui.separator()

    ui.label('Queen Lineage').classes('text-h6')
    queens = repo.list_queens()
    queen_options = {f"{q['code']} — {q['name']}": q['code'] for q in queens}
    selected_queen = ui.select(queen_options, label='Select queen').classes('w-96')
    queen_holder = ui.column().classes('w-full')

    def show_queen():
        queen_holder.clear()
        if not selected_queen.value:
            ui.notify('Select a queen first', type='warning')
            return
        rows = kg.queen_lineage(selected_queen.value)
        with queen_holder:
            ui.label(f'Lineage / relationships for {selected_queen.value}').classes('text-h6')
            ui.table(
                columns=[
                    {'name':'date','label':'Date','field':'date'},
                    {'name':'type','label':'Type','field':'type'},
                    {'name':'source','label':'Source','field':'source'},
                    {'name':'relationship','label':'Relationship','field':'relationship'},
                    {'name':'target','label':'Target','field':'target'},
                    {'name':'evidence','label':'Evidence','field':'evidence'},
                ],
                rows=rows,
                row_key='relationship',
            ).classes('w-full')

    ui.button('Show Queen Relationships', on_click=show_queen)
    queen_holder

    ui.separator()

    rel_holder = ui.column().classes('w-full')

    def render_relationships():
        rel_holder.clear()
        with rel_holder:
            ui.label('All Graph Relationships').classes('text-h6')
            ui.table(
                columns=[
                    {'name':'date','label':'Date','field':'date'},
                    {'name':'source','label':'Source','field':'source'},
                    {'name':'relationship','label':'Relationship','field':'relationship'},
                    {'name':'target','label':'Target','field':'target'},
                    {'name':'confidence','label':'Confidence','field':'confidence'},
                    {'name':'evidence','label':'Evidence','field':'evidence'},
                ],
                rows=kg.list_relationships(),
                row_key='id',
            ).classes('w-full')

    render_relationships()
