import os
import requests

api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY is missing")

r = requests.post(
    "https://api.openai.com/v1/responses",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    },
    json={
        "model": "gpt-5.5",
        "input": "Reply exactly: Agent online"
    },
    timeout=60
)

print(r.status_code)
print(r.text)
