# 🤖 Hatani – OpenVPN Bot

Телеграм-бот на Python (Aiogram 3) для простого и быстрого управления персональными VPN-конфигами на базе OpenVPN. Бот предоставляет удобный интерфейс с инлайн-кнопками и ограничивает доступ только для участников определенного чата или по списку ID.

---

## ✨ Возможности

- **Создание VPN-конфигов**: Автоматическая генерация `.ovpn` файлов.
- **Поддержка платформ**: Инструкции и клиенты для **Android**, **iOS**, **Windows** и **Linux (CLI)**.
- **Гибкое управление доступом**: Доступ по членству в Telegram-чате или по белому списку User ID.
- **Удобный интерфейс**: Взаимодействие через инлайн-кнопки.
- **Управление своим VPN**:
    - Запрос `.ovpn` файла.
    - Отзыв (удаление) сертификата.
    - Просмотр информации о сервере (IP, страна).
    - Проверка скорости по запросу через **Ookla Speedtest**.
- **База данных SQLite**: Предотвращает создание нескольких конфигов одним пользователем.
- **Надежность**: Использует кастомный bash-скрипт для управления VPN.
- **Автоматический запуск**: Управляется через менеджер процессов `pm2` и запускается после перезагрузки сервера.

---

## 🚀 Быстрая установка (рекомендуемый способ)

Для развертывания бота на чистом сервере **Debian/Ubuntu** достаточно выполнить одну команду. Скрипт-установщик сделает всё за вас.

```bash
wget -O installer.sh https://raw.githubusercontent.com/Rewixx-png/Hatani-OpenVPN-Bot/main/installer.sh && sudo bash installer.sh
```

Установщик последовательно выполнит следующие шаги:
1.  Обновит пакеты и установит `git`, `python3-pip`, `openvpn`.
2.  Предложит настроить OpenVPN-сервер, если он еще не установлен.
3.  Установит и настроит Ookla Speedtest CLI.
4.  Склонирует репозиторий бота.
5.  Установит необходимые Python-библиотеки.
6.  В интерактивном режиме запросит у вас **токен бота**, **ID чата** и **список пользователей**.
7.  Установит менеджер процессов `pm2`, запустит бота и настроит его автозапуск после перезагрузки сервера.

После завершения установки бот будет работать в фоновом режиме.

---

## 🔧 Ручная установка

Если вы хотите установить бота вручную, следуйте этим шагам.

### 1. Клонирование репозитория

```bash
git clone https://github.com/Rewixx-png/Hatani-OpenVPN-Bot.git
cd Hatani-OpenVPN-Bot
```

### 2. Установка зависимостей
- **Системные пакеты:**
  ```bash
  sudo apt-get update && sudo apt-get install -y openvpn git python3-pip curl
  ```
- **OpenVPN сервер:** Если он еще не установлен, настройте его с помощью [angristan/openvpn-install](https://github.com/angristan/openvpn-install).
- **Speedtest CLI:**
  ```bash
  curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | sudo bash
  sudo apt-get install speedtest
  # Примите лицензию
  speedtest
  ```
- **Python-библиотеки:**
  ```bash
  pip install -r requirements.txt
  ```

### 3. Конфигурация бота
- Скопируйте файл конфигурации: `cp config.example.py config.py`.
- Отредактируйте `config.py` и заполните все поля: `BOT_TOKEN`, `ALLOWED_CHAT_ID`, `ALLOWED_USER_IDS` и другие пути, если они отличаются.

### 4. Запуск
- Установите `pm2`: `sudo npm install pm2 -g`.
- Запустите бота:
  ```bash
  pm2 start bot.py --name "HataniVPNBot" --interpreter python3
  pm2 save
  pm2 startup
  ```
---

## ⚙️ Управление ботом через PM2

- Посмотреть логи: `pm2 logs HataniVPNBot`
- Остановить: `pm2 stop HataniVPNBot`
- Запустить: `pm2 start HataniVPNBot`
- Перезапустить: `pm2 restart HataniVPNBot`

---

## 🤝 Contributing

Pull request'ы приветствуются. Для серьезных изменений, пожалуйста, сначала откройте issue для обсуждения того, что вы хотели бы изменить.

## 📄 Лицензия

[MIT](https://choosealicense.com/licenses/mit/)