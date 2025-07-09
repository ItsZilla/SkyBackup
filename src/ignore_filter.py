import os
import fnmatch
import logging

logger = logging.getLogger(__name__)

def read_ignore_patterns():
    with open("backupignore.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return lines

def matches_ignore(path, patterns):
    path = path.replace(os.sep, '/')
    for pat in patterns:
        if pat.endswith('/'):
            if path.startswith(pat):
                return True
        elif fnmatch.fnmatch(path, pat):
            return True
    return False

def filter_ignored_files(base_path, ignore_patterns):
    logger.info("Filtering ignored files...")
    for root, dirs, files in os.walk(base_path, topdown=True):
        dirs[:] = [d for d in dirs if not matches_ignore(os.path.relpath(os.path.join(root, d), base_path).replace(os.sep, '/') + '/', ignore_patterns)]
        for f in files:
            rel_file = os.path.relpath(os.path.join(root, f), base_path).replace(os.sep, '/')
            if matches_ignore(rel_file, ignore_patterns):
                path_to_remove = os.path.join(root, f)
                logger.info(f"Removing ignored file: {path_to_remove}")
                os.remove(path_to_remove)