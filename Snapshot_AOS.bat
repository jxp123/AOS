@echo off
title AOS Snapshot
cd /d "%~dp0"

if not exist snapshots mkdir snapshots

for /f "tokens=1-4 delims=/ " %%a in ("%date%") do set D=%%d%%b%%c
for /f "tokens=1-2 delims=: " %%a in ("%time%") do set T=%%a%%b

set SNAP=snapshots\aos_snapshot_%D%_%T%

echo Creating snapshot folder:
echo %SNAP%
mkdir "%SNAP%"

xcopy aos "%SNAP%\aos" /E /I /Y >nul
if exist main.py copy main.py "%SNAP%\main.py" >nul
if exist requirements.txt copy requirements.txt "%SNAP%\requirements.txt" >nul
if exist Install_AOS.bat copy Install_AOS.bat "%SNAP%\Install_AOS.bat" >nul
if exist Run_AOS.bat copy Run_AOS.bat "%SNAP%\Run_AOS.bat" >nul
if exist Repair_AOS.bat copy Repair_AOS.bat "%SNAP%\Repair_AOS.bat" >nul
if exist Backup_AOS.bat copy Backup_AOS.bat "%SNAP%\Backup_AOS.bat" >nul
if exist Self_Test_AOS.bat copy Self_Test_AOS.bat "%SNAP%\Self_Test_AOS.bat" >nul

if exist data\aos.db (
    mkdir "%SNAP%\data"
    copy data\aos.db "%SNAP%\data\aos.db" >nul
)

echo %SNAP% > snapshots\last_snapshot.txt

echo.
echo Snapshot created.
pause
