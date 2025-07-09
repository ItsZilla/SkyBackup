import subprocess
import json
import logging

from config import RCLONE_REMOTE, KEEP_LAST_N

logger = logging.getLogger(__name__)

def upload_with_rclone(zip_file):
    logger.info(f"Uploading {zip_file} to {RCLONE_REMOTE} using rclone...")
    subprocess.run(["rclone", "copy", zip_file, RCLONE_REMOTE], check=True)
    logger.info("Upload complete.")

def cleanup_old_backups():
    logger.info("Listing backups for cleanup...")
    result = subprocess.run(
        ["rclone", "lsjson", RCLONE_REMOTE],
        check=True,
        capture_output=True,
        text=True
    )
    files = json.loads(result.stdout)
    files.sort(key=lambda x: x["ModTime"], reverse=True)
    to_delete = files[KEEP_LAST_N:]

    for f in to_delete:
        remote_path = f'{RCLONE_REMOTE}/{f["Name"]}'
        logger.info(f"Deleting old backup: {remote_path}")
        subprocess.run(["rclone", "deletefile", remote_path], check=True)