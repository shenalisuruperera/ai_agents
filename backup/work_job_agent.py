import json
import re
from pathlib import Path
from datetime import datetime, timedelta

BASE = Path.home() / "ai_agents"
JOBS_FILE = BASE / "work_messages" / "jobs.json"

def tomorrow_date():
    return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

def load_jobs():
    if not JOBS_FILE.exists():
        return []
    return json.loads(JOBS_FILE.read_text())

def save_jobs(jobs):
    JOBS_FILE.write_text(json.dumps(jobs, indent=2))

def detect_job_type(text):
    lower = text.lower()
    if "rx labour" in lower or "rx labor" in lower:
        return "RX Labour"
    if "opulent" in lower:
        return "Opulent"
    return "Cabrals"

def extract_time(text):
    match = re.search(r'\b(\d{1,2})(?::(\d{2}))?\s*(am|pm)\b', text, re.I)
    if not match:
        return None

    hour = int(match.group(1))
    minute = int(match.group(2) or 0)
    ampm = match.group(3).lower()

    if ampm == "pm" and hour != 12:
        hour += 12
    if ampm == "am" and hour == 12:
        hour = 0

    return f"{hour:02d}:{minute:02d}"

def extract_time(text):
    match = re.search(r'\b(\d{1,2})(?:[:.](\d{2}))?\s*(am|pm)\b', text, re.I)
    if not match:
        return None

    hour = int(match.group(1))
    minute = int(match.group(2) or 0)
    ampm = match.group(3).lower()

    if ampm == "pm" and hour != 12:
        hour += 12
    if ampm == "am" and hour == 12:
        hour = 0

    return f"{hour:02d}:{minute:02d}"

def extract_address(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    for i, line in enumerate(lines):
        if re.search(r'\d+', line) and re.search(r'\b(rd|road|st|street|dr|drive|ave|avenue|ct|court|cres|crescent|blvd|boulevard|lane|ln|way)\b', line, re.I):
            address_parts = [line]

            if i + 1 < len(lines):
                next_line = lines[i + 1]
                if not re.search(r'\b(council|library|labour|labor|formula|shenal|amila|tony)\b', next_line, re.I):
                    address_parts.append(next_line)

            return ", ".join(address_parts)

    return None

def extract_known_location(text):
    loc_file = BASE / "work_messages" / "known_locations.json"
    if not loc_file.exists():
        return None

    locations = json.loads(loc_file.read_text())
    lower = text.lower()

    for keyword, location in locations.items():
        if keyword.lower() in lower:
            return location

    return None

def parse_job(text):
    return {
        "date": tomorrow_date(),
        "start_time": extract_time(text),
        "address": extract_address(text) or extract_known_location(text),
        "job_type": detect_job_type(text),
        "raw_message": text,
        "created_at": datetime.now().isoformat(timespec="seconds")
    }

print("Paste the WhatsApp job message.")
print("When finished, type END on a new line.\n")

lines = []
while True:
    line = input()
    if line.strip().upper() == "END":
        break
    lines.append(line)

message = "\n".join(lines)
job = parse_job(message)

print("\nExtracted job:")
print(json.dumps(job, indent=2))

confirm = input("\nSave this job? y/n: ").strip().lower()

if confirm == "y":
    jobs = load_jobs()
    jobs.append(job)
    save_jobs(jobs)
    print("Saved.")
else:
    print("Not saved.")
