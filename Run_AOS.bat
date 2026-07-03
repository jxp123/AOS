@echo off
title Apiary Operating System
cd /d "%~dp0"

if not exist logs mkdir logs
if not exist backups mkdir backups
set LOGFILE=logs\aos_run.log
echo AOS run started %date% %time% > "%LOGFILE%"
echo Tip: run Snapshot_AOS.bat before applying a new release.

where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python was not found.
    echo Install Python 3.11+ and tick "Add Python to PATH".
    pause
    exit /b 1
)

if not exist .venv (
    echo Local environment not found. Running installer first...
    call Install_AOS.bat
    if errorlevel 1 (
        echo ERROR: Install failed. AOS cannot start.
        pause
        exit /b 1
    )
)

if exist data\aos.db (
    copy data\aos.db backups\aos_pre_start_backup.db >nul
)

call .venv\Scripts\activate.bat

python -m pip show nicegui >nul 2>nul
if errorlevel 1 (
    echo Dependencies missing. Installing...
    python -m pip install -r requirements.txt >> "%LOGFILE%" 2>&1
    if errorlevel 1 (
        echo ERROR: Dependency installation failed.
        echo Check logs\aos_run.log
        echo Try Clean_AOS_Cache.bat and Repair_AOS.bat
        pause
        exit /b 1
    )
)

echo Starting AOS...
start "" http://127.0.0.1:8000
python main.py >> "%LOGFILE%" 2>&1

echo.
echo AOS stopped. See logs\aos_run.log if there was an error.
pause
