import re
from datetime import date
from aos.services.repository import Repository

NUMBER_WORDS = {
    'zero': 0, 'none': 0, 'no': 0,
    'one': 1, 'a': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
    'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
    'half': 0.5,
}

def _num(value):
    if value is None:
        return 0
    value = str(value).strip().lower()
    if value in NUMBER_WORDS:
        return NUMBER_WORDS[value]
    try:
        return float(value)
    except Exception:
        return 0

def detect_colony(text):
    repo = Repository()
    lower = text.lower()
    entities = repo.list_apiary_entities(True)

    # Prefer exact code matches like H16, N100, NJOL
    for e in sorted(entities, key=lambda x: len(x['code']), reverse=True):
        code = e['code'].lower()
        if re.search(rf'\b{re.escape(code)}\b', lower):
            return e

    # Match "hive 16", "nuc 91"
    hive = re.search(r'\bhive\s*(\d+)\b', lower)
    if hive:
        code = f"H{hive.group(1)}"
        for e in entities:
            if e['code'].lower() == code.lower():
                return e

    nuc = re.search(r'\bnuc\s*(\d+)\b', lower)
    if nuc:
        code = f"N{nuc.group(1)}"
        for e in entities:
            if e['code'].lower() == code.lower():
                return e

    if 'jolanta' in lower:
        for e in entities:
            if e['code'] == 'NJOL':
                return e

    return None

def extract_frame_count(text, terms):
    lower = text.lower()
    term_pattern = '|'.join([re.escape(t) for t in terms])
    patterns = [
        rf'(?P<num>\d+(?:\.\d+)?|one|two|three|four|five|six|seven|eight|nine|ten|half)\s*(?:frames?|frame)?\s*(?:of\s*)?(?P<term>{term_pattern})',
        rf'(?P<term>{term_pattern})\s*(?:frames?|frame)?\s*(?P<num>\d+(?:\.\d+)?|one|two|three|four|five|six|seven|eight|nine|ten|half)',
    ]
    for pattern in patterns:
        m = re.search(pattern, lower)
        if m:
            return _num(m.group('num'))
    return 0

def parse_inspection_note(text):
    lower = text.lower()
    warnings = []
    entity = detect_colony(text)

    queen_seen = bool(re.search(r'queen\s+(seen|spotted|found|present)', lower))
    if re.search(r'queen\s+(not\s+seen|not found|missing)', lower):
        queen_seen = False

    eggs_seen = bool(re.search(r'\beggs?\b|fresh eggs|laying', lower))
    if re.search(r'no\s+eggs|eggs\s+not\s+seen', lower):
        eggs_seen = False

    larvae_seen = bool(re.search(r'\blarvae\b|larva|young brood|open brood', lower))
    if re.search(r'no\s+larvae|larvae\s+not\s+seen', lower):
        larvae_seen = False

    qcell_match = re.search(r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten|no|none)\s+(charged\s+)?queen\s+cells?', lower)
    if qcell_match:
        queen_cells = int(_num(qcell_match.group(1)))
    elif 'queen cell' in lower or 'queen cells' in lower:
        queen_cells = 1
    else:
        queen_cells = 0
    if re.search(r'no\s+queen\s+cells?', lower):
        queen_cells = 0

    brood_frames = extract_frame_count(lower, ['brood', 'capped brood'])
    stores_frames = extract_frame_count(lower, ['stores', 'honey', 'food'])
    bee_coverage_frames = extract_frame_count(lower, ['bees', 'bee coverage', 'covered with bees'])

    if 'calm' in lower:
        temperament = 'Calm'
    elif 'defensive' in lower:
        temperament = 'Defensive'
    elif 'aggressive' in lower:
        temperament = 'Aggressive'
    elif 'ok' in lower or 'fine' in lower:
        temperament = 'OK'
    else:
        temperament = 'Unknown'

    if not entity:
        warnings.append('Could not identify colony/nuc. Select one manually before staging.')
    if brood_frames == 0 and stores_frames == 0 and bee_coverage_frames == 0:
        warnings.append('No frame counts detected.')
    if 'queen cell' in lower and queen_cells == 0:
        warnings.append('Queen cells mentioned but count unclear.')

    score = 30
    if entity:
        score += 25
    if queen_seen or eggs_seen or larvae_seen:
        score += 15
    if brood_frames or stores_frames or bee_coverage_frames:
        score += 20
    if temperament != 'Unknown':
        score += 10
    if warnings:
        score -= 10 * len(warnings)
    score = max(0, min(100, score))

    return {
        'colony_id': entity['id'] if entity else None,
        'colony_code': entity['code'] if entity else '',
        'inspection_date': str(date.today()),
        'queen_seen': queen_seen,
        'eggs_seen': eggs_seen,
        'larvae_seen': larvae_seen,
        'queen_cells': queen_cells,
        'brood_frames': brood_frames,
        'stores_frames': stores_frames,
        'bee_coverage_frames': bee_coverage_frames,
        'temperament': temperament,
        'notes': text,
        'parser_confidence': score,
        'warnings': warnings,
    }
