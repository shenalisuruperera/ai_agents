import json
import subprocess
from pathlib import Path
from datetime import datetime

BASE = Path.home() / "ai_agents"
INBOX = BASE / "work_messages" / "notification_inbox.json"

msg = subprocess.check_output(["termux-clipboard-get"], text=True).strip()

items = []
if INBOX.exists():
    items = json.loads(INBOX.read_text())

items.append({
    "received_at": datetime.now().isoformat(timespec="seconds"),
    "message": msg
})

INBOX.write_text(json.dumps(items, indent=2))
print("Saved clipboard message.")
