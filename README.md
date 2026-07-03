# AOS v2.1 — Inspection Scheduler

This release makes the 7-day inspection rule explicit and visible.

## What is new

- **Inspection Scheduler** tab
- **Today's Inspection Plan** on the Morning Briefing
- Clear status for every hive and nuc:
  - 🔴 Overdue
  - 🟠 Due today
  - 🟡 Due soon
  - 🟢 Recent
  - ⚪ No inspection recorded
- Default active hive/nuc interval is **7 days**
- Higher-risk strategies can shorten the interval:
  - Queen rearing / mating: 4 days
  - Recovery / requeening / splits: 5 days
  - Standard active hive or nuc: 7 days
  - Winter / observation: longer interval
- Tasks now include overdue and due inspection actions
- AI export includes inspection schedule context

## Daily workflow

1. Open AOS.
2. Start with **Morning Briefing**.
3. Review **Today's Inspection Plan**.
4. Open **Inspection Scheduler** if you want the full list and 14-day plan.
5. Use **Guided Inspection** or **Natural Language** to record the inspection.

## Key principle

You should not need to calculate inspection dates manually. AOS now calculates them from the latest inspection record.
