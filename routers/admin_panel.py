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
from keyboards.user_keyboards import usual_cat_jokes_key, usual_cat_jokes_inds, read_keyboard, usual_lst_cats
from keyboards.vip_user_keyboards import vip_cat_jokes_key, vip_cat_jokes_inds, vip_lst_cats
from keyboards.admin_keyboards import admin_actions, ad_vip_us_key, yn_key
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
    await message.answer(f'чтобы сделать что то еще нажми /admin')
    log.info(f'command done, exit from state')


# /admin command
@rout_admin.message(Command(commands=['admin']), StateFilter(default_state))
async def admin_panel_start(message: Message, state: FSMContext):
    await state.set_state(Admin.selection_state)
    await message.answer(f'что хочешь сделать', reply_markup=admin_actions().as_markup(resize_keyboard=True))
    log.info('entering an admin panel')


# choose state
@rout_admin.callback_query(StateFilter(Admin.selection_state))
async def selection_action(callback: CallbackQuery, state: FSMContext):
    states_dct = {'add cat': Admin.add_cat_level, 'add joke': Admin.add_joke_level,
                  'delete cat': Admin.del_cat_level, 'delete joke': Admin.del_joke_level,
                  'more options': Admin.more_options}
    await state.set_state(state=states_dct[callback.data])
    await callback.message.answer(f'Эта категория вип или обычного пользователя?', reply_markup=ad_vip_us_key)
    log.info(f'set state add_cat1')



#############################################3#############################################3#############################################


#############################################3#############################################3
# add category state, for whom
@rout_admin.callback_query(StateFilter(Admin.add_cat_level))
async def add_cat_level(callback: CallbackQuery, state: FSMContext):
    user_dct = {'vip': 'VIP', 'usual': 'USUAL'}
    await state.update_data(cat_level=user_dct[callback.data])
    await state.set_state(Admin.add_cat_name)
    await callback.message.answer('Введите название для новой категории')
    log.info(f'add_cat1 is succes, set state add_cat2')


# add category state, name of category
@rout_admin.message(StateFilter(Admin.add_cat_name))
async def add_cat_name(message: Message, state: FSMContext):
    await state.update_data(cat_name=message.text)
    cat_name = (await state.get_data())['cat_name']
    cat_level = (await state.get_data())['cat_level']
    jokes_cat_dct = {'VIP': [vip_cat_jokes, vip_lst_cats, vip_cat_jokes_key],
                     'USUAL': [usual_cat_jokes, usual_lst_cats, usual_cat_jokes_key]}
    jokes_cat_dct[cat_level][0][cat_name] = {1: 'Пустой анекдот'}                    # add new category
    jokes_cat_dct[cat_level][1].append(cat_name)                                     # add new category to cat_key
    await message.answer(f'Название категории:\n{cat_name}\n/back чтобы вернуться и поменять данные',
                         reply_markup=jokes_cat_dct[cat_level][2]().as_markup(resize_keyboard=True))
    log.info('add_cat2 is succes, set state choose_state')

    await message.answer(f'что то еще?', reply_markup=admin_actions().as_markup(resize_keyboard=True,
                                                                                      input_field_placeholder='клавиатура обновлена'))
    await state.set_state(Admin.selection_state)


#############################################3#############################################3
# add joke state, for whom
@rout_admin.callback_query(StateFilter(Admin.add_joke_level))
async def add_joke_level(callback: CallbackQuery, state: FSMContext):
    user_dct = {'vip': 'VIP', 'usual': 'USUAL'}
    cat_dct = {'VIP': vip_cat_jokes_key, 'USUAL': usual_cat_jokes_key}
    await state.update_data(joke_level=user_dct[callback.data])
    await state.set_state(Admin.add_joke_cat)
    await callback.message.answer('Выбери категорию в которой будет новый анекдот',
                                  reply_markup=cat_dct[(await state.get_data())['joke_level']]().as_markup(resize_keyboard=True,
                                                                                                              input_field_placeholder='Выбери категорию'))
    log.info(f'add_joke_level is succes, set state add_cat2')


