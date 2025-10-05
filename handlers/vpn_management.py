# handlers/vpn_management.py

import os
import logging
import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from keyboards.inline import (
    VpnAction, get_my_vpn_keyboard, get_confirm_delete_keyboard, 
    get_back_to_main_keyboard, get_main_menu_keyboard
)
from database import manager as db
from utils import server_info, vpn_script
from config import CLIENT_CONFIGS_DIR
# Импортируем все необходимые тексты
from texts import *

router = Router()

@router.callback_query(F.data.startswith("my_vpn"))
async def show_my_vpn_menu(callback: CallbackQuery):
    """
    Универсальный обработчик для меню "Мой VPN".
    Запускает тест скорости, если в колбэке есть флаг ':speedtest'.
    """
    user_id = callback.from_user.id
    logging.info(f"Пользователь {user_id} вошел в меню 'Мой VPN'.")
    user_data = await db.get_user(user_id)
    if not user_data:
        await callback.answer(MY_VPN_NO_CONFIG_ALERT, show_alert=True)
        return

    client_name = user_data[0]
    run_speedtest = ":speedtest" in callback.data

    await callback.message.edit_text(MY_VPN_LOADING)
    await callback.answer()
    location_info = await server_info.get_server_location_info()

    message_text = MY_VPN_MENU_TEMPLATE.format(
        client_name=client_name,
        ip=location_info['ip'],
        country=location_info['country']
    )

    if run_speedtest:
        await callback.message.edit_text(
            f"{message_text}\n{MY_VPN_SPEEDTEST_LOADING}",
            parse_mode="HTML"
        )
        speed_results = await server_info.get_speedtest_results()
        message_text += MY_VPN_SPEEDTEST_RESULTS.format(**speed_results)

    message_text += MY_VPN_CHOOSE_ACTION
    await callback.message.edit_text(
        message_text,
        reply_markup=get_my_vpn_keyboard(client_name),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "request_vpn_file")
async def request_vpn_file(callback: CallbackQuery):
    user_id = callback.from_user.id
    logging.info(f"Пользователь {user_id} запросил свой файл конфига.")
    user_data = await db.get_user(user_id)
    if not user_data:
        await callback.answer("Не удалось найти ваш конфиг.", show_alert=True)
        return
    
    client_name = user_data[0]
    config_path = os.path.join(CLIENT_CONFIGS_DIR, f"{client_name}.ovpn")

    if os.path.exists(config_path):
        config_file = FSInputFile(config_path)
        await callback.message.answer_document(config_file)
        await callback.answer()
        logging.info(f"Повторно отправили конфиг '{client_name}' пользователю {user_id}.")
    else:
        logging.warning(f"Файл конфига '{config_path}' для пользователя {user_id} не найден на сервере.")
        await callback.answer(REQUEST_FILE_NOT_FOUND, show_alert=True)

@router.callback_query(VpnAction.filter(F.action == "delete"))
async def confirm_delete_config(callback: CallbackQuery, callback_data: VpnAction):
    logging.info(f"Пользователь {callback.from_user.id} нажал 'Удалить' для конфига '{callback_data.client_name}'. Запрос подтверждения.")
    await callback.message.edit_text(
        DELETE_CONFIRM,
        reply_markup=get_confirm_delete_keyboard(callback_data.client_name),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(VpnAction.filter(F.action == "confirm_delete"))
async def delete_config(callback: CallbackQuery, callback_data: VpnAction):
    user_id = callback.from_user.id
    client_name = callback_data.client_name
    logging.info(f"Пользователь {user_id} подтвердил удаление конфига '{client_name}'.")
    
    await callback.message.edit_text(
        DELETE_IN_PROGRESS.format(client_name=client_name), 
        parse_mode="HTML", 
        reply_markup=None
    )
    
    success = await vpn_script.revoke_vpn_config(client_name)
    
    if success:
        await db.delete_user(user_id)
        logging.info(f"Сертификат для '{client_name}' успешно отозван. Пользователь удален из БД.")
        
        await callback.message.edit_text(
            DELETE_SUCCESS_MSG,
            reply_markup=get_main_menu_keyboard()
        )
        await callback.answer(DELETE_SUCCESS_ALERT, show_alert=False)
    else:
        logging.error(f"Ошибка при отзыве сертификата для '{client_name}'.")
        await callback.message.edit_text(
            DELETE_ERROR + ADMIN_CONTACT,
            reply_markup=get_back_to_main_keyboard()
        )
        await callback.answer("Ошибка!", show_alert=True)