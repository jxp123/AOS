def colony_risk(colony):
    score=0; reasons=[]
    objective=(colony.get('objective') or '').lower(); notes=(colony.get('notes') or '').lower()
    if 'requeening' in objective: score+=40; reasons.append('requeening context')
    if 'swarm' in notes: score+=20; reasons.append('swarm history')
    if 'brood congestion' in objective or 'brood box full' in notes: score+=20; reasons.append('brood congestion watch')
    if 'recover after brood donation' in objective: score+=15; reasons.append('recovering after brood donation')
    if colony.get('equipment') == 'Unknown': score+=10; reasons.append('unknown equipment')
    return {'code':colony.get('code'), 'risk':'High' if score>=50 else 'Medium' if score>=25 else 'Low', 'score':score, 'reason':'; '.join(reasons) or 'No major flags'}
