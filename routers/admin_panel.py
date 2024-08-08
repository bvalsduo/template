from aiogram import Router
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from loguru import logger as log
from aiogram.filters import StateFilter, Command


from data.jokes import usual_cat_jokes, vip_cat_jokes
from filters.is_category import IsCategory
from filters.is_vip_user_ import IsVipUser, IsVipUser_func
from filters.is_admin import IsAdmin, IsAdmin_func
from keyboards.user_keyboards import usual_cat_jokes_key, usual_cat_jokes_inds, read_keyboard
from keyboards.vip_user_keyboards import vip_cat_jokes_key, vip_cat_jokes_inds
from states.FSM_reading import fsm_reading




rout_admin = Router()
rout_admin.message.filter(IsAdmin())
rout_admin.callback_query.filter(IsAdmin())


@rout_admin.message(Command(commands=['admin']))
async def admin_panel(message: Message):
    ad_us_dct = {True: 'ADMIN', False: 'USUAL'}
    await message.answer(f'hey,{message.from_user.id} you are {ad_us_dct[IsAdmin_func(message)]}')













