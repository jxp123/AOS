from aos.db.session import get_session
from aos.db.models import PendingCommit
from aos.engines.validation_engine import validation_summary
from aos.utils.backup import backup_database
from aos.services.repository import Repository

def validate_pending_commits():
    summary = validation_summary()
    with get_session() as s:
        for p in s.query(PendingCommit).filter(PendingCommit.status == 'Pending').all():
            p.validation_status = summary['status']
            p.validation_message = summary['message']
        s.commit()
    return summary

def commit_all_pending():
    summary = validate_pending_commits()
    if summary['status'] == 'FAIL':
        return {'status':'FAILED','message':'Commit blocked by critical validation issues','backup':None}
    backup = backup_database()
    repo = Repository()
    with get_session() as s:
        for p in s.query(PendingCommit).filter(PendingCommit.status == 'Pending').all():
            p.status = 'Committed'
            p.validation_status = summary['status']
            p.validation_message = summary['message']
        s.commit()
    repo.audit('COMMIT','System','AOS',f'Committed pending queue. Backup: {backup}')
    return {'status':'COMMITTED','message':'Pending commits marked as committed','backup':str(backup) if backup else ''}
