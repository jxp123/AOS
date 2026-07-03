from datetime import datetime
from aos.db.session import get_session
from aos.db.models import Colony,Queen,Equipment,Inspection,GenealogyEvent,GraphRelationship,AuditLog
class KnowledgeGraphService:
    def seed_graph(self):
        added=0
        with get_session() as s:
            for q in s.query(Queen).all():
                if q.current_colony_code and not s.query(GraphRelationship).filter_by(source_type='Queen',source_code=q.code,relationship='CURRENTLY_IN',target_type='Colony',target_code=q.current_colony_code).first(): s.add(GraphRelationship(date=str(datetime.now().date()),source_type='Queen',source_code=q.code,relationship='CURRENTLY_IN',target_type='Colony',target_code=q.current_colony_code,confidence=0.85,evidence='Queen register')); added+=1
            for g in s.query(GenealogyEvent).all():
                rel=g.event_type.upper().replace(' ','_')
                if g.source_colony and g.target_colony and not s.query(GraphRelationship).filter_by(source_type='Colony',source_code=g.source_colony,relationship=rel,target_type='Colony',target_code=g.target_colony).first(): s.add(GraphRelationship(date=g.date,source_type='Colony',source_code=g.source_colony,relationship=rel,target_type='Colony',target_code=g.target_colony,confidence=0.9,evidence=g.details or '')); added+=1
            for e in s.query(Equipment).all():
                if e.current_location and not s.query(GraphRelationship).filter_by(source_type='Equipment',source_code=e.code,relationship='LOCATED_AT',target_type='Colony',target_code=e.current_location).first(): s.add(GraphRelationship(date=str(datetime.now().date()),source_type='Equipment',source_code=e.code,relationship='LOCATED_AT',target_type='Colony',target_code=e.current_location,confidence=0.8,evidence='Equipment register')); added+=1
            s.add(AuditLog(date=str(datetime.now().replace(microsecond=0)),action='GRAPH_SEED',entity_type='System',entity_code='AOS',details=f'Relationships added={added}')); s.commit()
        return added
    def summary(self):
        with get_session() as s: return {'colonies':s.query(Colony).count(),'queens':s.query(Queen).count(),'equipment':s.query(Equipment).count(),'inspections':s.query(Inspection).count(),'genealogy_events':s.query(GenealogyEvent).count(),'relationships':s.query(GraphRelationship).count()}
    def relationships(self):
        with get_session() as s: return [{'id':r.id,'date':r.date,'source':f'{r.source_type}:{r.source_code}','relationship':r.relationship,'target':f'{r.target_type}:{r.target_code}','confidence':r.confidence,'evidence':r.evidence or ''} for r in s.query(GraphRelationship).order_by(GraphRelationship.id.desc()).all()]
    def export_graph(self):
        rels=self.relationships(); nodes={}
        for r in rels: nodes[r['source']]={'id':r['source']}; nodes[r['target']]={'id':r['target']}
        return {'summary':self.summary(),'nodes':list(nodes.values()),'edges':rels}
