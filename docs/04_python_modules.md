# Python Modules

This document describes every Python module used by the Work Agent.

The goal is to make each module responsible for one task only.

---

# Processing Order

The normal execution order is:

run_reminder_check.sh

↓

import_work_inbox.py

↓

process_imported_work.py

↓

process_job_confirmations.py

↓

travel_time.py

↓

notify_due_reminders.py

---

# run_reminder_check.sh

## Purpose

Main entry point.

Runs every Python module in the correct order.

## Called by

Automate through Termux:Tasker.

## Responsibilities

- import work messages
- process imported work
- process confirmations
- check reminders
- write scheduler log

---

# import_work_inbox.py

## Purpose

Imports messages from Automate.

## Reads

work_inbox.txt

run_work_parser.flag

## Writes

imported_messages.txt

## Deletes

run_work_parser.flag

work_inbox.txt

## Notes

Acts as the bridge between Automate and Python.

No parsing occurs here.

---

# process_imported_work.py

## Purpose

Parses imported work messages.

## Reads

imported_messages.txt

## Creates

pending_job.json

pending_job_display.txt

## Uses

work_job_agent.py

## Responsibilities

- detect work jobs
- parse message
- create pending confirmation
- prevent invalid jobs
- notify user

No travel calculations occur here.

---

# work_job_agent.py

## Purpose

Contains all parsing logic.

## Extracts

- date
- time
- address
- job type

## Also provides

- parser helper functions
- address detection
- job creation

This module should contain parsing only.

---

# process_job_confirmations.py

## Purpose

Processes user decisions.

## Reads

pending_job.json

confirm.flag

reject.flag

edit_request.txt

## Writes

jobs.json

travel_review.txt

alarm_request.txt

location_overrides.json

## Responsibilities

- apply edits
- reject jobs
- update existing jobs
- create travel review
- create alarm request
- save learned locations

---

# travel_time.py

## Purpose

Google Maps interface.

## Responsibilities

- resolve saved locations
- call Google Routes API
- cache travel estimates
- calculate arrival-time travel
- save location overrides

## Reads

location_overrides.json

travel_cache.json

## Writes

travel_cache.json

location_overrides.json

---

# notify_due_reminders.py

## Purpose

Checks general reminders.

The Work Agent itself creates Android alarms directly through Automate.

This module remains available for non-work reminders.

---

# Shared Design Rules

Every module should have one clear responsibility.

Modules should communicate through files rather than directly calling each other whenever possible.

Business logic belongs in Python.

Android interaction belongs in Automate.

---

# Adding New Modules

When creating a new module:

1. Give it one responsibility.
2. Clearly define its inputs.
3. Clearly define its outputs.
4. Avoid duplicating existing logic.
5. Update this document.
