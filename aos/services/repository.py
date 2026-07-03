from datetime import datetime
from aos.db.session import get_session
from aos.db.models import Colony,Queen,Equipment,Inspection,GenealogyEvent,AuditLog,WeatherObservation,SystemMeta
from aos.baseline import BASELINE_COLONIES, BASELINE_QUEENS, BASELINE_EQUIPMENT
class Repository:
    def audit(self,action,entity_type,entity_code,details):
        with get_session() as s: s.add(AuditLog(date=str(datetime.now().replace(microsecond=0)),action=action,entity_type=entity_type,entity_code=entity_code,details=details)); s.commit()
    def system_meta(self):
        with get_session() as s: return {m.key:m.value for m in s.query(SystemMeta).all()}
    def list_colonies(self,active_only=False):
        with get_session() as s:
            q=s.query(Colony)
            if active_only: q=q.filter(Colony.status=='Active')
            return [self._dict_colony(c) for c in q.order_by(Colony.colony_type,Colony.code).all()]
    def list_apiary_entities(self,active_only=True): return self.list_colonies(active_only)
    def create_colony(self,data):
        with get_session() as s:
            if s.query(Colony).filter_by(code=data.get('code')).first(): raise ValueError(f"Colony already exists: {data.get('code')}")
            s.add(Colony(**data)); s.commit()
        self.audit('CREATE','Colony',data.get('code'),'Colony created')
    def update_colony(self,code,data):
        with get_session() as s:
            c=s.query(Colony).filter_by(code=code).first()
            if not c: raise ValueError(f'Colony not found: {code}')
            for k,v in data.items(): setattr(c,k,v)
            s.commit()
        self.audit('UPDATE','Colony',code,'Colony updated')
    def delete_colony(self,code):
        with get_session() as s:
            c=s.query(Colony).filter_by(code=code).first()
            if not c: raise ValueError(f'Colony not found: {code}')
            s.delete(c); s.commit()
        self.audit('DELETE','Colony',code,'Colony deleted')
    def list_queens(self):
        with get_session() as s: return [self._dict_queen(q) for q in s.query(Queen).order_by(Queen.code).all()]
    def create_queen(self,data):
        with get_session() as s:
            if s.query(Queen).filter_by(code=data.get('code')).first(): raise ValueError(f"Queen already exists: {data.get('code')}")
            s.add(Queen(**data)); s.commit()
        self.audit('CREATE','Queen',data.get('code'),'Queen created')
    def update_queen(self,code,data):
        with get_session() as s:
            q=s.query(Queen).filter_by(code=code).first()
            if not q: raise ValueError(f'Queen not found: {code}')
            for k,v in data.items(): setattr(q,k,v)
            s.commit()
        self.audit('UPDATE','Queen',code,'Queen updated')
    def delete_queen(self,code):
        with get_session() as s:
            q=s.query(Queen).filter_by(code=code).first()
            if not q: raise ValueError(f'Queen not found: {code}')
            s.delete(q); s.commit()
        self.audit('DELETE','Queen',code,'Queen deleted')
    def list_equipment(self):
        with get_session() as s: return [self._dict_equipment(e) for e in s.query(Equipment).order_by(Equipment.code).all()]
    def create_equipment(self,data):
        with get_session() as s:
            if s.query(Equipment).filter_by(code=data.get('code')).first(): raise ValueError(f"Equipment already exists: {data.get('code')}")
            s.add(Equipment(**data)); s.commit()
        self.audit('CREATE','Equipment',data.get('code'),'Equipment created')
    def update_equipment(self,code,data):
        with get_session() as s:
            e=s.query(Equipment).filter_by(code=code).first()
            if not e: raise ValueError(f'Equipment not found: {code}')
            for k,v in data.items(): setattr(e,k,v)
            s.commit()
        self.audit('UPDATE','Equipment',code,'Equipment updated')
    def delete_equipment(self,code):
        with get_session() as s:
            e=s.query(Equipment).filter_by(code=code).first()
            if not e: raise ValueError(f'Equipment not found: {code}')
            s.delete(e); s.commit()
        self.audit('DELETE','Equipment',code,'Equipment deleted')
    def list_inspections(self):
        with get_session() as s:
            return [{'id':i.id,'date':i.date,'colony':i.colony.code if i.colony else '', 'inspection_type':i.inspection_type,'queen_seen':'Yes' if i.queen_seen else 'No','eggs_seen':'Yes' if i.eggs_seen else 'No','queen_cells':i.queen_cells,'brood_frames':i.brood_frames,'stores_frames':i.stores_frames,'bee_coverage_frames':i.bee_coverage_frames,'temperament':i.temperament,'notes':i.notes or ''} for i in s.query(Inspection).order_by(Inspection.date.desc(),Inspection.id.desc()).limit(500).all()]
    def latest_inspection_by_colony(self):
        latest={}
        for i in self.list_inspections():
            if i['colony'] not in latest: latest[i['colony']]=i
        return latest
    def create_inspection(self,data):
        with get_session() as s:
            c=s.query(Colony).get(data['colony_id'])
            if not c: raise ValueError('Selected colony/nuc does not exist.')
            s.add(Inspection(**data)); s.commit(); code=c.code
        self.audit('CREATE','Inspection',code,f"Inspection saved for {data.get('date')}")
    def list_genealogy(self):
        with get_session() as s: return [self._dict_genealogy(g) for g in s.query(GenealogyEvent).order_by(GenealogyEvent.date.desc(),GenealogyEvent.id.desc()).all()]
    def list_weather(self):
        with get_session() as s: return [{'id':w.id,'date':w.date,'temperature_c':w.temperature_c,'wind':w.wind,'rain':w.rain,'forage_flow':w.forage_flow,'inspection_suitability':w.inspection_suitability,'notes':w.notes or ''} for w in s.query(WeatherObservation).order_by(WeatherObservation.date.desc(),WeatherObservation.id.desc()).limit(100).all()]
    def create_weather(self,data):
        with get_session() as s: s.add(WeatherObservation(**data)); s.commit()
        self.audit('CREATE','Weather',data.get('date',''),'Weather saved')
    def list_audit(self):
        with get_session() as s: return [{'date':a.date,'action':a.action,'entity_type':a.entity_type,'entity_code':a.entity_code,'details':a.details} for a in s.query(AuditLog).order_by(AuditLog.id.desc()).limit(200).all()]
    def baseline_integrity(self):
        cc={c['code'] for c in self.list_colonies()}; cq={q['code'] for q in self.list_queens()}; ce={e['code'] for e in self.list_equipment()}
        return {'expected_colonies':len(BASELINE_COLONIES),'actual_colonies':len(cc),'missing_colonies':[{'code':c[0],'name':c[1],'type':c[2],'equipment':c[3]} for c in BASELINE_COLONIES if c[0] not in cc],'missing_queens':[{'code':q[0],'name':q[1],'line':q[2],'current_colony':q[4]} for q in BASELINE_QUEENS if q[0] not in cq],'missing_equipment':[{'code':e[0],'name':e[1],'type':e[2],'location':e[3]} for e in BASELINE_EQUIPMENT if e[0] not in ce]}
    def restore_missing_baseline(self):
        added={'colonies':0,'queens':0,'equipment':0}
        with get_session() as s:
            for c in BASELINE_COLONIES:
                if not s.query(Colony).filter_by(code=c[0]).first(): s.add(Colony(code=c[0],name=c[1],colony_type=c[2],equipment=c[3],objective=c[4],status=c[5],notes=c[6])); added['colonies']+=1
            for q in BASELINE_QUEENS:
                if not s.query(Queen).filter_by(code=q[0]).first(): s.add(Queen(code=q[0],name=q[1],line=q[2],source=q[3],current_colony_code=q[4],status=q[5],evidence_status=q[6],notes=q[7])); added['queens']+=1
            for e in BASELINE_EQUIPMENT:
                if not s.query(Equipment).filter_by(code=e[0]).first(): s.add(Equipment(code=e[0],name=e[1],type=e[2],current_location=e[3],compatible_with=e[4],status=e[5],notes=e[6])); added['equipment']+=1
            s.commit()
        self.audit('RESTORE_BASELINE','System','AOS',str(added)); return added
    @staticmethod
    def _dict_colony(c): return {'id':c.id,'code':c.code,'name':c.name,'type':c.colony_type,'equipment':c.equipment,'objective':c.objective,'status':c.status,'notes':c.notes or ''}
    @staticmethod
    def _dict_queen(q): return {'id':q.id,'code':q.code,'name':q.name,'line':q.line,'source':q.source,'current_colony':q.current_colony_code,'status':q.status,'evidence':q.evidence_status,'temperament_score':q.temperament_score,'brood_score':q.brood_score,'honey_score':q.honey_score,'notes':q.notes or ''}
    @staticmethod
    def _dict_equipment(e): return {'id':e.id,'code':e.code,'name':e.name,'type':e.type,'location':e.current_location,'compatible':e.compatible_with,'status':e.status,'notes':e.notes or ''}
    @staticmethod
    def _dict_genealogy(g): return {'date':g.date,'type':g.event_type,'source':g.source_colony,'target':g.target_colony,'queen':g.queen_code,'details':g.details or ''}
