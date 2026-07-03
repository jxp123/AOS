from nicegui import ui
from aos.db.migrations import migration_check, apply_safe_migrations

def migrations_page():
    ui.label('Migrations').classes('text-h5')
    holder = ui.column().classes('w-full')
    def render():
        holder.clear()
        rows = migration_check()
        with holder:
            if not rows:
                ui.label('✅ No missing schema items detected.')
            else:
                ui.label('⚠️ Missing schema items detected.')
                ui.table(columns=[
                    {'name':'table','label':'Table','field':'table'},
                    {'name':'column','label':'Column','field':'column'},
                    {'name':'sql','label':'Migration SQL','field':'sql'},
                ], rows=rows, row_key='sql').classes('w-full')
    def apply():
        rows = apply_safe_migrations()
        ui.notify(f'Applied {len(rows)} safe migration(s)', type='positive')
        render()
    with ui.row():
        ui.button('Run Migration Check', on_click=render)
        ui.button('Apply Safe Migrations', on_click=apply)
    render()
