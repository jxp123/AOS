@echo off
title AOS 2.0 Installer
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
 echo ERROR: Python was not found. Install Python 3.11+ and tick "Add Python to PATH".
 pause
 exit /b 1
)
if not exist data mkdir data
if not exist exports mkdir exports
if not exist imports mkdir imports
if not exist backups mkdir backups
if not exist logs mkdir logs
if not exist snapshots mkdir snapshots
if not exist .venv python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
 echo ERROR: Could not install packages. Free disk space and try again.
 pause
 exit /b 1
)
echo Installation complete.
pause
