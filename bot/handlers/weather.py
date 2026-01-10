from datetime import datetime

import httpx
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards.main import weather_menu
from bot.services.weather_client import WeatherClient
from bot.states.weather import WeatherStates

router = Router()



WEEKDAYS = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье",
]

DAY_MAP = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}

WEATHER_MAP = {
    0: "☀️ Ясно",
    1: "🌤 Частично облачно",
    2: "⛅ Облачно",
    3: "☁️ Пасмурно",
    45: "🌫 Туман",
    48: "🌫 Туман с изморосью",
    51: "🌦 Лёгкий дождь",
    53: "🌧 Дождь",
    55: "🌧 Сильный дождь",
    56: "🌧 Лёгкий моросящий дождь",
    57: "🌧 Сильный моросящий дождь",
    61: "🌧 Дождь",
    63: "🌧 Сильный дождь",
    65: "🌧 Очень сильный дождь",
    66: "🌧 Лёгкий дождь со снегом",
    67: "🌧 Сильный дождь со снегом",
    71: "❄️ Снег",
    73: "❄️ Сильный снег",
    75: "❄️ Очень сильный снег",
    77: "❄️ Снежные крупинки",
    80: "🌦 Ливневый дождь",
    81: "🌧 Сильный ливневый дождь",
    82: "🌧 Очень сильный ливневый дождь",
    85: "❄️ Лёгкий снегопад",
    86: "❄️ Сильный снегопад",
    95: "⛈ Гроза",
    96: "⛈ Гроза с лёгким дождем",
    99: "⛈ Гроза с сильным дождем",
}

@router.message(WeatherStates.waiting_for_city)
async def process_city(message: Message, state: FSMContext):
    city = message.text.strip()

    async with httpx.AsyncClient() as http:
        client = WeatherClient(http)
        try:
            forecast = await client.get_week_forecast(city)
        except ValueError:
            await message.answer("Город не найден. Попробуй ещё раз.")
            return
        except httpx.HTTPError:
            await message.answer("Сервис погоды временно недоступен.")
            return

    await state.update_data(
        city=city,
        forecast=forecast,
    )

    await message.answer(
        f"📍 Город сохранён: {city}\n"
        f"Выберите период прогноза 👇",
        reply_markup=weather_menu,
    )

async def format_weather_day(day) -> str:
    weekday = WEEKDAYS[datetime.fromisoformat(day.date).weekday()]
    weather_text = WEATHER_MAP.get(day.weather_code, "❓ Неизвестно")
    return (
        f"📍 {day.city}\n"
        f"📅 {weekday}, {day.date}\n"
        f"🌡 {day.temperature_min:.1f}°C — {day.temperature_max:.1f}°C\n"
        f"💨 Ветер: {day.wind_speed_max:.1f} км/с\n"
        f"{weather_text}"
    )

@router.callback_query(F.data == "weather_last")
async def use_last_city(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    city = data.get("city")

    if not city:
        await callback.message.answer(
            "Вы ещё не вводили город 🙁"
        )
        await callback.answer()
        return

    await state.set_state(WeatherStates.waiting_for_city)

    fake_message = callback.message
    fake_message.text = city

    await process_city(fake_message, state)

    await callback.answer()

@router.callback_query(F.data == "change_city")
async def change_city(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await state.set_state(WeatherStates.waiting_for_city)

    await callback.message.answer(
        "Введите город (например: Москва)"
    )

    await callback.answer()

@router.callback_query(F.data == "weather_today")
async def weather_today(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    forecast = data.get("forecast")

    if not forecast:
        await callback.message.answer("Сначала введи город.")
        await callback.answer()
        return

    today = forecast[0]
    text = await format_weather_day(today)
    await callback.message.edit_text(text)
    await callback.answer()

@router.callback_query(F.data == "weather_tomorrow")
async def weather_tomorrow(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    forecast = data.get("forecast")

    if not forecast or len(forecast) < 2:
        await callback.message.answer("Прогноз на завтра недоступен.")
        await callback.answer()
        return

    tomorrow = forecast[1]
    text = await format_weather_day(tomorrow)
    await callback.message.edit_text(text)
    await callback.answer()

@router.callback_query(F.data.in_(DAY_MAP))
async def week_day(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    forecast = data.get("forecast")

    if not forecast:
        await callback.message.answer("Сначала введи город.")
        await callback.answer()
        return

    target_weekday = DAY_MAP[callback.data]

    for day in forecast:
        if datetime.fromisoformat(day.date).weekday() == target_weekday:
            text = await format_weather_day(day)
            await callback.message.edit_text(text)
            break
    else:
        await callback.message.answer("Прогноз на этот день недоступен.")

