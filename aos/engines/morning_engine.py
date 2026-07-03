from aos.services.repository import Repository
from aos.engines.risk_engine import colony_risk
from aos.engines.decision_engine import recommendation_for_colony
def morning_briefing():
    rows=[]
    for c in Repository().list_apiary_entities(active_only=True):
        risk=colony_risk(c); dec=recommendation_for_colony(c,risk)
        rows.append({'code':c['code'],'risk':risk['risk'],'score':risk['score'],'reason':risk['reason'],'priority':dec['priority'],'recommendation':dec['recommendation'],'confidence':dec['confidence']})
    rows.sort(key=lambda r:r['score'], reverse=True)
    return rows
