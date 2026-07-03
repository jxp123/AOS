import json
from datetime import date
from aos.services.repository import Repository
from aos.engines.morning_engine import morning_briefing
from aos.engines.validation_engine import validation_summary
from aos.engines.seasonal_engine import seasonal_tasks
from aos.core.settings import EXPORT_DIR
def export_ai_state():
    EXPORT_DIR.mkdir(exist_ok=True); repo=Repository()
    state={'date':str(date.today()),'validation':validation_summary(),'seasonal':seasonal_tasks(),'apiary_entities':repo.list_apiary_entities(True),'queens':repo.list_queens(),'equipment':repo.list_equipment(),'weather':repo.list_weather(),'genealogy':repo.list_genealogy(),'morning_briefing':morning_briefing(),'hard_rules':['Never infer equipment type','Nuc 94 is 14x12, not National','Validate compatibility before frame transfer recommendations']}
    path=EXPORT_DIR/'apiary_state.json'; path.write_text(json.dumps(state,indent=2),encoding='utf-8'); return path
