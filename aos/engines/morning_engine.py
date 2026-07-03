
from aos.services.repository import Repository
from aos.engines.risk_engine import colony_risk
from aos.engines.decision_engine import recommendation_for_colony

def morning_briefing():
    repo = Repository()
    colonies = repo.list_colonies()
    rows = []
    for c in colonies:
        risk = colony_risk(c)
        decision = recommendation_for_colony(c, risk)
        rows.append({
            'code': c['code'], 'risk': risk['risk'], 'score': risk['score'],
            'reason': risk['reason'], 'priority': decision['priority'],
            'recommendation': decision['recommendation'], 'confidence': decision['confidence'],
        })
    rows.sort(key=lambda r: r['score'], reverse=True)
    return rows
