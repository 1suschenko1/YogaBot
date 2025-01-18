from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InputMediaPhoto
from aiogram.fsm.state import State, StatesGroup
from .menu import main_menu_kb


exer_router = Router()



'''@exer_router.message(lambda message: message.content_type == "photo")
async def get_file_id(message: types.Message):
    file_id = message.photo[-1].file_id
    await message.answer(f"Ваш file_id: {file_id}")'''

# Состояния
class AssignmentState(StatesGroup):
    level = State()
    poses = State()

# Распределение поз по уровням сложности с фото и подробными описаниями
POSES = {
    "Лёгкий": {
        "Поза горы (Тадасана)": {
            "description": (
                "ОПИСАНИЕ: Базовая поза, которая помогает улучшить осанку, выпрямить позвоночник и укрепить мышцы ног.\n\n"
                "КАК ВЫПОЛНЯТЬ: Встаньте прямо, ноги на ширине плеч. В идеальном варианте Тадасаны руки вытягиваются вверх над головою, но ради удобства можно их держать опущенными по бокам."
            ),
            "photos": ["AgACAgIAAxkBAAILu2eK9LM1KfiKewspHpPqo9ARyZ0VAAII6zEbqARRSDtKzVbOKhbTAQADAgADeAADNgQ"]
        },
        "Алмазная поза (Ваджрасана)": {
            "description": (
                "ОПИСАНИЕ: Простая поза для медитации, которая улучшает пищеварение и успокаивает ум.\n\n"
                "КАК ВЫПОЛНЯТЬ: Сядьте на пятки, держите спину прямой. Ладони положите на колени."
            ),
            "photos": ["AgACAgIAAxkBAAIL12eK9zw0gF38YFi4EDWiLMsZZd6RAAIL6zEbqARRSO0oDgZxrD_PAQADAgADbQADNgQ"]
        },
        "Половинная поза колеса (Ардха Чакрасана)": {
            "description": (
                "ОПИСАНИЕ: Укрепляет мышцы спины, помогает растянуть переднюю часть тела.\n\n"
                "КАК ВЫПОЛНЯТЬ: Стопы ставим вместе. Ладони поднятых рук разворачиваем вперёд, руки на ширине плеч. Выталкиваем таз вперёд, делая доступный по глубине прогиб."
            ),
            "photos": ["AgACAgIAAxkBAAIL2WeK90DR619oAe42id3R4Jk7h-JjAAIM6zEbqARRSGBKyvsI7u-wAQADAgADbQADNgQ"]
        },
        "Поза собаки мордой вниз (Адхо Мукха Шванасана)": {
            "description": (
                "ОПИСАНИЕ: Растягивает позвоночник, ноги и руки, улучшает кровообращение и успокаивает ум.\n\n"
                "КАК ВЫПОЛНЯТЬ: Встаньте на четвереньки, поднимите таз вверх, образуя треугольник телом."
            ),
            "photos": ["AgACAgIAAxkBAAIL22eK90PjWqY3Ws-H0CXZ0jH6GW2mAAIN6zEbqARRSOmIkkaGktJ8AQADAgADbQADNgQ"]
        }
    },
    "Средний": {
        "Поза Полумесяца (Ардха Чандрасана)": {
            "description": (
                "ОПИСАНИЕ: Балансовая поза, которая развивает равновесие, укрепляет ноги и растягивает тело.\n\n"
                "КАК ВЫПОЛНЯТЬ: Станьте на одну ногу, другую поднимите в сторону. Одну руку опустите на пол, другую вытяните вверх."
            ),
            "photos": ["AgACAgIAAxkBAAIL3WeK91Yr_hTD-7XV_bGD7i-CyRGrAAIO6zEbqARRSDdmKCiWre08AQADAgADeAADNgQ"]
        },
        "Поза Лотоса (Падмасана)": {
            "description": (
                "ОПИСАНИЕ: Классическая медитативная поза, которая укрепляет тазобедренные суставы и улучшает концентрацию.\n\n"
                "КАК ВЫПОЛНЯТЬ: Сядьте на пол, перекрестите ноги так, чтобы стопы лежали на бедрах."
            ),
            "photos": ["AgACAgIAAxkBAAIL32eK93v03v5uVrAa1yBFIpMKOVY2AAIQ6zEbqARRSEQJw8udXPhZAQADAgADbQADNgQ"]
        },
        "Поза Воина (Вирабхадрасана)": {
            "description": (
                "ОПИСАНИЕ: Укрепляет мышцы ног, развивает баланс и координацию.\n\n"
                "КАК ВЫПОЛНЯТЬ: Стоя на одной ноге, наклонитесь вперёд, вытянув противоположную ногу назад и руки вперёд."
            ),
            "photos": ["AgACAgIAAxkBAAIL4WeK95bitMbrMTExoHK4MfDEvftCAAIR6zEbqARRSGP6P5oL7DIHAQADAgADeAADNgQ"]
        },
        "Поза Моста (Двипада Питхасана)": {
            "description": (
                "ОПИСАНИЕ: Открывает грудную клетку, улучшает гибкость позвоночника и укрепляет мышцы спины.\n\n"
                "КАК ВЫПОЛНЯТЬ: Лёжа на спине, согните колени, поднимите таз вверх, опираясь на плечи."
            ),
            "photos": ["AgACAgIAAxkBAAIL42eK98mboWvhWq-SvkHleJnb8qcwAAIS6zEbqARRSMuCDdRbRCstAQADAgADbQADNgQ"]
        }
    },
    "Продвинутый": {
        "Поза Посвященного (Брахмачариасана)": {
            "description": (
                "ОПИСАНИЕ: Развивает силу и выносливость, помогает сосредоточиться и укрепить мышцы корпуса.\n\n"
                "КАК ВЫПОЛНЯТЬ: Удерживайте равновесие на руках, вытягивая ноги вперёд."
            ),
            "photos": ["AgACAgIAAxkBAAIL5WeK99rDlgR8BJFfDK0Rra7GKzX1AAIT6zEbqARRSL1guQ4hB9eFAQADAgADbQADNgQ"]
        },
        "Поза Скорпиона (Врищчикасана)": {
            "description": (
                "ОПИСАНИЕ: Сложная поза, которая развивает силу рук, гибкость позвоночника и баланс.\n\n"
                "КАК ВЫПОЛНЯТЬ: Перейдите в стойку на предплечьях и согните ноги над головой."
            ),
            "photos": ["AgACAgIAAxkBAAIL52eK9_afoS213wpbMKg1jbD-DMfGAAIU6zEbqARRSGX5eK4F9q4GAQADAgADbQADNgQ"]
        },
        "Стойка на голове с поддержкой (Ширшасана)": {
            "description": (
                "ОПИСАНИЕ: Улучшает кровообращение, стимулирует мозговую активность и укрепляет корпус.\n\n"
                "КАК ВЫПОЛНЯТЬ: Опираясь на предплечья и макушку, поднимите ноги вверх, удерживая равновесие."
            ),
            "photos": ["AgACAgIAAxkBAAIL6WeK-AxBru-UCpjRuiaLpP5vFg94AAIV6zEbqARRSOgZkaPS9O7zAQADAgADeAADNgQ"]
        },
        "Поперечный шпагат (Самаконасана)": {
            "description": (
                "ОПИСАНИЕ: Требует высокой гибкости, растягивает внутренние мышцы бедер и укрепляет таз.\n\n"
                "КАК ВЫПОЛНЯТЬ: Сядьте на шпагат, вытянув ноги в противоположные стороны."
            ),
            "photos": ["AgACAgIAAxkBAAIL62eK-CJ0mHxHDmtQvgv_-gs_rysvAAIW6zEbqARRSKWOnq8lqubhAQADAgADeAADNgQ"]
        }
    }
}


