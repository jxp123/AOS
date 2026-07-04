import json
from datetime import datetime
import pandas as pd
from aos.config import EXPORT_DIR
from aos.services.repository import Repository
from aos.services.guided_inspection_service import GuidedInspectionService
from aos.services.knowledge_graph_service import KnowledgeGraphService
from aos.engines.task_engine import generated_tasks
from aos.engines.advisor_engine import advisor_recommendations
from aos.engines.validation_engine import validation_summary
from aos.engines.operations_engine import todays_work, shift_briefing
from aos.engines.inspection_scheduler import inspection_schedule, scheduler_summary
def export_excel():
    EXPORT_DIR.mkdir(exist_ok=True); repo=Repository(); path=EXPORT_DIR/f"aos_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    with pd.ExcelWriter(path,engine='openpyxl') as writer:
        pd.DataFrame(repo.list_colonies()).to_excel(writer,sheet_name='Colonies',index=False)
        pd.DataFrame(repo.list_queens()).to_excel(writer,sheet_name='Queens',index=False)
        pd.DataFrame(repo.list_equipment()).to_excel(writer,sheet_name='Equipment',index=False)
        pd.DataFrame(repo.list_inspections()).to_excel(writer,sheet_name='Inspections',index=False)
        pd.DataFrame(repo.list_weather()).to_excel(writer,sheet_name='Weather',index=False)
        pd.DataFrame(repo.list_audit()).to_excel(writer,sheet_name='Audit',index=False)
    return path
def export_ai_json():
    EXPORT_DIR.mkdir(exist_ok=True); repo=Repository()
    state={'validation':validation_summary(),'colonies':repo.list_colonies(),'queens':repo.list_queens(),'equipment':repo.list_equipment(),'inspections':repo.list_inspections(),'drafts':GuidedInspectionService().list_drafts(),'tasks':generated_tasks(),'advisor':advisor_recommendations(),'knowledge_graph':KnowledgeGraphService().export_graph()}
    path=EXPORT_DIR/'apiary_state.json'; path.write_text(json.dumps(state,indent=2),encoding='utf-8'); return path
