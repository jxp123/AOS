from nicegui import ui
from datetime import date
from aos.services.repository import Repository
from aos.services.guided_inspection_service import GuidedInspectionService

def page():
    ui.label("Guided Inspection").classes("text-h5")
    repo=Repository(); svc=GuidedInspectionService()
    entities=repo.list_apiary_entities(True)
    options={f"{e['code']} — {e['name']} ({e['type']}, {e['equipment']})":e['id'] for e in entities}
    code_lookup={e['id']:e['code'] for e in entities}
    holder=ui.column().classes("w-full")
    with ui.card().classes("w-full"):
        sel=ui.select(options,label="Colony / Nuc").classes("w-96")
        d=ui.input("Date",value=str(date.today())).classes("w-48")
        q=ui.checkbox("Queen seen"); eggs=ui.checkbox("Eggs seen"); larvae=ui.checkbox("Larvae seen")
        qcells=ui.number("Queen cells",value=0,min=0).classes("w-48")
        brood=ui.number("Brood frames",value=0,min=0,step=0.5).classes("w-48")
        stores=ui.number("Stores frames",value=0,min=0,step=0.5).classes("w-48")
        bees=ui.number("Bee coverage frames",value=0,min=0,step=0.5).classes("w-48")
        temperament=ui.select(["Calm","OK","Defensive","Aggressive","Unknown"],label="Temperament",value="Unknown").classes("w-48")
        notes=ui.textarea("Notes").classes("w-full")
        evidence=ui.textarea("Evidence preview",value="").props("readonly").classes("w-full")
        def payload():
            return {"colony_id":sel.value,"inspection_date":d.value,"queen_seen":bool(q.value),"eggs_seen":bool(eggs.value),"larvae_seen":bool(larvae.value),"queen_cells":int(qcells.value or 0),"brood_frames":float(brood.value or 0),"stores_frames":float(stores.value or 0),"bee_coverage_frames":float(bees.value or 0),"temperament":temperament.value,"notes":notes.value or ""}
        def preview():
            if not sel.value:
                ui.notify("Select colony/nuc",type="warning"); return
            evidence.value="\n".join(svc.build_evidence(code_lookup.get(sel.value,"Unknown"),payload()))
        def stage():
            try:
                draft_id,validation,confidence=svc.stage_draft(payload())
                ui.notify(f"Draft staged #{draft_id}: {validation['status']} / confidence {confidence['score']}",type="positive")
                render()
            except Exception as e: ui.notify(str(e),type="negative")
        with ui.row(): ui.button("Preview",on_click=preview); ui.button("Stage Draft",on_click=stage)
    def render():
        holder.clear()
        with holder:
            table=ui.table(columns=[{"name":"id","label":"ID","field":"id"},{"name":"created_at","label":"Created","field":"created_at"},{"name":"colony_code","label":"Colony","field":"colony_code"},{"name":"inspection_date","label":"Date","field":"inspection_date"},{"name":"confidence","label":"Confidence","field":"confidence"},{"name":"validation_status","label":"Validation","field":"validation_status"},{"name":"status","label":"Status","field":"status"},{"name":"validation_message","label":"Message","field":"validation_message"}],rows=svc.list_drafts(),row_key="id",selection="single").classes("w-full")
            def commit():
                if not table.selected: ui.notify("Select draft",type="warning"); return
                try: svc.commit_draft(table.selected[0]["id"]); ui.notify("Committed",type="positive"); render()
                except Exception as e: ui.notify(str(e),type="negative")
            def reject():
                if not table.selected: ui.notify("Select draft",type="warning"); return
                try: svc.reject_draft(table.selected[0]["id"]); ui.notify("Rejected",type="positive"); render()
                except Exception as e: ui.notify(str(e),type="negative")
            with ui.row(): ui.button("Commit Selected",on_click=commit); ui.button("Reject Selected",color="red",on_click=reject); ui.button("Refresh",on_click=render)
    render()
