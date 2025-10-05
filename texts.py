# texts.py

# --- Общие тексты ---
WELCOME_MESSAGE = (
    "👋 Добро пожаловать в Hatani – OpenVPN!\n\n"
    "Выберите действие:"
)
ACCESS_DENIED = (
    "❌ <b>Доступ запрещен.</b>\n\n"
    "Этот бот доступен только для участников специальной беседы."
)
ADMIN_CONTACT = "\n\nПожалуйста, обратитесь к администратору."

# --- Меню создания VPN ---
CHOOSE_OS = "Для какой операционной системы вы хотите создать VPN профиль?"
CONFIG_ALREADY_EXISTS_ALERT = "У вас уже есть активный VPN конфиг."
CONFIG_ALREADY_EXISTS_MSG = "У вас уже есть конфиг. Вы можете управлять им в разделе 'Мой VPN'."

# --- Инструкции для ОС ---
ANDROID_INSTRUCTIONS = (
    "<b>Инструкция для Android:</b>\n\n"
    "1. Сейчас я скачаю и пришлю вам установочный файл приложения OpenVPN Connect (<code>.apk</code>).\n"
    "2. Затем я сгенерирую и пришлю вам персональный файл конфигурации (<code>.ovpn</code>).\n"
    "3. Установите приложение, а затем импортируйте в него файл конфигурации."
)
ANDROID_APP_CAPTION = "Приложение OpenVPN для Android."

WINDOWS_INSTRUCTIONS = (
    "<b>Инструкция для Windows:</b>\n\n"
    "1. Сейчас я скачаю и пришлю вам установщик OpenVPN Connect (<code>.msi</code>).\n"
    "2. Затем я сгенерирую и пришлю вам файл конфигурации (<code>.ovpn</code>).\n"
    "3. После установки программы импортируйте в нее файл конфигурации."
)
WINDOWS_APP_CAPTION = (
    "Установщик OpenVPN для Windows.\n\n"
    "<b>Как установить:</b>\n"
    "1. Дважды кликните по этому файлу.\n"
    "2. Следуйте инструкциям на экране (обычно достаточно нажимать 'Next' и 'Install').\n"
    "3. Вам могут потребоваться права администратора."
)

IOS_INSTRUCTIONS = (
    "<b>Инструкция для iOS (iPhone/iPad):</b>\n\n"
    "1. Установите приложение <b>OpenVPN Connect</b> из App Store по ссылке ниже.\n"
    "2. После этого я сгенерирую и пришлю ваш персональный файл конфигурации (<code>.ovpn</code>).\n"
    "3. Откройте полученный файл и выберите 'Скопировать в OpenVPN Connect'.\n\n"
    "<a href='{ios_url}'><b>📲 Ссылка на приложение в App Store</b></a>"
)

LINUX_INSTRUCTIONS = (
    "<b>Инструкция для Linux (командная строка):</b>\n\n"
    "1. Сначала установите клиент <b>OpenVPN 3</b>, используя команды для вашего дистрибутива.\n"
    "2. Затем я сгенерирую и пришлю вам файл конфигурации (<code>.ovpn</code>).\n"
    "3. Импортируйте и запустите его командами, указанными ниже.\n\n"
    "<b><u>Для Debian / Ubuntu:</u></b>\n"
    "<code>apt update && apt install openvpn3</code>\n\n"
    "<b><u>Для Fedora / CentOS / RHEL:</u></b>\n"
    "<code>yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm</code>\n"
    "<code>yum install -y openvpn3-client-configs</code>\n\n"
    "<b><u>После получения файла (например, user_123.ovpn):</u></b>\n"
    "<i>Импорт:</i> <code>openvpn3 config-import --config user_123.ovpn</code>\n"
    "<i>Запуск:</i> <code>openvpn3 session-start --config user_123.ovpn</code>"
)

# --- Процесс генерации конфига ---
DOWNLOADING_APP = "📥 Скачиваю приложение..."
DOWNLOADING_INSTALLER = "📥 Скачиваю установщик для Windows..."
DOWNLOAD_APP_ERROR = "⚠️ Не удалось скачать файл приложения."
GENERATING_CONFIG = "⚙️ Генерирую ваш персональный файл конфигурации..."
CONFIG_CAPTION = "✅ <b>Готово!</b>\nВаш личный VPN-файл. Импортируйте его в приложение OpenVPN."
GENERATION_ERROR = "❌ <b>Ошибка!</b>\nНе удалось создать конфигурацию."
FINAL_MESSAGE = "Теперь вы можете вернуться в главное меню."

# --- Меню управления VPN ---
MY_VPN_NO_CONFIG_ALERT = "У вас еще нет созданного VPN."
MY_VPN_LOADING = "🔄 Получаю информацию о сервере..."
MY_VPN_SPEEDTEST_LOADING = (
    "<b><u>Тест скорости (Ookla):</u></b>\n"
    "<code>Запускаю... Это может занять до минуты.</code>"
)
MY_VPN_MENU_TEMPLATE = (
    "<b>Управление вашим VPN</b>\n\n"
    "<b>Имя конфига:</b> <code>{client_name}</code>\n"
    "<b>IP сервера:</b> <code>{ip}</code>\n"
    "<b>Страна:</b> {country}\n"
)
MY_VPN_SPEEDTEST_RESULTS = (
    "\n<b><u>Тест скорости (Ookla):</u></b>\n"
    "<b>Пинг:</b> <code>{ping}</code>\n"
    "<b>⬇️ Загрузка:</b> <code>{download}</code>\n"
    "<b>⬆️ Выгрузка:</b> <code>{upload}</code>\n"
)
MY_VPN_CHOOSE_ACTION = "\nВыберите действие:"

# --- Удаление конфига ---
DELETE_CONFIRM = (
    "<b>Вы уверены, что хотите отозвать доступ и удалить свой VPN конфиг?</b>\n\n"
    "Это действие необратимо. Вам потребуется создавать новый конфиг."
)
DELETE_IN_PROGRESS = "⏳ Отзываю сертификат для <code>{client_name}</code>... Пожалуйста, подождите."
DELETE_SUCCESS_MSG = (
    "✅ Ваш VPN конфиг был успешно отозван.\n\n"
    + WELCOME_MESSAGE
)
DELETE_SUCCESS_ALERT = "Конфиг удален!"
DELETE_ERROR = "❌ Произошла ошибка при отзыве сертификата."

# --- Запрос файла ---
REQUEST_FILE_NOT_FOUND = "Файл вашего конфига не найден на сервере!"