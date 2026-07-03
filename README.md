# Apiary Operating System — v1.1 Dummy-Proof Launcher Release

## What this release adds

This release focuses on making AOS easier and safer to run.

New launchers:
- `Install_AOS.bat` — first-time setup
- `Run_AOS.bat` — daily launcher
- `Repair_AOS.bat` — repair dependencies
- `Backup_AOS.bat` — manual database backup
- `Start_AOS.bat` — compatibility launcher that calls `Run_AOS.bat`

New safeguards:
- Uses a local Python virtual environment `.venv`
- Does not install packages globally
- Checks Python is installed
- Creates required folders automatically
- Backs up the database before repair
- Writes startup logs to `logs/`
- Clearer error messages

## First time

Double-click:

`Install_AOS.bat`

Then double-click:

`Run_AOS.bat`

## Normal daily use

Double-click:

`Run_AOS.bat`

## If something breaks

Double-click:

`Repair_AOS.bat`

## Manual backup

Double-click:

`Backup_AOS.bat`
