import os
import json
import requests
from pathlib import Path
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import sys
sys.path.insert(0, str(Path.home() / 'ai_agents'))
from shared.notify import notify_error

BASE = Path.home() / "ai_agents"
ENV_FILE = BASE / ".env"
DATA = BASE / "work" / "data"

CACHE_FILE = DATA / "travel_cache.json"
OVERRIDES_FILE = DATA / "location_overrides.json"

ORIGIN = "43 Everlasting Boulevard, South Morang VIC, Australia"
TZ = ZoneInfo("Australia/Melbourne")


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


def resolve_address(address):
    overrides = load_json(OVERRIDES_FILE, {})
    lower = address.lower()

    for keyword, real_address in overrides.items():
        if keyword.lower() in lower:
            return real_address

    return address


def round_arrival_dt(arrival_dt):
    if not arrival_dt:
        return None

    if arrival_dt.tzinfo is None:
        arrival_dt = arrival_dt.replace(tzinfo=TZ)

    minute = 30 if arrival_dt.minute >= 30 else 0
    return arrival_dt.replace(minute=minute, second=0, microsecond=0)


def cache_key(address, arrival_dt=None):
    resolved = resolve_address(address).lower().strip()
    rounded = round_arrival_dt(arrival_dt)

    if rounded:
        return f"{resolved}|arrival={rounded.strftime('%Y-%m-%dT%H:%M')}"

    return resolved


def get_cached_minutes(address, arrival_dt=None):
    cache = load_json(CACHE_FILE, {})
    key = cache_key(address, arrival_dt)
    item = cache.get(key)

    if not item:
        return None

    checked = datetime.fromisoformat(item["last_checked"])
    if datetime.now() - checked > timedelta(days=7):
        return None

    return int(item["travel_minutes"])


def save_cache(address, minutes, arrival_dt=None):
    cache = load_json(CACHE_FILE, {})
    resolved = resolve_address(address)
    rounded = round_arrival_dt(arrival_dt)
    key = cache_key(address, arrival_dt)

    cache[key] = {
        "input_address": address,
        "resolved_address": resolved,
        "travel_minutes": int(minutes),
        "arrival_bucket": rounded.strftime("%H:%M") if rounded else None,
        "arrival_time": rounded.isoformat(timespec="minutes") if rounded else None,
        "last_checked": datetime.now().isoformat(timespec="seconds")
    }

    save_json(CACHE_FILE, cache)


def save_location_override(keyword, real_address):
    keyword_key = keyword.strip().lower()
    real_address = real_address.strip()

    overrides = load_json(OVERRIDES_FILE, {})
    overrides[keyword_key] = real_address
    save_json(OVERRIDES_FILE, overrides)

    cache = load_json(CACHE_FILE, {})

    bad_keys = [
        k for k, v in cache.items()
        if keyword_key in k
        or real_address.lower() in k
        or v.get("input_address", "").lower() == keyword_key
        or v.get("resolved_address", "").lower() == real_address.lower()
    ]

    for k in bad_keys:
        cache.pop(k, None)

    save_json(CACHE_FILE, cache)


def get_travel_minutes(address, arrival_dt=None):
    if not address:
        return 60

    resolved_address = resolve_address(address)

    cached = get_cached_minutes(address, arrival_dt)
    if cached is not None:
        return cached

    load_env()
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")

    if not api_key:
        msg = "GOOGLE_MAPS_API_KEY missing. Using default 60 minutes."
        print(msg)
        notify_error("Google Maps key missing", msg)
        return 60

    rounded_arrival = round_arrival_dt(arrival_dt)

    url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    payload = {
        "origin": {
            "address": ORIGIN
        },
        "destination": {
            "address": resolved_address + ", Victoria, Australia"
        },
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
        "computeAlternativeRoutes": False,
        "languageCode": "en-AU",
        "units": "METRIC"
    }

    if rounded_arrival:
        payload["arrivalTime"] = rounded_arrival.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.duration,routes.staticDuration"
    }

    r = requests.post(url, headers=headers, json=payload, timeout=30)

    if r.status_code != 200:
        msg = f"Google Maps error {r.status_code}: {r.text[:180]}"
        print(msg)
        notify_error("Google Maps error", msg)
        return 60

    data = r.json()
    routes = data.get("routes", [])

    if not routes:
        msg = "No route found. Using default 60 minutes."
        print(msg)
        notify_error("No route found", msg)
        return 60

    duration = routes[0].get("duration", "3600s")
    seconds = int(duration.replace("s", ""))
    minutes = round(seconds / 60)

    save_cache(address, minutes, rounded_arrival)
    return minutes


def get_resolved_address(address):
    return resolve_address(address)


if __name__ == "__main__":
    import sys

    address = " ".join(sys.argv[1:]).strip()
    if not address:
        address = input("Destination address: ")

    minutes = get_travel_minutes(address)
    print(f"{minutes} minutes")
