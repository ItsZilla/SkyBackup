import os
import sys
import logging
import subprocess
from datetime import datetime
from ignore_filter import read_ignore_patterns, filter_ignored_files
from notifier import notify_discord
from zipper import zip_dir
from rclone_uploader import upload_with_rclone, cleanup_old_backups
from utils import clean_folder, cleanup_old_logs

# Logger setup (updated, supports UTF-8)
os.makedirs("logs", exist_ok=True)
log_filename = datetime.now().strftime("logs/backup_%Y%m%d_%H%M%S.log")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_filename, encoding="utf-8")
file_formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def main():
    logger.info("🚀 Starting Minecraft server backup...")

    LOCAL_TEMP_DIR = "./backup_temp"
    clean_folder(LOCAL_TEMP_DIR)

    # Use rclone to download entire server
    RCLONE_SFTP_REMOTE = os.getenv("RCLONE_SFTP_REMOTE")
    logger.info(f"Downloading from remote: {RCLONE_SFTP_REMOTE}")
    try:
        subprocess.run([
            "rclone",
            "copy",
            f"{RCLONE_SFTP_REMOTE}:",
            LOCAL_TEMP_DIR,
            "--progress",
            "--transfers", "8",   # You can tune these
            "--checkers", "8",
            "--exclude-from", "backupignore.txt"  # Ignore patterns
        ], check=True)
    except subprocess.CalledProcessError as e:
        logger.error("❌ Rclone download failed!")
        notify_discord(type="error")
        raise

    # If additional filtering needed after, keep these
    ignore_patterns = read_ignore_patterns()
    filter_ignored_files(LOCAL_TEMP_DIR, ignore_patterns)

    BACKUP_ZIP_PREFIX = "SkyBlock_"
    TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
    BACKUP_ZIP_EXT = ".zip"
    zip_name = f"{BACKUP_ZIP_PREFIX}{TIMESTAMP}{BACKUP_ZIP_EXT}"
    zip_dir(LOCAL_TEMP_DIR, zip_name)

    upload_with_rclone(zip_name)
    cleanup_old_backups()

    clean_folder(LOCAL_TEMP_DIR)
    os.remove(zip_name)

    logger.info("✅ Backup process completed successfully!")
    notify_discord(type="success")
    cleanup_old_logs()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception("❌ Backup process failed!")
        notify_discord(type="error")