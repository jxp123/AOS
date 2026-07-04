from datetime import date
from aos.services.repository import Repository

try:
    from aos.engines.inspection_scheduler import inspection_schedule
except Exception:
    inspection_schedule = None

try:
    from aos.engines.task_engine import generated_tasks
except Exception:
    generated_tasks = None

def _priority_rank(priority):
    return {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}.get(priority, 9)

def _status_priority(status):
    s = (status or "").lower()
    if "critical" in s:
        return "Critical"
    if "overdue" in s:
        return "High"
    if "due today" in s or s == "due":
        return "High"
    if "due soon" in s:
        return "Medium"
    return "Low"

def _estimate_minutes(item):
    status = (item.get("status") or "").lower()
    colony = item.get("code") or item.get("colony_code") or ""
    base = 8
    if colony.startswith("N"):
        base = 6
    if "overdue" in status or item.get("priority") in ["Critical", "High"]:
        base += 4
    reason = (item.get("reason") or item.get("recommendation") or "").lower()
    if "queen" in reason or "brood congestion" in reason:
        base += 3
    if "super" in reason or "feed" in reason or "stores" in reason:
        base += 2
    return base

def _equipment_for_item(item):
    reason = (item.get("reason") or item.get("recommendation") or item.get("task_type") or "").lower()
    kit = ["Smoker", "Fuel", "Hive tool", "Notebook/phone"]
    if "queen" in reason:
        kit += ["Queen clip", "Marking pen"]
    if "feed" in reason or "stores" in reason:
        kit += ["Feeder", "Syrup/fondant as appropriate"]
    if "super" in reason or "honey" in reason:
        kit += ["Spare super", "Queen excluder check"]
    if "nuc" in reason or (item.get("colony_code") or item.get("code") or "").startswith("N"):
        kit += ["Spare nuc frames", "Compatible brood box check"]
    return list(dict.fromkeys(kit))

def _route_sort_key(code):
    if not code:
        return (99, 999)
    import re
    m = re.search(r"(\d+)", code)
    num = int(m.group(1)) if m else 999
    prefix_rank = 0 if code.startswith("H") else 1 if code.startswith("N") else 2
    return (prefix_rank, num)

def inspection_queue():
    rows = []
    if inspection_schedule:
        try:
            rows = inspection_schedule()
        except Exception:
            rows = []
    if not rows:
        repo = Repository()
        rows = [{"code": c["code"], "name": c["name"], "status": "Unknown", "days_since": "", "reason": "No scheduler data"} for c in repo.list_apiary_entities(True)]

    queue = []
    for r in rows:
        code = r.get("code") or r.get("colony_code") or ""
        status = r.get("status") or r.get("inspection_status") or "Unknown"
        priority = _status_priority(status)
        if priority in ["Critical", "High", "Medium"]:
            reason = r.get("reason", r.get("recommendation", "Inspection scheduling"))
            queue.append({
                "code": code,
                "name": r.get("name", code),
                "status": status,
                "priority": priority,
                "days_since": r.get("days_since", r.get("days_since_inspection", "")),
                "reason": reason,
                "estimated_minutes": _estimate_minutes({"status": status, "priority": priority, "code": code, "reason": reason}),
                "equipment": ", ".join(_equipment_for_item({"status": status, "priority": priority, "code": code, "reason": reason})),
            })
    queue.sort(key=lambda x: (_priority_rank(x["priority"]), _route_sort_key(x["code"])))
    return queue

def operations_tasks():
    rows = []
    if generated_tasks:
        try:
            rows = generated_tasks()
        except Exception:
            rows = []
    tasks = []
    for t in rows:
        tasks.append({
            "date": t.get("date", str(date.today())),
            "priority": t.get("priority", "Medium"),
            "colony_code": t.get("colony_code", ""),
            "task_type": t.get("task_type", "Task"),
            "reason": t.get("reason", ""),
            "recommendation": t.get("recommendation", ""),
            "estimated_minutes": _estimate_minutes(t),
            "equipment": ", ".join(_equipment_for_item(t)),
        })
    tasks.sort(key=lambda x: (_priority_rank(x["priority"]), _route_sort_key(x["colony_code"])))
    return tasks

def todays_work():
    queue = inspection_queue()
    tasks = operations_tasks()
    high_tasks = [t for t in tasks if t["priority"] in ["Critical", "High"]]
    combined_minutes = sum(i["estimated_minutes"] for i in queue) + sum(t["estimated_minutes"] for t in high_tasks)
    return {
        "date": str(date.today()),
        "overdue": len([i for i in queue if "overdue" in (i["status"] or "").lower()]),
        "due_today": len([i for i in queue if "due today" in (i["status"] or "").lower() or (i["status"] or "").lower() == "due"]),
        "due_soon": len([i for i in queue if "due soon" in (i["status"] or "").lower()]),
        "high_tasks": len(high_tasks),
        "estimated_minutes": combined_minutes,
        "estimated_duration": f"{combined_minutes // 60}h {combined_minutes % 60}m" if combined_minutes >= 60 else f"{combined_minutes}m",
        "inspection_queue": queue,
        "high_priority_tasks": high_tasks,
        "route": [i["code"] for i in sorted(queue, key=lambda x: _route_sort_key(x["code"]))],
        "equipment_checklist": sorted(set(item for row in queue + high_tasks for item in row["equipment"].split(", ") if item)),
    }

def shift_briefing():
    work = todays_work()
    parts = [
        f"Today you have {len(work['inspection_queue'])} inspection item(s) in the queue.",
        f"{work['overdue']} overdue, {work['due_today']} due today, {work['due_soon']} due soon.",
        f"There are {work['high_tasks']} high-priority operational task(s).",
        f"Estimated apiary visit duration is {work['estimated_duration']}.",
    ]
    if work["inspection_queue"]:
        top = work["inspection_queue"][0]
        parts.append(f"Highest priority: {top['code']} because {top['reason']}.")
    if work["route"]:
        parts.append("Suggested route: " + " → ".join(work["route"]) + ".")
    return " ".join(parts)
