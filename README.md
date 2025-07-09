# 📦 SkyBackup
#### Automated Minecraft server backup system that:
- Downloads your entire server files via SFTP (from your host)
- Filters out unimportant files and folders using a custom backupignore.txt file
- Compresses the cleaned files into a ZIP archive
- Uploads to Google Drive using rclone (configured with your Drive remote)
- Cleans up old backups automatically (keeps last N backups)
- Sends Discord notifications (with embed) on success or failure
- Keeps per-run logs and auto-cleans old logs
## ⚙️ Setup
### 1️⃣ Clone repo & install dependencies
```
git clone https://github.com/ItsZilla/SkyBackup.git
pip install -r requirements.txt
```
### 2️⃣ Create and fill in your .env
```
SFTP_HOST=your.server.host
SFTP_PORT=22
SFTP_USERNAME=yourusername
SFTP_PASSWORD=yourpassword

REMOTE_DIR=/path/to/minecraft/server

KEEP_LAST_N_LOGS=5
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...

KEEP_LAST_N_LOGS=5

RCLONE_REMOTE="rclone remote name:folder name"
KEEP_LAST_N=3
```
### 3️⃣ Configure rclone
```
rclone config
```
- Choose Google Drive
- Link your Google account
- Name your remote (e.g., SkyKingdom Backups)
- Use correct folder path in RCLONE_REMOTE
### 4️⃣ Adjust backupignore.txt with any files you dont want saved
```
logs/
*.log
crash-reports/
plugins/Essentials/backups/
plugins/*/update/
```
## 💬 Usage
```
python main.py
```
- Creates a ZIP archive in output/
- Uploads it to Google Drive
- Keeps only KEEP_LAST_N backups and deletes anything older
- Logs each run into logs/
- Sends Discord embed notification

## ✅ Dependencies
- Python 3.8+
- paramiko
- python-dotenv
- requests
- rclone (installed separately to your system PATH)