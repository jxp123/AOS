# Apiary Operating System — v1.0 Stable Local Release

AOS is a local browser-based apiary management application.

## v1.0 focus
This release consolidates the earlier prototypes into a more stable local build:
- One central repository layer
- Stable core tables
- Dashboard / Morning Briefing
- Colonies and Nucs
- Queens
- Equipment
- Inspections
- Genealogy
- Weather / Forage
- Seasonal Planner
- Validation
- Commit Queue
- Excel Export
- AI State Export
- Manual Backups
- Basic data quality checks

## Run
1. Extract the ZIP.
2. Double-click `Start_AOS.bat`.
3. Browser opens at `http://127.0.0.1:8000`.

## First-run note
A local SQLite database will be created in:

`data/aos.db`

This database is your local source of truth.

## Important
This is a stable local foundation, not the final commercial-grade product.
Next work should focus on:
- database migrations,
- stronger editing forms,
- test automation,
- migration from your real Excel/workbook history,
- richer rule/decision engine.
