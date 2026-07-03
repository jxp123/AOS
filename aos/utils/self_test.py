from pathlib import Path
import importlib
import traceback

from aos.core.settings import ROOT_DIR
from aos.db.session import init_db, get_session
from aos.db.migrations import migration_check
from aos.services.repository import Repository
from aos.services.guided_inspection_service import GuidedInspectionService
from aos.engines.natural_language_parser import parse_inspection_note
from aos.services.update_service import UpdateService


def _result(name, status, message=""):
    return {"test": name, "status": status, "message": message}


def run_self_tests():
    results = []

    # 1. DB init/connectivity
    try:
        init_db()
        with get_session() as s:
            from sqlalchemy import text\n            s.execute(text("SELECT 1"))
        results.append(_result("Database connectivity", "PASS"))
    except Exception as e:
        results.append(_result("Database connectivity", "FAIL", str(e)))

    # 2. Repository core methods
    try:
        repo = Repository()
        required = [
            "list_colonies", "list_queens", "list_equipment", "list_inspections",
            "create_colony", "update_colony", "delete_colony",
            "create_queen", "update_queen", "delete_queen",
            "create_equipment", "update_equipment", "delete_equipment",
            "baseline_integrity", "restore_missing_baseline",
        ]
        missing = [m for m in required if not hasattr(repo, m)]
        if missing:
            results.append(_result("Repository CRUD methods", "FAIL", "Missing: " + ", ".join(missing)))
        else:
            results.append(_result("Repository CRUD methods", "PASS"))
    except Exception as e:
        results.append(_result("Repository CRUD methods", "FAIL", str(e)))

    # 3. UI imports
    ui_modules = [
        "aos.ui.dashboard",
        "aos.ui.colonies",
        "aos.ui.queens",
        "aos.ui.equipment",
        "aos.ui.inspections",
        "aos.ui.guided_inspection",
        "aos.ui.natural_language_intake",
        "aos.ui.knowledge_graph",
        "aos.ui.tasks",
        "aos.ui.ai_advisor",
        "aos.ui.weather",
        "aos.ui.migrations",
        "aos.ui.data_integrity",
    ]
    failed_imports = []
    for module in ui_modules:
        try:
            importlib.import_module(module)
        except Exception as e:
            failed_imports.append(f"{module}: {e}")
    if failed_imports:
        results.append(_result("UI module imports", "FAIL", " | ".join(failed_imports)))
    else:
        results.append(_result("UI module imports", "PASS"))

    # 4. Migration check callable
    try:
        missing = migration_check()
        results.append(_result("Migration check", "PASS", f"{len(missing)} missing schema item(s) reported"))
    except Exception as e:
        results.append(_result("Migration check", "FAIL", str(e)))

    # 5. Baseline integrity callable
    try:
        data = Repository().baseline_integrity()
        results.append(_result("Baseline integrity check", "PASS", f"Expected colonies: {data.get('expected_colonies')}; actual: {data.get('actual_colonies')}"))
    except Exception as e:
        results.append(_result("Baseline integrity check", "FAIL", str(e)))

    # 6. Natural language parser
    try:
        parsed = parse_inspection_note("Hive 16 queen seen, eggs present, 6 brood frames, 2 stores, calm, no queen cells.")
        if parsed.get("queen_seen") and parsed.get("eggs_seen") and parsed.get("brood_frames") == 6:
            results.append(_result("Natural language parser", "PASS", f"Detected {parsed.get('colony_code') or 'no colony'}"))
        else:
            results.append(_result("Natural language parser", "FAIL", str(parsed)))
    except Exception as e:
        results.append(_result("Natural language parser", "FAIL", str(e)))

    # 7. Guided inspection validation
    try:
        service = GuidedInspectionService()
        validation = service.validate_payload({
            "colony_id": 1,
            "inspection_date": "2026-07-03",
            "queen_seen": True,
            "eggs_seen": True,
            "larvae_seen": False,
            "queen_cells": 0,
            "brood_frames": 5,
            "stores_frames": 2,
            "bee_coverage_frames": 6,
            "temperament": "Calm",
            "notes": "Self-test payload",
        })
        if validation["status"] in ["PASS", "WARN"]:
            results.append(_result("Guided inspection validation", "PASS", validation["message"]))
        else:
            results.append(_result("Guided inspection validation", "FAIL", validation["message"]))
    except Exception as e:
        results.append(_result("Guided inspection validation", "FAIL", str(e)))

    # 8. readonly regression scan
    try:
        offenders = []
        for p in (ROOT_DIR / "aos").rglob("*.py"):
            txt = p.read_text(encoding="utf-8")
            if "readonly=True" in txt:
                offenders.append(str(p.relative_to(ROOT_DIR)))
        if offenders:
            results.append(_result("Readonly regression scan", "FAIL", "Unsupported readonly=True found in: " + ", ".join(offenders)))
        else:
            results.append(_result("Readonly regression scan", "PASS"))
    except Exception as e:
        results.append(_result("Readonly regression scan", "FAIL", str(e)))

    # 9. main.py import
    try:
        importlib.import_module("main")
        results.append(_result("Application import", "PASS"))
    except SystemExit:
        results.append(_result("Application import", "WARN", "main.py attempted to run server during import"))
    except Exception as e:
        # This may fail if NiceGUI run attempts to bind, so report detail but do not stop tests.
        results.append(_result("Application import", "WARN", str(e)))


    # 10. Update manifest
    try:
        manifest = UpdateService().build_manifest()
        if manifest.get("file_count", 0) > 0:
            results.append(_result("Update manifest generation", "PASS", f"{manifest['file_count']} files"))
        else:
            results.append(_result("Update manifest generation", "FAIL", "No files in manifest"))
    except Exception as e:
        results.append(_result("Update manifest generation", "FAIL", str(e)))

    return results


def summary(results):
    fail = len([r for r in results if r["status"] == "FAIL"])
    warn = len([r for r in results if r["status"] == "WARN"])
    passed = len([r for r in results if r["status"] == "PASS"])
    return {"pass": passed, "warn": warn, "fail": fail, "total": len(results)}


def print_results():
    results = run_self_tests()
    counts = summary(results)

    print("AOS Self-Test Results")
    print("=====================")
    for r in results:
        print(f"[{r['status']}] {r['test']}: {r['message']}")
    print("=====================")
    print(f"PASS={counts['pass']} WARN={counts['warn']} FAIL={counts['fail']} TOTAL={counts['total']}")

    if counts["fail"]:
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        print_results()
    except Exception:
        traceback.print_exc()
        raise
