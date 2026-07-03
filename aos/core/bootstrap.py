from datetime import datetime
from aos.db.session import init_db, get_session
from aos.db.models import Colony, Queen, Equipment, GenealogyEvent, AuditLog, SystemMeta
from aos.core.settings import SCHEMA_VERSION, DATA_DIR, EXPORT_DIR, IMPORT_DIR, BACKUP_DIR, LOG_DIR
from aos.core.baseline import BASELINE_COLONIES, BASELINE_QUEENS, BASELINE_EQUIPMENT

def boot_aos():
    for folder in [DATA_DIR, EXPORT_DIR, IMPORT_DIR, BACKUP_DIR, LOG_DIR]:
        folder.mkdir(exist_ok=True)
    init_db()
    seed_data()

def seed_data():
    with get_session() as session:
        meta = session.query(SystemMeta).filter_by(key='schema_version').first()
        if not meta:
            session.add(SystemMeta(key='schema_version', value=SCHEMA_VERSION))
        elif meta.value != SCHEMA_VERSION:
            meta.value = SCHEMA_VERSION

        for c in BASELINE_COLONIES:
            if not session.query(Colony).filter_by(code=c[0]).first():
                session.add(Colony(code=c[0], name=c[1], colony_type=c[2], equipment=c[3], objective=c[4], status=c[5], notes=c[6]))
        for q in BASELINE_QUEENS:
            if not session.query(Queen).filter_by(code=q[0]).first():
                session.add(Queen(code=q[0], name=q[1], line=q[2], source=q[3], current_colony_code=q[4], status=q[5], evidence_status=q[6], notes=q[7]))
        for e in BASELINE_EQUIPMENT:
            if not session.query(Equipment).filter_by(code=e[0]).first():
                session.add(Equipment(code=e[0], name=e[1], type=e[2], current_location=e[3], compatible_with=e[4], status=e[5], notes=e[6]))

        if session.query(GenealogyEvent).count() == 0:
            session.add(GenealogyEvent(date='2026-07-03', event_type='Brood donation', source_colony='N91', target_colony='NJOL', queen_code='Q-JOLANTA', details='Nuc 91 donated 2 brood frames; queen seen.'))
            session.add(GenealogyEvent(date='2026-07-03', event_type='Brood donation', source_colony='N100', target_colony='NJOL', queen_code='Q-JOLANTA', details='Nuc 100 donated 1 brood frame; queen seen.'))

        session.add(AuditLog(date=str(datetime.now().replace(microsecond=0)), action='BOOT', entity_type='System', entity_code='AOS', details='Booted v1.3 with migration-safe baseline repair.'))
        session.commit()
