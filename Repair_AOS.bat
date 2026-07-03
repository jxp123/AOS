@echo off
title AOS Repair
cd /d "%~dp0"

echo ========================================
echo Apiary Operating System - Repair
echo ========================================
echo.

if not exist backups mkdir backups
if exist data\aos.db (
    for /f "tokens=1-4 delims=/ " %%a in ("%date%") do set TODAY=%%d%%b%%c
    copy data\aos.db backups\aos_repair_backup.db >nul
    echo Database backup created: backups\aos_repair_backup.db
)

if exist .venv (
    echo Removing old virtual environment...
    rmdir /s /q .venv
)

echo Reinstalling...
call Install_AOS.bat
