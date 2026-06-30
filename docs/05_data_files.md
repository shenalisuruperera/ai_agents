# Data Files

This document describes every important file used by the Work Agent.

Files are divided into two groups:

- Shared files (Automate ↔ Python)
- Local Python data

---

# Shared Files

Location

/storage/emulated/0/AI_Agents/

(Termux path)

~/storage/shared/AI_Agents/

These files are temporary communication files between Automate and Python.

---

## work_inbox.txt

Created by

Automate

Read by

import_work_inbox.py

Purpose

Contains the raw work message.

Lifetime

Temporary

Safe to delete

Yes

---

## run_work_parser.flag

Created by

Automate

Read by

import_work_inbox.py

Purpose

Signals that a new work message is available.

Lifetime

Temporary

Safe to delete

Yes

---

## pending_job.json

Created by

process_imported_work.py

Read by

process_job_confirmations.py

Purpose

Stores the structured pending job before confirmation.

Lifetime

Temporary

Safe to delete

Yes

---

## pending_job_display.txt

Created by

process_imported_work.py

Read by

Automate

Purpose

Human-readable confirmation screen.

Lifetime

Temporary

Safe to delete

Yes

---

## confirm.flag

Created by

Automate

Read by

process_job_confirmations.py

Purpose

User confirmed the pending job.

Lifetime

Temporary

Safe to delete

Yes

---

## reject.flag

Created by

Automate

Read by

process_job_confirmations.py

Purpose

User rejected the pending job.

Lifetime

Temporary

Safe to delete

Yes

---

## edit_request.txt

Created by

Automate

Read by

process_job_confirmations.py

Purpose

Contains edited values.

Supported keys

date

start_time

address

job_type

location_override

Lifetime

Temporary

Safe to delete

Yes

---

## travel_review.txt

Created by

process_job_confirmations.py

Read by

Automate

Purpose

Displays

- resolved destination
- travel time
- leave time

Allows the user to verify travel before creating an alarm.

Lifetime

Temporary

Safe to delete

Yes

---

## alarm_request.txt

Created by

process_job_confirmations.py

Read by

Automate

Purpose

Requests Android alarm creation.

Format

Line 1

Seconds after midnight

Line 2

Alarm title

Line 3

Alarm description

Lifetime

Temporary

Safe to delete

Yes

---

# Python Data

Location

~/ai_agents/work/data/

These files are maintained by Python.

---

## jobs.json

Purpose

Stores confirmed jobs.

Permanent

Yes

Safe to delete

No

---

## location_overrides.json

Purpose

Permanent memory for corrected locations.

Example

Air Services

↓

8RHJ+VV Melbourne Airport

Permanent

Yes

Safe to delete

No

---

## travel_cache.json

Purpose

Caches Google travel estimates.

Uses

30-minute arrival buckets.

Permanent

No

Safe to delete

Yes

Deleting this file simply forces Google Maps to be queried again.

---

## imported_messages.txt

Purpose

Temporary imported message queue.

Permanent

No

Safe to delete

Yes

---


# Logs

Location

~/ai_agents/logs/

---

## scheduler.log

Purpose

Records execution history.

Useful for debugging.

Permanent

No

Safe to delete

Yes

---

# Design Philosophy

Only useful information should remain permanently.

Permanent memory

- jobs.json
- location_overrides.json

Everything else should either be:

- temporary
- cached
- automatically regenerated

This keeps the system easy to maintain and avoids unnecessary stored data.
