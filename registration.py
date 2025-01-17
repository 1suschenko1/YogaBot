from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from db import SessionLocal, User
from aiogram.fsm.state import State, StatesGroup
import requests

registration_router = Router()

# FSM Состояния для регистрации
class RegistrationState(StatesGroup):
    name = State()
    age = State()
    sex = State()
    goal = State()
    level = State()
    settings = State()
    confirm_reset = State()
    change_name = State()
    change_age = State()
    change_sex = State()

GigaChatKey = 'ZTZjNDUxMzAtOTcxNC00MGIyLTk4MTUtNzcyYTU2ZTg4YzU5OmMwYjNhNTQ0LTQ1ZGQtNGQyYi05ZWM2LTVhM2E4ODkwNDhkYQ=='

# Начало регистрации
@registration_router.message(Command("start"))
async def start_registration(message: types.Message, state: FSMContext):
    db_session = SessionLocal()
    user = db_session.query(User).filter_by(tg_id=message.from_user.id).first()
    if user:
        await message.answer("Вы уже зарегистрированы!", reply_markup=main_menu_kb())
        return

    await message.answer("Добро пожаловать в Йога Бот! Пожалуйста, пройдите регистрацию.\nУкажите ваше имя:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationState.name)

# Имя
@registration_router.message(RegistrationState.name)
async def handle_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите ваш возраст (число):", reply_markup=back_button_kb())
    await state.set_state(RegistrationState.age)

# Возраст
@registration_router.message(RegistrationState.age)
async def handle_age(message: types.Message, state: FSMContext):
    if message.text.lower() == "назад":
        await message.answer("Укажите ваше имя:", reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegistrationState.name)
        return
    if not message.text.isdigit():
        await message.answer("Возраст должен быть числом. Попробуйте снова:")
        return
    await state.update_data(age=int(message.text))
    sex_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Мужской"), KeyboardButton(text="Женский")], [KeyboardButton(text="Назад")]],
        resize_keyboard=True
    )
    await message.answer("Введите ваш пол:", reply_markup=sex_kb)
    await state.set_state(RegistrationState.sex)

# Пол
@registration_router.message(RegistrationState.sex)
async def handle_sex(message: types.Message, state: FSMContext):
    if message.text.lower() == "назад":
        await message.answer("Введите ваш возраст (число):", reply_markup=back_button_kb())
        await state.set_state(RegistrationState.age)
        return
    if message.text.lower() not in ["мужской", "женский"]:
        await message.answer("Пожалуйста, выберите 'Мужской' или 'Женский':")
        return
    await state.update_data(sex=message.text.lower())
    goal_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Расслабление/Снижение стресса")],
            [KeyboardButton(text="Гибкость"), KeyboardButton(text="Улучшение осанки")],
            [KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True
    )
    await message.answer("Какая ваша цель занятий?", reply_markup=goal_kb)
    await state.set_state(RegistrationState.goal)

# Цель занятий
@registration_router.message(RegistrationState.goal)
async def handle_goal(message: types.Message, state: FSMContext):
    if message.text.lower() == "назад":
        sex_kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Мужской"), KeyboardButton(text="Женский")], [KeyboardButton(text="Назад")]],
            resize_keyboard=True
        )
        await message.answer("Введите ваш пол:", reply_markup=sex_kb)
        await state.set_state(RegistrationState.sex)
        return
    await state.update_data(goal=message.text)
    level_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Новичок"), KeyboardButton(text="Средний"), KeyboardButton(text="Продвинутый")],
            [KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True
    )
    await message.answer("Укажите ваш уровень подготовки:", reply_markup=level_kb)
    await state.set_state(RegistrationState.level)

# Уровень подготовки
@registration_router.message(RegistrationState.level)
async def handle_level(message: types.Message, state: FSMContext):
    if message.text.lower() == "назад":
        goal_kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Расслабление/Снижение стресса")],
                [KeyboardButton(text="Гибкость"), KeyboardButton(text="Улучшение осанки")],
                [KeyboardButton(text="Назад")]
            ],
            resize_keyboard=True
        )
        await message.answer("Какая ваша цель занятий?", reply_markup=goal_kb)
        await state.set_state(RegistrationState.goal)
        return

    data = await state.get_data()
    db_session = SessionLocal()
    new_user = User(
        tg_id=message.from_user.id,
        name=data["name"],
        age=data["age"],
        sex=data["sex"],
        goal=data["goal"],
        level=message.text,
    )
    db_session.add(new_user)
    db_session.commit()

    await state.clear()
    await message.answer(
        "Вы успешно зарегистрированы! Теперь вы можете приступить к занятиям.",
        reply_markup=main_menu_kb()
    )

