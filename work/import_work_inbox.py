from pathlib import Path
from datetime import datetime

SHARED = Path.home() / "storage/shared/AI_Agents"
INBOX = SHARED / "work_inbox.txt"
FLAG = SHARED / "run_work_parser.flag"

LOCAL_INBOX = Path.home() / "ai_agents/work_messages/imported_messages.txt"

if not FLAG.exists():
    print("No work parser flag found.")
    raise SystemExit

if not INBOX.exists():
    print("No work inbox found.")
    FLAG.unlink(missing_ok=True)
    raise SystemExit

text = INBOX.read_text().strip()

if text:
    with LOCAL_INBOX.open("a") as f:
        f.write(f"\n\nIMPORTED {datetime.now().isoformat(timespec='seconds')}\n")
        f.write(text)
        f.write("\n")

    INBOX.unlink()
    print("Imported work inbox.")
else:
    print("Inbox was empty.")

FLAG.unlink(missing_ok=True)
