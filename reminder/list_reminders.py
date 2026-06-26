import json
from pathlib import Path

MEMORY_FILE = Path.home() / "ai_agents" / "reminders.json"

reminders = json.loads(MEMORY_FILE.read_text())

if not reminders:
    print("No reminders.")
else:
    for i, r in enumerate(reminders, start=1):
        print(f"{i}. {r['task']} - {r['date']} {r['time']} - {r['notes']}")
