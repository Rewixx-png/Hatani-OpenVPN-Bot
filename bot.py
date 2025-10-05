# bot.py

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.types import Message, CallbackQuery

# Импортируем тексты и конфигурацию
import texts
from config import BOT_TOKEN, ALLOWED_CHAT_ID, ALLOWED_USER_IDS
from database import manager as db
from handlers import common, vpn_creation, vpn_management

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Middleware для проверки доступа (ОБНОВЛЕНО) ---
class AccessMiddleware:
    def __init__(self, chat_id: int, user_ids: list):
        self.chat_id = chat_id
        # Убедимся, что user_ids - это список целых чисел
        self.user_ids = [int(uid) for uid in user_ids]
        
        # Информационное сообщение при старте
        if self.chat_id == 0 and self.user_ids:
            logging.info(f"Режим доступа: Белый список пользователей. ID: {self.user_ids}")
        elif self.chat_id != 0:
            logging.info(f"Режим доступа: Членство в чате. ID чата: {self.chat_id}")
        else:
            logging.warning("Доступ не настроен! Бот не будет доступен никому.")

    async def __call__(self, handler, event: Message | CallbackQuery, data) -> None:
        user_id = event.from_user.id
        access_granted = False

        # --- Логика проверки ---
        # 1. Проверка по списку ID, если чат установлен в 0
        if self.chat_id == 0:
            if self.user_ids and user_id in self.user_ids:
                access_granted = True
        
        # 2. Проверка по членству в чате, если ID чата указан
        elif self.chat_id != 0:
            try:
                member = await bot.get_chat_member(chat_id=self.chat_id, user_id=user_id)
                if member.status not in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
                    access_granted = True
            except Exception as e:
                logging.warning(f"Ошибка проверки членства в чате для user_id {user_id}: {e}")
        
        # --- Результат ---
        if access_granted:
            return await handler(event, data) # Доступ разрешен, продолжаем
        else:
            # Если доступ запрещен
            logging.warning(f"Доступ запрещен для user_id {user_id}.")
            if isinstance(event, Message):
                await event.answer(texts.ACCESS_DENIED, parse_mode="HTML")
            elif isinstance(event, CallbackQuery):
                await event.answer("❌ Доступ запрещен.", show_alert=True)
            return

async def on_startup(dispatcher: Dispatcher):
    """Функция, выполняемая при старте бота."""
    await db.init_db()
    logging.info("База данных успешно инициализирована.")
    logging.info("Бот запущен и готов к работе.")

async def main():
    """Основная функция для запуска бота."""
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s - %(levelname)s - [%(name)s:%(funcName)s] - %(message)s"
    )
    
    # Регистрация middleware с новыми параметрами
    dp.message.middleware(AccessMiddleware(ALLOWED_CHAT_ID, ALLOWED_USER_IDS))
    dp.callback_query.middleware(AccessMiddleware(ALLOWED_CHAT_ID, ALLOWED_USER_IDS))
    
    # Регистрация роутеров
    dp.include_router(common.router)
    dp.include_router(vpn_creation.router)
    dp.include_router(vpn_management.router)
    
    # Регистрация функции на запуск
    dp.startup.register(on_startup)

    # Запуск бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())