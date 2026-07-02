import subprocess


def notify_error(title, message):
    subprocess.run([
        "termux-notification",
        "--id", "work-agent-error",
        "--title", f"Work Agent Error: {title}",
        "--content", str(message),
        "--priority", "high"
    ], check=False)
