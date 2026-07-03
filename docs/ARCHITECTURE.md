# AOS v0.6.1 Architecture

Central active apiary entity view:

`Repository.list_apiary_entities(active_only=True)`

Used by:
- Colonies screen
- New Inspection dropdown
- Morning briefing
- AI export

Invariant: if a hive/nuc appears in the inspection dropdown, it exists in the Colonies table.
