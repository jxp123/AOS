from datetime import datetime
from aos.db.session import init_db, get_session
from aos.db.models import Colony, Queen, Equipment, GenealogyEvent, AuditLog

def boot_aos():
    init_db()
    seed_data()

def seed_data():
    with get_session() as session:
        if session.query(Colony).count() == 0:
            colonies = [
                ('H3','Hive 3','Hive','Langstroth','Honey','Active','Queen seen; underpopulated; super unused.'),
                ('H5','Hive 5','Hive','Unknown','Requeening after swarm','Active','Swarm source; two queen cells left.'),
                ('H12','Hive 12','Hive','National','Expansion','Active','Former Nuc 99; feeder fitted.'),
                ('H15','Hive 15','Hive','National','Honey','Active','Feeder removed; first super filling.'),
                ('H16','Hive 16','Hive','National','Honey / Watch brood congestion','Active','Queen seen; no queen cells; brood box full.'),
                ('N91','Nuc 91','Nuc','National','Recover after brood donation','Active','Donated 2 brood frames for Jolanta nuc.'),
                ('N94','Nuc 94','Nuc','14x12','Build','Active','Hard rule: not National.'),
                ('N100','Nuc 100','Nuc','National','Recover after brood donation','Active','Donated 1 brood frame for Jolanta nuc.'),
                ('NJOL','Jolanta Nuc','Nuc','National','Scottish Carnica evaluation','Active','Created from brood frames from N91 and N100.'),
            ]
            for c in colonies:
                session.add(Colony(code=c[0], name=c[1], colony_type=c[2], equipment=c[3], objective=c[4], status=c[5], notes=c[6]))

        if session.query(Queen).count() == 0:
            session.add(Queen(code='Q-JOLANTA', name='Jolanta', line='Scottish Carnica', source='Denrosa / Jolanta', current_colony_code='NJOL', status='Introduced / pending confirmation', evidence_status='Confirmed', notes='Purchased queen; strategic asset.'))

        if session.query(Equipment).count() == 0:
            session.add(Equipment(code='FEED-001', name='Abelo Ashford Poly Feeder', type='Feeder', current_location='H12', compatible_with='National', status='In use', notes='Approx 1-1.5L syrup moved from Hive 15.'))

        if session.query(GenealogyEvent).count() == 0:
            session.add(GenealogyEvent(date='2026-07-03', event_type='Brood donation', source_colony='N91', target_colony='NJOL', queen_code='Q-JOLANTA', details='Nuc 91 donated 2 brood frames; queen seen.'))
            session.add(GenealogyEvent(date='2026-07-03', event_type='Brood donation', source_colony='N100', target_colony='NJOL', queen_code='Q-JOLANTA', details='Nuc 100 donated 1 brood frame; queen seen.'))

        if session.query(AuditLog).count() == 0:
            session.add(AuditLog(date=str(datetime.now().replace(microsecond=0)), action='BOOTSTRAP', entity_type='System', entity_code='AOS', details='Seeded v0.8 baseline data.'))
        session.commit()
