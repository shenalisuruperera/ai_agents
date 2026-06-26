import json
import subprocess
from pathlib import Path
from datetime import datetime

MEMORY_FILE = Path.home() / "ai_agents" / "reminders.json"

reminders = json.loads(MEMORY_FILE.read_text())
now = datetime.now()
updated = []

for r in reminders:
    if r.get("done"):
        updated.append(r)
        continue

    reminder_time = datetime.strptime(
        f"{r['date']} {r['time']}",
        "%Y-%m-%d %H:%M"
    )

    if reminder_time <= now:
        subprocess.run([
            "termux-notification",
            "--title", "Work Reminder",
            "--content", f"{r['task']} - {r.get('notes', '')}"
        ])
        r["done"] = True

    updated.append(r)

MEMORY_FILE.write_text(json.dumps(updated, indent=2))
