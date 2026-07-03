# Apiary Operating System — v0.6.2 CRUD Service Layer

## This release adds
- Add/Edit/Delete Colonies and Nucs through the repository layer
- Add/Edit/Delete Queens through the repository layer
- Add/Edit/Delete Equipment through the repository layer
- Central active apiary entity view retained
- New Inspection dropdown still reads from the same central source
- Audit logging for create/update/delete actions

## Run
1. Extract ZIP.
2. Double-click `Start_AOS.bat`.
3. Open `http://127.0.0.1:8000`.

## Notes
If you have an older `data/aos.db`, this release can create new tables but does not yet run migrations.
For clean testing, use the included empty `data` folder.
