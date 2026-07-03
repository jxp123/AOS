from datetime import date

def seasonal_tasks():
    m = date.today().month
    if m in [4,5,6,7]:
        phase = 'Swarm / expansion season'
        tasks = ['7-day brood inspection discipline', 'Monitor queen cells', 'Manage supers and brood congestion', 'Track new queen introductions']
    elif m in [8,9]:
        phase = 'Late summer / autumn preparation'
        tasks = ['Assess winter strength', 'Plan varroa treatment', 'Start feed planning', 'Reduce weak colonies']
    elif m in [10,11]:
        phase = 'Winter preparation'
        tasks = ['Confirm stores', 'Insulate as planned', 'Check entrances and wasps/mice']
    else:
        phase = 'Winter / monitoring'
        tasks = ['Minimal disturbance', 'Check stores externally', 'Prepare equipment for spring']
    return {'phase': phase, 'tasks': tasks}
