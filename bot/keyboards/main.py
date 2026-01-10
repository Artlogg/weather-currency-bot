from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", 
                              callback_data="cancel")]
    ]
)

back_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
            [InlineKeyboardButton(text="⬅ Назад", 
                                 callback_data="back_to_periods")]
        ]
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
        [   
            InlineKeyboardButton(
                text="Сменить город", callback_data="change_city"
            ),
        ],
        [
            InlineKeyboardButton(text="❌ Отмена", 
                                 callback_data="cancel"),
        ],
    ]
)

week_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Пн", callback_data="Monday"),
            InlineKeyboardButton(text="Вт", callback_data="Tuesday"),
            InlineKeyboardButton(text="Ср", callback_data="Wednesday"),
        ],
        [
            InlineKeyboardButton(text="Чт", callback_data="Thursday"),
            InlineKeyboardButton(text="Пт", callback_data="Friday"),
        ],
        [
            InlineKeyboardButton(text="Сб", callback_data="Saturday"),
            InlineKeyboardButton(text="Вс", callback_data="Sunday"),
        ],
        [
            InlineKeyboardButton(text="⬅ Назад", 
                                 callback_data="back_to_periods"),
        ]
    ]
)

CURRENCIES = ["USD", "EUR", "GBP", "PLN", "CNY"]

def currency_keyboard(exclude: str | None = None) -> InlineKeyboardMarkup:
    items = [c for c in CURRENCIES if c != exclude]

    rows: list[list[InlineKeyboardButton]] = []
    row: list[InlineKeyboardButton] = []
    for code in items:
        row.append(InlineKeyboardButton(text=code, callback_data=f"cur:{code}"))
        if len(row) == 3:
            rows.append(row)
            row = []
    if row:
        rows.append(row)

    rows.append([InlineKeyboardButton(
        text="✍️ Ввести вручную", callback_data="cur:manual")])
    rows.append([InlineKeyboardButton(
        text="❌ Отмена", callback_data="cur:cancel")])

    return InlineKeyboardMarkup(inline_keyboard=rows)