# Настройки
@registration_router.message(lambda message: message.text == "Настройки")
async def settings(message: types.Message, state: FSMContext):
    settings_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Изменить имя"), KeyboardButton(text="Изменить возраст")],
            [KeyboardButton(text="Изменить пол"), KeyboardButton(text="Пройти регистрацию заново")],
            [KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True
    )
    await message.answer("Что вы хотите изменить?", reply_markup=settings_kb)
    await state.set_state(RegistrationState.settings)

# Возврат из настроек
@registration_router.message(RegistrationState.settings)
async def handle_settings_back(message: types.Message, state: FSMContext):
    if message.text.lower() == "назад":
        await message.answer("Возврат в главное меню.", reply_markup=main_menu_kb())
        await state.clear()
# Изменить имя
@registration_router.message(lambda message: message.text == "Изменить имя")
async def change_name(message: types.Message, state: FSMContext):
    await message.answer("Введите новое имя:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationState.change_name)

@registration_router.message(RegistrationState.change_name)
async def handle_change_name(message: types.Message, state: FSMContext):
    db_session = SessionLocal()
    user = db_session.query(User).filter_by(tg_id=message.from_user.id).first()
    if user:
        user.name = message.text
        db_session.commit()
    await state.clear()
    await message.answer("Имя успешно изменено!", reply_markup=main_menu_kb())

# Изменить возраст
@registration_router.message(lambda message: message.text == "Изменить возраст")
async def change_age(message: types.Message, state: FSMContext):
    await message.answer("Введите новый возраст:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationState.change_age)

@registration_router.message(RegistrationState.change_age)
async def handle_change_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Возраст должен быть числом. Попробуйте снова:")
        return
    db_session = SessionLocal()
    user = db_session.query(User).filter_by(tg_id=message.from_user.id).first()
    if user:
        user.age = int(message.text)
        db_session.commit()
    await state.clear()
    await message.answer("Возраст успешно изменен!", reply_markup=main_menu_kb())

# Изменить пол
@registration_router.message(lambda message: message.text == "Изменить пол")
async def change_sex(message: types.Message, state: FSMContext):
    sex_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Мужской"), KeyboardButton(text="Женский")]],
        resize_keyboard=True
    )
    await message.answer("Выберите ваш пол:", reply_markup=sex_kb)
    await state.set_state(RegistrationState.change_sex)

@registration_router.message(RegistrationState.change_sex)
async def handle_change_sex(message: types.Message, state: FSMContext):
    if message.text not in ["Мужской", "Женский"]:
        await message.answer("Пожалуйста, выберите 'Мужской' или 'Женский':")
        return
    db_session = SessionLocal()
    user = db_session.query(User).filter_by(tg_id=message.from_user.id).first()
    if user:
        user.sex = message.text
        db_session.commit()
    await state.clear()
    await message.answer("Пол успешно изменен!", reply_markup=main_menu_kb())

# Пройти регистрацию заново
@registration_router.message(lambda message: message.text == "Пройти регистрацию заново")
async def reset_registration(message: types.Message, state: FSMContext):
    confirm_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Да"), KeyboardButton(text="Нет")]],
        resize_keyboard=True
    )
    await message.answer("Вы уверены, что хотите пройти регистрацию заново?", reply_markup=confirm_kb)
    await state.set_state(RegistrationState.confirm_reset)

@registration_router.message(RegistrationState.confirm_reset)
async def handle_confirm_reset(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        db_session = SessionLocal()
        user = db_session.query(User).filter_by(tg_id=message.from_user.id).first()
        if user:
            db_session.delete(user)
            db_session.commit()
        await state.clear()
        await message.answer("Регистрация сброшена. Укажите ваше имя:", reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegistrationState.name)
    elif message.text.lower() == "нет":
        await message.answer("Возврат в главное меню.", reply_markup=main_menu_kb())
        await state.clear()
    else:
        await message.answer("Пожалуйста, выберите 'Да' или 'Нет'.")

# Помощь тренера
@registration_router.message(lambda message: message.text == "Попросить помощи у тренера")
async def trainer_help(message: types.Message):
    response = requests.post(
        url="https://api.gigachat.com/chat",
        headers={"Authorization": f"Bearer {GigaChatKey}"},
        json={"message": message.text}
    )
    answer = response.json().get("answer", "Тренер пока не ответил.")
    await message.answer(answer)

# Главное меню
def main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Приступить к выполнению заданий")],
            [KeyboardButton(text="Попросить помощи у тренера")],
            [KeyboardButton(text="Настройки")]
        ],
        resize_keyboard=True
    )

# Клавиатура с кнопкой "Назад"
def back_button_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Назад")]],
        resize_keyboard=True
    )
