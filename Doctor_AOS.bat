@echo off
title AOS Doctor
cd /d "%~dp0"

echo ========================================
echo AOS Doctor
echo ========================================
echo.

echo Folder:
cd

echo.
echo Python:
where python
python --version

echo.
echo Required folders:
if exist data (echo data: OK) else (echo data: MISSING)
if exist exports (echo exports: OK) else (echo exports: MISSING)
if exist imports (echo imports: OK) else (echo imports: MISSING)
if exist backups (echo backups: OK) else (echo backups: MISSING)
if exist logs (echo logs: OK) else (echo logs: MISSING)

echo.
echo Database:
if exist data\aos.db (echo data\aos.db: FOUND) else (echo data\aos.db: NOT FOUND - will be created on first run)

echo.
echo Virtual environment:
if exist .venv (echo .venv: FOUND) else (echo .venv: NOT FOUND - run Install_AOS.bat)

echo.
echo Disk space:
dir | find "bytes free"

echo.
echo Doctor check complete.
pause
