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
    echo.
    echo Please install Python 3.11 or later from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: tick "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo Creating required folders...
if not exist data mkdir data
if not exist exports mkdir exports
if not exist imports mkdir imports
if not exist backups mkdir backups
if not exist logs mkdir logs

echo Creating local virtual environment...
if not exist .venv (
    python -m venv .venv
)

echo Installing packages into local environment...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo Installation complete.
echo.
echo Next: double-click Run_AOS.bat
echo.
pause