# add joke state, category
@rout_admin.message(StateFilter(Admin.add_joke_cat))
async def add_joke_cat(message: Message, state: FSMContext):
    await state.update_data(joke_cat=message.text)
    await message.answer('Введите текст нового анекдота')
    await state.set_state(Admin.add_joke_text)
    log.info(f'add_joke2 is succes')


# add joke state, text of joke
@rout_admin.message(StateFilter(Admin.add_joke_text))
async def add_joke_text(message: Message, state: FSMContext):
    await state.update_data(joke_text=message.text)
    await message.answer(f'Анекдот:\n{message.text}\n/back чтобы вернуться и поменять данные')
    jokes_cat_dct = {'VIP': vip_cat_jokes, 'USUAL': usual_cat_jokes}
    joke_text = (await state.get_data())['joke_text']
    joke_level = (await state.get_data())['joke_level']
    cat = (await state.get_data())['joke_cat']
    jokes_cat_dct[joke_level][cat][len(jokes_cat_dct[joke_level][cat]) + 1] = joke_text

    await message.answer(f'что то еще?', reply_markup=admin_actions().as_markup(resize_keyboard=True))
    await state.set_state(Admin.selection_state)
    log.info('anecdot is added, set state choose_state')


#############################################3#############################################3
# delete category state, choose category
@rout_admin.callback_query(StateFilter(Admin.del_cat_level))
async def del_cat_level(callback: CallbackQuery, state: FSMContext):
    user_dct = {'vip': 'VIP', 'usual': 'USUAL'}
    cat_dct = {'VIP': vip_cat_jokes_key, 'USUAL': usual_cat_jokes_key}
    await state.update_data(del_cat_level=user_dct[callback.data])
    await callback.message.answer('Выбери категорию для удаления',
                                  reply_markup=cat_dct[user_dct[callback.data]]().as_markup(resize_keyboard=True,
                                                                                            input_field_placeholder='Выбери категорию'))
    await state.set_state(Admin.del_cat)
    log.info('delete ca1 succes, set state del_cat2')



# delete category state, delete category
@rout_admin.message(StateFilter(Admin.del_cat))
async def del_cat(message: Message, state: FSMContext):
    level = (await state.get_data())['del_cat_level']
    cat_dct = {'VIP': [vip_lst_cats, vip_cat_jokes, vip_cat_jokes_key],
               'USUAL': [usual_lst_cats, usual_cat_jokes, usual_cat_jokes_key]}
    cat_dct[level][0].remove(message.text)
    cat_dct[level][1].pop(message.text)
    await message.answer(f'удаленная категория:\n{message.text}\n/back чтобы вернуться и поменять данные',
                         reply_markup=cat_dct[level][2]().as_markup(resize_keyboard=True,
                                                                    input_field_placeholder='Выбери категорию'))
    await message.answer(f'что то еще?', reply_markup=admin_actions().as_markup(resize_keyboard=True,
                                                                                      input_field_placeholder='клавиатура обновлена'))
    await state.set_state(Admin.selection_state)
    log.info(f'del cat2 succes, set state choose state')





#############################################3#############################################3
# delete joke state, choose  category
@rout_admin.callback_query(StateFilter(Admin.del_joke_level))
async def del_cat_level(callback: CallbackQuery, state: FSMContext):
    user_dct = {'vip': 'VIP', 'usual': 'USUAL'}
    cat_dct = {'VIP': vip_cat_jokes_key, 'USUAL': usual_cat_jokes_key}
    await state.update_data(del_joke_level=user_dct[callback.data])
    await callback.message.answer('Выбери категорию анекдота который хочешь удалить',
                                  reply_markup=cat_dct[user_dct[callback.data]]().as_markup(resize_keyboard=True,
                                                                                            input_field_placeholder='Выбери категорию'))
    await state.set_state(Admin.del_joke_inds)
    log.info('delete ca1 succes, set state del_cat2')


