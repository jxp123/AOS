from datetime import date
from aos.services.repository import Repository
from aos.services.guided_inspection_service import GuidedInspectionService
from aos.engines.risk_engine import colony_risk,nuc_expansion_score
def generated_tasks():
    repo=Repository(); latest=repo.latest_inspection_by_colony(); tasks=[]
    for c in repo.list_apiary_entities(True):
        risk=colony_risk(c)
        if risk['risk']=='High': tasks.append({'date':str(date.today()),'priority':'High','colony_code':c['code'],'task_type':'Risk Review','reason':risk['reason'],'recommendation':'Review before opening.','evidence':c.get('notes','')})
        if c.get('type')=='Nuc':
            nuc=nuc_expansion_score(c,latest.get(c['code']))
            if nuc['recommendation']=='Review for transfer to hive': tasks.append({'date':str(date.today()),'priority':'High','colony_code':c['code'],'task_type':'Nuc Expansion','reason':'Nuc may be ready.','recommendation':'Check before transfer.','evidence':''})
        if c.get('equipment')=='Unknown': tasks.append({'date':str(date.today()),'priority':'Medium','colony_code':c['code'],'task_type':'Data Quality','reason':'Equipment unknown.','recommendation':'Update equipment type.','evidence':''})
    for d in GuidedInspectionService().list_drafts():
        if d['status']=='Staged': tasks.append({'date':d['created_at'],'priority':'High' if d['validation_status']=='PASS' else 'Medium','colony_code':d['colony_code'],'task_type':'Commit Staged Inspection','reason':d['validation_message'],'recommendation':'Commit or reject staged draft.','evidence':d['evidence']})
    order={'High':0,'Medium':1,'Low':2}; tasks.sort(key=lambda x:order.get(x['priority'],9)); return tasks
def task_summary():
    tasks=generated_tasks(); return {'total':len(tasks),'high':len([t for t in tasks if t['priority']=='High']),'medium':len([t for t in tasks if t['priority']=='Medium'])}
