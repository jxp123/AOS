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
                ('H1','Hive 1','Hive','National','Honey / Build','Active','Double brood; super added.'),
                ('H2','Hive 2','Hive','National','Build / Recover','Active','Essex Buckfast; low population recovery.'),
                ('H3','Hive 3','Hive','Langstroth','Honey','Active','Queen seen; underpopulated; super unused.'),
                ('H4','Hive 4','Hive','Langstroth','Honey','Active','Replace brood box with rails.'),
                ('H5','Hive 5','Hive','Unknown','Requeening after swarm','Active','Swarm source; two queen cells left.'),
                ('H6','Hive 6','Hive','Unknown','Queenright / Recover','Active','Eggs seen.'),
                ('H7','Hive 7','Hive','Unknown','Honey','Active','Strong production colony; second super added.'),
                ('H8','Hive 8','Hive','Unknown','Honey','Active','Queen seen, eggs, approx six brood frames.'),
                ('H12','Hive 12','Hive','National','Expansion','Active','Former Nuc 99; feeder fitted.'),
                ('H13','Hive 13','Hive','National','Build / Carpathian evaluation','Active','Former Nuc 93; Carpathian queen.'),
                ('H14','Hive 14','Hive','National','Build / Queenright','Active','Eggs seen; not candidate for Jolanta.'),
                ('H15','Hive 15','Hive','National','Honey','Active','Feeder removed; first super filling.'),
                ('H16','Hive 16','Hive','National','Honey / Watch brood congestion','Active','Queen seen; no queen cells; brood box full.'),
                ('H17','Hive 17','Hive','National','Build','Active','Queen seen; developing colony.'),
                ('H19','Hive 19','Hive','National','Build / Carpathian evaluation','Active','Carpathian queen accepted; eggs seen.'),
                ('N90','Nuc 90','Nuc','Unknown','Queen event / monitor','Active','Queen status historically uncertain.'),
                ('N91','Nuc 91','Nuc','National','Recover after brood donation','Active','Donated 2 brood frames for Jolanta nuc.'),
                ('N92','Nuc 92','Nuc','Langstroth','Expansion candidate','Active','Strong Langstroth nuc.'),
                ('N94','Nuc 94','Nuc','14x12','Build','Active','Hard rule: not National.'),
                ('N96','Nuc 96','Nuc','Langstroth','Carpathian evaluation','Active','Confirmed Carpathian; Langstroth nuc.'),
                ('N98','Nuc 98','Nuc','Langstroth','Build','Active','Weaker Langstroth nuc.'),
                ('N100','Nuc 100','Nuc','National','Recover after brood donation','Active','Donated 1 brood frame for Jolanta nuc.'),
                ('NJOL','Jolanta Nuc','Nuc','National','Scottish Carnica evaluation','Active','Created from brood frames from N91 and N100.'),
            ]
            for c in colonies:
                session.add(Colony(code=c[0], name=c[1], colony_type=c[2], equipment=c[3], objective=c[4], status=c[5], notes=c[6]))

        if session.query(Queen).count() == 0:
            queens = [
                ('Q-JOLANTA','Jolanta','Scottish Carnica','Denrosa / Jolanta','NJOL','Introduced / pending confirmation','Confirmed','Purchased queen; strategic asset.'),
                ('Q-H13-CARP','Carpathian H13','Carpathian','Purchased','H13','Active','Confirmed','Former Nuc 93.'),
                ('Q-H19-CARP','Carpathian H19','Carpathian','Purchased','H19','Active','Confirmed','Carpathian queen accepted.'),
                ('Q-N96-CARP','Carpathian N96','Carpathian','Purchased','N96','Active','Confirmed','Langstroth nuc.'),
            ]
            for q in queens:
                session.add(Queen(code=q[0], name=q[1], line=q[2], source=q[3], current_colony_code=q[4], status=q[5], evidence_status=q[6], notes=q[7]))

        if session.query(Equipment).count() == 0:
            equipment = [
                ('FEED-001','Abelo Ashford Poly Feeder','Feeder','H12','National','In use','Approx 1-1.5L syrup moved from Hive 15.'),
                ('SUPER-H15-001','Hive 15 First Super','Super','H15','National','Filling','First super being filled.'),
                ('SUPER-H15-002','Hive 15 Second Super','Super','H15','National','Empty','Second super empty.'),
                ('SUPER-H16-001','Hive 16 First Super','Super','H16','National','Nearly full','Heavy / nearly full.'),
                ('SUPER-H16-002','Hive 16 Second Super','Super','H16','National','Unused','Do not add third super yet.'),
            ]
            for e in equipment:
                session.add(Equipment(code=e[0], name=e[1], type=e[2], current_location=e[3], compatible_with=e[4], status=e[5], notes=e[6]))

        if session.query(GenealogyEvent).count() == 0:
            events = [
                ('2026-07-03','Brood donation','N91','NJOL','Q-JOLANTA','Nuc 91 donated 2 brood frames; queen seen.'),
                ('2026-07-03','Brood donation','N100','NJOL','Q-JOLANTA','Nuc 100 donated 1 brood frame; queen seen.'),
                ('2026-07-03','Transfer','N99','H12','','Nuc 99 became Hive 12.'),
            ]
            for ev in events:
                session.add(GenealogyEvent(date=ev[0], event_type=ev[1], source_colony=ev[2], target_colony=ev[3], queen_code=ev[4], details=ev[5]))

        if session.query(AuditLog).count() == 0:
            session.add(AuditLog(date=str(datetime.now().replace(microsecond=0)), action='BOOTSTRAP', entity_type='System', entity_code='AOS', details='Seeded v0.6.2 baseline data.'))
        session.commit()
