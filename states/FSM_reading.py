from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state


class fsm_reading(StatesGroup):
    reading = State()



