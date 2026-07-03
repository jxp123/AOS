from nicegui import ui
from datetime import date
from aos.services.repository import Repository

def weather_page():
    ui.label('Weather / Forage').classes('text-h5')
    repo=Repository()
    with ui.card().classes('w-full'):
        ui.label('Add Weather / Forage Observation').classes('text-h6')
        d=ui.input('Date', value=str(date.today())).classes('w-48')
        temp=ui.number('Temperature C', value=0, step=0.5).classes('w-48')
        wind=ui.input('Wind').classes('w-64')
        rain=ui.input('Rain').classes('w-64')
        flow=ui.select(['Strong','Medium','Weak','None','Unknown'], label='Forage flow', value='Unknown').classes('w-48')
        suitability=ui.select(['Good','Marginal','Poor','Unknown'], label='Inspection suitability', value='Unknown').classes('w-48')
        notes=ui.textarea('Notes').classes('w-full')
        def save():
            repo.create_weather({'date':d.value,'temperature_c':float(temp.value or 0),'wind':wind.value or '', 'rain':rain.value or '', 'forage_flow':flow.value, 'inspection_suitability':suitability.value, 'notes':notes.value or ''})
            ui.notify('Weather/forage observation saved', type='positive')
        ui.button('Save Weather Observation', on_click=save)
    ui.table(columns=[{'name':'date','label':'Date','field':'date'},{'name':'temperature_c','label':'Temp C','field':'temperature_c'},{'name':'wind','label':'Wind','field':'wind'},{'name':'rain','label':'Rain','field':'rain'},{'name':'forage_flow','label':'Forage','field':'forage_flow'},{'name':'inspection_suitability','label':'Inspection','field':'inspection_suitability'},{'name':'notes','label':'Notes','field':'notes'}], rows=repo.list_weather(), row_key='date').classes('w-full')
