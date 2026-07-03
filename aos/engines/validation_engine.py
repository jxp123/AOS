from aos.services.repository import Repository
def validation_summary():
    repo=Repository(); issues=[]; baseline=repo.baseline_integrity()
    for m in baseline['missing_colonies']: issues.append({'severity':'High','item':m['code'],'issue':'Missing baseline colony/nuc'})
    for c in repo.list_colonies():
        if c['code']=='N94' and c['equipment']!='14x12': issues.append({'severity':'Critical','item':'N94','issue':'Nuc 94 must be 14x12'})
        if c['equipment']=='Unknown': issues.append({'severity':'Medium','item':c['code'],'issue':'Equipment type unknown'})
    status='PASS' if not issues else 'FAIL' if any(i['severity']=='Critical' for i in issues) else 'WARN'
    return {'status':status,'message':f'{len(issues)} issue(s)','issues':issues}
