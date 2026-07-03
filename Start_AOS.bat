
@echo off
title Apiary Operating System v0.6
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found.
    echo Install Python 3.11+ and tick "Add Python to PATH".
    pause
    exit /b 1
)

echo Installing/updating required packages...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo Starting AOS v0.6...
start "" http://127.0.0.1:8000
python main.py

pause
