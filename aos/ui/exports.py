from nicegui import ui
from aos.utils.exporters import export_excel,export_ai_json
from aos.utils.self_test import run_self_tests,summary
def page():
    ui.label('Exports / Self-Test').classes('text-h5'); holder=ui.column().classes('w-full')
    def excel(): path=export_excel(); ui.notify(f'Exported {path}',type='positive')
    def ai(): path=export_ai_json(); ui.notify(f'Exported {path}',type='positive')
    def self_test():
        holder.clear(); rows=run_self_tests(); s=summary(rows)
        with holder:
            ui.label(f"PASS={s['pass']} FAIL={s['fail']} TOTAL={s['total']}")
            ui.table(columns=[{'name':'status','label':'Status','field':'status'},{'name':'test','label':'Test','field':'test'},{'name':'message','label':'Message','field':'message'}],rows=rows,row_key='test').classes('w-full')
    with ui.row(): ui.button('Export Excel',on_click=excel); ui.button('Export AI JSON',on_click=ai); ui.button('Run Self-Test',on_click=self_test)
    self_test()
