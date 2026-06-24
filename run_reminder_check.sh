#!/data/data/com.termux/files/usr/bin/bash
cd /data/data/com.termux/files/home/ai_agents
echo "Job ran at $(date)" >> logs/scheduler.log
/data/data/com.termux/files/home/ai_agents/.venv/bin/python notify_due_reminders.py >> logs/scheduler.log 2>&1
