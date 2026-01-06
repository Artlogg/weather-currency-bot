from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🌤 Погода"),
            KeyboardButton(text="💱 Курс валют"),
        ],
        [
            KeyboardButton(text="ℹ️ Помощь"),
        ],
    ],
    resize_keyboard=True,
)

weather_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Сегодня", callback_data="weather_today"
            ),
            InlineKeyboardButton(
                text="Завтра", callback_data="weather_tomorrow"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Неделя", callback_data="weather_week"
            ),
        ],
    ]
)

last_city_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⭐ Последний город", callback_data="weather_last"
            ),
        ],
    ]
)

week_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Пн", callback_data="Monday"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Вт", callback_data="Tuesday"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Ср", callback_data="Wednesday"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Чт", callback_data="Thursday"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Пт", callback_data="Friday"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Сб", callback_data="Saturday"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Вс", callback_data="Sunday"
            ),
        ],
    ]
)
rates_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="USD / RUB", callback_data="rate_usd_rub"
            ),
            InlineKeyboardButton(
                text="CNY / RUB", callback_data="rate_cny_rub"
            ),
        ],
        [
            InlineKeyboardButton(
                text="⭐ Любимая пара", callback_data="rate_favorite"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔄 Обновить курс", callback_data="rate_refresh"
            ),
        ],
    ]
)

general_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🔄 Обновить", callback_data="general_refresh"
            ),
        ],
        [
            InlineKeyboardButton(
                text="❌ Убрать клавиатуру",
                callback_data="general_hide",
            ),
        ],
        [
            InlineKeyboardButton(
                text="ℹ️ Помощь", callback_data="general_help"
            ),
        ],
    ]
)
