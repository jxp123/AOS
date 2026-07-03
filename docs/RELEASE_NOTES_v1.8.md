# AOS v1.8 Release Notes — Self-Test + Regression Guard

## Added
- Self-Test tab.
- `Self_Test_AOS.bat`.
- Backend smoke tests.
- UI import tests.
- Repository CRUD method checks.
- Migration check.
- Baseline integrity check.
- Natural language parser check.
- Guided inspection validation check.
- Regression scan for unsupported `readonly=True`.

## Why
AOS is now large enough that every release needs a built-in check before live use.
