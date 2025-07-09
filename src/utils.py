import shutil
import os
import glob
import logging

logger = logging.getLogger(__name__)

def clean_folder(folder_path):
    if os.path.exists(folder_path):
        logger.info(f"Cleaning folder: {folder_path}")
        shutil.rmtree(folder_path)

def cleanup_old_logs():
    log_files = sorted(glob.glob("logs/backup_*.log"), key=os.path.getmtime, reverse=True)
    KEEP_LAST_N_LOGS = int(os.getenv("KEEP_LAST_N_LOGS"))
    if len(log_files) <= KEEP_LAST_N_LOGS:
        return

    to_delete = log_files[KEEP_LAST_N_LOGS:]
    for f in to_delete:
        try:
            os.remove(f)
            logger.info(f"Deleted old log file: {f}")
        except Exception as e:
            logger.warning(f"Failed to delete log file {f}: {e}")