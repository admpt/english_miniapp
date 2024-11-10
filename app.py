import json
import logging
import sys
import asyncio

import uvicorn
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from database import User, get_async_session
from my_token import TOKEN

API_TOKEN = TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Инициализация FastAPI
app = FastAPI()

# Настройка CORS, если необходимо
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Замените на ваши домены при необходимости
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Обработка команды /start
@dp.message(Command("start"))
async def send_start_message(message: types.Message, state: FSMContext):
    command = message.text.split(maxsplit=1)
    user_id = message.from_user.id
    referral_code = command[1] if len(command) > 1 else None
    if referral_code and referral_code.startswith('='):
        referral_code = referral_code[1:]  # Удаляем '=' если есть

    await process_start_command(message, referral_code, state, upsert_user)

async def process_start_command(message: types.Message, referral_code: str, state: FSMContext,
                                upsert_user_func) -> None:
    await state.clear()  # Сбрасываем состояние
    logging.info(f"process_start_command {message.from_user.id}")
    logging.info(f"Referral code: {referral_code}")

    web_app_url = "https://admpt.github.io/english_miniapp/"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть", web_app={"url": web_app_url})]
    ])

    await message.answer("Добро пожаловать! Нажмите на кнопку ниже, чтобы открыть мини-приложение.",
                         reply_markup=keyboard)
    try:
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        full_name = f"{first_name} {last_name}" if first_name and last_name else first_name or last_name or ""

        # Вставляем или обновляем пользователя
        await upsert_user_func(message.from_user.id, message.from_user.username or '', full_name, referral_code)

        logging.info(f"User data updated for {message.from_user.id}")

    except Exception as e:
        logging.error(f"Error while updating user data: {e}")

async def upsert_user(user_id: int, username_tg: str, full_name: str, referral_code: str = None) -> None:
    logging.info(f"Attempting to upsert user: {user_id}")

    # Здесь мы используем await
    async with await get_async_session() as session:
        try:
            user = await session.get(User, user_id)
            if user:
                user.username_tg = username_tg
                user.full_name = full_name
                user.referral_code = referral_code
                logging.info(f"Updating user {user_id}: {username_tg}, {full_name}, {referral_code}")
            else:
                user = User(id=user_id, username_tg=username_tg, full_name=full_name, referral_code=referral_code)
                session.add(user)
                logging.info(f"Adding new user {user_id}: {username_tg}, {full_name}, {referral_code}")

            await session.commit()
            logging.info(f"User {user_id} upserted successfully.")
        except Exception as e:
            logging.error(f"Database error while upserting user: {e}")
            await session.rollback()  # Откатываем сессию при ошибке

@app.get("/user/{user_id}")
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    # Используем сессию напрямую без вызова
    result = await session.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()

    if user is None:
        return {"full_name": "Имя не найдено", "balance": "Баланс не найден"}  # Возвращаем сообщения о ненайденных данных

    return {
        "full_name": user.full_name,
        "balance": str(user.balance)  # Преобразуем в строку, если нужно
    }

app.mount("/docs", StaticFiles(directory="docs"), name="docs")

# Запуск бота и FastAPI
async def main() -> None:
    logging.info("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    uvicorn.run(app, host="127.0.0.1", port=8000)