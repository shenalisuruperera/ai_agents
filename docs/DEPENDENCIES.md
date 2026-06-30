# Dependencies

This document lists the software, services and APIs required to run the AI Agents project.

---

# Runtime

Python

- Python 3.13+

Termux

- Latest stable version

Android

- Android 12 or newer recommended

---

# Android Applications

Required

- Automate (LlamaLab)
- Termux
- Termux:Tasker plugin

Optional

- WhatsApp (future live message integration)

---

# Python Packages

Install from:

requirements.txt

Current project uses packages such as:

- requests
- python-dotenv
- googlemaps (if used)
- tzdata (recommended for ZoneInfo support)

To install:

pip install -r requirements.txt

---

# Google Services

Google Routes API

Required for:

- Travel time estimation
- Arrival-time routing

Required configuration:

- Google Cloud Project
- Routes API enabled
- API Key

---

# Project Structure

Main folders:

work/
reminder/
docs/
logs/

Shared Android folder:

/storage/emulated/0/AI_Agents/

---

# Persistent Data

work/data/jobs.json

Confirmed work jobs.

work/data/location_overrides.json

Learnt Google Maps destinations.

---

# Temporary Data

Generated automatically.

Safe to delete.

Examples:

travel_cache.json

pending_job.json

alarm_request.txt

travel_review.txt

work_inbox.txt

edit_request.txt

---

# Environment Variables

Recommended:

GOOGLE_MAPS_API_KEY

Never commit API keys or secrets to Git.

---

# Git

Version control:

Git

Remote hosting:

GitHub

Release strategy:

Semantic version tags

Example:

v1.0

v1.1

v2.0

