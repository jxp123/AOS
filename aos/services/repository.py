from datetime import datetime
from aos.db.session import get_session
from aos.db.models import Colony, Queen, Equipment, Inspection, GenealogyEvent, AuditLog

class Repository:
    '''Single data access layer. All screens must use this class.'''

    def list_apiary_entities(self, active_only=True):
        '''Central view of all hives and nucs. Used by inspection dropdown and colonies screen.'''
        with get_session() as s:
            query = s.query(Colony)
            if active_only:
                query = query.filter(Colony.status == 'Active')
            return [self._dict_colony(c) for c in query.order_by(Colony.colony_type, Colony.code).all()]

    def list_colonies(self):
        return self.list_apiary_entities(active_only=False)

    def list_queens(self):
        with get_session() as s:
            return [self._dict_queen(q) for q in s.query(Queen).order_by(Queen.code).all()]

    def list_equipment(self):
        with get_session() as s:
            return [self._dict_equipment(e) for e in s.query(Equipment).order_by(Equipment.code).all()]

    def list_genealogy(self):
        with get_session() as s:
            return [self._dict_genealogy(g) for g in s.query(GenealogyEvent).order_by(GenealogyEvent.date.desc(), GenealogyEvent.id.desc()).all()]

    def list_audit(self):
        with get_session() as s:
            return [{'date': a.date, 'action': a.action, 'entity_type': a.entity_type, 'entity_code': a.entity_code, 'details': a.details}
                    for a in s.query(AuditLog).order_by(AuditLog.id.desc()).limit(100).all()]

    def list_inspections(self):
        with get_session() as s:
            return [{
                'date': i.date, 'colony': i.colony.code if i.colony else '',
                'inspection_type': i.inspection_type,
                'queen_seen': 'Yes' if i.queen_seen else 'No',
                'eggs_seen': 'Yes' if i.eggs_seen else 'No',
                'queen_cells': i.queen_cells,
                'brood_frames': i.brood_frames,
                'stores_frames': i.stores_frames,
                'temperament': i.temperament,
                'notes': i.notes or '',
            } for i in s.query(Inspection).order_by(Inspection.date.desc(), Inspection.id.desc()).limit(200).all()]

    def create_inspection(self, data):
        with get_session() as s:
            colony = s.query(Colony).get(data['colony_id'])
            if not colony:
                raise ValueError('Selected colony/nuc does not exist in central apiary entities.')
            insp = Inspection(**data)
            s.add(insp)
            s.commit()
            self.audit('CREATE', 'Inspection', colony.code, f"Inspection saved for {data.get('date')}")
            return insp.id

    def audit(self, action, entity_type, entity_code, details):
        with get_session() as s:
            s.add(AuditLog(date=str(datetime.now().replace(microsecond=0)), action=action, entity_type=entity_type, entity_code=entity_code, details=details))
            s.commit()

    @staticmethod
    def _dict_colony(c):
        return {'id': c.id, 'code': c.code, 'name': c.name, 'type': c.colony_type, 'equipment': c.equipment,
                'objective': c.objective, 'status': c.status, 'notes': c.notes or ''}

    @staticmethod
    def _dict_queen(q):
        return {'id': q.id, 'code': q.code, 'name': q.name, 'line': q.line, 'source': q.source,
                'current_colony': q.current_colony_code, 'status': q.status, 'evidence': q.evidence_status, 'notes': q.notes or ''}

    @staticmethod
    def _dict_equipment(e):
        return {'id': e.id, 'code': e.code, 'name': e.name, 'type': e.type, 'location': e.current_location,
                'compatible': e.compatible_with, 'status': e.status, 'notes': e.notes or ''}

    @staticmethod
    def _dict_genealogy(g):
        return {'date': g.date, 'type': g.event_type, 'source': g.source_colony, 'target': g.target_colony,
                'queen': g.queen_code, 'details': g.details or ''}
