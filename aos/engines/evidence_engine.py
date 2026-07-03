from aos.services.repository import Repository
def evidence_for_colony(colony_code):
    repo=Repository(); latest=repo.latest_inspection_by_colony().get(colony_code); colonies={c['code']:c for c in repo.list_colonies()}; colony=colonies.get(colony_code); evidence=[]
    if colony: evidence += [f"Entity: {colony['code']} / {colony['type']} / {colony['equipment']}",f"Objective: {colony.get('objective','')}",f"Colony notes: {colony.get('notes','')}"]
    if latest: evidence += [f"Latest inspection date: {latest.get('date')}",f"Queen seen: {latest.get('queen_seen')}",f"Eggs seen: {latest.get('eggs_seen')}",f"Brood frames: {latest.get('brood_frames')}",f"Stores frames: {latest.get('stores_frames')}",f"Bee coverage frames: {latest.get('bee_coverage_frames')}"]
    else: evidence.append('No inspection record found in AOS.')
    for q in repo.list_queens():
        if q.get('current_colony')==colony_code: evidence.append(f"Queen linked: {q['code']} / {q.get('line')} / {q.get('status')}")
    return evidence
