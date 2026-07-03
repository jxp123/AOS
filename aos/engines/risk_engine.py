def colony_risk(colony):
    score=0; reasons=[]; objective=(colony.get('objective') or '').lower(); notes=(colony.get('notes') or '').lower()
    if 'requeening' in objective: score+=40; reasons.append('requeening context')
    if 'swarm' in notes: score+=20; reasons.append('swarm history')
    if 'brood congestion' in objective or 'brood box full' in notes: score+=20; reasons.append('brood congestion watch')
    if 'recover after brood donation' in objective: score+=15; reasons.append('recovering after brood donation')
    if colony.get('equipment')=='Unknown': score+=10; reasons.append('unknown equipment')
    return {'risk':'High' if score>=50 else 'Medium' if score>=25 else 'Low','score':score,'reason':'; '.join(reasons) or 'No major flags'}
def nuc_expansion_score(colony,latest=None):
    if colony.get('type')!='Nuc': return {'score':0,'recommendation':'Not a nuc'}
    if colony.get('equipment')=='Unknown': return {'score':10,'recommendation':'Do not move: equipment unknown'}
    if 'recover after brood donation' in (colony.get('objective') or '').lower(): return {'score':15,'recommendation':'Do not move: recovering after brood donation'}
    score=0
    if latest:
        if (latest.get('brood_frames') or 0)>=5: score+=35
        if (latest.get('bee_coverage_frames') or 0)>=5: score+=25
    return {'score':score,'recommendation':'Review for transfer to hive' if score>=50 else 'Review again in 1 week' if score>=25 else 'Leave as nuc'}
