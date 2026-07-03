@echo off
title AOS Cache Cleaner
cd /d "%~dp0"

echo ========================================
echo AOS Cache Cleaner
echo ========================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo Python not found. Nothing to clean through pip.
    pause
    exit /b 1
)

echo Clearing pip cache...
python -m pip cache purge

echo.
echo Done.
echo You can also delete old AOS folders and old .venv folders manually.
pause
