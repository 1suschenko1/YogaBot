from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command
import requests
from config import GigaChatKey

menu_router = Router()

@menu_router.message(Command("menu"))
async def cmd_menu(message: Message):
    text = (
        "Меню:\n"
        "/workout_plan — Составить программу тренировок\n"
        "/chat — Задать вопрос тренеру\n"
        "/settings — Настройки"
    )
    await message.answer(text)

@menu_router.message(Command("chat"))
async def trainer_help(message: Message):
    response = requests.post(
        url="https://chatgpt-api.example.com/v1/chat",
        headers={"Authorization": f"Bearer {GigaChatKey}"},
        json={"question": message.text}
    )
    answer = response.json().get("answer", "Тренер пока не ответил.")
    await message.answer(answer)
