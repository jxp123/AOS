@echo off
title Apiary Operating System
cd /d "%~dp0"

if not exist logs mkdir logs
set LOGFILE=logs\aos_run.log

echo AOS run started %date% %time% > "%LOGFILE%"

where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python was not found.
    pause
    exit /b 1
)

if not exist .venv (
    call Install_AOS.bat
)

if not exist data mkdir data
if not exist exports mkdir exports
if not exist imports mkdir imports
if not exist backups mkdir backups

call .venv\Scripts\activate.bat
python -m pip show nicegui >nul 2>nul
if errorlevel 1 (
    python -m pip install -r requirements.txt >> "%LOGFILE%" 2>&1
)

start "" http://127.0.0.1:8000
python main.py >> "%LOGFILE%" 2>&1

echo AOS stopped. See logs\aos_run.log if there was an error.
pause
