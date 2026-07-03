@echo off
title AOS Self-Test
cd /d "%~dp0"

echo ========================================
echo Apiary Operating System - Self-Test
echo ========================================
echo.

if not exist .venv (
    echo Local environment not found. Run Install_AOS.bat first.
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat

python -m aos.utils.self_test

echo.
pause
