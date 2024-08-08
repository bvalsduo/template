from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state


class Admin(StatesGroup):
    add_cat1 = State()
    add_cat2 = State()
    set_vip_us = State()
    add_joke1 = State()
    add_joke2 = State()
    delete_cat = State()
    delete_joke = State()
    more_options = State()





