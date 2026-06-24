import json
from pathlib import Path

MEMORY_FILE = Path.home() / "ai_agents" / "reminders.json"


def load_reminders():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_reminders(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


while True:
    print("\n=== Work Reminders ===")
    print("1. Show reminders")
    print("2. Add reminder")
    print("3. Exit")

    choice = input("> ")

    reminders = load_reminders()

    if choice == "1":
        if not reminders:
            print("No reminders")
        else:
            for i, r in enumerate(reminders, start=1):
                print(f"{i}. {r}")

    elif choice == "2":
        text = input("Reminder: ")
        reminders.append(text)
        save_reminders(reminders)
        print("Saved")

    elif choice == "3":
        break
