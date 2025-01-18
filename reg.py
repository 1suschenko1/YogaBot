from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from db import SessionLocal, User

registration_router = Router()

class RegistrationState(StatesGroup):
    name = State()
    age = State()
    sex = State()

@registration_router.message(Command("start"))
async def start_registration(message: types.Message, state: FSMContext):
    db_session = SessionLocal()
    user = db_session.query(User).filter_by(tg_id=message.from_user.id).first()
    db_session.close()

    if user:
        from .menu import main_menu_kb
        await message.answer("Вы уже зарегистрированы!", reply_markup=main_menu_kb())
        return

    await message.answer(
        "Добро пожаловать в Йога Бот! Пожалуйста, пройдите регистрацию.\nУкажите ваше имя:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(RegistrationState.name)

@registration_router.message(RegistrationState.name)
async def handle_name(message: types.Message, state: FSMContext):
    if len(message.text.strip()) < 2:
        await message.answer("Имя слишком короткое. Введите имя ещё раз:")
        return

    await state.update_data(name=message.text.strip())
    await message.answer(
        "Введите ваш возраст (число):",
        reply_markup=back_button_kb()
    )
    await state.set_state(RegistrationState.age)

@registration_router.message(RegistrationState.age)
async def handle_age(message: types.Message, state: FSMContext):
    if message.text.lower() == "назад":
        await message.answer("Укажите ваше имя:", reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegistrationState.name)
        return

    if not message.text.isdigit():
        await message.answer("Возраст должен быть числом. Попробуйте снова:")
        return

    age_int = int(message.text)
    if age_int < 5 or age_int > 120:
        await message.answer("Некорректный возраст (5..120). Введите снова:")
        return

    await state.update_data(age=age_int)

    sex_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мужской"), KeyboardButton(text="Женский")],
            [KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True
    )
    await message.answer("Введите ваш пол:", reply_markup=sex_kb)
    await state.set_state(RegistrationState.sex)

@registration_router.message(RegistrationState.sex)
async def handle_sex(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer("Введите ваш возраст (число):", reply_markup=back_button_kb())
        await state.set_state(RegistrationState.age)
        return

    valid_sex = ["Мужской", "Женский"]
    if message.text not in valid_sex:
        await message.answer("Пожалуйста, выберите 'Мужской' или 'Женский':")
        return

    data = await state.get_data()
    db_session = SessionLocal()
    new_user = User(
        tg_id=message.from_user.id,
        name=data["name"],
        age=data["age"],
        sex=message.text,
    )
    db_session.add(new_user)
    db_session.commit()
    db_session.close()

    await state.clear()
    from .menu import main_menu_kb
    await message.answer(
        "Вы успешно зарегистрированы! Теперь вы можете приступить к занятиям.",
        reply_markup=main_menu_kb()
    )

def back_button_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Назад")]],
        resize_keyboard=True
    )
