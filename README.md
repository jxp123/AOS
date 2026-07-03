# AOS v1.10 — GitHub Update Preflight

## Purpose

This release prepares AOS for safer GitHub-based updating.

It does not automatically pull from GitHub yet. It adds the configuration, checks and workflow needed before automatic update is safe.

## Added

- GitHub Update Preflight tab
- GitHub settings file scaffold
- Repository URL / branch / mode checks
- Local manifest comparison foundation
- Update checklist
- Safer release workflow guidance
- `github_settings.json`
- `Configure_GitHub_Update.bat`
- Self-test includes GitHub update preflight

## Recommended workflow

1. Commit this release to GitHub as your baseline.
2. Open AOS.
3. Go to **GitHub Preflight**.
4. Enter/check your repository details in `github_settings.json`.
5. Use **Update Manager** snapshots before replacing files.

## Next target

v1.11 should add one-click download of a GitHub ZIP release into a staging folder.
