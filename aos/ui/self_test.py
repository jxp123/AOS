from nicegui import ui
from aos.utils.self_test import run_self_tests, summary

def self_test_page():
    ui.label('Self-Test').classes('text-h5')
    ui.label('Run this after installing a new release to catch broken imports, missing methods, migration issues and known regressions.')

    holder = ui.column().classes('w-full')

    def run():
        holder.clear()
        results = run_self_tests()
        counts = summary(results)
        with holder:
            with ui.row():
                with ui.card():
                    ui.label('PASS')
                    ui.label(str(counts['pass'])).classes('text-h5')
                with ui.card():
                    ui.label('WARN')
                    ui.label(str(counts['warn'])).classes('text-h5')
                with ui.card():
                    ui.label('FAIL')
                    ui.label(str(counts['fail'])).classes('text-h5')
            ui.table(
                columns=[
                    {'name':'status','label':'Status','field':'status'},
                    {'name':'test','label':'Test','field':'test'},
                    {'name':'message','label':'Message','field':'message'},
                ],
                rows=results,
                row_key='test',
            ).classes('w-full')
            if counts['fail']:
                ui.label('❌ Do not rely on this release until failures are fixed.').classes('text-negative')
            else:
                ui.label('✅ No self-test failures detected.').classes('text-positive')

    ui.button('Run Self-Test', on_click=run)
    run()
