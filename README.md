# AOS v1.8 — Self-Test + Regression Guard

## Purpose

This release adds a built-in health check so we can catch broken releases earlier.

## Added

- **Self-Test** tab
- `Self_Test_AOS.bat`
- automated backend smoke tests
- UI module import tests
- database connectivity test
- migration check test
- CRUD method presence checks
- parser test
- guided inspection service test
- latest regression check for unsupported `readonly=True`

## Why this matters

Previous releases had regressions:
- buttons disappeared,
- save buttons appeared to do nothing,
- unsupported NiceGUI arguments caused 500 errors.

This release adds a basic test harness so AOS can check itself before you rely on it.

## Recommended workflow

After each new release:

1. Run `Run_AOS.bat`.
2. Open **Self-Test**.
3. Click **Run Self-Test**.
4. Only then use the release for live data.

You can also double-click:

`Self_Test_AOS.bat`
