router = Router()


# Старт сценария по кнопке "💱 Курс валют"
@router.message(lambda m: m.text == "💱 Курс валют")
async def rate_start(message: Message, state: FSMContext) -> None:

    await state.clear()
    await state.set_state(RateFlow.choosing_base)
    await message.answer(
        "Выберите исходную валюту:",
        reply_markup=currency_keyboard(),
    )


# Отмена сценария
@router.callback_query(F.data == "cur:cancel")
async def rate_cancel(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text("Операция отменена.")
    await callback.answer()


# Выбор исходной валюты (кнопки)
@router.callback_query(RateFlow.choosing_base, F.data.startswith("cur:"))
async def choose_base(callback: CallbackQuery, state: FSMContext) -> None:
    code = callback.data.split(":", 1)[1]

    if code == "manual":
        await state.update_data(waiting_for="base")
        await callback.message.edit_text(
            "Введите исходную валюту (например: USD):"
        )
        await callback.answer()
        return

    await state.update_data(base=code)
    await state.set_state(RateFlow.choosing_target)

    await callback.message.edit_text(
        f"Исходная валюта: {code}\n"
        f"Теперь выберите конечную валюту:",
        reply_markup=currency_keyboard(exclude=code),
    )
    await callback.answer()


# Выбор конечной валюты (кнопки)
@router.callback_query(RateFlow.choosing_target, F.data.startswith("cur:"))
async def choose_target(callback: CallbackQuery, state: FSMContext) -> None:
    code = callback.data.split(":", 1)[1]
    data = await state.get_data()
    base = data.get("base")

    if code == "manual":
        await state.update_data(waiting_for="target")
        await callback.message.edit_text(
            "Введите конечную валюту (например: EUR):"
        )
        await callback.answer()
        return

    if code == base:
        await callback.answer(
            "Нельзя выбрать ту же валюту.",
            show_alert=True,
        )
        return

    target = code
@@ -97,79 +84,60 @@ async def choose_target(callback: CallbackQuery, state: FSMContext) -> None:
            return

    await callback.message.edit_text(
        f"💱 Курс валют:\n"
        f"{result.base} → {result.target}: {result.rate:.4f}"
    )
    await state.clear()
    await callback.answer()


# Ручной ввод исходной валюты
@router.message(RateFlow.choosing_base, F.text)
async def manual_base(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if data.get("waiting_for") != "base":
        return

    base = (message.text or "").strip().upper()
    if not base.isalpha() or len(base) != 3:
        await message.answer(
            "Введите 3-буквенный код валюты, например: USD"
        )
        return

    await state.update_data(base=base, waiting_for=None)
    await state.set_state(RateFlow.choosing_target)

    await message.answer(
        f"Исходная валюта: {base}\n"
        f"Теперь выберите конечную валюту:",
        reply_markup=currency_keyboard(exclude=base),
    )


# Ручной ввод конечной валюты
@router.message(RateFlow.choosing_target, F.text)
async def manual_target(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if data.get("waiting_for") != "target":
        return

    target = (message.text or "").strip().upper()
    base = data.get("base")

    if not target.isalpha() or len(target) != 3:
        await message.answer(
            "Введите 3-буквенный код валюты, например: EUR"
        )
        return

    if target == base:
        await message.answer(
            "Конечная валюта не должна совпадать с исходной."
        )
        return

    async with httpx.AsyncClient() as http:
        client = RatesClient(http)
        try:
            result = await client.get_rate(base, target)
        except ValueError:
            await message.answer(
                f"❌ Валютная пара {base} → {target} не поддерживается."
            )
            await state.clear()
            return
        except httpx.HTTPError:
            await message.answer(
                "⚠️ Сервис курсов валют временно недоступен."
            )
            await state.clear()
            return

    await message.answer(
        f"💱 Курс валют:\n"
        f"{result.base} → {result.target}: {result.rate:.4f}"
    )
    await state.clear()
