from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards.main import (
    last_city_menu,
    main_menu,
    week_menu,
)
from bot.states.weather import WeatherStates

router = Router()

user_last_city: dict[int, str] = {}
user_last_rate: dict[int, tuple[str, str]] = {}

@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        "Привет! Я бот «Погода / Курс валют».\n\n"
        "Команды:\n"
        "/weather <город> — погода по городу\n"
        "/rate <BASE> <TARGET> — курс валют\n\n"
        "Пример: /weather Riga",
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


@router.callback_query(F.data.in_({
    "weather_today",
    "weather_tomorrow",
    "weather_week",
}))
async def handle_callbacks(
    callback: CallbackQuery,
    state: FSMContext,
):
    data = callback.data

    if data == "weather_week":
        await callback.message.answer(
            "Выберите день недели:",
            reply_markup=week_menu
        )
    elif data in ("weather_today", "weather_tomorrow"):
        await state.set_state(WeatherStates.waiting_for_city)
        await state.update_data(period=data)

        await callback.message.answer(
            "Введите город (например: Москва)", reply_markup=last_city_menu
        )

    await callback.answer()
