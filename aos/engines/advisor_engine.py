from aos.services.repository import Repository
from aos.engines.risk_engine import colony_risk,nuc_expansion_score
from aos.engines.evidence_engine import evidence_for_colony
from aos.engines.confidence_engine import confidence_from_evidence
def advisor_recommendations():
    repo=Repository(); latest=repo.latest_inspection_by_colony(); rows=[]
    for c in repo.list_apiary_entities(True):
        risk=colony_risk(c); evidence=evidence_for_colony(c['code']); confidence=confidence_from_evidence(evidence); nuc=nuc_expansion_score(c,latest.get(c['code']))
        rec='No immediate action.'
        if risk['risk']=='High': rec='Review before disturbing colony.'
        elif risk['risk']=='Medium': rec='Inspect/review if time allows.'
        if c.get('type')=='Nuc': rec+=f" Nuc status: {nuc['recommendation']}."
        rows.append({'colony_code':c['code'],'priority':'High' if risk['risk']=='High' else 'Medium' if risk['risk']=='Medium' else 'Low','risk':risk['risk'],'confidence':confidence['score'],'confidence_band':confidence['band'],'recommendation':rec,'risk_reason':risk['reason'],'evidence':' | '.join(evidence)})
    rows.sort(key=lambda r:(r['priority']!='High',-r['confidence'])); return rows
def advisor_summary():
    rows=advisor_recommendations(); return {'total':len(rows),'high':len([r for r in rows if r['priority']=='High']),'low_confidence':len([r for r in rows if r['confidence']<50])}
