from datetime import date
from aos.services.repository import Repository
from aos.services.guided_inspection_service import GuidedInspectionService
from aos.engines.risk_engine import colony_risk, nuc_expansion_score
from aos.engines.seasonal_engine import seasonal_tasks

def generated_tasks():
    repo = Repository()
    latest = repo.latest_inspection_by_colony()
    tasks = []

    for colony in repo.list_apiary_entities(True):
        risk = colony_risk(colony)
        if risk['risk'] == 'High':
            tasks.append({
                'date': str(date.today()),
                'colony_code': colony['code'],
                'task_type': 'Risk Review',
                'priority': 'High',
                'status': 'Open',
                'reason': risk['reason'],
                'recommendation': 'Review before disturbing colony. Use evidence and confidence before action.',
                'evidence': colony.get('notes',''),
            })

        if colony.get('type') == 'Nuc':
            nuc = nuc_expansion_score(colony, latest.get(colony['code']))
            if nuc.get('recommendation') == 'Review for transfer to hive':
                tasks.append({
                    'date': str(date.today()),
                    'colony_code': colony['code'],
                    'task_type': 'Nuc Expansion Review',
                    'priority': 'High',
                    'status': 'Open',
                    'reason': 'Nuc may be ready for hive transfer.',
                    'recommendation': 'Check brood, bee coverage, stores and equipment compatibility.',
                    'evidence': nuc.get('reason',''),
                })
            elif 'recovering' in nuc.get('recommendation','').lower():
                tasks.append({
                    'date': str(date.today()),
                    'colony_code': colony['code'],
                    'task_type': 'Recovery Watch',
                    'priority': 'Medium',
                    'status': 'Open',
                    'reason': 'Recovering after brood donation.',
                    'recommendation': 'Avoid unnecessary disturbance.',
                    'evidence': colony.get('notes',''),
                })

        if colony.get('equipment') == 'Unknown':
            tasks.append({
                'date': str(date.today()),
                'colony_code': colony['code'],
                'task_type': 'Data Quality',
                'priority': 'Medium',
                'status': 'Open',
                'reason': 'Equipment type unknown.',
                'recommendation': 'Update colony equipment type before frame-transfer recommendations.',
                'evidence': 'Equipment unknown in colony record.',
            })

    phase = seasonal_tasks()
    for item in phase['tasks']:
        tasks.append({
            'date': str(date.today()),
            'colony_code': '',
            'task_type': 'Seasonal',
            'priority': 'Medium',
            'status': 'Open',
            'reason': phase['phase'],
            'recommendation': item,
            'evidence': 'Generated from seasonal planner.',
        })

    
    for draft in GuidedInspectionService().list_drafts():
        if draft['status'] == 'Staged':
            tasks.append({
                'date': draft['created_at'],
                'colony_code': draft['colony_code'],
                'task_type': 'Commit Staged Inspection',
                'priority': 'High' if draft['validation_status'] == 'PASS' else 'Medium',
                'status': 'Open',
                'reason': f"Draft inspection staged with validation {draft['validation_status']}.",
                'recommendation': 'Review and commit or reject the staged guided inspection.',
                'evidence': draft['validation_message'],
            })

    priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
    tasks.sort(key=lambda t: priority_order.get(t['priority'], 9))
    return tasks

def task_summary():
    tasks = generated_tasks()
    return {
        'total': len(tasks),
        'high': len([t for t in tasks if t['priority'] == 'High']),
        'medium': len([t for t in tasks if t['priority'] == 'Medium']),
        'low': len([t for t in tasks if t['priority'] == 'Low']),
    }
