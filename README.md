# AOS v1.3.2 — Installer Safety Release

## Main purpose

This release makes installation and running safer after the disk-space issue.

## Adds / fixes

- Disk space check before install and run.
- Clearer message if C: drive is low on space.
- `Clean_AOS_Cache.bat` to clear pip cache.
- `Doctor_AOS.bat` to check Python, folders, database and disk space.
- Run script creates a backup before starting.
- Installer no longer silently continues after failed package install.
- Previous v1.3.1 fixes retained:
  - Inspection save refreshes log.
  - Weather save refreshes table.
  - Colonies Add/Edit/Delete.
  - Equipment Add/Edit/Delete.
  - Queens Add/Edit/Delete.

## Recommended use

First time:

`Install_AOS.bat`

Daily:

`Run_AOS.bat`

If installation fails:

1. Run `Clean_AOS_Cache.bat`
2. Run `Doctor_AOS.bat`
3. Run `Repair_AOS.bat`
