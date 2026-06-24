import sys
import json
from pathlib import Path
from datetime import datetime

BASE = Path.home() / "ai_agents"
INBOX = BASE / "work_messages" / "notification_inbox.json"

message = " ".join(sys.argv[1:]).strip()

if not message:
    message = sys.stdin.read().strip()

items = []
if INBOX.exists():
    items = json.loads(INBOX.read_text())

items.append({
    "received_at": datetime.now().isoformat(timespec="seconds"),
    "message": message
})

INBOX.write_text(json.dumps(items, indent=2))

print("Saved notification message.")
