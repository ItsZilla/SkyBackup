import os
import logging
from datetime import datetime
from config import LOCAL_TMP_DIR, REMOTE_DIR, BACKUP_ZIP_PREFIX, BACKUP_ZIP_EXT
from sftp_downloader import connect_sftp, sftp_recursive_download
from ignore_filter import read_ignore_patterns, filter_ignored_files
from notifier import notify_discord
from zipper import zip_dir
from rclone_uploader import upload_with_rclone, cleanup_old_backups
from utils import clean_folder, cleanup_old_logs

os.makedirs("logs", exist_ok=True)
log_filename = datetime.now().strftime("logs/backup_%Y%m%d_%H%M%S.log")

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    logger.info("🚀 Starting Minecraft server backup...")

    clean_folder(LOCAL_TMP_DIR)

    sftp = connect_sftp()
    logger.info(f"Downloading files from {REMOTE_DIR} ...")
    sftp_recursive_download(sftp, REMOTE_DIR, LOCAL_TMP_DIR)
    sftp.close()

    ignore_patterns = read_ignore_patterns()
    filter_ignored_files(LOCAL_TMP_DIR, ignore_patterns)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"{BACKUP_ZIP_PREFIX}{timestamp}{BACKUP_ZIP_EXT}"
    zip_dir(LOCAL_TMP_DIR, zip_name)

    upload_with_rclone(zip_name)
    cleanup_old_backups()

    clean_folder(LOCAL_TMP_DIR)
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