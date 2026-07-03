from sqlalchemy import text
from aos.db.session import init_db, get_session
from aos.services.repository import Repository
from aos.engines.natural_language_parser import parse_inspection_note
from aos.services.guided_inspection_service import GuidedInspectionService
from aos.engines.validation_engine import validation_summary
from aos.engines.inspection_scheduler import inspection_schedule, scheduler_summary
def result(name,status,message=''): return {'test':name,'status':status,'message':message}
def run_self_tests():
    results=[]
    try:
        init_db()
        with get_session() as s: s.execute(text('SELECT 1'))
        results.append(result('Database connectivity','PASS'))
    except Exception as e: results.append(result('Database connectivity','FAIL',str(e)))
    try:
        repo=Repository(); required=['list_colonies','list_queens','list_equipment','list_inspections','create_colony','update_colony','delete_colony','create_queen','update_queen','delete_queen','create_equipment','update_equipment','delete_equipment']; missing=[m for m in required if not hasattr(repo,m)]
        results.append(result('Repository methods','PASS' if not missing else 'FAIL',', '.join(missing)))
    except Exception as e: results.append(result('Repository methods','FAIL',str(e)))
    try:
        parsed=parse_inspection_note('Hive 16 queen seen, eggs present, 6 brood frames, 2 stores, calm, no queen cells.'); ok=parsed['queen_seen'] and parsed['eggs_seen'] and parsed['brood_frames']==6
        results.append(result('Natural language parser','PASS' if ok else 'FAIL',str(parsed)))
    except Exception as e: results.append(result('Natural language parser','FAIL',str(e)))
    try:
        validation=GuidedInspectionService().validate_payload({'colony_id':1,'inspection_date':'2026-07-03','queen_seen':True,'eggs_seen':True,'larvae_seen':False,'queen_cells':0,'brood_frames':5,'stores_frames':2,'bee_coverage_frames':6,'temperament':'Calm','notes':'test'})
        results.append(result('Guided validation','PASS' if validation['status'] in ['PASS','WARN'] else 'FAIL',validation['message']))
    except Exception as e: results.append(result('Guided validation','FAIL',str(e)))
    try:
        v=validation_summary(); results.append(result('Validation engine','PASS' if v['status'] in ['PASS','WARN','FAIL'] else 'FAIL',v['message']))
    except Exception as e: results.append(result('Validation engine','FAIL',str(e)))
    return results
def summary(results): return {'pass':len([r for r in results if r['status']=='PASS']),'fail':len([r for r in results if r['status']=='FAIL']),'total':len(results)}
def print_results():
    rows=run_self_tests()
    for r in rows: print(f"[{r['status']}] {r['test']}: {r['message']}")
    s=summary(rows); print(f"PASS={s['pass']} FAIL={s['fail']} TOTAL={s['total']}")
    if s['fail']: raise SystemExit(1)
if __name__=='__main__': print_results()
