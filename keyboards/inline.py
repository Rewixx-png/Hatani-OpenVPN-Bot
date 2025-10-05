# keyboards/inline.py

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

class VpnAction(CallbackData, prefix="vpn"):
    action: str
    client_name: str

def get_main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔐 Создать VPN", callback_data="create_vpn")
    builder.button(text="📂 Мой VPN", callback_data="my_vpn")
    builder.adjust(1)
    return builder.as_markup()

def get_create_vpn_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🤖 Android", callback_data="create_for_android")
    builder.button(text="🍏 iOS (iPhone/iPad)", callback_data="create_for_ios")
    builder.button(text="💻 Windows", callback_data="create_for_windows")
    builder.button(text="🐧 Linux (CLI)", callback_data="create_for_linux")
    builder.button(text="⬅️ Назад", callback_data="back_to_main")
    builder.adjust(1)
    return builder.as_markup()

def get_my_vpn_keyboard(client_name: str):
    """
    Возвращает клавиатуру для управления VPN (ОБНОВЛЕНО).
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="📄 Запросить файл конфига", callback_data="request_vpn_file")
    # --- НОВАЯ КНОПКА ---
    # Для проверки скорости мы просто снова вызовем колбэк "my_vpn",
    # но с дополнительным параметром, чтобы запустить тест.
    builder.button(text="🏁 Проверить скорость", callback_data="my_vpn:speedtest")
    builder.button(text="❌ Отозвать/Удалить конфиг", callback_data=VpnAction(action="delete", client_name=client_name).pack())
    builder.button(text="⬅️ Назад", callback_data="back_to_main")
    builder.adjust(1)
    return builder.as_markup()

def get_confirm_delete_keyboard(client_name: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Да, я уверен", callback_data=VpnAction(action="confirm_delete", client_name=client_name).pack())
    builder.button(text="Отмена", callback_data="my_vpn")
    builder.adjust(1)
    return builder.as_markup()

def get_back_to_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ В главное меню", callback_data="back_to_main")
    return builder.as_markup()