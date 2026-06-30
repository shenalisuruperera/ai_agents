# Work Agent

## Purpose

The Work Agent automatically converts a work message into a confirmed Android alarm.

Its goal is to minimise manual data entry while ensuring the user always confirms important information before it is permanently saved.

---

# Inputs

The Work Agent currently accepts a message from Automate.

During testing this is provided through the variable:

message

In production this can later come directly from a WhatsApp notification.

---

# Information extracted

The parser attempts to identify:

- Job date
- Start time
- Address
- Job type
- Original message

The original message is always retained during processing so the user can verify the parser's output.

---

# Workflow

## Stage 1 — Import

Automate writes:

work_inbox.txt

Automate then creates:

run_work_parser.flag

Termux:Tasker starts the processing pipeline.

---

## Stage 2 — Parsing

Python reads the message.

The parser extracts:

- date
- start time
- address
- job type

A pending job is created.

Nothing is permanently accepted yet.

---

## Stage 3 — Confirmation

Automate displays the pending job.

The user can:

- Confirm
- Reject
- Edit

No job is saved without confirmation.

---

## Stage 4 — Travel review

After confirmation, Google Routes estimates travel time.

The user is shown:

- Job address
- Estimated travel time
- Leave time

The user may:

- Accept the estimate
- Enter a corrected Google Maps address or Plus Code

---

## Stage 5 — Location learning

If a corrected destination is entered, the Work Agent saves it as a permanent override.

Future jobs using the same keyword automatically resolve to the saved destination.

Example:

Air Services

↓

8RHJ+VV Melbourne Airport

↓

Future travel calculations use the saved destination.

---

## Stage 6 — Alarm generation

Python calculates:

Leave Time

=

Job Start Time

− Travel Time

− User Buffer

An alarm request is written.

Automate creates the Android alarm.

---

# Long-term memory

The Work Agent intentionally remembers only useful information.

Permanent:

- location_overrides.json

Temporary:

- pending_job.json
- travel_review.txt
- alarm_request.txt
- work_inbox.txt
- edit_request.txt

Temporary files are deleted once they are no longer required.

---

# Error handling

If parsing is uncertain:

- no job is saved
- the original message remains available
- the user can manually correct information

If Google Maps cannot calculate travel time:

- a default travel time is used
- the user still has the opportunity to correct the destination

---

# Design goals

The Work Agent prioritises:

1. Reliability over automation
2. User confirmation before saving
3. Minimal permanent data
4. Easy debugging
5. Modular design for future expansion
