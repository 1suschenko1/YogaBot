from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from db import SessionLocal, User
from .menu import main_menu_kb

settings_router = Router()


class MenuSettingsState(StatesGroup):
    settings = State()
    confirm_reset = State()
    change_name = State()
    change_age = State()
    change_sex = State()


# ---------- Кнопка «Настройки» ----------
@settings_router.message(lambda msg: msg.text == "Настройки ⚙️")
async def settings(message: types.Message, state: FSMContext):
    db_session = SessionLocal()
    user = db_session.query(User).filter_by(tg_id=message.from_user.id).first()
    db_session.close()

    if not user:
        await message.answer(
            "Пожалуйста, пройдите регистрацию, прежде чем изменять настройки.",
            reply_markup=main_menu_kb()
        )
        return

    # В выводе теперь goal/level могут быть None, если пользователь не выбирал
    user_info = (
        f"Текущие данные:\n"
        f"Имя: {user.name}\n"
        f"Возраст: {user.age}\n"
        f"Пол: {user.sex}\n"
    )

    await message.answer(
        user_info + "Что вы хотите изменить?",
        reply_markup=settings_kb()
    )
    await state.set_state(MenuSettingsState.settings)


@settings_router.message(MenuSettingsState.settings)
async def handle_settings_menu(message: types.Message, state: FSMContext):
    txt = message.text.lower()
    if txt == "назад":
        await state.clear()
        await message.answer("Вы вернулись в главное меню.", reply_markup=main_menu_kb())
        return

    if message.text == "Изменить имя":
        name_kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Назад")]],
            resize_keyboard=True
        )
        await message.answer("Введите новое имя:", reply_markup=name_kb)
        await state.set_state(MenuSettingsState.change_name)

    elif message.text == "Изменить возраст":
        age_kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Назад")]],
            resize_keyboard=True
        )
        await message.answer("Введите новый возраст:", reply_markup=age_kb)
        await state.set_state(MenuSettingsState.change_age)

    elif message.text == "Изменить пол":
        sex_kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Мужской"), KeyboardButton(text="Женский")],
                [KeyboardButton(text="Назад")]
            ],
            resize_keyboard=True
        )
        await message.answer("Выберите ваш пол:", reply_markup=sex_kb)
        await state.set_state(MenuSettingsState.change_sex)


    elif message.text == "Пройти регистрацию заново":
        confirm_kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Да"), KeyboardButton(text="Нет")]],
            resize_keyboard=True
        )
        await message.answer("Вы уверены, что хотите пройти регистрацию заново?", reply_markup=confirm_kb)
        await state.set_state(MenuSettingsState.confirm_reset)
    else:
        await message.answer("Пожалуйста, выберите один из вариантов или 'Назад'.")


@settings_router.message(MenuSettingsState.change_name)
async def handle_change_name(message: types.Message, state: FSMContext):
    if message.text.lower() == "назад":
        await state.set_state(MenuSettingsState.settings)
        await message.answer("Вы вернулись в настройки.", reply_markup=settings_kb())
        return

    if len(message.text.strip()) < 2:
        await message.answer("Имя слишком короткое. Введите имя ещё раз или нажмите 'Назад':")
        return

    db_session = SessionLocal()
    user = db_session.query(User).filter_by(tg_id=message.from_user.id).first()
    if user:
        user.name = message.text.strip()
        db_session.commit()
    db_session.close()

    await state.clear()
    await message.answer("Имя успешно изменено!", reply_markup=main_menu_kb())


@settings_router.message(MenuSettingsState.change_age)
async def handle_change_age(message: types.Message, state: FSMContext):
    if message.text.lower() == "назад":
        await state.set_state(MenuSettingsState.settings)
        await message.answer("Вы вернулись в настройки.", reply_markup=settings_kb())
        return

    if not message.text.isdigit():
        await message.answer("Возраст должен быть числом. Попробуйте снова или 'Назад':")
        return

    age_int = int(message.text)
    if age_int < 5 or age_int > 120:
        await message.answer("Некорректный возраст (5..120). Введите снова или 'Назад':")
        return

    db_session = SessionLocal()
    user = db_session.query(User).filter_by(tg_id=message.from_user.id).first()
    if user:
        user.age = age_int
        db_session.commit()
    db_session.close()

    await state.clear()
    await message.answer("Возраст успешно изменён!", reply_markup=main_menu_kb())


@settings_router.message(MenuSettingsState.change_sex)
async def handle_change_sex(message: types.Message, state: FSMContext):
    if message.text.lower() == "назад":
        await state.set_state(MenuSettingsState.settings)
        await message.answer("Вы вернулись в настройки.", reply_markup=settings_kb())
        return

    if message.text not in ["Мужской", "Женский"]:
        await message.answer("Пожалуйста, выберите 'Мужской' или 'Женский', или нажмите 'Назад':")
        return

    db_session = SessionLocal()
    user = db_session.query(User).filter_by(tg_id=message.from_user.id).first()
    if user:
        user.sex = message.text
        db_session.commit()
    db_session.close()

    await state.clear()
    await message.answer("Пол успешно изменён!", reply_markup=main_menu_kb())


@settings_router.message(MenuSettingsState.confirm_reset)
async def handle_confirm_reset(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        db_session = SessionLocal()
        user = db_session.query(User).filter_by(tg_id=message.from_user.id).first()
        if user:
            db_session.delete(user)
            db_session.commit()
        db_session.close()

        await state.clear()
        await message.answer("Регистрация сброшена. Укажите ваше имя:", reply_markup=ReplyKeyboardRemove())

        # Возвращаемся в процесс регистрации (в reg.py)
        from .reg import RegistrationState
        await state.set_state(RegistrationState.name)

    elif message.text.lower() == "нет":
        await state.clear()
        await message.answer("Возврат в главное меню.", reply_markup=main_menu_kb())
    else:
        await message.answer("Пожалуйста, выберите 'Да' или 'Нет'.")


# ---------- Клавиатура настроек ----------
def settings_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Изменить имя"), KeyboardButton(text="Изменить возраст")],
            [KeyboardButton(text="Изменить пол"), KeyboardButton(text="Пройти регистрацию заново")],
            [KeyboardButton(text="Назад")],
        ],
        resize_keyboard=True
    )