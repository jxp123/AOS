@echo off
cd /d "%~dp0"
if not exist backups mkdir backups
if exist data\aos.db copy data\aos.db backups\aos_manual_backup.db >nul
echo Backup created.
pause
