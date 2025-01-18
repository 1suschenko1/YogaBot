from aiogram import Router, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import ContentType

video_router = Router()

# Обработчик для получения file_id видео
'''@video_router.message(lambda message: message.content_type == ContentType.VIDEO)
async def get_video_file_id(message: types.Message):
    file_id = message.video.file_id
    file_name = message.video.file_name  # (необязательно) Получаем имя файла
    await message.answer(f"Ваш file_id: {file_id}\nИмя файла: {file_name}")'''



# Клавиатура для меню видео
def video_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="ЙОГА ДЛЯ ПОЗВОНОЧНИКА"), KeyboardButton(text="РАЗОГРЕВАЮЩЕЕ ДЫХАНИЕ")],
            [KeyboardButton(text="ПОЗЫ СТОЯ"), KeyboardButton(text="ГИБКОСТЬ ТАЗОБЕДРЕННЫХ СУСТАВОВ")],
            [KeyboardButton(text="РАСТЯЖЕНИЕ БЁДЕР"), KeyboardButton(text="РАСТЯЖЕНИЕ ТЗБ СУСТАВОВ ЛЁЖА НА СПИНЕ")],
            [KeyboardButton(text="Назад")],
        ],
        resize_keyboard=True
    )


# Обработчик кнопки "Видео"
@video_router.message(lambda msg: msg.text == "Видеоуроки 🎥")
async def video_menu(message: types.Message):
    await message.answer("Выберите видео:", reply_markup=video_menu_kb())


V1 = (
    "Комплекс поз йоги для улучшения гибкости позвоночника. Йога для спины.\n\n"
    "Чем йога хороша для позвоночника, тем что мы задействуем все возможные направления подвижности: "
    "прогибы, наклоны вперёд и в стороны, скручивания и даже осевое вытяжение.\n\n"
    "Это способствует улучшению его гибкости, пластичности и конечно же здоровью. "
    "А от состояния позвоночника зависит и молодость и здоровье всего нашего тела."
)


@video_router.message(lambda msg: msg.text == "ЙОГА ДЛЯ ПОЗВОНОЧНИКА")
async def send_video_1(message: types.Message):
    file_id = "BAACAgIAAxkBAAILP2eK5-D0oMXisGgHz1eJTHA7UvYtAAI0aQACqARRSO9g_EN3xG-nNgQ"
    await message.answer_video(video=file_id, caption=V1)

V2 = (
    "Эту короткую и не сложную практику можно выполнять без коврика где бы вы не находились."
    "Дома, в офисе, в парке после бега, эта практика как перезарядка поможет вам растянуть позвоночник и всю заднюю поверхность тела."
)

@video_router.message(lambda msg: msg.text == "РАЗОГРЕВАЮЩЕЕ ДЫХАНИЕ")
async def send_video_2(message: types.Message):
    file_id = "BAACAgIAAxkBAAILQWeK6DzSURv9tgiKi-8cXahyqpaBAAI1aQACqARRSGUIlHCrJFPBNgQ"
    await message.answer_video(video=file_id, caption=V2)

V3 = (
    "Эту короткую и не сложную практику можно выполнять без коврика где бы вы не находились."
    "Дома, в офисе, в парке после бега, эта практика как перезарядка поможет вам растянуть позвоночник и всю заднюю поверхность тела."
)

@video_router.message(lambda msg: msg.text == "ПОЗЫ СТОЯ")
async def send_video_3(message: types.Message):
    file_id = "BAACAgIAAxkBAAILQ2eK6GQEjeaxzRlX6ra7u0nxM5aUAAI2aQACqARRSCB_RFvDAAFUGjYE"
    await message.answer_video(video=file_id, caption=V3)


V4 = (
    "Небольшой комплекс упражнений сидя, улучшающий подвижность, гибкость суставов ног."
)


@video_router.message(lambda msg: msg.text == "ГИБКОСТЬ ТАЗОБЕДРЕННЫХ СУСТАВОВ")
async def send_video_4(message: types.Message):
    file_id = "BAACAgIAAxkBAAILRWeK6ITZ_iu6oNlzkvquR3qZI3LSAAI3aQACqARRSJ85ZVX70YF1NgQ"
    await message.answer_video(video=file_id, caption=V4)

V5 = (
    "Небольшой комплекс упражнений на 'раскрытие' таза. Улучшает подвижность, гибкость суставов ног, растягивает мышцы бёдер."
    "Усиливает кровоснабжение органов таза положительно влияя на репродуктивную систему."
)

@video_router.message(lambda msg: msg.text == "РАСТЯЖЕНИЕ БЁДЕР")
async def send_video_3(message: types.Message):
    file_id = "BAACAgIAAxkBAAILR2eK6KVsJ1QMHthEcuG4LwMSJXEaAAI4aQACqARRSHdXWEIWV-8LNgQ"
    await message.answer_video(video=file_id, caption=V5)

V6 =(
    "Эффективный комплекс йоги на всё тело, с акцентом на улучшение подвижности тазобедренных суставов."
)

@video_router.message(lambda msg: msg.text == "РАСТЯЖЕНИЕ ТЗБ СУСТАВОВ ЛЁЖА НА СПИНЕ")
async def send_video_4(message: types.Message):
    file_id = "BAACAgIAAxkBAAILSWeK6MOzexstp6CMt4ySzn4Ko_ETAAI5aQACqARRSH9DF8RfEAKENgQ"
    await message.answer_video(video=file_id, caption=V6)


# Обработчик кнопки "Назад"
@video_router.message(lambda msg: msg.text == "Назад")
async def back_to_main_menu(message: types.Message):
    from .menu import main_menu_kb  # Импорт главного меню
    await message.answer("Вы вернулись в главное меню.", reply_markup=main_menu_kb())
