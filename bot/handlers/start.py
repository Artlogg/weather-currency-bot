from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.keyboards.main import main_menu\

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
