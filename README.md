# AOS v1.9 — Update Manager Foundation

## Purpose

This release makes future updates safer and easier.

## Added

- **Update Manager** tab
- `Snapshot_AOS.bat`
- `Restore_Last_Snapshot.bat`
- local installation snapshot creation
- file manifest export
- version manifest export
- update readiness checklist
- GitHub baseline guidance
- self-test retained

## Why this matters

Before we move toward AOS 2.0, we need a safer update process.

This release does **not** yet automatically pull from GitHub. It prepares the structure:
- snapshot before update
- manifest before update
- self-test after update
- restore if broken

## Recommended workflow

Before replacing files with a new release:

1. Run `Snapshot_AOS.bat`
2. Replace files
3. Run `Run_AOS.bat`
4. Open **Self-Test**
5. If broken, run `Restore_Last_Snapshot.bat`

## GitHub recommendation

Commit this whole release as:

`AOS v1.9 update-manager baseline`
