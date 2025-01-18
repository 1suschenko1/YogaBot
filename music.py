from aiogram import Router, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from .menu import main_menu_kb
from aiogram.types import ContentType

music_router = Router()



'''# Обработчик для получения file_id аудио
@music_router.message(lambda message: message.content_type == ContentType.AUDIO)
async def get_audio_file_id(message: types.Message):
    file_id = message.audio.file_id  # Получаем file_id
    file_name = message.audio.file_name  # (необязательно) Получаем имя файла, если нужно
    await message.answer(f"Ваш file_id: {file_id}\nИмя файла: {file_name}")'''


# ---------- Подменю для кнопки "Музыка" ----------
def music_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Meditation Music"), KeyboardButton(text="Instrumental meditation")],
            [KeyboardButton(text="Ambient Yoga Music"), KeyboardButton(text="963 Hz pineal gland activation")],
            [KeyboardButton(text="Назад")],
        ],
        resize_keyboard=True
    )


# ---------- Обработчик кнопки "Музыка" ----------
@music_router.message(lambda msg: msg.text == "Музыка 🎶")
async def music_menu(message: types.Message):
    await message.answer("Выберите композицию:", reply_markup=music_menu_kb())


# ---------- Обработчики кнопок подменю ----------
@music_router.message(lambda msg: msg.text == "Meditation Music")
async def send_music_1(message: types.Message):
    file_id = "CQACAgIAAxkBAAIJ3WeKvna_L_wUCJhDK9fvDiFKcL7wAAIxaAACqARRSCve3Fs5HOYLNgQ"
    await message.answer_audio(audio=file_id, caption="Meditation Music 🎶")


@music_router.message(lambda msg: msg.text == "Instrumental meditation")
async def send_music_2(message: types.Message):
    file_id = "CQACAgIAAxkBAAIJ32eKvqV5OJWhvMLHpFrFxj4zuqeeAAI0aAACqARRSE1Zff6zbYrfNgQ"
    await message.answer_audio(audio=file_id, caption="Instrumental meditation 🎶")


@music_router.message(lambda msg: msg.text == "Ambient Yoga Music")
async def send_music_3(message: types.Message):
    file_id = "CQACAgIAAxkBAAIJ4WeKvsMhxcqkzqMZAAGxwbVxpRvV_gACNWgAAqgEUUg7IMToP8u0vjYE"
    await message.answer_audio(audio=file_id, caption="Ambient Yoga Music 🎶")


@music_router.message(lambda msg: msg.text == "963 Hz pineal gland activation")
async def send_music_4(message: types.Message):
    file_id = "CQACAgIAAxkBAAIJ42eKvu2FfFQk7dplNmMGO6sHsOV6AAI5aAACqARRSJ13nn_PsGmLNgQ"
    await message.answer_audio(audio=file_id, caption="963 Hz pineal gland activation 🎶")


# ---------- Обработчик кнопки "Назад" ----------
@music_router.message(lambda msg: msg.text == "Назад")
async def back_to_menu(message: types.Message):
    await message.answer("Вы вернулись в главное меню.", reply_markup=main_menu_kb())
