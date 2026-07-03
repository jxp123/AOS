@echo off
title Configure GitHub Update
cd /d "%~dp0"

if not exist github_settings.json (
    echo Creating github_settings.json...
    echo {> github_settings.json
    echo   "repository_url": "",>> github_settings.json
    echo   "branch": "main",>> github_settings.json
    echo   "update_mode": "manual_preflight",>> github_settings.json
    echo   "notes": "Enter your GitHub repository URL here later.">> github_settings.json
    echo }>> github_settings.json
)

echo Opening github_settings.json in Notepad.
echo Add your repository URL, save, then close Notepad.
notepad github_settings.json
pause
