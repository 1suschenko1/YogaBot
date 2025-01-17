import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties  # Для настройки parse_mode в aiogram 3.x
from config import BOT_TOKEN
from handlers import registration_router, menu_router

async def main():
    # Инициализируем бота с parse_mode="HTML" в aiogram 3.x
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher()

    # Подключаем роутеры
    dp.include_router(registration_router)
    dp.include_router(menu_router)

    print("Бот запущен. Ожидаем сообщения...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
