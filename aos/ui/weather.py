from nicegui import ui
from datetime import date
from aos.services.repository import Repository
def page():
    ui.label('Weather / Forage').classes('text-h5'); repo=Repository(); holder=ui.column().classes('w-full')
    with ui.card().classes('w-full'):
        d=ui.input('Date',value=str(date.today())).classes('w-48'); temp=ui.number('Temperature C',value=0,step=0.5).classes('w-48'); wind=ui.input('Wind').classes('w-64'); rain=ui.input('Rain').classes('w-64'); flow=ui.select(['Strong','Medium','Weak','None','Unknown'],label='Forage flow',value='Unknown').classes('w-48'); suitability=ui.select(['Good','Marginal','Poor','Unknown'],label='Inspection suitability',value='Unknown').classes('w-48'); notes=ui.textarea('Notes').classes('w-full')
        def save():
            try: repo.create_weather({'date':d.value,'temperature_c':float(temp.value or 0),'wind':wind.value or '','rain':rain.value or '','forage_flow':flow.value,'inspection_suitability':suitability.value,'notes':notes.value or ''}); ui.notify('Saved',type='positive'); render()
            except Exception as e: ui.notify(str(e),type='negative')
        ui.button('Save Weather',on_click=save)
    def render():
        holder.clear()
        with holder: ui.table(columns=[{'name':'date','label':'Date','field':'date'},{'name':'temperature_c','label':'Temp','field':'temperature_c'},{'name':'wind','label':'Wind','field':'wind'},{'name':'rain','label':'Rain','field':'rain'},{'name':'forage_flow','label':'Forage','field':'forage_flow'},{'name':'inspection_suitability','label':'Inspection','field':'inspection_suitability'},{'name':'notes','label':'Notes','field':'notes'}],rows=repo.list_weather(),row_key='id').classes('w-full')
    render()
