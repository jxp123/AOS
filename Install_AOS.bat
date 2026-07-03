@echo off
title AOS Installer
cd /d "%~dp0"

echo ========================================
echo Apiary Operating System - Installer
echo ========================================

where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python was not found.
    echo Install Python 3.11+ from https://www.python.org/downloads/
    echo IMPORTANT: tick "Add Python to PATH".
    pause
    exit /b 1
)

if not exist data mkdir data
if not exist exports mkdir exports
if not exist imports mkdir imports
if not exist backups mkdir backups
if not exist logs mkdir logs

if not exist .venv (
    python -m venv .venv
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo Installation complete. Run Run_AOS.bat.
pause
