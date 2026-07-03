from aos.services.repository import Repository
from aos.engines.risk_engine import colony_risk,nuc_expansion_score
from aos.engines.decision_engine import recommendation_for_colony
def morning_briefing():
    repo=Repository(); latest=repo.latest_inspection_by_colony(); rows=[]
    for c in repo.list_apiary_entities(True):
        risk=colony_risk(c); dec=recommendation_for_colony(c,risk); nuc=nuc_expansion_score(c, latest.get(c['code']))
        rows.append({'code':c['code'],'risk':risk['risk'],'score':risk['score'],'reason':risk['reason'],'priority':dec['priority'],'recommendation':dec['recommendation'],'nuc_expansion':nuc.get('recommendation',''),'confidence':dec['confidence']})
    rows.sort(key=lambda r:r['score'], reverse=True); return rows
