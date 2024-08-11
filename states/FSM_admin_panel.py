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
    del_cat1 = State()
    del_cat2 = State()
    del_joke1 = State()
    del_joke2 = State()
    more_options = State()