# delete joke state, send inline key with inds
@rout_admin.message(StateFilter(Admin.del_joke_inds))
async def del_joke_send_inds(message: Message, state: FSMContext):
    await state.update_data(del_joke_cat=message.text)
    cat = (await state.get_data())['del_joke_cat']

    await message.answer(cat, reply_markup=usual_cat_jokes_inds(cat).as_markup(input_field_placeholder='Выбери анекдот'))
    await state.set_state(Admin.del_joke_ind)
    log.info('sending keyboard with anecdots, set state del_joke3')


@rout_admin.callback_query(StateFilter(Admin.del_joke_ind))
async def del_joke_ind(callback: CallbackQuery, state: FSMContext):
    if callback.data.split('-')[1] == (await state.get_data())['category']:
        ind = int(callback.data.split('-')[0])
        await state.update_data(index=ind)
        level = (await state.get_data())['del_joke_level']
        cat = (await state.get_data())['del_joke_cat']
        dct_lst_jokes = {'VIP': vip_cat_jokes, 'USUAL': usual_cat_jokes}
        cat_len = len(dct_lst_jokes[level][cat])

        await callback.message.answer(usual_cat_jokes[cat][ind + 1],
                                      reply_markup=read_keyboard(index=ind + 1,
                                                                 count=(cat_len)).as_markup(resize_keyboard=True))      # !!!!!!!!!!!!!!!!!!!!!!!#!!!!!!!!!!!!!!!!!!!!!!!!!!!
        await callback.message.answer('Это тот анекдот?', reply_markup=yn_key)
        log.info(f'callback is handled, index - {ind + 1}')

        await state.set_state(Admin.del_joke)
    else:
        await callback.message.answer('Воспользуйтесь кнопками что ниже')
        log.debug(f'wrong inline keyboard - protected')


@rout_admin.callback_query(StateFilter(Admin.del_joke))
async def del_joke_filter(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'YES':
        level = (await state.get_data())['del_joke_for_whom']                       # когда удаляешь анекдота с самого начало
        cat = (await state.get_data())['category']                                  # vip/usual_cat_jokes_inds индексы
        ind = (await state.get_data())['index']                                     # работают не так, они сдвигаются
        cat_dct = {'VIP': [vip_cat_jokes, vip_cat_jokes_inds],                      # в инлайн клавиатуре он может быть с
                   'USUAL': [usual_cat_jokes, usual_cat_jokes_inds]}                # индексом 2, а из за удаления анекдота
        del_joke = cat_dct[level][0][cat][ind + 1]                                  # перед ним, на самом деле быть 1 (-1)
        del cat_dct[level][0][cat][ind + 1]
        await callback.message.answer(f'удаленный анекдот:\n{del_joke}\n/back чтобы вернуться и поменять данные',
                                      reply_markup=cat_dct[level][1](cat).as_markup(resize_keyboard=True,
                                                                                    input_field_placeholder='индексы категории'))
        await callback.message.answer(f'что то еще?',
                                      reply_markup=admin_actions().as_markup(resize_keyboard=True,
                                                                             input_field_placeholder='клавиатура обновлена'))
        await state.set_state(Admin.selection_state)
        log.info(f'del joke4 succes, set state choose state')

    elif callback.data == 'NO':
        cat = (await state.get_data())['category']
        await callback.message.answer(cat,
                                      reply_markup=usual_cat_jokes_inds(cat).as_markup(input_field_placeholder='Выбери анекдот'))
        await state.set_state(Admin.del_joke_ind)
        log.info('sending keyboard with anecdots, set state del_joke3')



#############################################3#############################################3
# more options state
@rout_admin.message(StateFilter(Admin.more_options))
async def s1(message: Message, state: FSMContext):
    pass
