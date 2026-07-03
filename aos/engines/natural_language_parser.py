import re
from datetime import date
from aos.services.repository import Repository
WORDS={'no':0,'none':0,'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10}
def _num(x):
    if x is None: return 0
    x=str(x).lower()
    if x in WORDS: return WORDS[x]
    try: return float(x)
    except Exception: return 0
def detect_colony(text):
    lower=text.lower(); entities=Repository().list_apiary_entities(True)
    for e in sorted(entities,key=lambda x:len(x['code']),reverse=True):
        if re.search(rf"{re.escape(e['code'].lower())}",lower): return e
    m=re.search(r"hive\s*(\d+)",lower)
    if m:
        code='H'+m.group(1)
        for e in entities:
            if e['code']==code: return e
    m=re.search(r"nuc\s*(\d+)",lower)
    if m:
        code='N'+m.group(1)
        for e in entities:
            if e['code']==code: return e
    if 'jolanta' in lower:
        for e in entities:
            if e['code']=='NJOL': return e
    return None
def frame_count(text,terms):
    lower=text.lower(); tp='|'.join([re.escape(t) for t in terms]); patterns=[rf"(\d+(?:\.\d+)?|one|two|three|four|five|six|seven|eight|nine|ten)\s*(frames?|frame)?\s*(of\s*)?({tp})",rf"({tp})\s*(frames?|frame)?\s*(\d+(?:\.\d+)?|one|two|three|four|five|six|seven|eight|nine|ten)"]
    for p in patterns:
        m=re.search(p,lower)
        if m:
            for g in m.groups():
                if g and (_num(g) or g in WORDS): return _num(g)
    return 0
def parse_inspection_note(text):
    lower=text.lower(); entity=detect_colony(text)
    queen_seen=bool(re.search(r"queen\s+(seen|spotted|found|present)",lower))
    if re.search(r"queen\s+(not\s+seen|not found|missing)",lower): queen_seen=False
    eggs_seen=bool(re.search(r"eggs?|fresh eggs|laying",lower)) and not bool(re.search(r"no\s+eggs",lower))
    larvae_seen=bool(re.search(r"larvae|larva|open brood",lower)) and not bool(re.search(r"no\s+larvae",lower))
    q=re.search(r"(\d+|one|two|three|four|five|six|seven|eight|nine|ten|no|none)\s+(charged\s+)?queen\s+cells?",lower)
    queen_cells=int(_num(q.group(1))) if q else (1 if 'queen cell' in lower else 0)
    if re.search(r"no\s+queen\s+cells?",lower): queen_cells=0
    temperament='Calm' if 'calm' in lower else 'Defensive' if 'defensive' in lower else 'Aggressive' if 'aggressive' in lower else 'OK' if ' ok ' in f' {lower} ' or 'fine' in lower else 'Unknown'
    brood=frame_count(lower,['brood','capped brood']); stores=frame_count(lower,['stores','honey','food']); bees=frame_count(lower,['bees','bee coverage','covered with bees'])
    warnings=[]
    if not entity: warnings.append('Could not identify colony/nuc.')
    if brood==0 and stores==0 and bees==0: warnings.append('No frame counts detected.')
    confidence=30+(25 if entity else 0)+(15 if queen_seen or eggs_seen or larvae_seen else 0)+(20 if brood or stores or bees else 0)+(10 if temperament!='Unknown' else 0)-(10*len(warnings))
    return {'colony_id':entity['id'] if entity else None,'colony_code':entity['code'] if entity else '','inspection_date':str(date.today()),'queen_seen':queen_seen,'eggs_seen':eggs_seen,'larvae_seen':larvae_seen,'queen_cells':queen_cells,'brood_frames':brood,'stores_frames':stores,'bee_coverage_frames':bees,'temperament':temperament,'notes':text,'parser_confidence':max(0,min(100,confidence)),'warnings':warnings}
