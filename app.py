import logging
import sys

from aiogram.fsm.context import FSMContext
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
import asyncio

from database import User, get_async_session

API_TOKEN = '7094389168:AAH54gBQDqxxLGDT4FxdSJo3jesLcMKVS3o'
# Настройка логирования
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


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

    web_app_url = "https://admpt.github.io/test-mini-app/"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть", web_app={"url": web_app_url})]
    ])

    await message.answer("Добро пожаловать! Нажмите на кнопку ниже, чтобы открыть мини-приложение.",
                         reply_markup=keyboard)

    button = InlineKeyboardButton(text="Начать обучение!", callback_data="start_learning")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])

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
    async for session in get_async_session():
        try:
            # Выполняем upsert
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
# Запуск бота
async def main() -> None:
    logging.info("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())