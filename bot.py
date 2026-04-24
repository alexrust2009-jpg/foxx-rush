import os
import asyncio
import logging
import time
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
    # Этот текст подтверждает, что сервер прошел проверку Render
    return "FoxRush Bot is Online!"

def run_flask():
    # Получаем порт от Render или используем 10000 по умолчанию
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"Flask запускается на порту {port}...")
    app.run(host='0.0.0.0', port=port)

# --- 3. НАСТРОЙКИ БОТА ---
# Твой токен (уже вписан)
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
        "Добро пожаловать в FoxRush! Нажми кнопку ниже, чтобы запустить игру.",
        reply_markup=builder.as_markup()
    )

# --- 4. ГЛАВНАЯ ФУНКЦИЯ ---
async def main_bot():
    logger.info("Очистка очереди обновлений...")
    # drop_pending_updates=True удаляет сообщения, пришедшие пока бот спал
    await bot.delete_webhook(drop_pending_updates=True)
    
    logger.info("Запуск polling (опроса Telegram)...")
    await dp.start_polling(bot)

# --- 5. ТОЧКА ВХОДА ---
if __name__ == "__main__":
    try:
        # Шаг A: Запускаем Flask в фоновом потоке
        server_thread = Thread(target=run_flask, daemon=True)
        server_thread.start()
        
        # Шаг B: Даем серверу 3 секунды, чтобы Render его "увидел"
        logger.info("Ожидание стабилизации сервера (3 сек)...")
        time.sleep(3)
        
        # Шаг C: Запускаем асинхронную часть бота
        asyncio.run(main_bot())
        
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот полностью остановлен.")