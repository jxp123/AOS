from aos.services.repository import Repository

def run_integrity_checks():
    repo = Repository()
    issues = []
    colonies = repo.list_colonies()
    codes = {c['code'] for c in colonies}

    for c in colonies:
        if not c['code']:
            issues.append({'severity':'High','item':'Colony','issue':'Missing code'})
        if c['equipment'] == 'Unknown':
            issues.append({'severity':'Medium','item':c['code'],'issue':'Equipment type is unknown'})
        if c['code'] == 'N94' and c['equipment'] != '14x12':
            issues.append({'severity':'Critical','item':'N94','issue':'Nuc 94 must be 14x12, not National'})

    for q in repo.list_queens():
        if q['current_colony'] and q['current_colony'] not in codes:
            issues.append({'severity':'High','item':q['code'],'issue':f"Queen current colony not found: {q['current_colony']}"})

    return issues

def validation_summary():
    issues = run_integrity_checks()
    if not issues:
        return {'status':'PASS','message':'No validation issues found','issues':[]}
    critical = any(i['severity'] == 'Critical' for i in issues)
    return {'status':'FAIL' if critical else 'WARN','message':f'{len(issues)} validation issue(s) found','issues':issues}
