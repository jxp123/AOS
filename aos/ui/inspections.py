from nicegui import ui
from datetime import date
from aos.services.repository import Repository
def inspections_page():
    ui.label('Inspections').classes('text-h5')
    repo=Repository()
    entities=repo.list_apiary_entities(True)
    options={f"{e['code']} — {e['name']} ({e['type']}, {e['equipment']})": e['id'] for e in entities}
    sel=ui.select(options,label='Colony / Nuc').classes('w-96')
    d=ui.input('Date',value=str(date.today())).classes('w-48')
    q=ui.checkbox('Queen seen'); eggs=ui.checkbox('Eggs seen')
    notes=ui.textarea('Notes').classes('w-full')
    def save():
        if not sel.value: ui.notify('Select colony/nuc',type='warning'); return
        repo.create_inspection({'colony_id':sel.value,'date':d.value,'inspection_type':'Brood','queen_seen':bool(q.value),'eggs_seen':bool(eggs.value),'larvae_seen':False,'queen_cells':0,'brood_frames':0,'stores_frames':0,'temperament':'Unknown','notes':notes.value or ''})
        ui.notify('Inspection saved',type='positive')
    ui.button('Save Inspection',on_click=save)
    ui.table(columns=[{'name':'date','label':'Date','field':'date'},{'name':'colony','label':'Colony','field':'colony'},{'name':'queen_seen','label':'Queen','field':'queen_seen'},{'name':'eggs_seen','label':'Eggs','field':'eggs_seen'},{'name':'notes','label':'Notes','field':'notes'}], rows=repo.list_inspections(), row_key='date').classes('w-full')
