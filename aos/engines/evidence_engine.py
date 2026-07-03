from aos.services.repository import Repository

def evidence_for_colony(colony_code):
    repo = Repository()
    latest = repo.latest_inspection_by_colony().get(colony_code)
    colonies = {c['code']: c for c in repo.list_colonies()}
    colony = colonies.get(colony_code)
    evidence = []

    if colony:
        evidence.append(f"Entity: {colony['code']} / {colony['type']} / {colony['equipment']}")
        if colony.get('objective'):
            evidence.append(f"Objective: {colony['objective']}")
        if colony.get('notes'):
            evidence.append(f"Colony notes: {colony['notes']}")

    if latest:
        evidence.append(f"Latest inspection date: {latest.get('date')}")
        evidence.append(f"Queen seen: {latest.get('queen_seen')}")
        evidence.append(f"Eggs seen: {latest.get('eggs_seen')}")
        evidence.append(f"Brood frames: {latest.get('brood_frames')}")
        evidence.append(f"Stores frames: {latest.get('stores_frames')}")
        evidence.append(f"Bee coverage frames: {latest.get('bee_coverage_frames')}")
        if latest.get('notes'):
            evidence.append(f"Inspection notes: {latest.get('notes')}")
    else:
        evidence.append("No inspection record found in AOS.")

    for q in repo.list_queens():
        if q.get('current_colony') == colony_code:
            evidence.append(f"Queen linked: {q['code']} / {q.get('line')} / {q.get('status')}")
    return evidence
