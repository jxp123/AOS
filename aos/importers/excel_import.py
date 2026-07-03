import pandas as pd
from pathlib import Path
from aos.services.repository import Repository

def import_colonies_from_excel(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(str(path))
    df = pd.read_excel(path, sheet_name='Colonies')
    repo = Repository()
    count = 0
    for _, row in df.iterrows():
        code = str(row.get('code', '')).strip()
        if not code or code == 'nan':
            continue
        repo.upsert_colony({
            'code': code,
            'name': str(row.get('name', code)).strip(),
            'type': str(row.get('type', 'Hive')).strip(),
            'equipment': str(row.get('equipment', 'Unknown')).strip(),
            'objective': str(row.get('objective', '')).strip(),
            'status': str(row.get('status', 'Active')).strip(),
            'notes': str(row.get('notes', '')).strip(),
        })
        count += 1
    return count
