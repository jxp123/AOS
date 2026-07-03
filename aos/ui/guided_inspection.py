from nicegui import ui
from datetime import date
from aos.services.repository import Repository
from aos.engines.evidence_engine import evidence_for_colony
from aos.engines.confidence_engine import confidence_from_evidence

def guided_inspection_page():
    ui.label('Guided Inspection').classes('text-h5')
    ui.label('AOS 2.0 foundation: step-based inspection entry with evidence and confidence.')

    repo = Repository()
    entities = repo.list_apiary_entities(True)
    options = {f"{e['code']} — {e['name']} ({e['type']}, {e['equipment']})": e['id'] for e in entities}
    code_lookup = {e['id']: e['code'] for e in entities}

    with ui.card().classes('w-full'):
        colony = ui.select(options, label='1. Select colony / nuc').classes('w-96')
        inspection_date = ui.input('2. Date', value=str(date.today())).classes('w-48')

        ui.label('3. Queen / brood evidence').classes('text-h6')
        queen_seen = ui.checkbox('Queen seen')
        eggs_seen = ui.checkbox('Eggs seen')
        larvae_seen = ui.checkbox('Larvae seen')
        queen_cells = ui.number('Queen cells', value=0, min=0).classes('w-48')

        ui.label('4. Strength').classes('text-h6')
        brood_frames = ui.number('Brood frames', value=0, min=0, step=0.5).classes('w-48')
        stores_frames = ui.number('Stores frames', value=0, min=0, step=0.5).classes('w-48')
        bee_coverage = ui.number('Bee coverage frames', value=0, min=0, step=0.5).classes('w-48')

        ui.label('5. Behaviour / notes').classes('text-h6')
        temperament = ui.select(['Calm','OK','Defensive','Aggressive','Unknown'], label='Temperament', value='Unknown').classes('w-48')
        notes = ui.textarea('Notes').classes('w-full')

        evidence_box = ui.textarea('Generated evidence', value='', readonly=True).classes('w-full')
        confidence_label = ui.label('Confidence: not calculated')

        def preview():
            if not colony.value:
                ui.notify('Select a colony/nuc first', type='warning')
                return
            code = code_lookup[colony.value]
            evidence = evidence_for_colony(code)
            evidence.extend([
                f"Draft queen seen: {'Yes' if queen_seen.value else 'No'}",
                f"Draft eggs seen: {'Yes' if eggs_seen.value else 'No'}",
                f"Draft brood frames: {brood_frames.value}",
                f"Draft bee coverage frames: {bee_coverage.value}",
                f"Draft notes: {notes.value or ''}",
            ])
            confidence = confidence_from_evidence(evidence)
            evidence_box.value = "\n".join(evidence)
            confidence_label.text = f"Confidence: {confidence['score']} / {confidence['band']}"

        def save():
            if not colony.value:
                ui.notify('Select a colony/nuc first', type='warning')
                return
            try:
                repo.create_inspection({
                    'colony_id': colony.value,
                    'date': inspection_date.value,
                    'inspection_type': 'Guided',
                    'queen_seen': bool(queen_seen.value),
                    'eggs_seen': bool(eggs_seen.value),
                    'larvae_seen': bool(larvae_seen.value),
                    'queen_cells': int(queen_cells.value or 0),
                    'brood_frames': float(brood_frames.value or 0),
                    'stores_frames': float(stores_frames.value or 0),
                    'bee_coverage_frames': float(bee_coverage.value or 0),
                    'temperament': temperament.value,
                    'notes': notes.value or '',
                })
                ui.notify('Guided inspection saved', type='positive')
                preview()
            except Exception as e:
                ui.notify(str(e), type='negative')

        with ui.row():
            ui.button('Preview Evidence + Confidence', on_click=preview)
            ui.button('Save Guided Inspection', on_click=save)
