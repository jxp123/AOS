from datetime import date
def seasonal_tasks():
    m=date.today().month
    if m in [4,5,6,7]: return {'phase':'Swarm / expansion season','tasks':['7-day brood inspection discipline','Monitor queen cells','Manage supers and brood congestion','Track new queen introductions']}
    if m in [8,9]: return {'phase':'Late summer / autumn preparation','tasks':['Assess winter strength','Plan varroa treatment','Start feed planning','Reduce weak colonies']}
    if m in [10,11]: return {'phase':'Winter preparation','tasks':['Confirm stores','Insulate as planned','Check entrances and wasps/mice']}
    return {'phase':'Winter / monitoring','tasks':['Minimal disturbance','Check stores externally','Prepare equipment for spring']}
