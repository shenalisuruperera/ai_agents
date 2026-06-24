import os
import json
import requests
from pathlib import Path
from datetime import datetime

BASE_DIR = Path.home() / "ai_agents"
MEMORY_FILE = BASE_DIR / "reminders.json"


def load_reminders():
    if not MEMORY_FILE.exists():
        return []
    return json.loads(MEMORY_FILE.read_text())


def save_reminders(reminders):
    MEMORY_FILE.write_text(json.dumps(reminders, indent=2))


def extract_output_text(data):
    for item in data.get("output", []):
        if item.get("type") == "message":
            for content in item.get("content", []):
                if content.get("type") == "output_text":
                    return content.get("text")

    print(json.dumps(data, indent=2))
    raise RuntimeError("Could not find output text")


def ask_ai(user_text):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing")

    prompt = f"""
Today is {datetime.now().date()}.

Extract a reminder from this message.

Return ONLY valid JSON in this format:
{{
  "task": "...",
  "date": "...",
  "time": "...",
  "notes": "..."
}}

If date or time is unknown, use null.

Message: {user_text}
"""

    r = requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-5",
            "input": prompt
        },
        timeout=60
    )

    data = r.json()

    if data.get("error"):
        print("API ERROR:")
        print(json.dumps(data, indent=2))
        raise RuntimeError("OpenAI API error")

    text = extract_output_text(data)
    return json.loads(text)


while True:
    print("\n=== AI Reminder Agent ===")
    print("Type a reminder, or type exit")
    user_text = input("> ")

    if user_text.lower() == "exit":
        break

    reminder = ask_ai(user_text)

    reminders = load_reminders()
    reminders.append(reminder)
    save_reminders(reminders)

    print("\nSaved reminder:")
    print(json.dumps(reminder, indent=2))
