from datetime import datetime
import shutil
from aos.core.settings import DB_PATH, BACKUP_DIR
def backup_database():
    BACKUP_DIR.mkdir(exist_ok=True)
    if not DB_PATH.exists(): return None
    target=BACKUP_DIR/f'aos_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
    shutil.copy2(DB_PATH,target); return target
def list_backups():
    BACKUP_DIR.mkdir(exist_ok=True)
    return sorted([p.name for p in BACKUP_DIR.glob('*.db')], reverse=True)
