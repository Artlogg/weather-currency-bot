from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.keyboards.main import main_menu, general_menu, weather_menu, rates_menu



router = Router()

@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        "Привет! Я бот «Погода / Курс валют».\n\n"
        "Команды:\n"
        "/weather <город> — погода по городу\n"
        "/rate <BASE> <TARGET> — курс валют\n\n"
        "Пример: /weather Riga", reply_markup=main_menu,
    )


@router.message()
async def handle_main_buttons(message: Message):
    text = message.text

    if text == "🌤 Погода":
        await message.answer("Выберите опцию:", reply_markup=weather_menu)
    elif text == "💱 Курсы валют":
        await message.answer("Выберите пару:", reply_markup=rates_menu)
    elif text == "⚙️ Общее":
        await message.answer("Настройки:", reply_markup=general_menu)
    elif text == "⬅️ Назад":
        await message.answer("Главное меню:", reply_markup=main_menu)
    elif text == "❌ Убрать клавиатуру":
        await message.answer("Клавиатура убрана", reply_markup=None)
    else:
        await message.answer("Выберите действие из меню!")
