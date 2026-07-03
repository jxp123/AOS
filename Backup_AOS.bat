@echo off
title AOS Backup
cd /d "%~dp0"

if not exist backups mkdir backups

if not exist data\aos.db (
    echo No database found at data\aos.db
    echo Run AOS once first.
    pause
    exit /b 1
)

for /f "tokens=1-4 delims=/ " %%a in ("%date%") do set D=%%d%%b%%c
for /f "tokens=1-2 delims=: " %%a in ("%time%") do set T=%%a%%b

copy data\aos.db backups\aos_manual_backup_%D%_%T%.db >nul

echo Backup created in backups folder.
pause
