import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.config import settings
from bot.handlers.rates import router as rates_router
from bot.handlers.start import router as start_router
from bot.handlers.weather import router as weather_router


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(weather_router)
    dp.include_router(rates_router)

    logging.info("Bot started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
