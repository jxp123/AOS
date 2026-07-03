@echo off
title Apiary Operating System
cd /d "%~dp0"

if not exist logs mkdir logs
set LOGFILE=logs\aos_run.log

echo ======================================== > "%LOGFILE%"
echo AOS run started %date% %time% >> "%LOGFILE%"
echo ======================================== >> "%LOGFILE%"

where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python was not found.
    echo Install Python 3.11+ and tick "Add Python to PATH".
    echo See README.md for instructions.
    pause
    exit /b 1
)

if not exist .venv (
    echo Local environment not found.
    echo Running installer first...
    call Install_AOS.bat
)

if not exist data mkdir data
if not exist exports mkdir exports
if not exist imports mkdir imports
if not exist backups mkdir backups

call .venv\Scripts\activate.bat

echo Checking dependencies...
python -m pip show nicegui >nul 2>nul
if errorlevel 1 (
    echo Dependencies missing. Installing...
    python -m pip install -r requirements.txt >> "%LOGFILE%" 2>&1
)

echo Starting AOS...
echo Browser will open at http://127.0.0.1:8000
start "" http://127.0.0.1:8000
python main.py >> "%LOGFILE%" 2>&1

echo.
echo AOS stopped. See logs\aos_run.log if there was an error.
pause
