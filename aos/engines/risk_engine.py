def colony_risk(colony):
    score=0; reasons=[]; objective=(colony.get('objective') or '').lower(); notes=(colony.get('notes') or '').lower()
    if 'requeening' in objective: score+=40; reasons.append('requeening context')
    if 'swarm' in notes: score+=20; reasons.append('swarm history')
    if 'brood congestion' in objective or 'brood box full' in notes: score+=20; reasons.append('brood congestion watch')
    if 'recover after brood donation' in objective: score+=15; reasons.append('recovering after brood donation')
    if colony.get('equipment')=='Unknown': score+=10; reasons.append('unknown equipment')
    return {'code':colony.get('code'),'risk':'High' if score>=50 else 'Medium' if score>=25 else 'Low','score':score,'reason':'; '.join(reasons) or 'No major flags'}

def nuc_expansion_score(colony, latest_inspection=None):
    if colony.get('type') != 'Nuc':
        return {'score':0, 'recommendation':'Not a nuc'}
    if colony.get('equipment') == 'Unknown':
        return {'score':10, 'recommendation':'Do not move: equipment unknown'}
    if 'recover after brood donation' in (colony.get('objective') or '').lower():
        return {'score':15, 'recommendation':'Do not move: recovering after brood donation'}
    score = 0
    reasons = []
    if latest_inspection:
        brood = latest_inspection.get('brood_frames') or 0
        bees = latest_inspection.get('bee_coverage_frames') or 0
        if brood >= 5: score += 35; reasons.append('strong brood')
        if bees >= 5: score += 25; reasons.append('good bee coverage')
    if score >= 50:
        rec = 'Review for transfer to hive'
    elif score >= 25:
        rec = 'Review again in 1 week'
    else:
        rec = 'Leave as nuc'
    return {'score':score, 'recommendation':rec, 'reason':'; '.join(reasons) or 'limited evidence'}
