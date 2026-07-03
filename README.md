# Apiary Operating System — v0.8 Excel Import/Export + Backups

## This release adds
- Excel export of core AOS data
- Excel import scaffold
- Manual backup button
- Backup log
- AI state export retained
- Validation retained
- Commit queue retained

## How to run
1. Extract ZIP.
2. Double-click `Start_AOS.bat`.
3. Browser opens at `http://127.0.0.1:8000`.

## Important
Excel import is intentionally conservative in this release:
- It imports Colonies only from a sheet called `Colonies`.
- It expects columns: code, name, type, equipment, objective, status, notes.
- Export produces a workbook you can edit and later re-import.
