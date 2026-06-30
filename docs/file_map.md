# File Map

This document describes every file used by the Work Agent, who creates it, who reads it, and whether it is permanent.

---

# Shared Files

Location

/storage/emulated/0/AI_Agents/

(Termux)

/storage/shared/AI_Agents/

| File | Created By | Read By | Lifetime | Safe to Delete |
|------|------------|----------|----------|----------------|
| work_inbox.txt | Automate | import_work_inbox.py | Temporary | Yes |
| run_work_parser.flag | Automate | import_work_inbox.py | Temporary | Yes |
| pending_job.json | process_imported_work.py | process_job_confirmations.py | Temporary | Yes |
| pending_job_display.txt | process_imported_work.py | Automate | Temporary | Yes |
| confirm.flag | Automate | process_job_confirmations.py | Temporary | Yes |
| reject.flag | Automate | process_job_confirmations.py | Temporary | Yes |
| edit_request.txt | Automate | process_job_confirmations.py | Temporary | Yes |
| travel_review.txt | process_job_confirmations.py | Automate | Temporary | Yes |
| alarm_request.txt | process_job_confirmations.py | Automate | Temporary | Yes |

---

# Local Data

Location

~/ai_agents/work/data/

| File | Created By | Read By | Lifetime | Safe to Delete |
|------|------------|----------|----------|----------------|
| jobs.json | process_job_confirmations.py | Work Agent | Permanent | No |
| location_overrides.json | process_job_confirmations.py | travel_time.py | Permanent | No |
| travel_cache.json | travel_time.py | travel_time.py | Cache | Yes |
| imported_messages.txt | import_work_inbox.py | process_imported_work.py | Temporary | Yes |

---

# Logs

| File | Purpose |
|------|---------|
| scheduler.log | Complete execution history for debugging |

---

# Processing Pipeline

Automate
    │
    ▼
work_inbox.txt
    │
    ▼
run_work_parser.flag
    │
    ▼
run_reminder_check.sh
    │
    ▼
import_work_inbox.py
    │
    ▼
imported_messages.txt
    │
    ▼
process_imported_work.py
    │
    ├────────► pending_job.json
    │
    └────────► pending_job_display.txt
                    │
                    ▼
             Automate Dialog
                    │
        ┌───────────┴───────────┐
        │                       │
     Confirm                Reject/Edit
        │                       │
        └───────────┬───────────┘
                    ▼
      process_job_confirmations.py
                    │
        ├────────► jobs.json
        ├────────► travel_review.txt
        ├────────► location_overrides.json
        └────────► alarm_request.txt
                    │
                    ▼
              Automate Alarm

---

# Design Notes

The Work Agent intentionally keeps only two important permanent data files:

- jobs.json
- location_overrides.json

Everything else is either:

- temporary
- cache
- regenerated automatically

This keeps the system lightweight and easy to recover if temporary files are deleted.
