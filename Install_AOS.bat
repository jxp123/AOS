@echo off
title AOS Installer
cd /d "%~dp0"

echo ========================================
echo Apiary Operating System - Installer
echo ========================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python was not found.
    echo Install Python 3.11+ and tick "Add Python to PATH".
    pause
    exit /b 1
)

echo Checking free disk space...
for /f "tokens=3" %%a in ('dir /-c ^| find "bytes free"') do set FREEBYTES=%%a
echo Free space check completed.
echo If installation fails with "no space left on device", run Clean_AOS_Cache.bat and free disk space.
echo.

if not exist data mkdir data
if not exist exports mkdir exports
if not exist imports mkdir imports
if not exist backups mkdir backups
if not exist logs mkdir logs

if not exist .venv (
    echo Creating local virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Could not create virtual environment.
        pause
        exit /b 1
    )
)

call .venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ERROR: pip upgrade failed.
    echo Try running Clean_AOS_Cache.bat, then Repair_AOS.bat.
    pause
    exit /b 1
)

echo Installing packages...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Package installation failed.
    echo.
    echo Most common cause: not enough disk space.
    echo Run Clean_AOS_Cache.bat and delete old AOS folders / old .venv folders.
    echo Then run Repair_AOS.bat.
    pause
    exit /b 1
)

echo.
echo Installation complete.
echo Next: double-click Run_AOS.bat
pause
