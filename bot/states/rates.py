from aiogram.fsm.state import State, StatesGroup


class RateFlow(StatesGroup):
    choosing_base = State()
    choosing_target = State()
