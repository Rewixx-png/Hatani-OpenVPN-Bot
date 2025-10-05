# handlers/common.py

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from keyboards.inline import get_main_menu_keyboard
from texts import WELCOME_MESSAGE # <-- Импортируем текст

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(
        WELCOME_MESSAGE,
        reply_markup=get_main_menu_keyboard()
    )

@router.callback_query(F.data == "back_to_main")
async def back_to_main_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        WELCOME_MESSAGE,
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()