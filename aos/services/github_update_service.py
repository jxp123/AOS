import json
from pathlib import Path
from urllib.parse import urlparse
from aos.core.settings import ROOT_DIR
from aos.services.update_service import UpdateService

SETTINGS_PATH = ROOT_DIR / 'github_settings.json'

class GitHubUpdateService:
    def load_settings(self):
        if not SETTINGS_PATH.exists():
            return {
                'repository_url': '',
                'branch': 'main',
                'update_mode': 'manual_preflight',
                'notes': 'github_settings.json missing',
            }
        try:
            return json.loads(SETTINGS_PATH.read_text(encoding='utf-8'))
        except Exception as e:
            return {
                'repository_url': '',
                'branch': 'main',
                'update_mode': 'error',
                'notes': f'Could not read github_settings.json: {e}',
            }

    def save_settings(self, repository_url, branch='main'):
        data = {
            'repository_url': repository_url or '',
            'branch': branch or 'main',
            'update_mode': 'manual_preflight',
            'notes': 'Configured from AOS GitHub Preflight tab',
        }
        SETTINGS_PATH.write_text(json.dumps(data, indent=2), encoding='utf-8')
        return data

    def validate_repository_url(self, url):
        if not url:
            return {'status': 'WARN', 'message': 'Repository URL not configured.'}
        parsed = urlparse(url)
        if parsed.scheme not in ['http', 'https']:
            return {'status': 'FAIL', 'message': 'Repository URL must start with https://'}
        if 'github.com' not in parsed.netloc.lower():
            return {'status': 'FAIL', 'message': 'Repository URL should be a GitHub URL.'}
        parts = [p for p in parsed.path.split('/') if p]
        if len(parts) < 2:
            return {'status': 'FAIL', 'message': 'Repository URL should include owner and repository name.'}
        return {'status': 'PASS', 'message': f'GitHub repository detected: {parts[0]}/{parts[1]}'}

    def zip_download_url(self):
        settings = self.load_settings()
        url = settings.get('repository_url', '').rstrip('/')
        branch = settings.get('branch', 'main') or 'main'
        validation = self.validate_repository_url(url)
        if validation['status'] != 'PASS':
            return ''
        return f'{url}/archive/refs/heads/{branch}.zip'

    def preflight_checks(self):
        settings = self.load_settings()
        repo_url = settings.get('repository_url', '')
        branch = settings.get('branch', 'main')
        validation = self.validate_repository_url(repo_url)
        manifest = UpdateService().build_manifest()

        checks = [
            {'check': 'github_settings.json exists', 'status': 'PASS' if SETTINGS_PATH.exists() else 'WARN', 'detail': str(SETTINGS_PATH)},
            {'check': 'Repository URL', 'status': validation['status'], 'detail': validation['message']},
            {'check': 'Branch configured', 'status': 'PASS' if branch else 'WARN', 'detail': branch or 'No branch configured'},
            {'check': 'Local manifest available', 'status': 'PASS' if manifest.get('file_count', 0) > 0 else 'FAIL', 'detail': f"{manifest.get('file_count', 0)} files"},
            {'check': 'Download ZIP URL can be formed', 'status': 'PASS' if self.zip_download_url() else 'WARN', 'detail': self.zip_download_url() or 'Not available until repository URL is valid'},
            {'check': 'Update mode', 'status': 'INFO', 'detail': settings.get('update_mode', 'manual_preflight')},
        ]
        return checks

    def update_checklist(self):
        return [
            'Create snapshot using Update Manager.',
            'Export file manifest.',
            'Commit current working version to GitHub.',
            'Download/replace files only after snapshot exists.',
            'Run migrations.',
            'Run data integrity check.',
            'Run self-test.',
            'Restore snapshot if self-test fails.',
        ]
