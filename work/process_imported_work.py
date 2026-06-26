import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

from work_job_agent import parse_job

BASE = Path.home() / "ai_agents"
IMPORTED = BASE / "work" / "data" / "imported_messages.txt"

SHARED = Path.home() / "storage/shared/AI_Agents"
PENDING = SHARED / "pending_job.json"
DISPLAY = SHARED / "pending_job_display.txt"


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

saved_pending = 0
uncertain = 0

for part in parts:
    job = parse_job(part)

    if job["start_time"] and job["address"]:
        pending_item = {
            "status": "pending",
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "expires_at": (datetime.now() + timedelta(hours=1)).isoformat(timespec="seconds"),
            "job": job
        }

        PENDING.write_text(json.dumps(pending_item, indent=2))
        DISPLAY.write_text(make_display_text(job))
        notify_pending(job)

        saved_pending += 1
        print(f"Pending: {job['start_time']} {job['address']}")
    else:
        uncertain += 1
        print("Uncertain, not saved:")
        print(part)

IMPORTED.unlink(missing_ok=True)

print(f"Done. Pending={saved_pending}, uncertain={uncertain}")
