
from pathlib import Path

APP_VERSION = '0.6.0'
ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / 'data'
DB_PATH = DATA_DIR / 'aos.db'
EXPORT_DIR = ROOT_DIR / 'exports'
BACKUP_DIR = ROOT_DIR / 'backups'
