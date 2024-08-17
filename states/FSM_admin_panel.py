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
    chng_cat_level = State()
    chng_cat_name = State()
    chng_cat = State()
    chng_joke_level = State()
    chng_joke = State()
    del_cat_level = State()
    del_cat = State()
    del_joke_level = State()
    del_joke_inds = State()
    del_joke_ind = State()
    del_joke = State()
    more_options = State()
    add_admin_id = State()
    add_admin_user = State()
    add_vip_id = State()
    add_vip_user = State()
    contacts = State()





