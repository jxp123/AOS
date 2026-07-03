from datetime import datetime
from aos.db.session import get_session
from aos.db.models import Colony, Queen, Equipment, Inspection, GenealogyEvent, AuditLog, PendingCommit, WeatherObservation, SystemMeta
from aos.core.baseline import BASELINE_COLONIES, BASELINE_QUEENS, BASELINE_EQUIPMENT

class Repository:
    def system_meta(self):
        with get_session() as s:
            return {m.key: m.value for m in s.query(SystemMeta).all()}

    def list_apiary_entities(self, active_only=True):
        with get_session() as s:
            q = s.query(Colony)
            if active_only:
                q = q.filter(Colony.status == 'Active')
            return [self._dict_colony(c) for c in q.order_by(Colony.colony_type, Colony.code).all()]

    def list_colonies(self): return self.list_apiary_entities(False)

    def list_queens(self):
        with get_session() as s:
            return [self._dict_queen(q) for q in s.query(Queen).order_by(Queen.code).all()]

    def list_equipment(self):
        with get_session() as s:
            return [self._dict_equipment(e) for e in s.query(Equipment).order_by(Equipment.code).all()]

    def baseline_integrity(self):
        current_colonies = {c['code'] for c in self.list_colonies()}
        current_queens = {q['code'] for q in self.list_queens()}
        current_equipment = {e['code'] for e in self.list_equipment()}
        missing_colonies = [c for c in BASELINE_COLONIES if c[0] not in current_colonies]
        missing_queens = [q for q in BASELINE_QUEENS if q[0] not in current_queens]
        missing_equipment = [e for e in BASELINE_EQUIPMENT if e[0] not in current_equipment]
        return {
            'expected_colonies': len(BASELINE_COLONIES),
            'actual_colonies': len(current_colonies),
            'missing_colonies': [{'code': c[0], 'name': c[1], 'type': c[2], 'equipment': c[3], 'status': c[5]} for c in missing_colonies],
            'missing_queens': [{'code': q[0], 'name': q[1], 'line': q[2], 'current_colony': q[4]} for q in missing_queens],
            'missing_equipment': [{'code': e[0], 'name': e[1], 'type': e[2], 'location': e[3]} for e in missing_equipment],
        }

    def restore_missing_baseline(self):
        with get_session() as s:
            added = {'colonies':0, 'queens':0, 'equipment':0}
            for c in BASELINE_COLONIES:
                if not s.query(Colony).filter_by(code=c[0]).first():
                    s.add(Colony(code=c[0], name=c[1], colony_type=c[2], equipment=c[3], objective=c[4], status=c[5], notes=c[6]))
                    added['colonies'] += 1
            for q in BASELINE_QUEENS:
                if not s.query(Queen).filter_by(code=q[0]).first():
                    s.add(Queen(code=q[0], name=q[1], line=q[2], source=q[3], current_colony_code=q[4], status=q[5], evidence_status=q[6], notes=q[7]))
                    added['queens'] += 1
            for e in BASELINE_EQUIPMENT:
                if not s.query(Equipment).filter_by(code=e[0]).first():
                    s.add(Equipment(code=e[0], name=e[1], type=e[2], current_location=e[3], compatible_with=e[4], status=e[5], notes=e[6]))
                    added['equipment'] += 1
            s.add(AuditLog(date=str(datetime.now().replace(microsecond=0)), action='RESTORE_BASELINE', entity_type='System', entity_code='AOS', details=str(added)))
            s.commit()
        return added

    def list_genealogy(self):
        with get_session() as s:
            return [self._dict_genealogy(g) for g in s.query(GenealogyEvent).order_by(GenealogyEvent.date.desc(), GenealogyEvent.id.desc()).all()]

    def list_weather(self):
        with get_session() as s:
            return [{'date': w.date, 'temperature_c': w.temperature_c, 'wind': w.wind, 'rain': w.rain, 'forage_flow': w.forage_flow, 'inspection_suitability': w.inspection_suitability, 'notes': w.notes or ''} for w in s.query(WeatherObservation).order_by(WeatherObservation.date.desc()).limit(50).all()]

    def create_weather(self, data):
        with get_session() as s:
            s.add(WeatherObservation(**data)); s.commit()
            self.audit('CREATE','Weather',data.get('date',''), 'Weather/forage observation saved')

    def list_inspections(self):
        with get_session() as s:
            return [{'date': i.date, 'colony': i.colony.code if i.colony else '', 'inspection_type': i.inspection_type, 'queen_seen': 'Yes' if i.queen_seen else 'No', 'eggs_seen': 'Yes' if i.eggs_seen else 'No', 'queen_cells': i.queen_cells, 'brood_frames': i.brood_frames, 'stores_frames': i.stores_frames, 'bee_coverage_frames': i.bee_coverage_frames, 'temperament': i.temperament, 'notes': i.notes or ''} for i in s.query(Inspection).order_by(Inspection.date.desc(), Inspection.id.desc()).limit(300).all()]

    def latest_inspection_by_colony(self):
        latest = {}
        for i in self.list_inspections():
            if i['colony'] not in latest:
                latest[i['colony']] = i
        return latest

    def create_inspection(self, data):
        with get_session() as s:
            colony = s.query(Colony).get(data['colony_id'])
            if not colony: raise ValueError('Selected colony/nuc does not exist.')
            s.add(Inspection(**data)); s.commit()
            self.audit('CREATE','Inspection',colony.code,f"Inspection saved for {data.get('date')}")

    def list_audit(self):
        with get_session() as s:
            return [{'date': a.date, 'action': a.action, 'entity_type': a.entity_type, 'entity_code': a.entity_code, 'details': a.details} for a in s.query(AuditLog).order_by(AuditLog.id.desc()).limit(150).all()]

    def audit(self, action, entity_type, entity_code, details):
        with get_session() as s:
            s.add(AuditLog(date=str(datetime.now().replace(microsecond=0)), action=action, entity_type=entity_type, entity_code=entity_code, details=details))
            s.commit()

    def create_pending_commit(self, event_type, entity_type, entity_code, payload):
        with get_session() as s:
            s.add(PendingCommit(date=str(datetime.now().replace(microsecond=0)), event_type=event_type, entity_type=entity_type, entity_code=entity_code, payload=payload))
            s.commit()
            self.audit('STAGE','PendingCommit',entity_code,f'Staged {event_type}')

    def list_pending_commits(self):
        with get_session() as s:
            return [{'id': p.id, 'date': p.date, 'event_type': p.event_type, 'entity_type': p.entity_type, 'entity_code': p.entity_code, 'payload': p.payload, 'status': p.status, 'validation_status': p.validation_status, 'validation_message': p.validation_message} for p in s.query(PendingCommit).order_by(PendingCommit.id.desc()).all()]

    @staticmethod
    def _dict_colony(c):
        return {'id': c.id, 'code': c.code, 'name': c.name, 'type': c.colony_type, 'equipment': c.equipment, 'objective': c.objective, 'status': c.status, 'notes': c.notes or ''}

    @staticmethod
    def _dict_queen(q):
        return {'id': q.id, 'code': q.code, 'name': q.name, 'line': q.line, 'source': q.source, 'current_colony': q.current_colony_code, 'status': q.status, 'evidence': q.evidence_status, 'temperament_score': q.temperament_score, 'brood_score': q.brood_score, 'honey_score': q.honey_score, 'notes': q.notes or ''}

    @staticmethod
    def _dict_equipment(e):
        return {'id': e.id, 'code': e.code, 'name': e.name, 'type': e.type, 'location': e.current_location, 'compatible': e.compatible_with, 'status': e.status, 'notes': e.notes or ''}

    @staticmethod
    def _dict_genealogy(g):
        return {'date': g.date, 'type': g.event_type, 'source': g.source_colony, 'target': g.target_colony, 'queen': g.queen_code, 'details': g.details or ''}
