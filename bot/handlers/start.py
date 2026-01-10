from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards.main import (
    last_city_menu,
    main_menu,
)
from bot.states.weather import WeatherStates

router = Router()

user_last_city: dict[int, str] = {}
user_last_rate: dict[int, tuple[str, str]] = {}

@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
"Привет! 👋\n"  
"Я бот «Погода / Курс валют».\n"
"\n"
"Я умею:\n"
"🌤 показывать погоду по городу\n"  
"💱 показывать курс валют\n"  
"\n"
"👇 Чтобы начать, просто пользуйся кнопками снизу.\n" ,
        reply_markup=main_menu,
    )

  
@router.message(lambda m: m.text == "🌤 Погода")
async def weather_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(WeatherStates.waiting_for_city)
    await message.answer(
        "Введите город (например: Москва):",
        reply_markup=last_city_menu,
    )

@router.message(F.text == "ℹ️ Помощь")
async def help_button(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
"Привет! 👋\n"  
"Я бот «Погода / Курс валют».\n"
"\n"
"Я умею:\n"
"🌤 показывать погоду по городу\n"  
"💱 показывать курс валют\n"  
"\n"
"👇 Чтобы начать, просто пользуйся кнопками снизу.\n"
    )

