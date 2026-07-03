from nicegui import ui
from aos.engines.inspection_scheduler import inspection_schedule, scheduler_summary, todays_plan, rolling_plan


def page():
    ui.label('Inspection Scheduler').classes('text-h5')
    ui.label('AOS now calculates inspection due dates automatically. Default active hive/nuc interval: 7 days.').classes('text-subtitle1')

    holder = ui.column().classes('w-full')

    def render():
        holder.clear()
        with holder:
            summary = scheduler_summary()
            with ui.row():
                for label, key in [
                    ('Overdue', 'overdue'),
                    ('Due Today', 'due_today'),
                    ('Due Soon', 'due_soon'),
                    ('No Record', 'no_record'),
                    ('Recent', 'recent'),
                ]:
                    with ui.card():
                        ui.label(label)
                        ui.label(str(summary[key])).classes('text-h5')

            ui.label("Today's Inspection Plan").classes('text-h6')
            ui.table(
                columns=[
                    {'name':'priority','label':'Priority','field':'priority'},
                    {'name':'status','label':'Status','field':'status'},
                    {'name':'code','label':'Colony/Nuc','field':'code'},
                    {'name':'type','label':'Type','field':'type'},
                    {'name':'equipment','label':'Equipment','field':'equipment'},
                    {'name':'last_inspection','label':'Last Inspection','field':'last_inspection'},
                    {'name':'days_since','label':'Days Since','field':'days_since'},
                    {'name':'next_due','label':'Next Due','field':'next_due'},
                    {'name':'strategy','label':'Strategy','field':'strategy'},
                    {'name':'action','label':'Action','field':'action'},
                ],
                rows=todays_plan(),
                row_key='code',
            ).classes('w-full')

            ui.label('All Colonies / Nucs').classes('text-h6')
            ui.table(
                columns=[
                    {'name':'status','label':'Status','field':'status'},
                    {'name':'priority','label':'Priority','field':'priority'},
                    {'name':'code','label':'Code','field':'code'},
                    {'name':'name','label':'Name','field':'name'},
                    {'name':'type','label':'Type','field':'type'},
                    {'name':'equipment','label':'Equipment','field':'equipment'},
                    {'name':'last_inspection','label':'Last Inspection','field':'last_inspection'},
                    {'name':'days_since','label':'Days Since','field':'days_since'},
                    {'name':'next_due','label':'Next Due','field':'next_due'},
                    {'name':'days_until_due','label':'Days Until Due','field':'days_until_due'},
                    {'name':'interval_days','label':'Interval','field':'interval_days'},
                    {'name':'strategy','label':'Strategy','field':'strategy'},
                    {'name':'strategy_reason','label':'Reason','field':'strategy_reason'},
                ],
                rows=inspection_schedule(),
                row_key='code',
            ).classes('w-full')

            ui.label('14-Day Inspection Calendar').classes('text-h6')
            ui.table(
                columns=[
                    {'name':'day','label':'Day','field':'day'},
                    {'name':'date','label':'Date','field':'date'},
                    {'name':'due_count','label':'Due Count','field':'due_count'},
                    {'name':'due_items','label':'Due Colonies / Nucs','field':'due_items'},
                ],
                rows=rolling_plan(14),
                row_key='date',
            ).classes('w-full')

    ui.button('Refresh Inspection Schedule', on_click=render)
    render()
