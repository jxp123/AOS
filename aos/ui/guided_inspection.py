from nicegui import ui
from datetime import date
from aos.services.repository import Repository
from aos.services.guided_inspection_service import GuidedInspectionService

def guided_inspection_page():
    ui.label('Guided Inspection').classes('text-h5')
    ui.label('Draft → Validate → Stage → Commit').classes('text-subtitle1')

    repo = Repository()
    service = GuidedInspectionService()
    entities = repo.list_apiary_entities(True)
    options = {f"{e['code']} — {e['name']} ({e['type']}, {e['equipment']})": e['id'] for e in entities}
    code_lookup = {e['id']: e['code'] for e in entities}

    draft_holder = ui.column().classes('w-full')

    with ui.card().classes('w-full'):
        ui.label('Inspection Draft').classes('text-h6')
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

        evidence_box = ui.textarea('Evidence preview', value='', readonly=True).classes('w-full')
        result_label = ui.label('Validation: not run')

        def payload():
            return {
                'colony_id': colony.value,
                'inspection_date': inspection_date.value,
                'queen_seen': bool(queen_seen.value),
                'eggs_seen': bool(eggs_seen.value),
                'larvae_seen': bool(larvae_seen.value),
                'queen_cells': int(queen_cells.value or 0),
                'brood_frames': float(brood_frames.value or 0),
                'stores_frames': float(stores_frames.value or 0),
                'bee_coverage_frames': float(bee_coverage.value or 0),
                'temperament': temperament.value,
                'notes': notes.value or '',
            }

        def preview():
            if not colony.value:
                ui.notify('Select a colony/nuc first', type='warning')
                return
            data = payload()
            validation = service.validate_payload(data)
            code = code_lookup.get(colony.value, 'Unknown')
            evidence = service.build_evidence(code, data)
            from aos.engines.confidence_engine import confidence_from_evidence
            confidence = confidence_from_evidence(evidence)
            evidence_box.value = "\n".join(evidence)
            result_label.text = f"Validation: {validation['status']} — {validation['message']} | Confidence: {confidence['score']} / {confidence['band']}"

        def stage():
            if not colony.value:
                ui.notify('Select a colony/nuc first', type='warning')
                return
            try:
                draft_id, validation, confidence = service.stage_draft(payload())
                ui.notify(f"Draft staged #{draft_id}: {validation['status']} / confidence {confidence['score']}", type='positive' if validation['status'] != 'FAIL' else 'warning')
                preview()
                render_drafts()
            except Exception as e:
                ui.notify(str(e), type='negative')

        with ui.row():
            ui.button('Preview Validation + Evidence', on_click=preview)
            ui.button('Stage Draft Inspection', on_click=stage)

    def render_drafts():
        draft_holder.clear()
        with draft_holder:
            ui.label('Staged Guided Inspections').classes('text-h6')
            rows = service.list_drafts()
            table = ui.table(
                columns=[
                    {'name':'id','label':'ID','field':'id'},
                    {'name':'created_at','label':'Created','field':'created_at'},
                    {'name':'colony_code','label':'Colony','field':'colony_code'},
                    {'name':'inspection_date','label':'Inspection Date','field':'inspection_date'},
                    {'name':'queen_seen','label':'Queen','field':'queen_seen'},
                    {'name':'eggs_seen','label':'Eggs','field':'eggs_seen'},
                    {'name':'brood_frames','label':'Brood','field':'brood_frames'},
                    {'name':'stores_frames','label':'Stores','field':'stores_frames'},
                    {'name':'bee_coverage_frames','label':'Bees','field':'bee_coverage_frames'},
                    {'name':'confidence','label':'Confidence','field':'confidence'},
                    {'name':'validation_status','label':'Validation','field':'validation_status'},
                    {'name':'status','label':'Status','field':'status'},
                    {'name':'validation_message','label':'Message','field':'validation_message'},
                ],
                rows=rows,
                row_key='id',
                selection='single',
            ).classes('w-full')

            def commit_selected():
                if not table.selected:
                    ui.notify('Select one draft first', type='warning')
                    return
                try:
                    service.commit_draft(table.selected[0]['id'])
                    ui.notify('Draft committed to inspection log', type='positive')
                    render_drafts()
                except Exception as e:
                    ui.notify(str(e), type='negative')

            def reject_selected():
                if not table.selected:
                    ui.notify('Select one draft first', type='warning')
                    return
                try:
                    service.reject_draft(table.selected[0]['id'])
                    ui.notify('Draft rejected', type='positive')
                    render_drafts()
                except Exception as e:
                    ui.notify(str(e), type='negative')

            with ui.row():
                ui.button('Commit Selected Draft', on_click=commit_selected)
                ui.button('Reject Selected Draft', color='red', on_click=reject_selected)
                ui.button('Refresh Drafts', on_click=render_drafts)

    render_drafts()
