
# Apiary Operating System — v0.6 Core Framework

This release moves AOS from prototype screens toward a maintainable application architecture.

## What is new in v0.6

- Shared repository/service layer
- Stable SQLite schema
- Colony, Queen, Equipment, Inspection and Genealogy models
- CRUD-ready services
- Validation engine foundation
- Risk engine foundation
- Decision engine foundation
- Commit/audit groundwork
- UI pages separated into modules
- Basic AI state export skeleton

## How to run

1. Extract the ZIP.
2. Double-click `Start_AOS.bat`.
3. Browser opens at `http://127.0.0.1:8000`.

## Requirements

- Python 3.11+
- During Python installation, tick **Add Python to PATH**.

## Development principle

All UI screens must read/write through services and repositories.
No UI page should own independent copies of the database state.
