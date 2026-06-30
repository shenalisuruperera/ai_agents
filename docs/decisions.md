# Design Decisions

This document records important design decisions made during development.

The purpose is to explain WHY the system works the way it does.

Future modifications should consider these decisions before changing behaviour.

---

## Decision 1

Title

Automate handles Android.

Decision

Automate is responsible for:

- dialogs
- notifications
- Android alarms
- Android permissions
- launching Python

Python should never directly control Android UI.

Reason

Automate is significantly better suited to Android integration.

Python is better suited to business logic.

Status

Active

---

## Decision 2

Title

Python owns business logic.

Decision

All parsing, calculations, memory and Google API calls belong in Python.

Reason

Python is easier to maintain, debug and extend than large Automate flows.

Status

Active

---

## Decision 3

Title

Shared file communication.

Decision

Automate and Python communicate using shared files.

Reason

Android restrictions make direct execution unreliable.

Shared storage has proven to be reliable and easy to debug.

Status

Active

---

## Decision 4

Title

User confirmation before saving.

Decision

No parsed job is automatically accepted.

Every job must be confirmed by the user.

Reason

Incorrect alarms are worse than requiring one confirmation.

Reliability is more important than automation.

Status

Active

---

## Decision 5

Title

Location learning.

Decision

Corrected destinations are permanently stored.

Reason

The same workplace should never require repeated correction.

Status

Active

---

## Decision 6

Title

Case-insensitive matching.

Decision

Location keywords ignore upper and lower case.

Reason

Work messages frequently change capitalisation.

Status

Active

---

## Decision 7

Title

No fuzzy location matching.

Decision

Only exact keyword matches are used.

Reason

Avoid accidentally matching different workplaces with similar names.

The user should explicitly approve new variations.

Status

Active

---

## Decision 8

Title

Arrival-time routing.

Decision

Google Routes calculates travel based on the expected arrival time.

Reason

Traffic conditions vary significantly throughout the day.

Arrival-based routing produces more realistic leave times.

Status

Active

---

## Decision 9

Title

Travel cache.

Decision

Travel estimates are cached using 30-minute arrival buckets.

Reason

Reduces Google API usage while maintaining practical accuracy.

Status

Active

---

## Decision 10

Title

Minimal permanent storage.

Decision

Only valuable information is retained permanently.

Permanent data

- jobs.json
- location_overrides.json

Temporary files are deleted whenever possible.

Reason

Keeps the system simple and reduces unnecessary data.

Status

Active

---

## Decision 11

Title

Duplicate detection.

Decision

Duplicate detection in the parser may remain disabled during testing and correction workflows.

Reason

If a corrected job is reprocessed, a second alarm is preferable to silently ignoring the updated job.

The user can manually remove redundant alarms if required.

Status

Temporary

Review again before enabling live WhatsApp automation.

---

## Decision 12

Title

Documentation.

Decision

Every significant feature must include a documentation update.

Reason

Documentation should remain synchronised with the implementation.

Status

Permanent project rule

