from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state


class Admin(StatesGroup):
    choose = State()
    choose_state = State()
    add_cat1 = State()
    add_cat2 = State()
    add_joke1 = State()
    add_joke2 = State()
    add_joke3 = State()
    delete_cat = State()
    delete_joke = State()
    more_options = State()





