import os
import zipfile
import logging

logger = logging.getLogger(__name__)

def zip_dir(folder_path, output_path):
    logger.info(f"Creating zip archive: {output_path}")
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, folder_path)
                zipf.write(filepath, arcname)
    logger.info("Zip archive created.")