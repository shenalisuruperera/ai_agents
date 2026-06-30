# Contributing Guide

This document defines the development standards for the AI Agents project.

These standards apply to both human developers and AI-assisted development.

---

# Project Philosophy

The project should remain:

- Modular
- Easy to debug
- Well documented
- Easy to extend
- Reliable before automated

Correctness is preferred over convenience.

---

# Architecture Rules

## Automate

Automate is responsible for:

- Android interaction
- Notifications
- Dialogs
- Alarms
- Launching Python

Automate should NOT contain:

- Parsing logic
- Business rules
- Google API calls
- Persistent memory

---

## Python

Python is responsible for:

- Parsing
- Business logic
- Google APIs
- Calculations
- Long-term memory
- Decision making

Python should NOT directly control Android UI.

---

# Module Design

Each module should have ONE clear responsibility.

Good examples:

- import_work_inbox.py
- process_imported_work.py
- process_job_confirmations.py
- travel_time.py

Avoid large modules that perform multiple unrelated tasks.

---

# Data Storage

Permanent data should be kept to a minimum.

Permanent:

- jobs.json
- location_overrides.json

Temporary files should be deleted after use whenever practical.

Cache files should always be safe to delete.

---

# Development Workflow

Every feature should follow this process:

1. Design
2. Implement
3. Test
4. Update documentation
5. Update session_history.md
6. Commit
7. Tag a release if appropriate

---

# Testing Checklist

Before committing:

✓ Python compiles

✓ Parser works

✓ Confirmation workflow works

✓ Edit workflow works

✓ Travel review works

✓ Alarm creation works

✓ No Python tracebacks

✓ Documentation updated

---

# Documentation Requirements

Every significant feature must update the relevant documentation.

Possible documents include:

README.md

Overview

Architecture

Automate Flow

Python Modules

Data Files

Location Learning

Testing

Design Decisions

Roadmap

Session History

File Map

---

# Commit Message Format

Use short descriptive commits.

Recommended prefixes:

feat:

New feature

fix:

Bug fix

docs:

Documentation

refactor:

Internal cleanup

test:

Testing changes

chore:

Maintenance

Examples:

feat(work): add travel review confirmation

fix(parser): improve short street parsing

docs(work): update architecture documentation

refactor(travel): simplify cache logic

---

# Release Process

Stable releases should:

- Pass all tests
- Update documentation
- Update changelog
- Update session history
- Be tagged in Git

Example:

v1.0

v1.1

v2.0

---

# Coding Standards

Prefer readability over clever code.

Avoid duplicated logic.

Keep functions focused.

Use descriptive names.

Comment WHY rather than WHAT.

---

# Future Agents

New agents should follow the same architecture.

Each agent should:

- Have one responsibility
- Maintain separate documentation
- Be independently testable
- Reuse shared infrastructure where appropriate

Examples:

Work Agent

Finance Agent

Calendar Agent

Travel Agent

CEO Agent

---

# Final Principle

Every commit should leave the project in a better state than before.

Code, documentation, and architecture should evolve together.
