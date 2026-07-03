@echo off
title AOS Restore Last Snapshot
cd /d "%~dp0"

if not exist snapshots\last_snapshot.txt (
    echo No last snapshot record found.
    pause
    exit /b 1
)

set /p SNAP=<snapshots\last_snapshot.txt

if not exist "%SNAP%" (
    echo Snapshot folder not found:
    echo %SNAP%
    pause
    exit /b 1
)

echo Restoring from:
echo %SNAP%
echo.
echo This will overwrite application files.
pause

if exist aos rmdir /s /q aos
xcopy "%SNAP%\aos" aos /E /I /Y >nul

if exist "%SNAP%\main.py" copy "%SNAP%\main.py" main.py /Y >nul
if exist "%SNAP%\requirements.txt" copy "%SNAP%\requirements.txt" requirements.txt /Y >nul
if exist "%SNAP%\Install_AOS.bat" copy "%SNAP%\Install_AOS.bat" Install_AOS.bat /Y >nul
if exist "%SNAP%\Run_AOS.bat" copy "%SNAP%\Run_AOS.bat" Run_AOS.bat /Y >nul
if exist "%SNAP%\Repair_AOS.bat" copy "%SNAP%\Repair_AOS.bat" Repair_AOS.bat /Y >nul
if exist "%SNAP%\Backup_AOS.bat" copy "%SNAP%\Backup_AOS.bat" Backup_AOS.bat /Y >nul
if exist "%SNAP%\Self_Test_AOS.bat" copy "%SNAP%\Self_Test_AOS.bat" Self_Test_AOS.bat /Y >nul

if exist "%SNAP%\data\aos.db" (
    if not exist data mkdir data
    copy "%SNAP%\data\aos.db" data\aos.db /Y >nul
)

echo.
echo Restore complete.
pause
