def recommendation_for_colony(colony, risk):
    objective = (colony.get('objective') or '').lower()
    if 'requeening after swarm' in objective:
        return {'priority': 'High', 'recommendation': 'Do not disturb; monitor externally unless urgent.', 'confidence': 'High'}
    if 'recover after brood donation' in objective:
        return {'priority': 'Medium', 'recommendation': 'External check only; allow recovery.', 'confidence': 'High'}
    if risk['risk'] == 'High':
        return {'priority': 'High', 'recommendation': 'Review today; validate before opening.', 'confidence': 'Medium'}
    if risk['risk'] == 'Medium':
        return {'priority': 'Medium', 'recommendation': 'Inspect/review if time allows.', 'confidence': 'Medium'}
    return {'priority': 'Low', 'recommendation': 'No immediate action.', 'confidence': 'Medium'}
