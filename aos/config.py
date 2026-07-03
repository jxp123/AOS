from pathlib import Path
APP_VERSION='2.0.0'
SCHEMA_VERSION='2.0'
ROOT_DIR=Path(__file__).resolve().parents[1]
DATA_DIR=ROOT_DIR/'data'
DB_PATH=DATA_DIR/'aos.db'
EXPORT_DIR=ROOT_DIR/'exports'
IMPORT_DIR=ROOT_DIR/'imports'
BACKUP_DIR=ROOT_DIR/'backups'
LOG_DIR=ROOT_DIR/'logs'
SNAPSHOT_DIR=ROOT_DIR/'snapshots'
