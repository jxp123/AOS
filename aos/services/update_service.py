from pathlib import Path
from datetime import datetime
import hashlib
import json
import shutil

from aos.core.settings import ROOT_DIR, SNAPSHOT_DIR, APP_VERSION, SCHEMA_VERSION, DB_PATH

IGNORED_DIRS = {'.venv', '__pycache__', 'snapshots', 'backups', 'exports', 'logs'}
INCLUDED_SUFFIXES = {'.py', '.bat', '.txt', '.md', '.json'}

class UpdateService:
    def file_hash(self, path):
        h = hashlib.sha256()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                h.update(chunk)
        return h.hexdigest()

    def build_manifest(self):
        files = []
        for p in ROOT_DIR.rglob('*'):
            if not p.is_file():
                continue
            rel = p.relative_to(ROOT_DIR)
            if any(part in IGNORED_DIRS for part in rel.parts):
                continue
            if p.suffix.lower() not in INCLUDED_SUFFIXES and p.name not in ['requirements.txt']:
                continue
            files.append({
                'path': str(rel).replace('\\', '/'),
                'size': p.stat().st_size,
                'sha256': self.file_hash(p),
            })
        files.sort(key=lambda x: x['path'])
        return {
            'generated_at': str(datetime.now().replace(microsecond=0)),
            'app_version': APP_VERSION,
            'schema_version': SCHEMA_VERSION,
            'file_count': len(files),
            'files': files,
        }

    def write_manifest(self):
        target = ROOT_DIR / 'exports' / 'aos_manifest.json'
        target.parent.mkdir(exist_ok=True)
        target.write_text(json.dumps(self.build_manifest(), indent=2), encoding='utf-8')
        return target

    def update_readiness(self):
        checks = []
        checks.append({'check': 'Application version', 'status': 'INFO', 'detail': APP_VERSION})
        checks.append({'check': 'Schema version', 'status': 'INFO', 'detail': SCHEMA_VERSION})
        checks.append({'check': 'Database exists', 'status': 'PASS' if DB_PATH.exists() else 'WARN', 'detail': str(DB_PATH)})
        checks.append({'check': 'Snapshot folder exists', 'status': 'PASS' if SNAPSHOT_DIR.exists() else 'WARN', 'detail': str(SNAPSHOT_DIR)})
        checks.append({'check': 'Manifest can be generated', 'status': 'PASS', 'detail': f"{self.build_manifest()['file_count']} files"})
        return checks

    def create_snapshot(self):
        SNAPSHOT_DIR.mkdir(exist_ok=True)
        stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        target = SNAPSHOT_DIR / f'aos_snapshot_{stamp}'
        target.mkdir(parents=True, exist_ok=True)

        for item in ['aos', 'main.py', 'requirements.txt', 'Install_AOS.bat', 'Run_AOS.bat', 'Repair_AOS.bat', 'Backup_AOS.bat', 'Self_Test_AOS.bat']:
            src = ROOT_DIR / item
            if src.is_dir():
                shutil.copytree(src, target / item, dirs_exist_ok=True)
            elif src.exists():
                shutil.copy2(src, target / item)

        if DB_PATH.exists():
            (target / 'data').mkdir(exist_ok=True)
            shutil.copy2(DB_PATH, target / 'data' / 'aos.db')

        (SNAPSHOT_DIR / 'last_snapshot.txt').write_text(str(target), encoding='utf-8')
        return target

    def last_snapshot(self):
        marker = SNAPSHOT_DIR / 'last_snapshot.txt'
        if not marker.exists():
            return ''
        return marker.read_text(encoding='utf-8').strip()
