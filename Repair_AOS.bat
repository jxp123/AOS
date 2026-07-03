@echo off
title AOS Repair
cd /d "%~dp0"
if not exist backups mkdir backups
if exist data\aos.db copy data\aos.db backups\aos_repair_backup.db >nul
if exist .venv rmdir /s /q .venv
call Install_AOS.bat
