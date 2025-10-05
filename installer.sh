#!/bin/bash

# --- Цвета для красивого вывода ---
C_RED='\033[0;31m'
C_GREEN='\033[0;32m'
C_YELLOW='\033[0;33m'
C_BLUE='\033[0;34m'
C_NC='\033[0m' # No Color

# --- Название процесса для PM2 ---
PM2_PROCESS_NAME="HataniVPNBot"

# --- Функция для вывода сообщений ---
log() {
    echo -e "${C_BLUE}> ${C_NC}$1"
}
success() {
    echo -e "${C_GREEN}> ${C_NC}$1"
}
warn() {
    echo -e "${C_YELLOW}> Предупреждение: ${C_NC}$1"
}
error() {
    echo -e "${C_RED}> Ошибка: ${C_NC}$1"
    exit 1
}

# --- Проверка на root ---
if [ "$EUID" -ne 0 ]; then
  error "Пожалуйста, запустите этот скрипт с правами root (через sudo)."
fi

# --- 1. Установка системных зависимостей ---
log "Обновление списка пакетов..."
apt-get update -y || error "Не удалось обновить пакеты."

log "Установка curl, git, python3-pip и openvpn..."
apt-get install -y curl git python3-pip openvpn || error "Не удалось установить базовые пакеты."

# --- 2. Установка OpenVPN сервера (если нужно) ---
if ! command -v openvpn &> /dev/null || [ ! -f /etc/openvpn/server.conf ]; then
    warn "OpenVPN сервер не найден. Запускаю скрипт установки..."
    read -p "Нажмите Enter для начала настройки OpenVPN..."
    curl -O https://raw.githubusercontent.com/angristan/openvpn-install/master/openvpn-install.sh
    chmod +x openvpn-install.sh
    ./openvpn-install.sh || error "Установка OpenVPN завершилась с ошибкой."
fi
success "OpenVPN сервер готов к работе."

# --- 3. Установка Speedtest CLI ---
if ! command -v speedtest &> /dev/null; then
    log "Установка Ookla Speedtest CLI..."
    curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | bash || error "Не удалось настроить репозиторий Speedtest."
    apt-get install -y speedtest || error "Не удалось установить Speedtest."
    # Автоматическое принятие лицензии
    speedtest --accept-license --accept-gdpr > /dev/null 2>&1
    success "Speedtest CLI установлен."
else
    success "Speedtest CLI уже установлен."
fi


# --- 4. Клонирование репозитория ---
log "Клонирование репозитория бота..."
git clone https://github.com/Rewixx-png/Hatani-OpenVPN-Bot.git || error "Не удалось клонировать репозиторий."
cd Hatani-OpenVPN-Bot || error "Не удалось перейти в папку проекта."

# --- 5. Установка зависимостей Python ---
log "Установка зависимостей Python через pip..."
pip install -r requirements.txt || error "Не удалось установить Python-зависимости."

# --- 6. Интерактивная настройка конфига ---
log "Настройка конфигурационного файла..."
cp config.example.py config.py

# Спрашиваем токен
read -p "Введите ваш BOT_TOKEN от @BotFather: " BOT_TOKEN
sed -i "s|BOT_TOKEN = \".*\"|BOT_TOKEN = \"$BOT_TOKEN\"|" config.py

# Спрашиваем ID чата
read -p "Введите ID чата для проверки доступа (0, если доступ только по списку ID): " ALLOWED_CHAT_ID

# --- Новая логика для списка разрешенных пользователей ---
if [ "$ALLOWED_CHAT_ID" -eq 0 ]; then
    sed -i "s/ALLOWED_CHAT_ID = .*/ALLOWED_CHAT_ID = 0/" config.py
    log "Выбран доступ по списку ID."
    read -p "Введите разрешенные Telegram User ID через запятую (например, 12345,67890): " USER_IDS
    # Добавляем новую переменную в конец config.py
    echo "" >> config.py
    echo "# Список ID пользователей, которым разрешен доступ, если ALLOWED_CHAT_ID = 0" >> config.py
    echo "ALLOWED_USER_IDS = [$USER_IDS]" >> config.py
else
    sed -i "s/ALLOWED_CHAT_ID = .*/ALLOWED_CHAT_ID = $ALLOWED_CHAT_ID/" config.py
    # Если используется чат, оставляем список пользователей пустым
    echo "" >> config.py
    echo "# Список ID пользователей, которым разрешен доступ, если ALLOWED_CHAT_ID = 0" >> config.py
    echo "ALLOWED_USER_IDS = []" >> config.py
fi

# Устанавливаем пути автоматически
VPN_SCRIPT_PATH=$(realpath "CreateVPN/vpn_manager.sh")
sed -i "s|VPN_SCRIPT_PATH = \".*\"|VPN_SCRIPT_PATH = \"$VPN_SCRIPT_PATH\"|" config.py

success "Файл config.py успешно настроен."

# --- 7. Настройка прав для скрипта ---
log "Установка прав на выполнение для vpn_manager.sh..."
chmod +x CreateVPN/vpn_manager.sh

# --- 8. Установка и настройка PM2 ---
log "Установка/обновление Node.js и npm..."
apt-get install -y nodejs npm || warn "Не удалось установить Node.js/npm. Пожалуйста, установите их вручную."

if ! command -v pm2 &> /dev/null; then
    log "Установка PM2..."
    npm install pm2 -g || error "Не удалось установить PM2."
else
    log "PM2 уже установлен."
fi

log "Запуск бота через PM2..."
pm2 start bot.py --name "$PM2_PROCESS_NAME" --interpreter python3 || error "Не удалось запустить бота через PM2."

log "Сохранение списка процессов PM2 для автозапуска после перезагрузки..."
pm2 save
pm2 startup || warn "Не удалось настроить автозапуск PM2. Выполните команду, предложенную PM2, вручную."

success "----------------------------------------------------"
success "Установка завершена! Бот '$PM2_PROCESS_NAME' запущен."
success "Чтобы посмотреть логи, используйте команду: pm2 logs $PM2_PROCESS_NAME"
success "Чтобы остановить бота: pm2 stop $PM2_PROCESS_NAME"
success "Чтобы запустить снова: pm2 start $PM2_PROCESS_NAME"
success "----------------------------------------------------"

exit 0