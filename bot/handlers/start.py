from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from bot.keyboards.main import general_menu, main_menu, rates_menu, weather_menu
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


@router.message()
async def handle_main_buttons(message: Message):
    text = message.text

    if text == "🌤 Погода":
        await message.answer("Выберите опцию:", reply_markup=weather_menu)
    elif text == "💱 Курсы валют":
        await message.answer("Выберите пару:", reply_markup=rates_menu)
    elif text == "⚙️ Общее":
        await message.answer("Настройки:", reply_markup=general_menu)


@router.callback_query()
async def handle_callbacks(
    callback: CallbackQuery,
    state: FSMContext,
):
    data = callback.data
    user_id = callback.from_user.id

    if data in ("weather_today", "weather_tomorrow"):
        await state.set_state(WeatherStates.waiting_for_city)
        await state.update_data(period=data)  # today / tomorrow

        await callback.message.answer(
            "Введите город (например: Riga)"
        )

    await callback.answer()

    elif data.startswith("rate_"):
        if data == "rate_usd_rub":
            user_last_rate[user_id] = ("USD", "RUB")
            await callback.message.answer("USD → RUB")
        elif data == "rate_cny_rub":
            user_last_rate[user_id] = ("CNY", "RUB")
            await callback.message.answer("CNY → RUB")
        elif data == "rate_favorite":
            pair = user_last_rate.get(user_id)
            if pair:
                await callback.message.answer(
                    f"Любимая пара: {pair[0]} → {pair[1]}"
                )
            else:
                await callback.message.answer(
                    "Любимая пара не сохранена"
                )

    elif data == "general_hide":
        await callback.message.answer(
            "Клавиатура убрана",
            reply_markup=None,
        )
    await callback.answer()
