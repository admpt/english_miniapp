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

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(commands=['start'])
async def send_start_message(message: types.Message):
    await message.answer("Откройте мини-приложение!",
                         reply_markup=types.ReplyKeyboardMarkup(
                             keyboard=[
                                 [types.KeyboardButton(text="Запустить Mini-App",
                                                       request_contact=False)]
                             ],
                             resize_keyboard=True))

@dp.message_handler(lambda message: message.text == "Запустить Mini-App")
async def open_web_app(message: types.Message):
    web_app_url = "https://your-web-app-url.com"  # Вставьте ваш URL
    await message.answer("Открываю мини-приложение...",
                         reply_markup=types.InlineKeyboardMarkup().add(
                             types.InlineKeyboardButton("Открыть", web_app=web_app_url)
                         ))
# Запуск бота
async def main() -> None:
    logging.info("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

