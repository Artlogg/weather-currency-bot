import httpx
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.services.weather_client import WeatherClient
from bot.states.weather import WeatherStates

router = Router()

user_last_city: dict[int, str] = {}

@router.message(Command("weather"))
async def weather(message: Message) -> None:
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Напиши так: /weather <город>\\nНапример: /weather Riga")
        return

    city = parts[1].strip()

    async with httpx.AsyncClient() as http:
        client = WeatherClient(http)
        try:
            result = await client.get_current_weather(city)
        except ValueError as e:
            if str(e) == "CITY_NOT_FOUND":
                await message.answer("Город не найден. Попробуй написать по-другому.")
                return
            raise
        except httpx.HTTPError:
            await message.answer("Сервис погоды временно недоступен. Попробуй позже.")
            return

    await message.answer(
        f"Погода в {result.city}:\\n"
        f"🌡 Температура: {result.temperature_c:.1f}°C\\n"
        f"💨 Ветер: {result.wind_speed_ms:.1f} м/с"
    )

@router.message(WeatherStates.waiting_for_city)
async def process_city(
    message: Message,
    state: FSMContext,
):
    city = message.text.strip()
    data = await state.get_data()
    period = data.get("period")

    async with httpx.AsyncClient() as http:
        client = WeatherClient(http)
        try:
            result = await client.get_current_weather(city)
        except ValueError:
            await message.answer(
                "Город не найден. Попробуй ещё раз."
            )
            return
        except httpx.HTTPError:
            await message.answer(
                "Сервис погоды временно недоступен."
            )
            return

    user_last_city[message.from_user.id] = city

    label = "сегодня" if period == "weather_today" else "завтра"

    await message.answer(
        f"Погода {label} в {result.city}:\n"
        f"🌡 Температура: {result.temperature_c:.1f}°C\n"
        f"💨 Ветер: {result.wind_speed_ms:.1f} м/с"
    )

    await state.clear()
