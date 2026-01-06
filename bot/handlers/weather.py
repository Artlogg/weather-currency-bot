import httpx
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.services.weather_client import WeatherClient
from bot.states.weather import WeatherStates

router = Router()

user_last_city: dict[int, str] = {}


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
        f"🌡 Минимальная температура: {result.temperature_c_min:.1f}°C\n"
        f"🌡 Максимальная температура: {result.temperature_c_max:.1f}°C\n"
        f"💨 Ветер: {result.wind_speed_ms:.1f} м/с"
    )

    await state.clear()

@router.callback_query(F.data.in_({
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday",
}))
async def handle_callbacks(callback: CallbackQuery, state: FSMContext):
    data = callback.data
    user_id = callback.from_user.id
    
    if data in ("Monday", "Tuesday", "Wednesday", "Thursday", 
                "Friday", "Saturday", "Sunday"):
        city = user_last_city.get(user_id)
        if not city:
            await callback.message.answer(
                "Ты ещё не вводил город. Введите город текстом."
            )
            await callback.answer()
            return

        async with httpx.AsyncClient() as http:
            client = WeatherClient(http)
            week_forecast = await client.get_week_forecast(city)

        days_map = {
            "Monday": 0,
            "Tuesday": 1,
            "Wednesday": 2,
            "Thursday": 3,
            "Friday": 4,
            "Saturday": 5,
            "Sunday": 6,
        }
        index = days_map[data]

        if index >= len(week_forecast):
            await callback.message.answer("Прогноз на этот день недоступен.")
        else:
            day = week_forecast[index]
            await callback.message.answer(
                f"Погода в {city} на {data} ({day.date}):\n"
                f"🌡 Минимальная температура: {day.temperature_c_min:.1f}°C\n"
                f"🌡 Максимальная температура: {day.temperature_c_max:.1f}°C\n"
                f"💨 Ветер: {day.wind_speed_max:.1f} м/с"
            )
    await callback.answer()
