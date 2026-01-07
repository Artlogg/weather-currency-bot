from datetime import datetime

import httpx
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

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

    await state.update_data(city=city, forecast=forecast)
    await state.clear()

    today = forecast[0]
    weekday = WEEKDAYS[
        datetime.fromisoformat(today.date).weekday()
    ]

    await message.answer(
        f"📍 {today.city}\n"
        f"📅 {weekday} (сегодня)\n"
        f"🌡 {today.temperature_min:.1f}°C — {today.temperature_max:.1f}°C\n"
        f"💨 Ветер: {today.wind_speed_max:.1f} м/с"
    )


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
            weekday = WEEKDAYS[target_weekday]
            await callback.message.answer(
                f"📍 {day.city}\n"
                f"📅 {weekday}, {day.date}\n"
                f"🌡 {day.temperature_min:.1f}°C — {day.temperature_max:.1f}°C\n"
                f"💨 Ветер: {day.wind_speed_max:.1f} м/с"
            )
            break
    else:
        await callback.message.answer("Прогноз на этот день недоступен.")

    await callback.answer()
