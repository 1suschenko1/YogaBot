import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.registration import registration_router

# Создаем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Регистрация маршрутов
dp.include_router(registration_router)

async def main():
    try:
        print("Бот запущен.")
        await dp.start_polling(bot)  # Ожидание запуска polling
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")

if __name__ == "__main__":
    asyncio.run(main())  # Запуск события с использованием asyncio
