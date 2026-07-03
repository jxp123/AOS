# AOS v1.3 Release Notes

## Added
- Migration tab
- Safe missing-column checks
- Safe migration runner
- Pre-start database backup
- AI export includes migration status

## Why
Older AOS folders may contain an older `data/aos.db` schema. This release helps detect and safely add missing columns.
