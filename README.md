# Apiary Operating System — v0.7 Commit + Validation

## This release adds
- Pending commit queue
- Validation gates
- Commit / reject workflow
- Data integrity checks
- Automatic SQLite database backup before commit
- AI export retained
- CRUD for Colonies, Queens and Equipment retained

## How this changes usage
Instead of critical changes going straight into permanent state, they can be staged as pending commits and validated first.

## Run
1. Extract ZIP.
2. Double-click `Start_AOS.bat`.
3. Open `http://127.0.0.1:8000`.

## Note
This is still a local developer build. If you have an older `data/aos.db`, use a clean folder first.
