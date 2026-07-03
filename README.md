# AOS v1.6 — Guided Workflow + Staged Commits

## Purpose

This release strengthens the AOS 2.0 foundation by making inspection entry safer.

## Added

- Guided inspection now stages draft inspections before committing.
- Inspection validation before save.
- Evidence preview before staging.
- Confidence score before staging.
- Pending guided inspections list.
- Commit staged guided inspection into the real inspection log.
- Reject staged guided inspection.
- Task engine and AI advisor retained.
- Knowledge graph retained.
- Installer safety retained.

## Why this matters

AOS should not silently write weak or incomplete records. This release introduces the safer pattern:

Draft → Validate → Stage → Commit

This becomes the foundation for future AI-assisted natural language entry.
