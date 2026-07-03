# AOS v1.3.1 — UI + CRUD Fix Release

## Fixes in this release

This release addresses the issues reported in v1.3:

- Inspection save button appeared to do nothing.
- Weather / forage save showed success but did not refresh the table.
- Colonies add/edit/delete disappeared.
- Equipment add/edit/delete disappeared.
- Queens add/edit/delete restored as well.

## What changed

- Inspection table now refreshes after saving.
- Weather table now refreshes after saving.
- Colonies screen has Add / Edit / Delete buttons again.
- Equipment screen has Add / Edit / Delete buttons again.
- Queens screen has Add / Edit / Delete buttons again.
- Repository methods for create/update/delete have been restored.
- Errors now show a visible notification rather than silently failing.

## Recommended after installing

1. Run `Run_AOS.bat`.
2. Open **Migrations** and run **Apply Safe Migrations** if needed.
3. Open **Data Integrity** and run **Restore Missing Baseline Entities** if needed.
4. Test by adding one inspection and one weather record.
