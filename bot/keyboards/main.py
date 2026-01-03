from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

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

weather_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сегодня"), KeyboardButton(text="Завтра")],
        [KeyboardButton(text="Ветер")],
        [KeyboardButton(text="⬅️ Назад")],
    ],
    resize_keyboard=True,
)

rates_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="EUR/USD"), KeyboardButton(text="USD/JPY")],  # популярные пары
        [KeyboardButton(text="Любимая пара")],
        [KeyboardButton(text="Обновить курс")],
        [KeyboardButton(text="⬅️ Назад")],
    ],
    resize_keyboard=True,
)

general_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔄 Обновить")],
        [KeyboardButton(text="❌ Убрать клавиатуру")],
        [KeyboardButton(text="ℹ️ Помощь")],
        [KeyboardButton(text="⬅️ Назад")],
    ],
    resize_keyboard=True,
)
