import os
from dotenv import load_dotenv

load_dotenv()

SFTP_HOST = os.getenv("SFTP_HOST")
SFTP_PORT = int(os.getenv("SFTP_PORT"))
SFTP_USERNAME = os.getenv("SFTP_USERNAME")
SFTP_PASSWORD = os.getenv("SFTP_PASSWORD")

REMOTE_DIR = os.getenv("REMOTE_DIR")
LOCAL_TMP_DIR = "./mc_backup_tmp"

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

KEEP_LAST_N_LOGS = int(os.getenv("KEEP_LAST_N_LOGS"))

BACKUPIGNORE_FILE = "backupignore.txt"
BACKUP_ZIP_PREFIX = "SkyBlock_"
BACKUP_ZIP_EXT = ".zip"

RCLONE_REMOTE = os.getenv("RCLONE_REMOTE")
KEEP_LAST_N = int(os.getenv("KEEP_LAST_N"))