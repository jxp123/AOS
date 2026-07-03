from datetime import datetime
import shutil
from aos.core.settings import DB_PATH, BACKUP_DIR

def backup_database():
    BACKUP_DIR.mkdir(exist_ok=True)
    if not DB_PATH.exists():
        return None
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    target = BACKUP_DIR / f'aos_backup_{stamp}.db'
    shutil.copy2(DB_PATH, target)
    return target
