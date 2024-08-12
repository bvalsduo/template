from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state


class Admin(StatesGroup):
    selection_state = State()
    add_cat_level = State()
    add_cat_name = State()
    add_joke_level = State()
    add_joke_cat = State()
    add_joke_text = State()
    del_cat_level = State()
    del_cat = State()
    del_joke_level = State()
    del_joke_inds = State()
    del_joke_ind = State()
    del_joke = State()
    more_options = State()





