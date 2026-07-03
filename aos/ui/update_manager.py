from nicegui import ui
from aos.services.update_service import UpdateService

def update_manager_page():
    ui.label('Update Manager').classes('text-h5')
    ui.label('Foundation for safer AOS updates. Create a snapshot before replacing files.')

    service = UpdateService()
    holder = ui.column().classes('w-full')

    def render_readiness():
        holder.clear()
        with holder:
            ui.label('Update Readiness').classes('text-h6')
            ui.table(
                columns=[
                    {'name':'check','label':'Check','field':'check'},
                    {'name':'status','label':'Status','field':'status'},
                    {'name':'detail','label':'Detail','field':'detail'},
                ],
                rows=service.update_readiness(),
                row_key='check',
            ).classes('w-full')
            last = service.last_snapshot()
            ui.label(f'Last snapshot: {last or "None"}')

    def snapshot():
        target = service.create_snapshot()
        ui.notify(f'Snapshot created: {target}', type='positive')
        render_readiness()

    def manifest():
        path = service.write_manifest()
        ui.notify(f'Manifest exported: {path}', type='positive')
        render_readiness()

    with ui.row():
        ui.button('Run Update Readiness Check', on_click=render_readiness)
        ui.button('Create Snapshot Now', on_click=snapshot)
        ui.button('Export File Manifest', on_click=manifest)

    ui.separator()
    ui.label('Manual update workflow').classes('text-h6')
    ui.label('1. Create snapshot. 2. Replace files from new release. 3. Run AOS. 4. Run Self-Test. 5. Restore snapshot if broken.')

    render_readiness()
