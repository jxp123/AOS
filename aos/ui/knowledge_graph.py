from nicegui import ui
from aos.services.knowledge_graph_service import KnowledgeGraphService
def page():
    ui.label('Knowledge Graph').classes('text-h5'); kg=KnowledgeGraphService(); holder=ui.column().classes('w-full')
    def seed(): added=kg.seed_graph(); ui.notify(f'Relationships added: {added}',type='positive'); render()
    ui.button('Seed / Refresh Graph',on_click=seed)
    def render():
        holder.clear()
        with holder:
            s=kg.summary()
            with ui.row():
                for k,v in s.items():
                    with ui.card(): ui.label(k.replace('_',' ').title()); ui.label(str(v)).classes('text-h6')
            ui.table(columns=[{'name':'date','label':'Date','field':'date'},{'name':'source','label':'Source','field':'source'},{'name':'relationship','label':'Relationship','field':'relationship'},{'name':'target','label':'Target','field':'target'},{'name':'confidence','label':'Confidence','field':'confidence'},{'name':'evidence','label':'Evidence','field':'evidence'}],rows=kg.relationships(),row_key='id').classes('w-full')
    render()
