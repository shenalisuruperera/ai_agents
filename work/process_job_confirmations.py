import json
from pathlib import Path
from datetime import datetime, timedelta

from travel_time import get_travel_minutes

BASE = Path.home() / "ai_agents"
WORK = BASE / "work" / "data"

JOBS_FILE = WORK / "jobs.json"
REMINDERS_FILE = BASE / "reminders.json"

SHARED = Path.home() / "storage/shared/AI_Agents"
PENDING = SHARED / "pending_job.json"
DISPLAY = SHARED / "pending_job_display.txt"
ALARM_REQUEST = SHARED / "alarm_request.txt"
CONFIRM = SHARED / "confirm.flag"
REJECT = SHARED / "reject.flag"


def load_json(path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text())


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2))


def cleanup():
    PENDING.unlink(missing_ok=True)
    DISPLAY.unlink(missing_ok=True)
    CONFIRM.unlink(missing_ok=True)
    REJECT.unlink(missing_ok=True)


def create_alarm_request(job):
    date = job.get("date")
    start_time = job.get("start_time")
    address = job.get("address", "")
    job_type = job.get("job_type", "Work")

    if not date or not start_time:
        return

    start_dt = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
    travel_minutes = get_travel_minutes(address) if address else 60

    alarm_dt = start_dt - timedelta(minutes=travel_minutes + 30)

    seconds_after_midnight = (
        alarm_dt.hour * 3600 +
        alarm_dt.minute * 60 +
        alarm_dt.second
    )

    label = f"Leave for work: {address or 'address not detected'}"
    details = f"{job_type} starts at {start_time}. Travel {travel_minutes} min + 30 min buffer."

    ALARM_REQUEST.write_text(
        f"{seconds_after_midnight}\n"
        f"{label}\n"
        f"{details}\n"
    )

    reminders = load_json(REMINDERS_FILE, [])
    reminders.append({
        "task": label,
        "date": alarm_dt.strftime("%Y-%m-%d"),
        "time": alarm_dt.strftime("%H:%M"),
        "notes": details,
        "done": False
    })
    save_json(REMINDERS_FILE, reminders)


if CONFIRM.exists():
    pending = load_json(PENDING, {})

    pending_items = pending if isinstance(pending, list) else [pending]
    jobs = load_json(JOBS_FILE, [])

    for item in pending_items:
        job = item.get("job", item)
        job["confirmed_at"] = datetime.now().isoformat(timespec="seconds")
        jobs.append(job)
        create_alarm_request(job)

    save_json(JOBS_FILE, jobs)
    cleanup()

    print(f"Confirmed {len(pending_items)} job(s) and created alarm request.")
    raise SystemExit


if REJECT.exists():
    cleanup()
    print("Rejected pending job(s).")
    raise SystemExit


print("No confirmation flags.")
