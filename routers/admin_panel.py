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
from keyboards.admin_keyboards import admin_actions, ad_vip_us_key
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



# /done command
@rout_admin.message(Command(commands=['done']), ~StateFilter(default_state))
async def admin_panel_done(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('data is saved')
    await message.answer(f'что то еще?', reply_markup=admin_actions().as_markup(resize_keyboard=True))
    log.info(f'command done, exit from state')



# /admin command
@rout_admin.message(Command(commands=['admin']), StateFilter(default_state))
async def admin_panel_start(message: Message, state: FSMContext):
    await state.set_state(Admin.choose_state)
    await message.answer(f'что хочешь сделать', reply_markup=admin_actions().as_markup(resize_keyboard=True))
    log.info('entering an admin panel')



# choose state
@rout_admin.callback_query(StateFilter(Admin.choose_state))
async def start_actions(callback: CallbackQuery, state: FSMContext):
    states_dct = {'add cat': Admin.add_cat1, 'add joke': Admin.add_joke1,
                   'delete cat': Admin.delete_cat, 'delete joke': Admin.delete_joke,
                   'more options': Admin.more_options}
    await state.set_state(state=states_dct[callback.data])
    await callback.message.answer(f'Эта категория вип или обычного пользователя?', reply_markup=ad_vip_us_key)
    log.info(f'set state add_cat1')


####################################################################
####################################################################
# add category state, for whom
@rout_admin.callback_query(StateFilter(Admin.add_cat1))
async def add_cat_for_whom(callback: CallbackQuery, state: FSMContext):
    user_dct = {'vip': 'VIP', 'usual': 'USUAl'}
    await state.update_data(cat_for_whom=user_dct[callback.data])
    await state.set_state(Admin.add_cat2)
    await callback.message.answer('Введите название для новой категории')
    log.info(f'add_cat1 is succes, set state add_cat2')


# add category state, name of category
@rout_admin.message(StateFilter(Admin.add_cat2))
async def add_cat_name(message: Message, state: FSMContext):
    await state.update_data(cat_name=message.text)
    await message.answer(f'Название категории:\n{(await state.get_data())["cat_name"]}\n/back чтобы вернуться и поменять данные')
    log.info('add_cat2 is succes, set state choose_state')

    await message.answer(f'что то еще?', reply_markup=admin_actions().as_markup(resize_keyboard=True))
    await state.set_state(Admin.choose_state)

####################################################################
####################################################################



# add joke state, for whom
@rout_admin.callback_query(StateFilter(Admin.add_joke1))
async def add_joke_for_whom(callback: CallbackQuery, state: FSMContext):
    user_dct = {'vip': 'VIP', 'usual': 'USUAL'}
    cat_dct = {'VIP': vip_cat_jokes_key, 'USUAL': usual_cat_jokes_key}
    await state.update_data(joke_for_whom=user_dct[callback.data])
    await state.set_state(Admin.add_joke2)
    await callback.message.answer('Выбери категорию в которой будет новый анекдот', reply_markup=cat_dct[(await state.get_data())['joke_for_whom']])

    log.info(f'add_cat1 is succes, set state add_cat2')



# add joke state, category
@rout_admin.message(StateFilter(Admin.add_joke2))
async def add_joke_cat(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer('Введите текст нового анекдота')
    await state.set_state(Admin.add_joke3)
    log.info(f'add_joke2 is succes')


# add joke state, text of joke
@rout_admin.message(StateFilter(Admin.add_joke3))
async def add_joke_text(message: Message, state: FSMContext):
    await state.update_data(joke_text=message.text)
    await message.answer(f'Анекдот:\n{(await state.get_data())["joke_text"]}\n/back чтобы вернуться и поменять данные')
    jokes_cat_dct = {'VIP': vip_cat_jokes, 'USUAL': usual_cat_jokes}
    jokes_cat_dct[(await state.get_data())['joke_for_whom']][(await state.get_data())['category']][len(jokes_cat_dct[(await state.get_data())['joke_for_whom']][(await state.get_data())['category']]) + 1] = (await state.get_data())['joke_text']
    log.info('anecdot is added, set state choose_state')

    await message.answer(f'что то еще?', reply_markup=admin_actions().as_markup(resize_keyboard=True))
    await state.set_state(Admin.choose_state)



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
