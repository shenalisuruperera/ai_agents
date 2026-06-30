# Automate Flow

## Purpose

The Automate flow is responsible for all Android interaction.

It should remain lightweight.

Complex logic belongs in Python.

The flow communicates with Python entirely through shared files.

---

# Main Flow

## 1. Receive message

Current behaviour:

A test variable called:

message

is used instead of a real WhatsApp notification.

Future versions may replace this with an actual WhatsApp trigger.

---

## 2. Write inbox

Automate writes the message to:

work_inbox.txt

This becomes the input for Python.

---

## 3. Trigger processing

Automate creates:

run_work_parser.flag

It then launches:

run_reminder_check.sh

through Termux:Tasker.

This starts the Python processing pipeline.

---

## 4. Pending confirmation

Python creates:

pending_job_display.txt

Automate displays this file to the user.

The user may:

- Confirm
- Reject
- Edit

---

## 5. Confirm

If confirmed:

confirm.flag

is created.

Python continues processing.

---

## 6. Reject / Edit

If edits are required:

Automate collects the required fields.

Supported edits:

- Date
- Start Time
- Address
- Job Type

Only edited fields are written.

The results are stored in:

edit_request.txt

Python applies the edits.

---

## 7. Travel review

Python creates:

travel_review.txt

Automate displays:

- destination
- travel time
- leave time

The user chooses:

Accept

or

Correct Location

---

## 8. Location correction

If travel is incorrect:

Automate asks for:

Google Maps address

or

Plus Code

The value is written as:

location_override=<value>

inside:

edit_request.txt

Automate creates:

confirm.flag

Python saves the corrected destination.

---

## 9. Alarm creation

Python creates:

alarm_request.txt

The file contains:

Line 1

Seconds after midnight

Line 2

Alarm title

Line 3

Alarm description

Automate reads the file and creates the Android alarm.

---

## 10. Cleanup

After successful completion Automate removes temporary shared files.

This prevents stale data from affecting future runs.

---

# Variables

Current important variables

message

Test work message.

selected

Checkbox selections from edit dialog.

new_date

Edited job date.

new_time

Edited start time.

new_address

Edited address.

new_job_type

Edited job type.

location_override

Corrected Maps destination or Plus Code.

---

# Design Principles

The Automate flow should:

- remain simple
- avoid business logic
- avoid parsing
- avoid duplicate calculations

Its purpose is to connect Android with Python.

All decision making belongs in Python.

---

# Future Improvements

Possible future enhancements:

- Replace test message with live WhatsApp trigger.
- Improve dialog layout.
- Better error messages.
- Optional progress notifications during processing.

No major structural changes are currently planned.
