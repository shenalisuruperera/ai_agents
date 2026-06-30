import json
import re
from pathlib import Path
from datetime import datetime, timedelta

BASE = Path.home() / "ai_agents"
WORK_DIR = BASE / "work" / "data"
JOBS_FILE = WORK_DIR / "jobs.json"


BAD_ADDRESS_VALUES = {"y", "n", "yes", "no", "confirm", "reject", "ok"}
BAD_NEXT_LINE_WORDS = r"\b(council|library|labour|labor|formula|shenal|amila|tony|keith|call|cleaning)\b"


def tomorrow_date():
    return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")


def load_json(file, default):
    if not file.exists():
        return default
    return json.loads(file.read_text())


def save_json(file, data):
    file.write_text(json.dumps(data, indent=2))


def detect_job_type(text):
    lower = text.lower()
    if "rx labour" in lower or "rx labor" in lower:
        return "RX Labour"
    if "opulent" in lower:
        return "Opulent"
    return "Cabrals"


def extract_time(text):
    match = re.search(r"\b(\d{1,2})(?:[:.](\d{2}))?\s*(am|pm)\b", text, re.I)
    if not match:
        return ""

    hour = int(match.group(1))
    minute = int(match.group(2) or 0)
    ampm = match.group(3).lower()

    if ampm == "pm" and hour != 12:
        hour += 12
    if ampm == "am" and hour == 12:
        hour = 0

    return f"{hour:02d}:{minute:02d}"


def is_bad_address(value):
    return value.strip().lower() in BAD_ADDRESS_VALUES


def looks_like_address(line):
    if is_bad_address(line):
        return False

    # Normal address: 687 Doncaster Rd
    if re.search(r"\d+", line) and re.search(
        r"\b(rd|road|st|street|dr|drive|ave|avenue|ct|court|cres|crescent|blvd|boulevard|lane|ln|way|pl|place)\b",
        line,
        re.I,
    ):
        return True

    # Short city-style address: 55 Collins, 269 Lonsdale, 550 Latrobe
    if re.match(r"^\d{1,5}\s+[A-Za-z][A-Za-z\s'-]{2,}$", line):
        if not re.search(r"\b(call|phone|keith|shenal|amila|tony|l7|labour|labor|cleaning)\b", line, re.I):
            return True

    return False


def extract_address(text):
    lines = [line.strip() for line in text.splitlines() if line.strip() and not is_bad_address(line)]

    for i, line in enumerate(lines):
        if looks_like_address(line):
            address_parts = [line]

            if i + 1 < len(lines):
                next_line = lines[i + 1]
                if not re.search(BAD_NEXT_LINE_WORDS, next_line, re.I) and not is_bad_address(next_line):
                    # Add suburb line only if it does not look like a phone/contact/task line.
                    if not re.search(r"\b(call|phone|cleaning|labour|labor|sign|loading|dock)\b", next_line, re.I):
                        address_parts.append(next_line)

            return ", ".join(address_parts)

    return ""


def ask_edit(label, current):
    print(f"{label}: {current}")
    new_value = input("Press Enter to keep, or type correction: ").strip()
    return new_value if new_value else current


def parse_job(text):
    return {
        "date": tomorrow_date(),
        "start_time": extract_time(text),
        "address": extract_address(text),
        "job_type": detect_job_type(text),
        "raw_message": text,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }


def save_job(job):
    jobs = load_json(JOBS_FILE, [])
    jobs.append(job)
    save_json(JOBS_FILE, jobs)


def interactive_main():
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

    print("\n--- Confirm extracted job ---")
    job["date"] = ask_edit("Date", job["date"])
    job["start_time"] = ask_edit("Start time", job["start_time"])
    job["address"] = ask_edit("Address", job["address"])
    job["job_type"] = ask_edit("Job type", job["job_type"])

    print("\n--- Original message ---")
    print(message)

    print("\n--- Final job record ---")
    print(json.dumps(job, indent=2))

    confirm = input("\nSave this job? y/n: ").strip().lower()

    if confirm == "y":
        save_job(job)
        print("Saved job.")
    else:
        print("Not saved.")


if __name__ == "__main__":
    interactive_main()
