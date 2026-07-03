@echo off
title AOS Repair
cd /d "%~dp0"

echo ========================================
echo AOS Repair
echo ========================================
echo.

if not exist backups mkdir backups
if exist data\aos.db copy data\aos.db backups\aos_repair_backup.db >nul

if exist .venv (
    echo Removing old virtual environment...
    rmdir /s /q .venv
)

echo Cleaning pip cache...
python -m pip cache purge

echo Reinstalling AOS environment...
call Install_AOS.bat
