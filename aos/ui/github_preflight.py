from nicegui import ui
from aos.services.github_update_service import GitHubUpdateService

def github_preflight_page():
    ui.label('GitHub Update Preflight').classes('text-h5')
    ui.label('Prepare AOS for safer GitHub-based updates. This does not yet auto-download code.')

    service = GitHubUpdateService()
    settings = service.load_settings()

    with ui.card().classes('w-full'):
        ui.label('GitHub Settings').classes('text-h6')
        repo_url = ui.input('Repository URL', value=settings.get('repository_url', '')).classes('w-full')
        branch = ui.input('Branch', value=settings.get('branch', 'main')).classes('w-64')

        def save():
            service.save_settings(repo_url.value, branch.value)
            ui.notify('GitHub settings saved', type='positive')
            render()

        ui.button('Save GitHub Settings', on_click=save)

    holder = ui.column().classes('w-full')

    def render():
        holder.clear()
        with holder:
            ui.label('Preflight Checks').classes('text-h6')
            ui.table(
                columns=[
                    {'name':'check','label':'Check','field':'check'},
                    {'name':'status','label':'Status','field':'status'},
                    {'name':'detail','label':'Detail','field':'detail'},
                ],
                rows=service.preflight_checks(),
                row_key='check',
            ).classes('w-full')

            ui.label('Future GitHub ZIP URL').classes('text-h6')
            ui.label(service.zip_download_url() or 'Configure a valid GitHub URL first.')

            ui.label('Safe Update Checklist').classes('text-h6')
            for item in service.update_checklist():
                ui.label('• ' + item)

    ui.button('Run GitHub Preflight', on_click=render)
    render()
