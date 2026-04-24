import os
import asyncio
import logging
from flask import Flask
from threading import Thread
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

# --- 1. НАСТРОЙКА ЛОГИРОВАНИЯ ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 2. ВЕБ-СЕРВЕР ДЛЯ RENDER (FLASK) ---
app = Flask('')

@app.route('/')
def home():
    return "FoxRush Bot is Online!"

def run_flask():
    # Порт для Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- 3. НАСТРОЙКИ БОТА ---
# Твой новый токен
API_TOKEN = "8675521925:AAEX-QViQGct02fz0HgQ-kjUM5EKyoMelhI"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="🦊 Играть в FoxRush", 
        web_app=WebAppInfo(url="https://foxrush-2777e.web.app")
    ))

    await message.answer(
        f"Привет, {message.from_user.first_name}! 🦊\n\n"
        "Добро пожаловать в FoxRush. Нажимай на кнопку ниже, чтобы начать игру!",
        reply_markup=builder.as_markup()
    )

# --- 4. ГЛАВНЫЙ ЗАПУСК ---
async def main():
    # Запуск Flask в отдельном потоке
    Thread(target=run_flask, daemon=True).start()
    
    logger.info("--- ВЕБ-СЕРВЕР ЗАПУЩЕН ---")

    # Очистка очереди (удаляет старые сообщения перед стартом)
    await bot.delete_webhook(drop_pending_updates=True)
    
    logger.info("--- БОТ ЗАПУСКАЕТСЯ ---")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен")