AI Agents

A modular collection of AI-powered automation agents built using Python, Termux, Android Automate, and Google APIs.

Current Status

Current Release: v1.0

Status: Stable

The first stable agent is the Work Agent.

Work Agent

The Work Agent converts work messages into confirmed Android alarms.

Current capabilities:

• Import work messages from Android Automate
• Parse job date, time, address, and job type
• Confirm before saving
• Edit or reject detected jobs
• Estimate travel time using Google Routes API
• Calculate leave time using arrival-time routing
• Review travel estimate before creating alarm
• Learn corrected locations using Google Maps addresses or Plus Codes
• Store permanent location memory
• Generate Android alarms through Automate
• Clean temporary files after processing

Architecture

The project separates Android interaction from business logic.

Automate handles:

• Android dialogs
• Notifications
• Alarm creation
• User input
• Launching Termux through Termux:Tasker

Python handles:

• Parsing
• Business logic
• Google API calls
• Travel calculations
• Location memory
• Alarm request generation

Automate and Python communicate through shared files.

Documentation Index


Document
Description

docs/00_overview.md
High-level overview

docs/01_architecture.md
Overall system architecture

docs/02_work_agent.md
Complete Work Agent workflow

docs/03_automate_flow.md
Android Automate workflow

docs/04_python_modules.md
Python module reference

docs/05_data_files.md
Data files and storage

docs/06_location_learning.md
Location learning system

docs/07_testing.md
Testing and debugging guide

docs/file_map.md
Complete file reference

docs/decisions.md
Design decisions

docs/changelog.md
Project release history

docs/roadmap.md
Future development

docs/session_history.md
Development session history



Design Principles

• Modular agents
• One responsibility per module
• Reliability before automation
• User confirmation before saving
• Minimal permanent storage
• Automate handles Android
• Python handles business logic
• Documentation evolves with the code

Development Workflow

Every feature should follow this process:

1. Design
2. Implement
3. Test
4. Update documentation
5. Update session history
6. Commit
7. Tag a release for major milestones

Technologies

• Python
• Android Automate
• Termux
• Termux:Tasker
• Google Routes API
• Git
• GitHub

Future Vision

The Work Agent is the first module in a larger ecosystem of specialised automation agents.

Possible future agents:

• Work Agent
• Personal Reminders
• Calendar Agent
• Finance Agent
• Travel Agent
• Health Agent
• CEO Agent

Each agent should remain modular, independently testable, and documented.

Contributing

Development standards are documented in CONTRIBUTING.md.

License

This project is licensed under the MIT License.

See the LICENSE file for details.

