from pathlib import Path
from datetime import datetime

BASE_DIR = Path.home() / "ai_agents"

test_file = BASE_DIR / "logs" / "agent_test.txt"

test_file.write_text(
    f"Agent wrote this at {datetime.now()}\n",
    encoding="utf-8"
)

print("Created:", test_file)
print("Content:")
print(test_file.read_text(encoding="utf-8"))
