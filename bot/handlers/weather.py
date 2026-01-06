import httpx
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup

from bot.services.weather_client import WeatherClient

router = Router()



class WeatherStates(StatesGroup):
    waiting_for_city = State()


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
