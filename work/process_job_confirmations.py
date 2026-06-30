import json
from pathlib import Path
from datetime import datetime, timedelta

from travel_time import get_travel_minutes, save_location_override, get_resolved_address

BASE = Path.home() / "ai_agents"
WORK = BASE / "work" / "data"

JOBS_FILE = WORK / "jobs.json"
REMINDERS_FILE = BASE / "reminders.json"

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


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2))


def clear_flags_only():
    CONFIRM.unlink(missing_ok=True)
    EDIT_REQUEST.unlink(missing_ok=True)


def full_cleanup():
    PENDING.unlink(missing_ok=True)
    DISPLAY.unlink(missing_ok=True)
    ALARM_REQUEST.unlink(missing_ok=True)
    TRAVEL_REVIEW.unlink(missing_ok=True)
    EDIT_REQUEST.unlink(missing_ok=True)
    CONFIRM.unlink(missing_ok=True)
    REJECT.unlink(missing_ok=True)


def load_edits():
    edits = {}
    if not EDIT_REQUEST.exists():
        return edits

    for line in EDIT_REQUEST.read_text().splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            edits[key.strip()] = value.strip()

    return edits


def is_bad_value(value):
    return value.strip().lower() in {"y", "n", "yes", "no", "confirm", "reject", "ok"}

def apply_edits(job, edits):
    for key in ["date", "start_time", "address", "job_type"]:
        if key in edits and edits[key] and not is_bad_value(edits[key]):
            job[key] = edits[key]

    if edits:
        job["edited_at"] = datetime.now().isoformat(timespec="seconds")
        job["edits_applied"] = edits

    return job


def same_job(a, b):
    return (
        a.get("date") == b.get("date")
        and a.get("start_time") == b.get("start_time")
        and a.get("address", "").strip().lower() == b.get("address", "").strip().lower()
        and a.get("job_type", "").strip().lower() == b.get("job_type", "").strip().lower()
    )


def create_alarm_request(job):
    date = job.get("date")
    start_time = job.get("start_time")
    address = job.get("address", "")
    job_type = job.get("job_type", "Work")

    if not date or not start_time:
        return

    start_dt = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
    travel_minutes = get_travel_minutes(address, arrival_dt=start_dt) if address else 60
    alarm_dt = start_dt - timedelta(minutes=travel_minutes + 30)

    seconds_after_midnight = alarm_dt.hour * 3600 + alarm_dt.minute * 60 + alarm_dt.second

    label = f"Leave for work: {address or 'address not detected'}"
    details = f"{job_type} starts at {start_time}. Travel {travel_minutes} min + 30 min buffer."

    resolved_address = get_resolved_address(address) if address else ""

    TRAVEL_REVIEW.write_text(
        f"Travel estimate\n\n"
        f"Job address: {address or 'address not detected'}\n"
        f"Maps destination: {resolved_address or 'address not detected'}\n"
        f"Travel time: {travel_minutes} minutes\n"
        f"Arrival time used: {start_dt.strftime('%H:%M')}\n"
        f"Leave alarm: {alarm_dt.strftime('%H:%M')}\n\n"
        f"{details}\n"
    )

    ALARM_REQUEST.write_text(
        f"{seconds_after_midnight}\n"
        f"{label}\n"
        f"{details}\n"
    )



def confirm_pending(reason):
    if not PENDING.exists():
        print("No pending job to confirm.")
        clear_flags_only()
        return

    pending = load_json(PENDING, {})
    pending_items = pending if isinstance(pending, list) else [pending]

    jobs = load_json(JOBS_FILE, [])
    edits = load_edits()

    added = 0
    updated = 0

    for item in pending_items:
        job = item.get("job", item)
        original_address = job.get("address", "")

        if edits.get("location_override") and original_address:
            save_location_override(original_address, edits["location_override"])
            print(f"Saved location override: {original_address} -> {edits['location_override']}")

        job = apply_edits(job, edits)

        job["confirmed_at"] = datetime.now().isoformat(timespec="seconds")
        job["confirmation_reason"] = reason

        existing_index = None
        for i, existing in enumerate(jobs):
            if same_job(existing, job):
                existing_index = i
                break

        if existing_index is None:
            jobs.append(job)
            added += 1
        else:
            jobs[existing_index].update(job)
            updated += 1

        create_alarm_request(job)

    save_json(JOBS_FILE, jobs)
    clear_flags_only()

    print(f"Confirmed {added} new job(s), updated {updated} existing job(s). Reason: {reason}")


if CONFIRM.exists():
    confirm_pending("manual_or_edited")
    raise SystemExit


if REJECT.exists():
    full_cleanup()
    print("Rejected pending job(s).")
    raise SystemExit


if PENDING.exists():
    pending = load_json(PENDING, {})
    item = pending[0] if isinstance(pending, list) else pending
    expires_at = item.get("expires_at")

    if expires_at and datetime.now() >= datetime.fromisoformat(expires_at):
        confirm_pending("auto_timeout")
        raise SystemExit

    print("Pending job exists, waiting for confirmation.")
    raise SystemExit


print("No confirmation flags.")
