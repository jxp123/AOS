from collections import defaultdict
from datetime import datetime
from aos.db.session import get_session
from aos.db.models import Colony, Queen, Equipment, Inspection, GenealogyEvent, GraphRelationship, AuditLog

class KnowledgeGraphService:
    def seed_graph_from_existing_data(self):
        added = 0
        with get_session() as s:
            # Queen -> colony relationships
            for q in s.query(Queen).all():
                if q.current_colony_code:
                    exists = s.query(GraphRelationship).filter_by(
                        source_type='Queen',
                        source_code=q.code,
                        relationship='CURRENTLY_IN',
                        target_type='Colony',
                        target_code=q.current_colony_code,
                    ).first()
                    if not exists:
                        s.add(GraphRelationship(
                            date=str(datetime.now().date()),
                            source_type='Queen',
                            source_code=q.code,
                            relationship='CURRENTLY_IN',
                            target_type='Colony',
                            target_code=q.current_colony_code,
                            confidence=0.85,
                            evidence=f'Queen register current_colony_code={q.current_colony_code}',
                            notes='Generated from Queen register',
                        ))
                        added += 1

            # Genealogy event relationships
            for g in s.query(GenealogyEvent).all():
                if g.source_colony and g.target_colony:
                    exists = s.query(GraphRelationship).filter_by(
                        source_type='Colony',
                        source_code=g.source_colony,
                        relationship=g.event_type.upper().replace(' ', '_'),
                        target_type='Colony',
                        target_code=g.target_colony,
                    ).first()
                    if not exists:
                        s.add(GraphRelationship(
                            date=g.date,
                            source_type='Colony',
                            source_code=g.source_colony,
                            relationship=g.event_type.upper().replace(' ', '_'),
                            target_type='Colony',
                            target_code=g.target_colony,
                            confidence=0.9,
                            evidence=g.details or '',
                            notes='Generated from Genealogy event',
                        ))
                        added += 1

                if g.queen_code and g.target_colony:
                    exists = s.query(GraphRelationship).filter_by(
                        source_type='Queen',
                        source_code=g.queen_code,
                        relationship='ASSOCIATED_WITH',
                        target_type='Colony',
                        target_code=g.target_colony,
                    ).first()
                    if not exists:
                        s.add(GraphRelationship(
                            date=g.date,
                            source_type='Queen',
                            source_code=g.queen_code,
                            relationship='ASSOCIATED_WITH',
                            target_type='Colony',
                            target_code=g.target_colony,
                            confidence=0.75,
                            evidence=g.details or '',
                            notes='Generated from Genealogy queen reference',
                        ))
                        added += 1

            # Equipment -> location relationships
            for e in s.query(Equipment).all():
                if e.current_location:
                    exists = s.query(GraphRelationship).filter_by(
                        source_type='Equipment',
                        source_code=e.code,
                        relationship='LOCATED_AT',
                        target_type='Colony',
                        target_code=e.current_location,
                    ).first()
                    if not exists:
                        s.add(GraphRelationship(
                            date=str(datetime.now().date()),
                            source_type='Equipment',
                            source_code=e.code,
                            relationship='LOCATED_AT',
                            target_type='Colony',
                            target_code=e.current_location,
                            confidence=0.8,
                            evidence=f'Equipment register current_location={e.current_location}',
                            notes='Generated from Equipment register',
                        ))
                        added += 1

            s.add(AuditLog(
                date=str(datetime.now().replace(microsecond=0)),
                action='GRAPH_SEED',
                entity_type='System',
                entity_code='AOS',
                details=f'Knowledge graph seeded; relationships added={added}',
            ))
            s.commit()
        return added

    def list_relationships(self):
        with get_session() as s:
            return [{
                'id': r.id,
                'date': r.date,
                'source': f'{r.source_type}:{r.source_code}',
                'relationship': r.relationship,
                'target': f'{r.target_type}:{r.target_code}',
                'confidence': r.confidence,
                'evidence': r.evidence or '',
                'notes': r.notes or '',
            } for r in s.query(GraphRelationship).order_by(GraphRelationship.id.desc()).all()]

    def graph_summary(self):
        with get_session() as s:
            return {
                'colonies': s.query(Colony).count(),
                'queens': s.query(Queen).count(),
                'equipment': s.query(Equipment).count(),
                'inspections': s.query(Inspection).count(),
                'genealogy_events': s.query(GenealogyEvent).count(),
                'relationships': s.query(GraphRelationship).count(),
            }

    def colony_timeline(self, colony_code):
        events = []
        with get_session() as s:
            colony = s.query(Colony).filter_by(code=colony_code).first()
            if colony:
                events.append({
                    'date': '',
                    'type': 'Colony',
                    'title': f'{colony.code} — {colony.name}',
                    'details': f'{colony.colony_type}, {colony.equipment}, {colony.objective}. {colony.notes or ""}',
                })

            for i in s.query(Inspection).join(Colony).filter(Colony.code == colony_code).order_by(Inspection.date.desc(), Inspection.id.desc()).all():
                events.append({
                    'date': i.date,
                    'type': 'Inspection',
                    'title': f'{i.inspection_type} inspection',
                    'details': f'Queen seen={i.queen_seen}; eggs={i.eggs_seen}; brood={i.brood_frames}; stores={i.stores_frames}; bees={i.bee_coverage_frames}; notes={i.notes or ""}',
                })

            for g in s.query(GenealogyEvent).filter(
                (GenealogyEvent.source_colony == colony_code) | (GenealogyEvent.target_colony == colony_code)
            ).order_by(GenealogyEvent.date.desc(), GenealogyEvent.id.desc()).all():
                events.append({
                    'date': g.date,
                    'type': 'Genealogy',
                    'title': g.event_type,
                    'details': f'{g.source_colony} → {g.target_colony}; queen={g.queen_code}; {g.details or ""}',
                })

            for r in s.query(GraphRelationship).filter(
                (GraphRelationship.source_code == colony_code) | (GraphRelationship.target_code == colony_code)
            ).order_by(GraphRelationship.date.desc(), GraphRelationship.id.desc()).all():
                events.append({
                    'date': r.date,
                    'type': 'Relationship',
                    'title': f'{r.source_type}:{r.source_code} {r.relationship} {r.target_type}:{r.target_code}',
                    'details': r.evidence or r.notes or '',
                })
        return events

    def queen_lineage(self, queen_code):
        with get_session() as s:
            rows = []
            queen = s.query(Queen).filter_by(code=queen_code).first()
            if queen:
                rows.append({
                    'date': '',
                    'type': 'Queen',
                    'source': queen.code,
                    'relationship': 'PROFILE',
                    'target': queen.current_colony_code,
                    'evidence': f'{queen.name}; {queen.line}; {queen.source}; status={queen.status}',
                })
            for r in s.query(GraphRelationship).filter(
                (GraphRelationship.source_code == queen_code) | (GraphRelationship.target_code == queen_code)
            ).order_by(GraphRelationship.date.desc(), GraphRelationship.id.desc()).all():
                rows.append({
                    'date': r.date,
                    'type': 'Relationship',
                    'source': f'{r.source_type}:{r.source_code}',
                    'relationship': r.relationship,
                    'target': f'{r.target_type}:{r.target_code}',
                    'evidence': r.evidence or r.notes or '',
                })
            return rows

    def export_graph(self):
        relationships = self.list_relationships()
        nodes = {}
        edges = []
        for r in relationships:
            nodes[r['source']] = {'id': r['source']}
            nodes[r['target']] = {'id': r['target']}
            edges.append({
                'source': r['source'],
                'target': r['target'],
                'relationship': r['relationship'],
                'confidence': r['confidence'],
                'evidence': r['evidence'],
            })
        return {
            'summary': self.graph_summary(),
            'nodes': list(nodes.values()),
            'edges': edges,
        }
