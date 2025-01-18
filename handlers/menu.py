from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)
from aiogram.fsm.state import State, StatesGroup

from db import SessionLocal, User
from Ai import AI  # для «тренера», если нужно

menu_router = Router()


# ---------- Главное меню ----------
def main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Видеоуроки 🎥"), KeyboardButton(text="Приступить к выполнению заданий 🧎‍♀️")],
            [KeyboardButton(text="Музыка 🎶"), KeyboardButton(text="Попросить помощи у тренера 🧘")],
            [KeyboardButton(text="Настройки ⚙️")]
        ],
        resize_keyboard=True
    )


# ---------- Состояния для дополнительных действий ----------


class MenuSettingsState(StatesGroup):
    settings = State()
    confirm_reset = State()
    change_name = State()
    change_age = State()
    change_sex = State()


class TrainerState(StatesGroup):
    question = State()


# ---------- Команда /menu ----------
@menu_router.message(Command("menu"))
async def cmd_menu(message: types.Message, state: FSMContext):
    db_session = SessionLocal()
    user = db_session.query(User).filter_by(tg_id=message.from_user.id).first()
    db_session.close()

    if not user:
        await message.answer("Вы не зарегистрированы! Введите /start для регистрации.")
        return

    await message.answer("Главное меню:", reply_markup=main_menu_kb())


# ---------- Кнопка «Попросить помощи у тренера» ----------
@menu_router.message(lambda msg: msg.text == "Попросить помощи у тренера 🧘")
async def ask_trainer_intro(message: types.Message, state: FSMContext):
    await message.answer(
        "О чём вы хотите спросить тренера?\nПросто напишите ваш вопрос.",
        reply_markup=trainer_kb()
    )
    await state.set_state(TrainerState.question)


@menu_router.message(TrainerState.question)
async def handle_trainer_question(message: types.Message, state: FSMContext):
    if message.text.lower() == "назад":
        await state.clear()
        await message.answer("Вы вернулись в главное меню.", reply_markup=main_menu_kb())
        return

    ai = AI()
    try:
        answer = await ai.chat(message.text)
    except Exception as e:
        await message.answer(f"Ошибка при обращении к GigaChat: {str(e)}")
        await state.clear()
        await message.answer("Возвращаюсь в главное меню.", reply_markup=main_menu_kb())
        return

    await message.answer(answer)
    await message.answer(
        "Чем я могу ещё помочь?\n(Чтобы вернуться в главное меню, нажмите 'Назад'.)",
        reply_markup=trainer_kb()
    )


def trainer_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True
    )