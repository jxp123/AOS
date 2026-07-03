# AOS v1.2 Release Notes

## Main change
Data integrity and missing baseline recovery.

## Why
Some earlier generated releases seeded smaller baseline lists, which could make it look like data had been lost.

## Added
- Data Integrity tab
- Baseline colony/nuc list
- Missing baseline detection
- One-click restore missing baseline entities
- Non-destructive bootstrap repair

## Important
This does not overwrite existing user-edited records. It only adds missing baseline records.
