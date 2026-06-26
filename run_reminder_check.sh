#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/ai_agents"
cd "$BASE" || exit 1

echo "Job ran at $(date)" >> logs/scheduler.log

.venv/bin/python work/import_work_inbox.py >> logs/scheduler.log 2>&1
.venv/bin/python work/process_imported_work.py >> logs/scheduler.log 2>&1
.venv/bin/python work/process_job_confirmations.py >> logs/scheduler.log 2>&1
.venv/bin/python reminder/notify_due_reminders.py >> logs/scheduler.log 2>&1
