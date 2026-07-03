# AOS v1.4 — Knowledge Graph Foundation

## Purpose

This release pulls forward the Phase 5 architecture: the Knowledge Graph.

It does not attempt to finish all future 2.0 intelligence, but it introduces the core structures needed for:

- Queen genealogy
- Colony lineage
- Event-based history
- Relationships between colonies, queens, equipment and inspections
- Timeline-style views
- Graph export for future AI reasoning

## Added

- Knowledge Graph tab
- Colony timeline view
- Queen lineage view
- Graph relationship export
- Graph summary cards
- `KnowledgeGraphService`
- AI export now includes graph data
- Migration check for graph tables
- Existing CRUD/UI fixes retained

## Important

This is a foundation release. It creates the graph layer and views, but it does not yet do advanced visual node-link diagrams.
