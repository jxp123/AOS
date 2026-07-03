from nicegui import ui
from aos.engines.natural_language_parser import parse_inspection_note
from aos.services.repository import Repository
from aos.services.guided_inspection_service import GuidedInspectionService

def natural_language_intake_page():
    ui.label('Natural Language Intake').classes('text-h5')
    ui.label('Type an inspection note. AOS will parse it and stage a guided inspection draft for review.')

    repo = Repository()
    service = GuidedInspectionService()
    entities = repo.list_apiary_entities(True)
    options = {f"{e['code']} — {e['name']} ({e['type']}, {e['equipment']})": e['id'] for e in entities}
    reverse = {e['id']: f"{e['code']} — {e['name']}" for e in entities}

    note = ui.textarea('Inspection note', placeholder='Example: Hive 16 queen seen, eggs present, 6 brood frames, 2 stores, calm, no queen cells.').classes('w-full')
    manual_colony = ui.select(options, label='Optional manual colony/nuc override').classes('w-96')

    result_holder = ui.column().classes('w-full')
    parsed_cache = {'data': None}

    def parse():
        result_holder.clear()
        if not note.value:
            ui.notify('Enter an inspection note first', type='warning')
            return

        parsed = parse_inspection_note(note.value)
        if manual_colony.value:
            parsed['colony_id'] = manual_colony.value
            parsed['colony_code'] = reverse.get(manual_colony.value, '').split(' — ')[0]

        parsed_cache['data'] = parsed

        with result_holder:
            ui.label('Parsed Result').classes('text-h6')
            ui.table(
                columns=[
                    {'name':'field','label':'Field','field':'field'},
                    {'name':'value','label':'Value','field':'value'},
                ],
                rows=[
                    {'field':'Colony/Nuc', 'value': parsed.get('colony_code') or 'Not detected'},
                    {'field':'Date', 'value': parsed.get('inspection_date')},
                    {'field':'Queen seen', 'value': parsed.get('queen_seen')},
                    {'field':'Eggs seen', 'value': parsed.get('eggs_seen')},
                    {'field':'Larvae seen', 'value': parsed.get('larvae_seen')},
                    {'field':'Queen cells', 'value': parsed.get('queen_cells')},
                    {'field':'Brood frames', 'value': parsed.get('brood_frames')},
                    {'field':'Stores frames', 'value': parsed.get('stores_frames')},
                    {'field':'Bee coverage frames', 'value': parsed.get('bee_coverage_frames')},
                    {'field':'Temperament', 'value': parsed.get('temperament')},
                    {'field':'Parser confidence', 'value': parsed.get('parser_confidence')},
                    {'field':'Warnings', 'value': '; '.join(parsed.get('warnings') or [])},
                ],
                row_key='field',
            ).classes('w-full')

    def stage():
        if parsed_cache['data'] is None:
            parse()
        parsed = parsed_cache['data']
        if not parsed:
            ui.notify('Nothing parsed yet', type='warning')
            return
        if not parsed.get('colony_id'):
            ui.notify('Colony/nuc was not detected. Select manual override and parse again.', type='warning')
            return
        try:
            draft_id, validation, confidence = service.stage_draft(parsed)
            ui.notify(f"Draft staged #{draft_id}: {validation['status']} / confidence {confidence['score']}", type='positive' if validation['status'] != 'FAIL' else 'warning')
        except Exception as e:
            ui.notify(str(e), type='negative')

    with ui.row():
        ui.button('Parse Note', on_click=parse)
        ui.button('Stage Parsed Draft', on_click=stage)

    result_holder

    ui.separator()
    ui.label('Guidance').classes('text-h6')
    ui.label('Good notes include: colony/nuc, queen evidence, eggs/larvae, brood frames, stores, bee coverage, temperament, queen cells and action taken.')
