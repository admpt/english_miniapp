import logging
import sys

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
import asyncio

API_TOKEN = '7094389168:AAH54gBQDqxxLGDT4FxdSJo3jesLcMKVS3o'
# Настройка логирования
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Обработка команды /start
@dp.message(Command("start"))
async def send_start_message(message: types.Message):
    web_app_url = "https://admpt.github.io/test-mini-app/"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть", web_app={"url": web_app_url})]
    ])

    await message.answer("Открываю мини-приложение...", reply_markup=keyboard)

# Запуск бота
async def main() -> None:
    logging.info("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())