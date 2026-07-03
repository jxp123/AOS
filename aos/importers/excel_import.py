import pandas as pd
from pathlib import Path
from aos.services.repository import Repository

def import_colonies_from_excel(path):
    path = Path(path)
    if not path.exists(): raise FileNotFoundError(str(path))
    df = pd.read_excel(path, sheet_name='Colonies')
    repo = Repository()
    count = 0
    for _, row in df.iterrows():
        code = str(row.get('code', '')).strip()
        if not code or code == 'nan': continue
        repo.audit('IMPORT', 'Colony', code, 'Colony seen in Excel import scaffold')
        count += 1
    return count
