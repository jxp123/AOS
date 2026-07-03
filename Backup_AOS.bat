@echo off
title AOS Backup
cd /d "%~dp0"
if not exist backups mkdir backups
if not exist data\aos.db (
    echo No database found at data\aos.db
    pause
    exit /b 1
)
copy data\aos.db backups\aos_manual_backup.db >nul
echo Backup created: backups\aos_manual_backup.db
pause
