import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties  # Для настройки parse_mode в aiogram 3.x
from config import BOT_TOKEN
from handlers import registration_router, menu_router
from handlers.exer import exer_router  # Импортируем роутер для заданий
from handlers.settings import settings_router
from handlers.music import music_router
from handlers.video import video_router

async def main():
    # Инициализируем бота с parse_mode="HTML"
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher()

    # Подключаем роутеры
    dp.include_router(registration_router)  # Регистрация
    dp.include_router(menu_router)         # Меню
    dp.include_router(exer_router)         # Задания
    dp.include_router(settings_router)
    dp.include_router(music_router)
    dp.include_router(video_router)

    print("Бот запущен. Ожидаем сообщения...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
