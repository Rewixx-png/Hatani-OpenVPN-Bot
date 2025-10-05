# config.py

# --- Основные настройки ---
BOT_TOKEN = "7685653050:AAHGUTnwYeeEU3CrLHryWtC3AFgAtiSrANE" 

# --- Настройки доступа ---
ALLOWED_CHAT_ID = -1002033901364

# --- Пути и URL ---
VPN_SCRIPT_PATH = "/root/Bots/HataniVPN/CreateVPN/vpn_manager.sh"
CLIENT_CONFIGS_DIR = "/root/" 

# URL-адреса клиентов OpenVPN
OPENVPN_APK_URL = "https://github.com/schwabe/ics-openvpn/releases/download/v0.7.61/ics-openvpn-0.7.61.apk"
OPENVPN_MSI_URL = "https://openvpn.net/downloads/openvpn-connect-v3-windows.msi" # <-- НОВОЕ
OPENVPN_IOS_URL = "https://itunes.apple.com/us/app/openvpn-connect/id590379981?mt=8" # <-- НОВОЕ

# Временная папка для скачивания файлов
TEMP_DOWNLOAD_DIR = "/tmp/"

# --- Настройки базы данных ---
DB_NAME = "vpn_users.db"