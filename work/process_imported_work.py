import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

from work_job_agent import parse_job

BASE = Path.home() / "ai_agents"
WORK = BASE / "work" / "data"
IMPORTED = WORK / "imported_messages.txt"
JOBS_FILE = WORK / "jobs.json"

SHARED = Path.home() / "storage/shared/AI_Agents"
PENDING = SHARED / "pending_job.json"
DISPLAY = SHARED / "pending_job_display.txt"
ALARM_REQUEST = SHARED / "alarm_request.txt"
TRAVEL_REVIEW = SHARED / "travel_review.txt"
EDIT_REQUEST = SHARED / "edit_request.txt"
CONFIRM = SHARED / "confirm.flag"
REJECT = SHARED / "reject.flag"


def load_json(path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text())


def same_job(a, b):
    return (
        a.get("date") == b.get("date")
        and a.get("start_time") == b.get("start_time")
        and a.get("address", "").strip().lower() == b.get("address", "").strip().lower()
        and a.get("job_type", "").strip().lower() == b.get("job_type", "").strip().lower()
    )


def job_already_exists(job):
    jobs = load_json(JOBS_FILE, [])

    for existing in jobs:
        if same_job(existing, job):
            return True

    if PENDING.exists():
        pending = load_json(PENDING, {})
        pending_job = pending.get("job", pending)
        if same_job(pending_job, job):
            return True

    return False


def clear_old_shared_outputs():
    for path in [ALARM_REQUEST, TRAVEL_REVIEW, EDIT_REQUEST, CONFIRM, REJECT]:
        path.unlink(missing_ok=True)


def notify_pending(job):
    subprocess.run([
        "termux-notification",
        "--title", "Work job needs confirmation",
        "--content", f"{job['start_time']} | {job['address']} | {job['job_type']}"
    ])


def make_display_text(job):
    return f"""WORK JOB DETECTED

Date: {job['date']}
Time: {job['start_time']}
Address: {job['address']}
Job Type: {job['job_type']}

Original Message:
-----------------
{job['raw_message']}
"""


if not IMPORTED.exists():
    print("No imported messages.")
    raise SystemExit

text = IMPORTED.read_text().strip()

if not text:
    print("Imported messages empty.")
    IMPORTED.unlink(missing_ok=True)
    raise SystemExit

parts = [p.strip() for p in text.split("---") if p.strip()]

pending_count = 0
duplicate = 0
uncertain = 0

for part in parts:
    job = parse_job(part)

    if not (job["start_time"] and job["address"]):
        uncertain += 1
        print("Uncertain, not saved:")
        print(part)
        continue

    if job_already_exists(job):
        duplicate += 1
        print(f"Duplicate skipped: {job['start_time']} {job['address']}")
        continue

    clear_old_shared_outputs()

    pending_item = {
        "status": "pending",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "expires_at": (datetime.now() + timedelta(hours=1)).isoformat(timespec="seconds"),
        "job": job
    }

    PENDING.write_text(json.dumps(pending_item, indent=2))
    DISPLAY.write_text(make_display_text(job))
    notify_pending(job)

    pending_count += 1
    print(f"Pending: {job['start_time']} {job['address']}")

IMPORTED.unlink(missing_ok=True)

print(f"Done. Pending={pending_count}, duplicate={duplicate}, uncertain={uncertain}")
