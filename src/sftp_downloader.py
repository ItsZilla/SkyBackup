import os
import stat
import paramiko
import logging

from config import SFTP_HOST, SFTP_PORT, SFTP_USERNAME, SFTP_PASSWORD

logger = logging.getLogger(__name__)

def connect_sftp():
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=SFTP_USERNAME, password=SFTP_PASSWORD)
    return paramiko.SFTPClient.from_transport(transport)

def sftp_recursive_download(sftp, remote_path, local_path):
    os.makedirs(local_path, exist_ok=True)
    for entry in sftp.listdir_attr(remote_path):
        remote_item = remote_path + "/" + entry.filename
        local_item = os.path.join(local_path, entry.filename)
        if stat.S_ISDIR(entry.st_mode):
            logger.debug(f"Entering directory: {remote_item}")
            sftp_recursive_download(sftp, remote_item, local_item)
        else:
            logger.info(f"Downloading file: {remote_item}")
            sftp.get(remote_item, local_item)