from nicegui import ui
from aos.engines.operations_engine import todays_work, shift_briefing

def page():
    ui.label("Apiary Operations Centre").classes("text-h5")
    ui.label("Today's work, route, equipment and operational briefing.").classes("text-subtitle1")

    holder = ui.column().classes("w-full")

    def render():
        holder.clear()
        work = todays_work()
        with holder:
            ui.label("Today's Apiary Status").classes("text-h6")
            with ui.row():
                for title, value in [
                    ("Overdue", work["overdue"]),
                    ("Due Today", work["due_today"]),
                    ("Due Soon", work["due_soon"]),
                    ("High Tasks", work["high_tasks"]),
                    ("Estimated Visit", work["estimated_duration"]),
                ]:
                    with ui.card():
                        ui.label(title)
                        ui.label(str(value)).classes("text-h5")

            ui.label("AI Shift Briefing").classes("text-h6")
            with ui.card().classes("w-full"):
                ui.label(shift_briefing()).classes("text-body1")

            ui.label("Inspection Queue").classes("text-h6")
            ui.table(
                columns=[
                    {"name":"priority","label":"Priority","field":"priority"},
                    {"name":"code","label":"Colony/Nuc","field":"code"},
                    {"name":"status","label":"Status","field":"status"},
                    {"name":"days_since","label":"Days Since","field":"days_since"},
                    {"name":"reason","label":"Reason","field":"reason"},
                    {"name":"estimated_minutes","label":"Minutes","field":"estimated_minutes"},
                    {"name":"equipment","label":"Equipment","field":"equipment"},
                ],
                rows=work["inspection_queue"],
                row_key="code",
            ).classes("w-full")

            ui.label("Suggested Route").classes("text-h6")
            ui.label(" → ".join(work["route"]) if work["route"] else "No route required today.")

            ui.label("Equipment Checklist").classes("text-h6")
            if work["equipment_checklist"]:
                for item in work["equipment_checklist"]:
                    ui.checkbox(item)
            else:
                ui.label("No special equipment generated.")

            ui.label("High Priority Tasks").classes("text-h6")
            ui.table(
                columns=[
                    {"name":"priority","label":"Priority","field":"priority"},
                    {"name":"colony_code","label":"Colony/Nuc","field":"colony_code"},
                    {"name":"task_type","label":"Task","field":"task_type"},
                    {"name":"reason","label":"Reason","field":"reason"},
                    {"name":"recommendation","label":"Recommendation","field":"recommendation"},
                    {"name":"estimated_minutes","label":"Minutes","field":"estimated_minutes"},
                ],
                rows=work["high_priority_tasks"],
                row_key="recommendation",
            ).classes("w-full")

    ui.button("Refresh Operations Centre", on_click=render)
    render()
