from datetime import datetime
from sqlalchemy.exc import IntegrityError
from aos.db.session import get_session
from aos.db.models import Colony, Queen, Equipment, Inspection, GenealogyEvent, AuditLog

class Repository:
    '''Single data access layer. All screens must use this class.'''

    # ---------- Colonies / Apiary Entities ----------
    def list_apiary_entities(self, active_only=True):
        with get_session() as s:
            query = s.query(Colony)
            if active_only:
                query = query.filter(Colony.status == 'Active')
            return [self._dict_colony(c) for c in query.order_by(Colony.colony_type, Colony.code).all()]

    def list_colonies(self):
        return self.list_apiary_entities(active_only=False)

    def create_colony(self, data):
        with get_session() as s:
            c = Colony(**data)
            s.add(c)
            try:
                s.commit()
            except IntegrityError:
                s.rollback()
                raise ValueError(f"Colony code already exists: {data.get('code')}")
            self.audit('CREATE', 'Colony', data.get('code'), 'Colony created')

    def update_colony(self, code, data):
        with get_session() as s:
            c = s.query(Colony).filter_by(code=code).first()
            if not c:
                raise ValueError(f'Colony not found: {code}')
            for k, v in data.items():
                setattr(c, k, v)
            s.commit()
            self.audit('UPDATE', 'Colony', code, 'Colony updated')

    def delete_colony(self, code):
        with get_session() as s:
            c = s.query(Colony).filter_by(code=code).first()
            if not c:
                raise ValueError(f'Colony not found: {code}')
            s.delete(c)
            s.commit()
            self.audit('DELETE', 'Colony', code, 'Colony deleted')

    # ---------- Queens ----------
    def list_queens(self):
        with get_session() as s:
            return [self._dict_queen(q) for q in s.query(Queen).order_by(Queen.code).all()]

    def create_queen(self, data):
        with get_session() as s:
            q = Queen(**data)
            s.add(q)
            try:
                s.commit()
            except IntegrityError:
                s.rollback()
                raise ValueError(f"Queen code already exists: {data.get('code')}")
            self.audit('CREATE', 'Queen', data.get('code'), 'Queen created')

    def update_queen(self, code, data):
        with get_session() as s:
            q = s.query(Queen).filter_by(code=code).first()
            if not q:
                raise ValueError(f'Queen not found: {code}')
            for k, v in data.items():
                setattr(q, k, v)
            s.commit()
            self.audit('UPDATE', 'Queen', code, 'Queen updated')

    def delete_queen(self, code):
        with get_session() as s:
            q = s.query(Queen).filter_by(code=code).first()
            if not q:
                raise ValueError(f'Queen not found: {code}')
            s.delete(q)
            s.commit()
            self.audit('DELETE', 'Queen', code, 'Queen deleted')

    # ---------- Equipment ----------
    def list_equipment(self):
        with get_session() as s:
            return [self._dict_equipment(e) for e in s.query(Equipment).order_by(Equipment.code).all()]

    def create_equipment(self, data):
        with get_session() as s:
            e = Equipment(**data)
            s.add(e)
            try:
                s.commit()
            except IntegrityError:
                s.rollback()
                raise ValueError(f"Equipment code already exists: {data.get('code')}")
            self.audit('CREATE', 'Equipment', data.get('code'), 'Equipment created')

    def update_equipment(self, code, data):
        with get_session() as s:
            e = s.query(Equipment).filter_by(code=code).first()
            if not e:
                raise ValueError(f'Equipment not found: {code}')
            for k, v in data.items():
                setattr(e, k, v)
            s.commit()
            self.audit('UPDATE', 'Equipment', code, 'Equipment updated')

    def delete_equipment(self, code):
        with get_session() as s:
            e = s.query(Equipment).filter_by(code=code).first()
            if not e:
                raise ValueError(f'Equipment not found: {code}')
            s.delete(e)
            s.commit()
            self.audit('DELETE', 'Equipment', code, 'Equipment deleted')

    # ---------- Logs ----------
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
