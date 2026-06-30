# Roadmap

This document records planned improvements for the AI Agents project.

Items may move between releases as priorities change.

---

# Version 1.1

Status

Planned

## Parser

Improve address extraction for unusual message formats.

Improve handling of abbreviated street names.

Improve support for business names.

---

## Travel

Improve travel estimate validation.

Better handling of Google Maps failures.

Improve Plus Code suggestions.

---

## Documentation

Keep documentation synchronised with every feature.

Expand troubleshooting examples.

Document additional agents as they are created.

---

# Version 1.2

Status

Future

## Work Agent

Support multiple jobs contained in one message.

Improve duplicate detection strategy.

Improve parser confidence scoring.

Better handling of uncertain messages.

---

## Memory

Continue reducing unnecessary stored data.

Review old cache formats.

Simplify configuration.

---

# Future Agents

The Work Agent is intended to become one module within a larger AI Agent system.

Possible future agents include:

Work.Reminders

Personal.Reminders

Finance

Calendar

Travel

Health

CEO Agent

Each new agent should remain independent while sharing a common architecture.

---

# Long Term Vision

Develop a collection of modular AI-powered assistants.

Each agent should:

- have one responsibility
- be independently testable
- communicate through well-defined interfaces
- maintain its own documentation
- minimise unnecessary stored data

The overall system should remain modular so that new agents can be added without rewriting existing ones.
