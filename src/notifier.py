import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def notify_discord(type):
    if not DISCORD_WEBHOOK_URL:
        return
    if type == "success":
        message = "✅ Backup completed successfully."
    elif type == "error":
        message = "❌ Backup failed. Please check the logs."
    else:
        message = f"ℹ️ Backup status: {type}"

    embed = {
        "title": "SkyKingdom Backups",
        "description": message,
        "color": 0x74e8a6,
    }

    payload = {
        "embeds": [embed]
    }

    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
    except Exception as e:
        print(f"Discord notification failed: {e}")
