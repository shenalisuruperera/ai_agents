# Changelog

This document records user-visible changes between project versions.

Git history records every commit.

The changelog records milestones.

---

# Version 1.0

Status

Stable

Release Date

2026-06-30

---

## Features

### Work Message Processing

✓ Import work messages from Automate

✓ Parse

- Date
- Start Time
- Address
- Job Type

✓ Preserve original message

---

### Confirmation Workflow

✓ Pending job confirmation

✓ Edit before saving

✓ Reject workflow

✓ Prevent automatic saving

---

### Travel System

✓ Google Routes API integration

✓ Arrival-time routing

✓ Leave time calculation

✓ Configurable travel buffer

✓ Travel review confirmation

---

### Location Learning

✓ Save corrected destinations

✓ Google Maps Plus Code support

✓ Case-insensitive keyword matching

✓ Permanent location memory

---

### Alarm System

✓ Android alarm generation

✓ Alarm title

✓ Alarm description

✓ Automatic leave time

---

### Data Management

✓ Temporary processing files

✓ Persistent job history

✓ Persistent learned locations

✓ Automatic cleanup

✓ Travel cache

---

### Architecture

✓ Automate

Android interface

✓ Python

Business logic

✓ Shared file communication

✓ Modular processing pipeline

---

## Testing Completed

✓ Parser

✓ Confirmation workflow

✓ Edit workflow

✓ Travel review

✓ Location learning

✓ Alarm generation

✓ Cleanup

✓ Google Routes

---

## Known Limitations

Current parser assumes one job per message.

Location matching is exact keyword matching.

Duplicate detection remains disabled during testing.

WhatsApp integration currently uses a test variable.

---

## Next Release

Version 1.1

Planned improvements

- Parser improvements
- Better handling of unusual addresses
- Continued documentation updates
