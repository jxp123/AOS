from nicegui import ui
from datetime import date
from aos.services.repository import Repository
def weather_page():
    ui.label('Weather / Forage').classes('text-h5')
    repo=Repository()
    d=ui.input('Date', value=str(date.today())).classes('w-48')
    temp=ui.number('Temperature C', value=0, step=0.5).classes('w-48')
    flow=ui.select(['Strong','Medium','Weak','None','Unknown'], label='Forage flow', value='Unknown').classes('w-48')
    suitability=ui.select(['Good','Marginal','Poor','Unknown'], label='Inspection suitability', value='Unknown').classes('w-48')
    notes=ui.textarea('Notes').classes('w-full')
    def save():
        repo.create_weather({'date':d.value,'temperature_c':float(temp.value or 0),'wind':'','rain':'','forage_flow':flow.value,'inspection_suitability':suitability.value,'notes':notes.value or ''})
        ui.notify('Weather/forage observation saved', type='positive')
    ui.button('Save Weather Observation', on_click=save)
    ui.table(columns=[{'name':'date','label':'Date','field':'date'},{'name':'temperature_c','label':'Temp C','field':'temperature_c'},{'name':'forage_flow','label':'Forage','field':'forage_flow'},{'name':'inspection_suitability','label':'Inspection','field':'inspection_suitability'},{'name':'notes','label':'Notes','field':'notes'}], rows=repo.list_weather(), row_key='date').classes('w-full')
