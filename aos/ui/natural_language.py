from nicegui import ui
from aos.engines.natural_language_parser import parse_inspection_note
from aos.services.repository import Repository
from aos.services.guided_inspection_service import GuidedInspectionService
def page():
    ui.label('Natural Language Intake').classes('text-h5'); repo=Repository(); svc=GuidedInspectionService(); entities=repo.list_apiary_entities(True); options={f"{e['code']} — {e['name']} ({e['type']}, {e['equipment']})":e['id'] for e in entities}; reverse={e['id']:e['code'] for e in entities}; note=ui.textarea('Inspection note',placeholder='Hive 16 queen seen, eggs present, 6 brood frames, 2 stores, calm, no queen cells.').classes('w-full'); manual=ui.select(options,label='Manual colony/nuc override').classes('w-96'); holder=ui.column().classes('w-full'); cache={'parsed':None}
    def parse():
        holder.clear(); parsed=parse_inspection_note(note.value or '')
        if manual.value: parsed['colony_id']=manual.value; parsed['colony_code']=reverse.get(manual.value,'')
        cache['parsed']=parsed
        with holder: ui.table(columns=[{'name':'field','label':'Field','field':'field'},{'name':'value','label':'Value','field':'value'}],rows=[{'field':k,'value':str(v)} for k,v in parsed.items() if k!='notes'],row_key='field').classes('w-full')
    def stage():
        if cache['parsed'] is None: parse()
        parsed=cache['parsed']
        if not parsed.get('colony_id'): ui.notify('No colony/nuc detected. Use manual override.',type='warning'); return
        try: draft_id,validation,confidence=svc.stage_draft(parsed); ui.notify(f"Draft staged #{draft_id}: {validation['status']} / confidence {confidence['score']}",type='positive')
        except Exception as e: ui.notify(str(e),type='negative')
    with ui.row(): ui.button('Parse Note',on_click=parse); ui.button('Stage Parsed Draft',on_click=stage)
