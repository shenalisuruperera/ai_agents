# Architecture

## Summary

The Work Agent is split into two systems:

1. Automate on Android
2. Python inside Termux

They communicate through files in shared Android storage.

This is intentional because Automate is good at Android UI and alarms, while Python is better for parsing, API calls, and persistent logic.

## Storage bridge

Automate path:

/storage/emulated/0/AI_Agents/

Termux path:

~/storage/shared/AI_Agents/

Both paths point to the same shared folder.

## Automate responsibilities

Automate handles:

- message input
- writing work_inbox.txt
- creating run_work_parser.flag
- running Termux:Tasker
- showing confirmation dialogs
- collecting corrections
- reading alarm_request.txt
- creating Android alarms
- cleaning temporary shared files

## Python responsibilities

Python handles:

- importing messages
- parsing job details
- creating pending job files
- applying edits
- saving location overrides
- calling Google Routes API
- calculating leave time
- creating alarm_request.txt

## Main processing sequence

1. Automate writes message text to work_inbox.txt.
2. Automate creates run_work_parser.flag.
3. Termux:Tasker runs run_reminder_check.sh.
4. import_work_inbox.py imports the message.
5. process_imported_work.py parses the message.
6. pending_job.json and pending_job_display.txt are created.
7. Automate shows the pending job to the user.
8. User confirms, rejects, or edits the job.
9. process_job_confirmations.py applies the user decision.
10. travel_time.py calculates the travel estimate.
11. travel_review.txt is created for confirmation.
12. alarm_request.txt is created.
13. Automate creates the Android alarm.

## Why shared files are used

Direct execution between Automate and Termux can be blocked by Android permissions.

Shared files are reliable because both Automate and Termux can access external storage.

## Key design rule

Automate should control Android interaction.

Python should control logic.

If a feature requires parsing, memory, API calls, or decision making, it belongs in Python.
