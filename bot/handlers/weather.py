@router.callback_query(F.data.in_({
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday",
}))
async def handle_callbacks(callback: CallbackQuery, state: FSMContext):
    dataday = callback.data

    data = await state.get_data()
    city = data.get("city")

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

    index = days_map[dataday]

    if index >= len(week_forecast):
        await callback.message.answer("Прогноз на этот день недоступен.")
    else:
        day = week_forecast[index]
        await callback.message.answer(
            f"Погода в {city} на {dataday} ({day.date}):\n"
            f"🌡 Минимальная температура: {day.temperature_c_min:.1f}°C\n"
            f"🌡 Максимальная температура: {day.temperature_c_max:.1f}°C\n"
            f"💨 Ветер: {day.wind_speed_max:.1f} м/с"
        )

    await callback.answer()
