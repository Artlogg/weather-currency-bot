import logging

import httpx
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.services.rates_client import RatesClient

router = Router()


@router.message(Command("rate"))
async def rate(message: Message) -> None:
    logging.info("RATE HANDLER TRIGGERED: %s", message.text)

    parts = (message.text or "").split()
    if len(parts) != 3:
        await message.answer(
            "Напиши так:\n"
            "/rate <BASE> <TARGET>\n"
            "Например: /rate EUR USD"
        )
        return

    base, target = parts[1].strip(), parts[2].strip()

    async with httpx.AsyncClient() as http:
        client = RatesClient(http)
        try:
            result = await client.get_rate(base, target)
        except ValueError:
            await message.answer("Эта валютная пара не поддерживается.")
            return
        except httpx.HTTPError:
            await message.answer(
                "Сервис курсов валют временно недоступен. Попробуй позже."
            )
            return

    await message.answer(
        f"💱 Курс валют:\n"
        f"{result.base} → {result.target}: {result.rate:.4f}"
    )
