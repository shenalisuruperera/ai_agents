# Work Agent Overview

## Purpose

The Work Agent automatically converts a work message into a confirmed Android alarm.

It separates Android interaction from business logic.

- Automate is responsible for Android interaction.
- Python is responsible for parsing, memory, travel calculations, and decision making.

This separation keeps the system reliable, easy to debug, and easy to extend.

## High Level Workflow

Message
  -> Automate
  -> work_inbox.txt
  -> run_work_parser.flag
  -> Termux:Tasker
  -> Python import_work_inbox.py
  -> Python process_imported_work.py
  -> pending_job.json and pending_job_display.txt
  -> Automate confirmation dialog
  -> Confirm / Edit / Reject
  -> process_job_confirmations.py
  -> travel_review.txt
  -> Travel OK or Enter Plus Code
  -> location_overrides.json if corrected
  -> alarm_request.txt
  -> Automate creates Android alarm

## Main Components

### Automate

Automate is responsible for:

- receiving messages
- showing dialogs
- collecting edits
- creating Android alarms
- triggering Termux through Termux:Tasker

Automate should not contain complex parsing logic.

### Python

Python is responsible for:

- parsing messages
- learning locations
- Google Routes API calls
- travel calculations
- persistent memory
- alarm calculations

Python should not directly interact with Android UI.

## Design Philosophy

The Work Agent follows four principles.

### 1. Confirm before saving

Every detected job is shown to the user before it is accepted.

### 2. Learn once

If a location is corrected once, it should automatically work next time.

Example:

Air Services -> 8RHJ+VV Melbourne Airport -> future jobs automatically use the corrected location.

### 3. Keep temporary data temporary

Files used only during processing are deleted after use.

Only useful long-term information is retained.

### 4. Keep responsibilities separate

Automate handles Android.

Python handles logic.

Shared files connect the two.

This makes the system easier to debug and easier to expand.
