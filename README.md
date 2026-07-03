# AOS v1.7.1 — Readonly Fix

## Fix

This release fixes the NiceGUI server error:

`TypeError: got an unexpected keyword argument 'readonly'`

## Cause

Some NiceGUI versions do not accept `readonly=True` as a direct argument on `ui.textarea`.

## Change

Changed:

`ui.textarea(..., readonly=True)`

to:

`ui.textarea(...).props('readonly')`

## Included

This release is based on v1.7, so it also includes:
- Natural Language Intake
- Guided Inspection Drafts
- Tasks
- AI Advisor
- Knowledge Graph
- CRUD fixes
- Installer safety
