from datetime import datetime
import pandas as pd
from aos.services.repository import Repository
from aos.core.settings import EXPORT_DIR
def export_excel():
    EXPORT_DIR.mkdir(exist_ok=True); repo=Repository(); path=EXPORT_DIR/f'aos_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        pd.DataFrame(repo.list_colonies()).to_excel(writer,sheet_name='Colonies',index=False)
        pd.DataFrame(repo.list_queens()).to_excel(writer,sheet_name='Queens',index=False)
        pd.DataFrame(repo.list_equipment()).to_excel(writer,sheet_name='Equipment',index=False)
        pd.DataFrame(repo.list_inspections()).to_excel(writer,sheet_name='Inspections',index=False)
        pd.DataFrame(repo.list_genealogy()).to_excel(writer,sheet_name='Genealogy',index=False)
        pd.DataFrame(repo.list_weather()).to_excel(writer,sheet_name='Weather',index=False)
        pd.DataFrame(repo.list_audit()).to_excel(writer,sheet_name='Audit',index=False)
    return path
