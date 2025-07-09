import subprocess
import logging
import os

logger = logging.getLogger(__name__)

def zip_dir(folder_path, output_path):
    logger.info(f"Creating zip archive: {output_path}")

    # Ensure output_path has .zip extension
    if not output_path.lower().endswith(".zip"):
        output_path += ".zip"

    # Remove existing zip if it already exists
    if os.path.exists(output_path):
        os.remove(output_path)

    try:
        # Use PowerShell Compress-Archive (faster than Python zipfile)
        subprocess.run([
            "powershell",
            "Compress-Archive",
            "-Path", f"{folder_path}\\*",    # Important: backslash and * to include contents
            "-DestinationPath", output_path
        ], check=True)
        logger.info("Zip archive created successfully using Compress-Archive.")
    except subprocess.CalledProcessError as e:
        logger.exception("❌ Failed to create zip archive with Compress-Archive.")
        raise