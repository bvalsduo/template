from aiogram import Router
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from loguru import logger as log
from aiogram.filters import StateFilter, Command


from data.jokes import usual_cat_jokes, vip_cat_jokes
from filters.is_category import IsCategory
from filters.is_vip_user import IsVipUser, IsVipUser_func
from filters.is_admin import IsAdmin, IsAdmin_func
from keyboards.user_keyboards import usual_cat_jokes_key, usual_cat_jokes_inds, read_keyboard
from keyboards.vip_user_keyboards import vip_cat_jokes_key, vip_cat_jokes_inds
from keyboards.admin_keyboards import admin_actions, vip_us_key
from states.FSM_reading import fsm_reading
from states.FSM_admin_panel import Admin





rout_admin = Router()
rout_admin.message.filter(IsAdmin())
rout_admin.callback_query.filter(IsAdmin())



# ФУНКЦИИ
# добавление/удаление категорий/анекдотов
# поменять название категории/пользователей категории+
# добавить админа/vip юзера по его id, наверное тогда надо пароль сделать,
# в случае если он его забыл, то отправлять первому(главному) админу в тг
# наверное надо сделать работу с сообщениями, надо их обрабатывать, типо
# если стоит --/: ставить перед знаком \n, вот такое
# выслать все категории/анекдоты которые есть





# /admin command
@rout_admin.message(Command(commands=['admin']), StateFilter(default_state))
async def admin_panel_start(message: Message):
    await message.answer(f'что хочешь сделать', reply_markup=admin_actions().as_markup(resize_keyboard=True))
    log.info('entering an admin panel')

# choose state
@rout_admin.callback_query(StateFilter(default_state))
async def start_actions(callback: CallbackQuery, state: FSMContext):
    states_dct = {'add cat': Admin.add_cat1, 'add joke': Admin.set_vip_us,
                   'delete cat': Admin.delete_cat, 'delete joke': Admin.delete_joke,
                   'more options': Admin.more_options}
    await state.set_state(state=states_dct[callback.data])
    await callback.message.answer(f'Эта категория для вип или обычного пользователя?\nНадо написать Vip либо Usual')



# add category state, for whom
@rout_admin.message(StateFilter(Admin.add_cat1))
async def add_cat_for_whom(message: Message, state: FSMContext):
    if message.text.lower() in ['vip', 'usual']:
        await state.update_data(for_whom=message.text.lower())
        await message.answer(f'принятые данные: {(await state.get_data())["for_whom"]}\n/back чтобы вернуться и поменять данные')
        await state.set_state(Admin.add_cat2)
        await message.answer('Введите название категории')
        log.info(f'state: add cat1 ending right')
    else:
        await message.answer('Неккоректный ввод')
        log.info(f'state: add cat1 ending wrong')


# add category state, name of category
@rout_admin.message(StateFilter(Admin.add_cat2))
async def add_cat_name(message: Message, state: FSMContext):
    await state.update_data(cat_name=message.text)
    await message.answer(f'принятые данные: {(await state.get_data())["cat_name"]}\n/back чтобы вернуться и поменять данные')

    # await state.set_state(Admin.set_vip_us)
    # await message.answer('выберите vip или usual категорию для нового анекдота', reply_markup=vip_us_key)


# set vip/usual categories
@rout_admin.callback_query(StateFilter(Admin.set_vip_us))
async def set_vip_us(callback: CallbackQuery, state: FSMContext):
    await state.update_data(set_cat=callback.data)
    await callback.message.answer(f'принятые данные: {(await state.get_data())["set_cat"]}')





# add joke state
@rout_admin.message(StateFilter(Admin.add_joke1))
async def add_joke_cat(message: Message, state: FSMContext):
    pass

# delete category state
@rout_admin.message(StateFilter(Admin.delete_cat))
async def s1(message: Message, state: FSMContext):
    pass


# delete joke state
@rout_admin.message(StateFilter(Admin.delete_joke))
async def s1(message: Message, state: FSMContext):
    pass


# more options state
@rout_admin.message(StateFilter(Admin.more_options))
async def s1(message: Message, state: FSMContext):
    pass
