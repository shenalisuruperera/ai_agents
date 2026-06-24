import json
from pathlib import Path
from datetime import datetime

MEMORY_FILE = Path.home() / "ai_agents" / "reminders.json"

reminders = json.loads(MEMORY_FILE.read_text())

now = datetime.now()

for r in reminders:
    try:
        reminder_time = datetime.strptime(
            f"{r['date']} {r['time']}",
            "%Y-%m-%d %H:%M"
        )

        if reminder_time <= now:
            print(f"DUE: {r['task']}")
    except Exception as e:
        print("Skipped:", r, e)
