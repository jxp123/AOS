from datetime import date, datetime, timedelta
from aos.services.repository import Repository

DATE_FORMATS = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']


def parse_date(value):
    if not value:
        return None
    if isinstance(value, date):
        return value
    text = str(value).strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except Exception:
            pass
    # tolerate ISO datetime strings
    try:
        return datetime.fromisoformat(text).date()
    except Exception:
        return None


def strategy_for_colony(colony):
    ctype = (colony.get('type') or '').lower()
    objective = (colony.get('objective') or '').lower()
    notes = (colony.get('notes') or '').lower()

    # Default rule requested by user: inspect active hives and nucs every 7 days.
    strategy = 'Standard 7-day inspection'
    interval = 7
    reason = 'Default active hive/nuc 7-day inspection rule.'

    if 'queen rearing' in objective or 'mating' in objective or 'queen event' in objective:
        strategy = 'Queen event / mating watch'
        interval = 4
        reason = 'Queen event or mating context needs closer follow-up.'
    elif 'requeening' in objective or 'recover' in objective or 'split' in objective or 'brood donation' in notes:
        strategy = 'Recovery / requeening watch'
        interval = 5
        reason = 'Recovery, requeening or recent manipulation needs closer follow-up.'
    elif 'winter' in objective or 'observation' in objective:
        strategy = 'Observation / winter watch'
        interval = 14
        reason = 'Observation/winter context uses longer interval unless risk flags appear.'
    elif ctype == 'nuc':
        strategy = 'Standard nuc 7-day inspection'
        interval = 7
        reason = 'Default nuc rule: inspect every 7 days unless in recovery/queen event mode.'

    return {'strategy': strategy, 'interval_days': interval, 'reason': reason}


def inspection_schedule(today=None):
    today = today or date.today()
    repo = Repository()
    latest = repo.latest_inspection_by_colony()
    rows = []

    for colony in repo.list_apiary_entities(True):
        code = colony['code']
        strategy = strategy_for_colony(colony)
        last = latest.get(code)
        last_date = parse_date(last.get('date')) if last else None

        if last_date is None:
            days_since = None
            next_due = today
            days_until_due = 0
            status = '⚪ No inspection recorded'
            priority = 'High'
            action = 'Inspect as soon as possible and establish baseline.'
        else:
            days_since = (today - last_date).days
            next_due = last_date + timedelta(days=strategy['interval_days'])
            days_until_due = (next_due - today).days
            if days_until_due < 0:
                status = '🔴 Overdue'
                priority = 'High'
                action = 'Inspect today if weather allows.'
            elif days_until_due == 0:
                status = '🟠 Due today'
                priority = 'High'
                action = 'Inspect today.'
            elif days_until_due == 1:
                status = '🟡 Due tomorrow'
                priority = 'Medium'
                action = 'Prepare to inspect tomorrow.'
            elif days_until_due <= 2:
                status = '🟡 Due soon'
                priority = 'Medium'
                action = 'Inspect within the next 1–2 days.'
            else:
                status = '🟢 Recent'
                priority = 'Low'
                action = 'No inspection due yet.'

        rows.append({
            'code': code,
            'name': colony.get('name',''),
            'type': colony.get('type',''),
            'equipment': colony.get('equipment',''),
            'strategy': strategy['strategy'],
            'interval_days': strategy['interval_days'],
            'strategy_reason': strategy['reason'],
            'last_inspection': str(last_date) if last_date else '',
            'days_since': '' if days_since is None else days_since,
            'next_due': str(next_due),
            'days_until_due': days_until_due,
            'status': status,
            'priority': priority,
            'action': action,
        })

    priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
    rows.sort(key=lambda r: (priority_order.get(r['priority'], 9), r['days_until_due'], r['code']))
    return rows


def scheduler_summary():
    rows = inspection_schedule()
    overdue = [r for r in rows if 'Overdue' in r['status']]
    due_today = [r for r in rows if 'Due today' in r['status']]
    due_soon = [r for r in rows if 'Due soon' in r['status'] or 'Due tomorrow' in r['status']]
    no_record = [r for r in rows if 'No inspection' in r['status']]
    recent = [r for r in rows if 'Recent' in r['status']]
    return {
        'total': len(rows),
        'overdue': len(overdue),
        'due_today': len(due_today),
        'due_soon': len(due_soon),
        'no_record': len(no_record),
        'recent': len(recent),
    }


def todays_plan():
    return [r for r in inspection_schedule() if r['priority'] == 'High']


def rolling_plan(days=14):
    rows = inspection_schedule()
    today = date.today()
    plan = []
    for offset in range(days + 1):
        target = today + timedelta(days=offset)
        due = [r for r in rows if parse_date(r['next_due']) == target]
        plan.append({
            'date': str(target),
            'day': 'Today' if offset == 0 else 'Tomorrow' if offset == 1 else f'+{offset} days',
            'due_count': len(due),
            'due_items': ', '.join([r['code'] for r in due]) if due else '',
        })
    return plan
