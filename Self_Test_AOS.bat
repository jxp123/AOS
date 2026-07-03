@echo off
cd /d "%~dp0"
if not exist .venv call Install_AOS.bat
call .venv\Scripts\activate.bat
python -m aos.utils.self_test
pause
