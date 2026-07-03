@echo off
title Apiary Operating System
cd /d "%~dp0"
if not exist logs mkdir logs
if not exist backups mkdir backups
set LOGFILE=logs\aos_run.log
echo AOS run started %date% %time% > "%LOGFILE%"

where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python was not found.
    pause
    exit /b 1
)

if not exist .venv call Install_AOS.bat

if exist data\aos.db (
    copy data\aos.db backups\aos_pre_start_backup.db >nul
    echo Pre-start database backup created: backups\aos_pre_start_backup.db
)

call .venv\Scripts\activate.bat
python -m pip show nicegui >nul 2>nul
if errorlevel 1 python -m pip install -r requirements.txt >> "%LOGFILE%" 2>&1

start "" http://127.0.0.1:8000
python main.py >> "%LOGFILE%" 2>&1
echo AOS stopped. See logs\aos_run.log if there was an error.
pause
