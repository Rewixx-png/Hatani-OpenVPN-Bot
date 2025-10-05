# bot.py

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.types import Message, CallbackQuery

from config import BOT_TOKEN, ALLOWED_CHAT_ID
from database import manager as db
from handlers import common, vpn_creation, vpn_management

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Middleware для проверки доступа ---
class AccessMiddleware:
    def __init__(self, chat_id: int):
        self.chat_id = chat_id

    async def __call__(self, handler, event: Message | CallbackQuery, data) -> None:
        user_id = event.from_user.id
        try:
            member = await bot.get_chat_member(chat_id=self.chat_id, user_id=user_id)
            if member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
                raise Exception("User is not a member of the allowed chat.")
        except Exception as e:
            logging.warning(f"Доступ запрещен для user_id {user_id}. Ошибка: {e}")
            if isinstance(event, Message):
                await event.answer("❌ **Доступ запрещен.**\n\nЭтот бот доступен только для участников специальной беседы.")
            elif isinstance(event, CallbackQuery):
                await event.answer("❌ Доступ запрещен.", show_alert=True)
            return
        
        return await handler(event, data)

async def on_startup(dispatcher: Dispatcher):
    """Функция, выполняемая при старте бота."""
    await db.init_db()
    logging.info("База данных успешно инициализирована.")
    logging.info("Бот запущен и готов к работе.")

async def main():
    """Основная функция для запуска бота."""
    # Улучшенный формат логирования для более детальной отладки
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s - %(levelname)s - [%(name)s:%(funcName)s] - %(message)s"
    )
    
    # Регистрация middleware
    dp.message.middleware(AccessMiddleware(ALLOWED_CHAT_ID))
    dp.callback_query.middleware(AccessMiddleware(ALLOWED_CHAT_ID))
    
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