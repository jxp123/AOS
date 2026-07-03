from datetime import datetime
from aos.db.session import get_session
from aos.db.models import Colony,Inspection,GuidedInspectionDraft,AuditLog
from aos.engines.confidence_engine import confidence_from_evidence

class GuidedInspectionService:
    def validate_payload(self,payload):
        messages=[]; status="PASS"
        if not payload.get("colony_id"):
            messages.append("Colony/nuc is required."); status="FAIL"
        if not payload.get("inspection_date"):
            messages.append("Inspection date is required."); status="FAIL"
        brood=float(payload.get("brood_frames") or 0); stores=float(payload.get("stores_frames") or 0); bees=float(payload.get("bee_coverage_frames") or 0); qcells=int(payload.get("queen_cells") or 0)
        if brood==0 and stores==0 and bees==0 and not payload.get("notes"):
            messages.append("Very little evidence entered."); status="WARN" if status!="FAIL" else status
        if qcells>0 and not payload.get("notes"):
            messages.append("Queen cells recorded; add notes."); status="WARN" if status!="FAIL" else status
        return {"status":status,"message":" ".join(messages) if messages else "Validation passed."}

    def build_evidence(self,colony_code,payload):
        return [
            f"Colony/Nuc: {colony_code}",
            f"Inspection date: {payload.get('inspection_date')}",
            f"Queen seen: {'Yes' if payload.get('queen_seen') else 'No'}",
            f"Eggs seen: {'Yes' if payload.get('eggs_seen') else 'No'}",
            f"Larvae seen: {'Yes' if payload.get('larvae_seen') else 'No'}",
            f"Queen cells: {payload.get('queen_cells')}",
            f"Brood frames: {payload.get('brood_frames')}",
            f"Stores frames: {payload.get('stores_frames')}",
            f"Bee coverage frames: {payload.get('bee_coverage_frames')}",
            f"Temperament: {payload.get('temperament')}",
            f"Notes: {payload.get('notes') or ''}",
        ]

    def stage_draft(self,payload):
        with get_session() as s:
            colony=s.query(Colony).get(payload.get("colony_id"))
            if not colony:
                raise ValueError("Selected colony/nuc does not exist.")
            validation=self.validate_payload(payload)
            evidence_items=self.build_evidence(colony.code,payload)
            confidence=confidence_from_evidence(evidence_items)
            d=GuidedInspectionDraft(
                created_at=str(datetime.now().replace(microsecond=0)),
                colony_id=colony.id,
                colony_code=colony.code,
                inspection_date=payload.get("inspection_date"),
                queen_seen=bool(payload.get("queen_seen")),
                eggs_seen=bool(payload.get("eggs_seen")),
                larvae_seen=bool(payload.get("larvae_seen")),
                queen_cells=int(payload.get("queen_cells") or 0),
                brood_frames=float(payload.get("brood_frames") or 0),
                stores_frames=float(payload.get("stores_frames") or 0),
                bee_coverage_frames=float(payload.get("bee_coverage_frames") or 0),
                temperament=payload.get("temperament") or "Unknown",
                notes=payload.get("notes") or "",
                evidence="\n".join(evidence_items),
                confidence=float(confidence["score"]),
                validation_status=validation["status"],
                validation_message=validation["message"],
                status="Staged",
            )
            s.add(d)
            s.add(AuditLog(date=str(datetime.now().replace(microsecond=0)),action="STAGE",entity_type="GuidedInspectionDraft",entity_code=colony.code,details=validation["message"]))
            s.commit()
            return d.id, validation, confidence

    def list_drafts(self):
        with get_session() as s:
            return [{"id":d.id,"created_at":d.created_at,"colony_code":d.colony_code,"inspection_date":d.inspection_date,"queen_seen":"Yes" if d.queen_seen else "No","eggs_seen":"Yes" if d.eggs_seen else "No","brood_frames":d.brood_frames,"stores_frames":d.stores_frames,"bee_coverage_frames":d.bee_coverage_frames,"confidence":d.confidence,"validation_status":d.validation_status,"validation_message":d.validation_message,"status":d.status,"evidence":d.evidence} for d in s.query(GuidedInspectionDraft).order_by(GuidedInspectionDraft.id.desc()).limit(200).all()]

    def commit_draft(self,draft_id):
        with get_session() as s:
            d=s.query(GuidedInspectionDraft).get(draft_id)
            if not d: raise ValueError("Draft not found.")
            if d.status!="Staged": raise ValueError(f"Draft is not staged: {d.status}")
            if d.validation_status=="FAIL": raise ValueError("Cannot commit a failed draft.")
            s.add(Inspection(colony_id=d.colony_id,date=d.inspection_date,inspection_type="Guided",queen_seen=d.queen_seen,eggs_seen=d.eggs_seen,larvae_seen=d.larvae_seen,queen_cells=d.queen_cells,brood_frames=d.brood_frames,stores_frames=d.stores_frames,bee_coverage_frames=d.bee_coverage_frames,temperament=d.temperament,notes=d.notes))
            d.status="Committed"
            s.add(AuditLog(date=str(datetime.now().replace(microsecond=0)),action="COMMIT",entity_type="GuidedInspectionDraft",entity_code=d.colony_code,details=f"Committed draft {draft_id}."))
            s.commit()

    def reject_draft(self,draft_id):
        with get_session() as s:
            d=s.query(GuidedInspectionDraft).get(draft_id)
            if not d: raise ValueError("Draft not found.")
            d.status="Rejected"
            s.add(AuditLog(date=str(datetime.now().replace(microsecond=0)),action="REJECT",entity_type="GuidedInspectionDraft",entity_code=d.colony_code,details=f"Rejected draft {draft_id}."))
            s.commit()
