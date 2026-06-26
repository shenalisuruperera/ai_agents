import os
import json
import requests
from pathlib import Path
from datetime import datetime, timedelta

BASE = Path.home() / "ai_agents"
ENV_FILE = BASE / ".env"
CACHE_FILE = BASE / "work" / "data" / "travel_cache.json"

ORIGIN = "43 Everlasting Boulevard, South Morang VIC, Australia"


def load_env():
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()


def load_json(path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text())


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2))


def get_cached_minutes(address):
    cache = load_json(CACHE_FILE, {})
    item = cache.get(address.lower())

    if not item:
        return None

    checked = datetime.fromisoformat(item["last_checked"])
    if datetime.now() - checked > timedelta(days=7):
        return None

    return int(item["travel_minutes"])


def save_cache(address, minutes):
    cache = load_json(CACHE_FILE, {})
    cache[address.lower()] = {
        "address": address,
        "travel_minutes": int(minutes),
        "last_checked": datetime.now().isoformat(timespec="seconds")
    }
    save_json(CACHE_FILE, cache)


def get_travel_minutes(address):
    if not address:
        return 60

    cached = get_cached_minutes(address)
    if cached is not None:
        return cached

    load_env()
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")

    if not api_key:
        print("GOOGLE_MAPS_API_KEY missing. Using default 60 minutes.")
        return 60

    url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    payload = {
        "origin": {
            "address": ORIGIN
        },
        "destination": {
            "address": address + ", Victoria, Australia"
        },
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
        "computeAlternativeRoutes": False,
        "languageCode": "en-AU",
        "units": "METRIC"
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.duration,routes.staticDuration"
    }

    r = requests.post(url, headers=headers, json=payload, timeout=30)

    if r.status_code != 200:
        print("Google Maps error:", r.status_code, r.text)
        return 60

    data = r.json()
    routes = data.get("routes", [])

    if not routes:
        print("No route found. Using default 60 minutes.")
        return 60

    duration = routes[0].get("duration", "3600s")
    seconds = int(duration.replace("s", ""))
    minutes = round(seconds / 60)

    save_cache(address, minutes)
    return minutes


if __name__ == "__main__":
    import sys

    address = " ".join(sys.argv[1:]).strip()
    if not address:
        address = input("Destination address: ")

    minutes = get_travel_minutes(address)
    print(f"{minutes} minutes")
