from nicegui import ui
from datetime import date
from aos.services.repository import Repository
def page():
    ui.label('Inspections').classes('text-h5'); repo=Repository(); holder=ui.column().classes('w-full'); entities=repo.list_apiary_entities(True); options={f"{e['code']} — {e['name']} ({e['type']}, {e['equipment']})":e['id'] for e in entities}
    with ui.card().classes('w-full'):
        sel=ui.select(options,label='Colony / Nuc').classes('w-96'); d=ui.input('Date',value=str(date.today())).classes('w-48'); q=ui.checkbox('Queen seen'); eggs=ui.checkbox('Eggs seen'); larvae=ui.checkbox('Larvae seen'); qcells=ui.number('Queen cells',value=0,min=0).classes('w-48'); brood=ui.number('Brood frames',value=0,min=0,step=0.5).classes('w-48'); stores=ui.number('Stores frames',value=0,min=0,step=0.5).classes('w-48'); bees=ui.number('Bee coverage frames',value=0,min=0,step=0.5).classes('w-48'); temperament=ui.select(['Calm','OK','Defensive','Aggressive','Unknown'],label='Temperament',value='Unknown').classes('w-48'); notes=ui.textarea('Notes').classes('w-full')
        def save():
            if not sel.value: ui.notify('Select colony/nuc',type='warning'); return
            try: repo.create_inspection({'colony_id':sel.value,'date':d.value,'inspection_type':'Brood','queen_seen':bool(q.value),'eggs_seen':bool(eggs.value),'larvae_seen':bool(larvae.value),'queen_cells':int(qcells.value or 0),'brood_frames':float(brood.value or 0),'stores_frames':float(stores.value or 0),'bee_coverage_frames':float(bees.value or 0),'temperament':temperament.value,'notes':notes.value or ''}); ui.notify('Inspection saved',type='positive'); render()
            except Exception as e: ui.notify(str(e),type='negative')
        ui.button('Save Inspection',on_click=save)
    def render():
        holder.clear()
        with holder: ui.table(columns=[{'name':'date','label':'Date','field':'date'},{'name':'colony','label':'Colony','field':'colony'},{'name':'inspection_type','label':'Type','field':'inspection_type'},{'name':'queen_seen','label':'Queen','field':'queen_seen'},{'name':'eggs_seen','label':'Eggs','field':'eggs_seen'},{'name':'brood_frames','label':'Brood','field':'brood_frames'},{'name':'stores_frames','label':'Stores','field':'stores_frames'},{'name':'bee_coverage_frames','label':'Bees','field':'bee_coverage_frames'},{'name':'notes','label':'Notes','field':'notes'}],rows=repo.list_inspections(),row_key='id').classes('w-full')
    render()
