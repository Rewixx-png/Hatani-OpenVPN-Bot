#!/bin/bash

# Выходим немедленно, если какая-либо команда завершилась с ошибкой
set -e

# --- НАСТРОЙКИ ---
# Укажите правильные пути к вашим директориям OpenVPN
EASYRSA_DIR="/etc/openvpn/easy-rsa"
OVPN_DIR="/etc/openvpn"
OUTPUT_DIR="/root" # Папка, куда будут сохраняться готовые .ovpn файлы

# --- ПРОВЕРКИ ---
if [ "$#" -ne 2 ]; then
    echo "Ошибка: неверное количество аргументов."
    echo "Использование: $0 {add|revoke} CLIENT_NAME"
    exit 1
fi

ACTION=$1
CLIENT_NAME=$2

# Проверка имени клиента на безопасность
if [[ ! "$CLIENT_NAME" =~ ^[a-zA-Z0-9_-]+$ ]]; then
    echo "Ошибка: Имя клиента содержит недопустимые символы."
    exit 1
fi

# --- ОСНОВНАЯ ЛОГИКА ---
case "$ACTION" in
    add)
        echo "--- Создание нового клиента: $CLIENT_NAME ---"
        
        cd "$EASYRSA_DIR"
        
        # Создаем сертификат клиента без пароля в неинтерактивном режиме
        ./easyrsa --batch build-client-full "$CLIENT_NAME" nopass
        
        echo "Сертификат для '$CLIENT_NAME' успешно создан."
        
        # Собираем .ovpn файл
        {
            cat "$OVPN_DIR/client-template.txt"
            echo "<ca>"
            cat "$EASYRSA_DIR/pki/ca.crt"
            echo "</ca>"
            echo "<cert>"
            # Используем awk, чтобы извлечь только сам сертификат
            awk '/BEGIN/,/END CERTIFICATE/' "$EASYRSA_DIR/pki/issued/$CLIENT_NAME.crt"
            echo "</cert>"
            echo "<key>"
            cat "$EASYRSA_DIR/pki/private/$CLIENT_NAME.key"
            echo "</key>"
            
            # Определяем, используется tls-crypt или tls-auth
            if [ -f "$OVPN_DIR/tls-crypt.key" ]; then
                echo "<tls-crypt>"
                cat "$OVPN_DIR/tls-crypt.key"
                echo "</tls-crypt>"
            elif [ -f "$OVPN_DIR/tls-auth.key" ]; then
                echo "key-direction 1"
                echo "<tls-auth>"
                cat "$OVPN_DIR/tls-auth.key"
                echo "</tls-auth>"
            fi
        } > "$OUTPUT_DIR/$CLIENT_NAME.ovpn"
        
        echo "Конфигурационный файл '$OUTPUT_DIR/$CLIENT_NAME.ovpn' успешно собран."
        echo "Клиент '$CLIENT_NAME' добавлен."
        ;;

    revoke)
        echo "--- Отзыв сертификата для клиента: $CLIENT_NAME ---"
        
        cd "$EASYRSA_DIR"
        
        # Отзываем сертификат
        ./easyrsa --batch revoke "$CLIENT_NAME"
        
        # Генерируем новый список отозванных сертификатов
        EASYRSA_CRL_DAYS=3650 ./easyrsa gen-crl
        
        # Копируем обновленный CRL файл
        cp "$EASYRSA_DIR/pki/crl.pem" "$OVPN_DIR/crl.pem"
        chmod 644 "$OVPN_DIR/crl.pem"
        
        # Удаляем старый .ovpn файл
        rm -f "$OUTPUT_DIR/$CLIENT_NAME.ovpn"
        
        echo "Сертификат для '$CLIENT_NAME' успешно отозван."
        ;;
        
    *)
        echo "Ошибка: неизвестное действие '$ACTION'."
        echo "Доступные действия: add, revoke."
        exit 1
        ;;
esac

exit 0