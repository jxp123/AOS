# Apiary Operating System — v0.6.1

## Fix in this release

The New Inspection dropdown now pulls from one central view:

`Repository.list_apiary_entities()`

The Colonies screen, Morning Briefing, AI Export and New Inspection dropdown all use the same source: the `colonies` table through the repository layer.

## Invariant

If a hive/nuc appears in the New Inspection dropdown, it must exist in the Colonies screen.

## Run

1. Extract ZIP.
2. Double-click `Start_AOS.bat`.
3. Open `http://127.0.0.1:8000`.
