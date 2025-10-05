# database/manager.py

import aiosqlite
import logging
from config import DB_NAME

async def init_db():
    """Инициализирует базу данных и создает таблицу, если её нет."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                client_name TEXT NOT NULL UNIQUE,
                is_active BOOLEAN NOT NULL DEFAULT 1
            )
        ''')
        await db.commit()
    logging.info("Проверка и инициализация таблицы 'users' завершена.")

async def add_user(user_id: int, client_name: str):
    """Добавляет нового пользователя в базу данных."""
    logging.info(f"Добавление пользователя user_id={user_id} с client_name='{client_name}' в БД.")
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO users (user_id, client_name) VALUES (?, ?)",
            (user_id, client_name)
        )
        await db.commit()

async def get_user(user_id: int):
    """Получает данные пользователя по его ID."""
    logging.info(f"Запрос данных для user_id={user_id} из БД.")
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT client_name, is_active FROM users WHERE user_id = ?", (user_id,))
        return await cursor.fetchone()

async def delete_user(user_id: int):
    """Удаляет пользователя из базы данных."""
    logging.info(f"Удаление пользователя user_id={user_id} из БД.")
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        await db.commit()