# Обработчик кнопки "Приступить к выполнению заданий"
@exer_router.message(lambda msg: msg.text == "Приступить к выполнению заданий 🧎‍♀️")
async def start_assignments(message: types.Message, state: FSMContext):
    await message.answer(
        "Выберите сложность упражнений:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Лёгкий"), KeyboardButton(text="Средний"), KeyboardButton(text="Продвинутый")],
                [KeyboardButton(text="Назад")]
            ],
            resize_keyboard=True
        )
    )
    await state.set_state(AssignmentState.level)

# Уровни сложности
@exer_router.message(AssignmentState.level)
async def handle_level(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.clear()
        await message.answer("Возврат в главное меню.", reply_markup=main_menu_kb())
        return

    level = message.text
    if level not in POSES:
        await message.answer("Выберите один из уровней сложности.")
        return

    await state.update_data(level=level)  # Сохраняем уровень в состояние

    # Формируем клавиатуру для поз
    poses_keyboard = [
        [KeyboardButton(text=pose) for pose in list(POSES[level].keys())[:2]],
        [KeyboardButton(text=pose) for pose in list(POSES[level].keys())[2:]],
        [KeyboardButton(text="Назад")]
    ]

    await message.answer(
        f"Вы выбрали уровень: {level}. Теперь выберите позу:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=poses_keyboard,
            resize_keyboard=True
        )
    )
    await state.set_state(AssignmentState.poses)

# Показ поз
@exer_router.message(AssignmentState.poses)
async def show_pose(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await state.set_state(AssignmentState.level)
        await message.answer(
            "Возврат к выбору уровня сложности.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="Лёгкий"), KeyboardButton(text="Средний"), KeyboardButton(text="Продвинутый")],
                    [KeyboardButton(text="Назад")]
                ],
                resize_keyboard=True
            )
        )
        return

    data = await state.get_data()
    level = data.get("level", "")

    if level not in POSES or message.text not in POSES[level]:
        await message.answer("Выберите одну из доступных поз.")
        return

    pose = POSES[level][message.text]
    photos = pose["photos"]
    description = pose["description"]

    # Отправка фото
    media = [InputMediaPhoto(media=photo) for photo in photos]
    if len(media) > 1:
        await message.answer_media_group(media)
    elif len(media) == 1:
        await message.answer_photo(photo=photos[0])

    # Отправка описания
    await message.answer(description)

    # Возврат к выбору поз
    await message.answer(
        "Выберите следующую позу или нажмите 'Назад':",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=pose_name) for pose_name in list(POSES[level].keys())[:2]],
                [KeyboardButton(text=pose_name) for pose_name in list(POSES[level].keys())[2:]],
                [KeyboardButton(text="Назад")]
            ],
            resize_keyboard=True
        )
    )
