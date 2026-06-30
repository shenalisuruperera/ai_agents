# Testing

## Purpose

This document describes the standard tests for the Work Agent.

Whenever changes are made, these tests should be completed before committing to Git.

---

# Test 1 — Python Syntax

Ensure every Python file compiles.

Command

~/ai_agents/.venv/bin/python -m py_compile work/*.py reminder/*.py

Expected result

No output.

---

# Test 2 — Message Parsing

Use the Automate testing variable:

message

Run the Work Agent.

Verify:

✓ Correct date

✓ Correct start time

✓ Correct address

✓ Correct job type

If any field is incorrect:

Reject

↓

Edit

↓

Confirm

---

# Test 3 — Pending Confirmation

Confirm that:

pending_job_display.txt

contains the expected information.

Automate should display exactly what Python generated.

---

# Test 4 — Edit Workflow

Reject the job.

Edit:

- Date
- Time
- Address
- Job Type

Confirm again.

Verify that the updated values appear correctly.

---

# Test 5 — Travel Review

Confirm the job.

Verify that:

travel_review.txt

contains:

- Original address
- Resolved destination
- Travel time
- Arrival time
- Leave time

---

# Test 6 — Location Learning

Use an unknown location.

Example

Air Services

Reject the travel estimate.

Enter a Plus Code or Google Maps address.

Confirm.

Verify:

location_overrides.json

contains the new mapping.

Run the same job again.

The corrected destination should be used automatically.

No additional correction should be required.

---

# Test 7 — Alarm Request

Verify that:

alarm_request.txt

contains:

Line 1

Seconds after midnight

Line 2

Alarm title

Line 3

Alarm description

Automate should successfully create the Android alarm.

---

# Test 8 — Cleanup

After the workflow finishes:

Shared folder should not contain stale temporary files.

Typical remaining files:

None

or

Files currently waiting for user confirmation.

---

# Test 9 — Travel Cache

Delete

travel_cache.json

Run the same job.

Verify:

- Google Routes is queried.
- A new cache entry is created.
- Future runs use the cache.

---

# Test 10 — Scheduler Log

Check:

~/ai_agents/logs/scheduler.log

Verify:

- no Python tracebacks
- expected workflow
- successful confirmation
- successful alarm creation

---

# Regression Testing

Every significant change should repeat:

✓ Parsing

✓ Confirmation

✓ Editing

✓ Travel Review

✓ Location Learning

✓ Alarm Creation

Only commit after all regression tests pass.

---

# Debugging Checklist

If a workflow fails:

1. Check scheduler.log.

2. Check shared files.

3. Verify pending_job.json.

4. Verify edit_request.txt.

5. Verify location_overrides.json.

6. Verify travel_cache.json.

7. Verify alarm_request.txt.

Most issues can be located by following the files in this order.
