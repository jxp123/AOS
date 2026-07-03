from aos.services.repository import Repository
from aos.engines.risk_engine import colony_risk, nuc_expansion_score
from aos.engines.decision_engine import recommendation_for_colony
from aos.engines.evidence_engine import evidence_for_colony
from aos.engines.confidence_engine import confidence_from_evidence

def advisor_recommendations():
    repo = Repository()
    latest = repo.latest_inspection_by_colony()
    rows = []
    for colony in repo.list_apiary_entities(True):
        risk = colony_risk(colony)
        decision = recommendation_for_colony(colony, risk)
        evidence = evidence_for_colony(colony['code'])
        confidence = confidence_from_evidence(evidence)
        nuc = nuc_expansion_score(colony, latest.get(colony['code']))

        recommendation = decision['recommendation']
        if colony.get('type') == 'Nuc' and nuc.get('recommendation') != 'Not a nuc':
            recommendation = f"{recommendation} Nuc status: {nuc.get('recommendation')}."

        rows.append({
            'colony_code': colony['code'],
            'priority': decision['priority'],
            'risk': risk['risk'],
            'confidence': confidence['score'],
            'confidence_band': confidence['band'],
            'recommendation': recommendation,
            'evidence': " | ".join(evidence),
            'risk_reason': risk['reason'],
        })
    rows.sort(key=lambda r: (r['priority'] != 'High', -r['confidence']))
    return rows

def advisor_summary():
    rows = advisor_recommendations()
    high = [r for r in rows if r['priority'] == 'High']
    low_conf = [r for r in rows if r['confidence'] < 50]
    return {
        'total_recommendations': len(rows),
        'high_priority': len(high),
        'low_confidence': len(low_conf),
        'top_items': rows[:5],
    }
