# handlers/vpn_creation.py

import os
import aiohttp
import logging
import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from keyboards.inline import get_create_vpn_keyboard, get_back_to_main_keyboard
from database import manager as db
from utils import vpn_script
from config import (
    OPENVPN_APK_URL, OPENVPN_MSI_URL, OPENVPN_IOS_URL,
    TEMP_DOWNLOAD_DIR, CLIENT_CONFIGS_DIR
)
# Импортируем все необходимые тексты
from texts import *

router = Router()

@router.callback_query(F.data == "create_vpn")
async def show_create_vpn_menu(callback: CallbackQuery):
    """
    Проверяет, есть ли у пользователя конфиг, и показывает меню создания.
    """
    user_id = callback.from_user.id
    user_data = await db.get_user(user_id)
    if user_data:
        await callback.answer(CONFIG_ALREADY_EXISTS_ALERT, show_alert=True)
        return

    await callback.message.edit_text(
        CHOOSE_OS,
        reply_markup=get_create_vpn_keyboard()
    )
    await callback.answer()


# --- ОБРАБОТЧИКИ ДЛЯ КАЖДОЙ ПЛАТФОРМЫ ---

@router.callback_query(F.data == "create_for_android")
async def create_for_android(callback: CallbackQuery):
    await callback.message.edit_text(ANDROID_INSTRUCTIONS, parse_mode="HTML")
    
    status_message = await callback.message.answer(DOWNLOADING_APP)
    apk_path = os.path.join(TEMP_DOWNLOAD_DIR, "openvpn-connect.apk")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(OPENVPN_APK_URL) as response:
                if response.status == 200:
                    with open(apk_path, "wb") as f:
                        f.write(await response.read())
                    apk_file = FSInputFile(apk_path)
                    await callback.message.answer_document(apk_file, caption=ANDROID_APP_CAPTION)
                    await status_message.delete()
                else:
                    await status_message.edit_text(DOWNLOAD_APP_ERROR)
    except Exception as e:
        logging.error(f"Ошибка скачивания APK для Android: {e}")
        await status_message.edit_text(DOWNLOAD_APP_ERROR + ADMIN_CONTACT)
    finally:
        if os.path.exists(apk_path):
            os.remove(apk_path)

    await _generate_and_send_config(callback)


@router.callback_query(F.data == "create_for_windows")
async def create_for_windows(callback: CallbackQuery):
    await callback.message.edit_text(WINDOWS_INSTRUCTIONS, parse_mode="HTML")

    status_message = await callback.message.answer(DOWNLOADING_INSTALLER)
    msi_path = os.path.join(TEMP_DOWNLOAD_DIR, "openvpn-connect-v3-windows.msi")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(OPENVPN_MSI_URL) as response:
                if response.status == 200:
                    with open(msi_path, "wb") as f:
                        f.write(await response.read())
                    msi_file = FSInputFile(msi_path)
                    await callback.message.answer_document(msi_file, caption=WINDOWS_APP_CAPTION, parse_mode="HTML")
                    await status_message.delete()
                else:
                    await status_message.edit_text(DOWNLOAD_APP_ERROR)
    except Exception as e:
        logging.error(f"Ошибка скачивания MSI для Windows: {e}")
        await status_message.edit_text(DOWNLOAD_APP_ERROR + ADMIN_CONTACT)
    finally:
        if os.path.exists(msi_path):
            os.remove(msi_path)
    
    await _generate_and_send_config(callback)


@router.callback_query(F.data == "create_for_ios")
async def create_for_ios(callback: CallbackQuery):
    await callback.message.edit_text(
        IOS_INSTRUCTIONS.format(ios_url=OPENVPN_IOS_URL),
        parse_mode="HTML",
        disable_web_page_preview=True
    )
    await _generate_and_send_config(callback)


@router.callback_query(F.data == "create_for_linux")
async def create_for_linux(callback: CallbackQuery):
    await callback.message.edit_text(LINUX_INSTRUCTIONS, parse_mode="HTML")
    await _generate_and_send_config(callback)


# --- ОБЩАЯ ФУНКЦИЯ ДЛЯ ГЕНЕРАЦИИ КОНФИГА ---

async def _generate_and_send_config(callback: CallbackQuery):
    """
    Общая логика для создания и отправки .ovpn файла.
    """
    user_id = callback.from_user.id
    if await db.get_user(user_id):
        await callback.answer(CONFIG_ALREADY_EXISTS_ALERT, show_alert=True)
        await callback.message.answer(CONFIG_ALREADY_EXISTS_MSG, reply_markup=get_back_to_main_keyboard())
        return

    client_name = f"user_{user_id}"
    config_path = os.path.join(CLIENT_CONFIGS_DIR, f"{client_name}.ovpn")

    status_message = await callback.message.answer(GENERATING_CONFIG)
    
    try:
        success = await vpn_script.create_vpn_config(client_name)
        if not success or not os.path.exists(config_path):
            raise ValueError("Скрипт сообщил об ошибке или файл конфигурации не был создан.")
        
        await db.add_user(user_id, client_name)
        
        config_file = FSInputFile(config_path)
        await callback.message.answer_document(
            config_file,
            caption=CONFIG_CAPTION,
            parse_mode="HTML"
        )
        await status_message.delete()
        await callback.message.answer(FINAL_MESSAGE, reply_markup=get_back_to_main_keyboard())

    except Exception as e:
        logging.error(f"Ошибка при генерации конфига для user_id={user_id}: {e}", exc_info=True)
        await status_message.edit_text(
            GENERATION_ERROR + ADMIN_CONTACT,
            parse_mode="HTML", reply_markup=get_back_to_main_keyboard()
        )