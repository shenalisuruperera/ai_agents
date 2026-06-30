# Location Learning

## Purpose

The Work Agent remembers corrected job locations so the same mistake never needs to be corrected twice.

This allows short job names or nicknames to resolve to an exact Google Maps destination.

---

# Example

Original work message

Air Services

↓

User notices the travel time is incorrect.

↓

User enters

8RHJ+VV Melbourne Airport, Victoria

↓

The Work Agent stores:

Air Services

↓

8RHJ+VV Melbourne Airport, Victoria

↓

Every future job containing

Air Services

automatically uses the saved destination.

---

# Workflow

Unknown location

↓

Google Routes estimate

↓

Travel review

↓

User confirms travel

OR

User enters corrected destination

↓

Python saves location override

↓

Future jobs automatically resolve correctly

---

# Stored Data

Location overrides are stored in:

~/ai_agents/work/data/location_overrides.json

Example

{
    "air services": "8RHJ+VV Melbourne Airport, Victoria, Australia",
    "55 collins": "55 Little Collins St, Melbourne VIC 3000"
}

This file represents the long-term location memory of the Work Agent.

---

# Matching Rules

Location matching is intentionally conservative.

Current behaviour

✓ Ignore upper/lower case

✓ Ignore leading and trailing spaces

✗ No fuzzy matching

Examples

Air Services

AIR SERVICES

air services

↓

All resolve to the same saved destination.

However

Air Services Tullamarine

Air Services Melbourne

↓

Will require confirmation before becoming new saved locations.

This avoids accidentally sending the user to the wrong workplace.

---

# Google Routes

The saved destination is passed directly to the Google Routes API.

This means the stored value can be:

- Full street address
- Google Maps Plus Code
- Google-recognised business name

The Work Agent does not need to understand the location.

It simply stores the corrected destination and reuses it.

---

# Travel Cache

Travel estimates are cached separately from learned locations.

Location memory

location_overrides.json

↓

Permanent

Travel cache

travel_cache.json

↓

Temporary

Deleting the cache does NOT delete learned locations.

The cache is recreated automatically.

---

# Design Philosophy

The user should only have to teach the Work Agent once.

After a location has been corrected and saved, future jobs should calculate travel correctly without additional user input.

Only new or changed locations should require confirmation.
