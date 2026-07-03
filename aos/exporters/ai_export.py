import json
from datetime import date
from aos.services.repository import Repository
from aos.engines.morning_engine import morning_briefing
from aos.core.settings import EXPORT_DIR

def export_ai_state():
    EXPORT_DIR.mkdir(exist_ok=True)
    repo = Repository()
    state = {
        'date': str(date.today()),
        'apiary_entities': repo.list_apiary_entities(active_only=True),
        'colonies': repo.list_colonies(),
        'queens': repo.list_queens(),
        'equipment': repo.list_equipment(),
        'genealogy': repo.list_genealogy(),
        'morning_briefing': morning_briefing(),
        'hard_rules': [
            'Never infer equipment type.',
            'Nuc 94 is 14x12, not National.',
            'Validate frame compatibility before recommendations.'
        ]
    }
    path = EXPORT_DIR / 'apiary_state.json'
    path.write_text(json.dumps(state, indent=2), encoding='utf-8')
    return path
