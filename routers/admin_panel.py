from aiogram import Router, F
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from loguru import logger as log
from aiogram.filters import StateFilter, Command


from data.jokes import usual_cat_jokes, vip_cat_jokes
from data.config import admin_ids, vip_ids
from filters.is_category import IsCategory
from filters.is_vip_user import IsVipUser, IsVipUser_func
from filters.is_admin import IsAdmin, IsAdmin_func
from keyboards.user_keyboards import usual_cat_jokes_key, usual_cat_jokes_inds, read_keyboard, usual_lst_cats
from keyboards.vip_user_keyboards import vip_cat_jokes_key, vip_cat_jokes_inds, vip_lst_cats
from keyboards.admin_keyboards import admin_actions, ad_vip_us_key, yn_key, options_key, contacts_key, dct_rename
from states.FSM_reading import fsm_reading
from states.FSM_admin_panel import Admin


rout_admin = Router()
rout_admin.message.filter(IsAdmin())
rout_admin.callback_query.filter(IsAdmin())


# ФУНКЦИИ
# поменять название категории/пользователей категории+
# наверное надо сделать работу с сообщениями, надо их обрабатывать, типо
# если стоит --/: ставить перед знаком \n, вот такое
# выслать все категории/анекдоты которые есть


# нужно сделать генератор reply клавиатуры с категориями анекдотов






#########################################################################################
#                            HANDLERS FOR ENTERING, COMMANDS


# /done command
@rout_admin.message(Command(commands=['done']), ~StateFilter(default_state))
async def admin_panel_done(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('data is saved')
    await message.answer('чтобы сделать что то еще нажми /admin')
    log.info(f"command done, exit from state")


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
                  'change cat': Admin.chng_cat_level, 'change joke': Admin.chng_joke_level,
                  'more options': Admin.more_options}

    if callback.data in states_dct:
        if callback.data != 'more options':
            await state.set_state(state=states_dct[callback.data])
            await callback.message.answer(f'Эта категория вип или обычного пользователя?', reply_markup=ad_vip_us_key)
            log.info(f'set state {callback.data}')
        else:
            await state.set_state(state=states_dct[callback.data])
            await callback.message.answer('что хочешь сделать', reply_markup=options_key)
            log.info(f'set state {callback.data}')
    else:
        if callback.data.split('-')[1] in [*usual_lst_cats, *vip_lst_cats]:
            ind = int(callback.data.split('-')[0])
            await state.update_data(index=ind)
            level = (await state.get_data())['del_joke_level']
            cat = callback.data.split('-')[1]
            dct_lst_jokes = {'VIP': vip_cat_jokes, 'USUAL': usual_cat_jokes}
            await callback.message.answer(f'{usual_cat_jokes[cat][ind]}')
            log.info(f'callback is handled, index - {ind + 1}')



#########################################################################################
#                            HANDLERS FOR CATEGORIES


# add category state, for whom
@rout_admin.callback_query(StateFilter(Admin.add_cat_level), lambda x: x.data in ['VIP', 'USUAL'])
async def add_cat_level(callback: CallbackQuery, state: FSMContext):
    user_dct = {'VIP': 'VIP', 'USUAL': 'USUAL'}
    await state.update_data(cat_level=user_dct[callback.data])
    await state.set_state(Admin.add_cat_name)
    await callback.message.answer('Введите название для новой категории')
    log.info(f'add_cat_level is succes, set state add_cat_name')


# add category state, name of category
@rout_admin.message(StateFilter(Admin.add_cat_name), F.text)
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

    await message.answer(f'что то еще?', reply_markup=admin_actions().as_markup(resize_keyboard=True,
                                                                                      input_field_placeholder='клавиатура обновлена'))
    await state.set_state(Admin.selection_state)
    log.info('add_cat_name is succes, set state selection_state')


# change category state, choose category
@rout_admin.callback_query(StateFilter(Admin.chng_cat_level), lambda x: x.data in ['VIP', 'USUAL'])
async def change_cat_level(callback: CallbackQuery, state: FSMContext):
    await state.update_data(chng_cat_level=callback.data)
    jokes_cat_dct = {'VIP': vip_cat_jokes_key,
                     'USUAL': usual_cat_jokes_key}
    await callback.message.answer('Выберите категорию название которой хотите поменять',
                                  reply_markup=jokes_cat_dct[(await state.get_data())['chng_cat_level']]().as_markup(resize_keyboard=True))
    await state.set_state(Admin.chng_cat_name)
    log.info('chng cat level succes, set chng cat state')


# change category state, set new name
@rout_admin.message(StateFilter(Admin.chng_cat_name), lambda x: x.text in [*usual_lst_cats, *vip_lst_cats])
async def change_cat_new_name(message: Message, state: FSMContext):
    await message.answer(f'Старое имя категории ---\n{message.text},\nВведите новое имя')
    await state.update_data(chng_cat_old_name=message.text)
    await state.set_state(Admin.chng_cat)
    log.info(f'chng cat name succes, set chng name')


@rout_admin.message(StateFilter(Admin.chng_cat), lambda x: x.isalpha())
async def change_cat_name(message: Message, state: FSMContext):
    old_cat_name = (await state.get_data())['chng_cat_old_name']
    level = (await state.get_data())['chng_cat_level']
    new_cat_name = message.text
    cat_dct = {'VIP': [vip_lst_cats, vip_cat_jokes, vip_cat_jokes_key],
               'USUAL': [usual_lst_cats, usual_cat_jokes, usual_cat_jokes_key]}

    

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# # change category state, change category name
# @rout_admin.message(StateFilter(Admin.chng_cat), F.text)
# async def change_name(message: Message, state: FSMContext):
#     level = (await state.get_data())['chng_cat_level']
#     old_cat_name = (await state.get_data())['chng_cat_old_name']
#     new_cat_name = message.text
#     # global vip_lst_cats, vip_cat_jokes, vip_cat_jokes_key, \
#     #        usual_lst_cats, usual_cat_jokes, usual_cat_jokes_key
#     # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#     cat_dct = {'VIP': [vip_lst_cats, vip_cat_jokes, vip_cat_jokes_key],
#                'USUAL': [usual_lst_cats, usual_cat_jokes, usual_cat_jokes_key]}
#
#     cat_dct[level][1] = dct_rename(cat_dct[level][1], old_cat_name, new_cat_name)
#     cat_dct[level][0] = list(cat_dct[level][1].keys())
#     # print(cat_dct[level][1], cat_dct[level][0])
#     # print(usual_lst_cats, usual_cat_jokes)
#     await message.answer(f'{old_cat_name} -> {new_cat_name}\n/back чтобы вернуться и поменять данные',
#                          reply_markup=cat_dct[level][2]().as_markup(resize_keyboard=True))
#     await message.answer(f'что то еще?',
#                          reply_markup=admin_actions().as_markup(resize_keyboard=True,
#                                                                 input_field_placeholder='клавиатура обновлена'))
#     await state.set_state(Admin.selection_state)
#     log.info(f'del_cat succes, set state selection state')


# delete category state, choose category
@rout_admin.callback_query(StateFilter(Admin.del_cat_level), lambda x: x.data in ['VIP', 'USUAL'])
async def del_cat_level(callback: CallbackQuery, state: FSMContext):
    cat_dct = {'VIP': vip_cat_jokes_key, 'USUAL': usual_cat_jokes_key}
    user_dct = {'VIP': 'VIP', 'USUAL': 'USUAL'}
    await state.update_data(del_cat_level=user_dct[callback.data])
    await callback.message.answer('Выбери категорию для удаления',
                                  reply_markup=cat_dct[callback.data]().as_markup(resize_keyboard=True,
                                                                                            input_field_placeholder='Выбери категорию'))
    await state.set_state(Admin.del_cat)
    log.info('delete_cat_level is succes, set del_cat')


# delete category state, delete category
@rout_admin.message(StateFilter(Admin.del_cat), lambda x: x.text in [*usual_lst_cats, *vip_lst_cats])
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
    log.info(f'del_cat succes, set state selection state')




#########################################################################################
#                            HANDLERS FOR JOKES


# add joke state, for whom
@rout_admin.callback_query(StateFilter(Admin.add_joke_level), lambda x: x.data in ['VIP', 'USUAL'])
async def add_joke_level(callback: CallbackQuery, state: FSMContext):
    cat_dct = {'VIP': vip_cat_jokes_key, 'USUAL': usual_cat_jokes_key}
    user_dct = {'VIP': 'VIP', 'USUAL': 'USUAL'}
    await state.update_data(joke_level=user_dct[callback.data])
    await state.set_state(Admin.add_joke_cat)
    await callback.message.answer('Выбери категорию в которой будет новый анекдот',
                                  reply_markup=cat_dct[(await state.get_data())['joke_level']]().as_markup(resize_keyboard=True,
                                                                                                           input_field_placeholder='Выбери категорию'))
    log.info(f'add_joke_level is succes, set state add_joke_cat')


# add joke state, category
@rout_admin.message(StateFilter(Admin.add_joke_cat), lambda x: x.text in [*usual_lst_cats, *vip_lst_cats])
async def add_joke_cat(message: Message, state: FSMContext):
    await state.update_data(joke_cat=message.text)
    await message.answer('Введите текст нового анекдота')
    await state.set_state(Admin.add_joke_text)
    log.info(f'add_joke_cat is succes, set add_joke_text')


# add joke state, text of joke
@rout_admin.message(StateFilter(Admin.add_joke_text))
async def add_joke_text(message: Message, state: FSMContext):
    await state.update_data(joke_text=message.text)
    await message.answer(f'Анекдот:\n{message.text}\n/back чтобы вернуться и поменять данные')
    joke_text = (await state.get_data())['joke_text']
    joke_level = (await state.get_data())['joke_level']
    cat = (await state.get_data())['joke_cat']
    jokes_cat_dct = {'VIP': vip_cat_jokes, 'USUAL': usual_cat_jokes}
    jokes_cat_dct[joke_level][cat].append(joke_text)

    await message.answer(f'что то еще?', reply_markup=admin_actions().as_markup(resize_keyboard=True))
    await state.set_state(Admin.selection_state)
    log.info('add_joke_text is succes, set state choose_state')


# delete joke state, choose  category
@rout_admin.callback_query(StateFilter(Admin.del_joke_level), lambda x: x.data in ['VIP', 'USUAL'])
async def del_cat_level(callback: CallbackQuery, state: FSMContext):
    cat_dct = {'VIP': vip_cat_jokes_key, 'USUAL': usual_cat_jokes_key}
    user_dct = {'VIP': 'VIP', 'USUAL': 'USUAL'}
    # if callback.data in user_dct:
    await state.update_data(del_joke_level=user_dct[callback.data])
    await callback.message.answer('Выбери категорию анекдота который хочешь удалить',
                                  reply_markup=cat_dct[user_dct[callback.data]]().as_markup(resize_keyboard=True,
                                                                                            input_field_placeholder='Выбери категорию'))
    await state.set_state(Admin.del_joke_inds)
    log.info('delete_joke_level succes, set del_joke_inds')


# delete joke state, send inline key with inds
@rout_admin.message(StateFilter(Admin.del_joke_inds), lambda x: x.text in [*usual_lst_cats, *vip_lst_cats])
async def del_joke_send_inds(message: Message, state: FSMContext):
    await state.update_data(del_joke_cat=message.text)
    cat = (await state.get_data())['del_joke_cat']

    await message.answer(cat, reply_markup=usual_cat_jokes_inds(cat).as_markup(input_field_placeholder='Выбери анекдот'))
    await state.set_state(Admin.del_joke_ind)
    log.info('sending keyboard with anecdots, set state del_joke_ind')


# delete joke state, set index of joke
@rout_admin.callback_query(StateFilter(Admin.del_joke_ind))
async def del_joke_ind(callback: CallbackQuery, state: FSMContext):
    if callback.data.split('-')[1] == (await state.get_data())['del_joke_cat']:
        ind = int(callback.data.split('-')[0])
        await state.update_data(index=ind)
        level = (await state.get_data())['del_joke_level']
        cat = (await state.get_data())['del_joke_cat']
        dct_lst_jokes = {'VIP': vip_cat_jokes, 'USUAL': usual_cat_jokes}
        cat_len = len(dct_lst_jokes[level][cat])

        await callback.message.answer(f'{usual_cat_jokes[cat][ind]}\n\nЭто тот анекдот?', reply_markup=yn_key)
        log.info(f'callback is handled, index - {ind + 1}')

        await state.set_state(Admin.del_joke)
        log.info(f'del_joke_ind succes, set del_joke')
    else:
        await callback.message.answer('Воспользуйтесь кнопками что ниже')
        log.debug(f'wrong inline keyboard - protected')


# delete joke state, delete joke
@rout_admin.callback_query(StateFilter(Admin.del_joke))
async def del_joke_filter(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'YES':
        level = (await state.get_data())['del_joke_level']
        cat = (await state.get_data())['del_joke_cat']
        ind = (await state.get_data())['index']
        cat_dct = {'VIP': [vip_cat_jokes, vip_cat_jokes_inds],
                   'USUAL': [usual_cat_jokes, usual_cat_jokes_inds]}

        del_joke = cat_dct[level][0][cat][ind]
        del cat_dct[level][0][cat][ind]
        await callback.message.answer(f'удаленный анекдот:\n{del_joke}\n/back чтобы вернуться и поменять данные',
                                      reply_markup=cat_dct[level][1](cat).as_markup(resize_keyboard=True,
                                                                                    input_field_placeholder='индексы категории'))
        await callback.message.answer(f'что то еще?',
                                      reply_markup=admin_actions().as_markup(resize_keyboard=True,
                                                                             input_field_placeholder='клавиатура обновлена'))
        await state.set_state(Admin.selection_state)
        log.info(f'del joke succes, set state selection state')
    elif callback.data == 'NO':
        cat = (await state.get_data())['del_joke_cat']
        await callback.message.answer(cat,
                                      reply_markup=usual_cat_jokes_inds(cat).as_markup(input_field_placeholder='Выбери анекдот'))
        await state.set_state(Admin.del_joke_ind)
        log.info('sending keyboard with anecdots, set state del_joke3')



#########################################################################################
#                            HANDLERS FOR MORE OPTIONS


# more options state
@rout_admin.callback_query(StateFilter(Admin.more_options), lambda x: x.data in ['add_admin', 'add_vip', 'contacts'])
async def more_options(callback: CallbackQuery, state: FSMContext):
    options_dct = {'add_admin': Admin.add_admin_id,
                   'add_vip': Admin.add_vip_id ,
                   'contacts': Admin.contacts}
    if callback.data in ['add_admin', 'add_vip']:
        await callback.message.answer('отправь новый id')
        await state.set_state(options_dct[callback.data])
        log.info(f'more options succes, set something')
    else:
        await callback.message.answer('contacts:', reply_markup=contacts_key)


# add admin id state
@rout_admin.message(StateFilter(Admin.add_admin_id), F.text.isdigit())
async def add_admin_id(message: Message, state: FSMContext):
    new_admin_id = message.text
    await state.update_data(new_admin_id=new_admin_id)
    await message.answer(f'id -- {new_admin_id}\nЭто правильный ID?', reply_markup=yn_key)

    await state.set_state(Admin.add_admin_user)
    log.info(f'add admin id succes, set add_admin_user')


# add admin user state
@rout_admin.callback_query(StateFilter(Admin.add_admin_user))
async def add_admin_user(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'YES':
        new_admin_id = (await state.get_data())['new_admin_id']
        admin_ids.append(new_admin_id)
        await callback.message.answer('новый админ добавлен',
                                      reply_markup=admin_actions().as_markup(resize_keyboard=True))
        await state.set_state(Admin.selection_state)
        log.info(f'add admin user succes, set selection_state')
    elif callback.data == 'NO':
        await callback.message.answer('отправь id')
        await state.set_state(Admin.add_admin_id)
        log.info(f'add admin user failed, set add admin id')


# add vip id state
@rout_admin.message(StateFilter(Admin.add_vip_id), F.text.isdigit())
async def add_vip_id(message: Message, state: FSMContext):
    new_vip_id = message.text
    await state.update_data(new_vip_id=new_vip_id)
    await message.answer(f'id -- {new_vip_id}\nЭто правильный ID?', reply_markup=yn_key)

    await state.set_state(Admin.add_vip_user)
    log.info(f'add vip id succes, set add_admin_user')


# add vip user state
@rout_admin.callback_query(StateFilter(Admin.add_vip_user))
async def add_vip_user(callback: CallbackQuery, state: FSMContext):
    if callback.data == "YES":
        new_vip_id = (await state.get_data())['new_vip_id']
        admin_ids.append(new_vip_id)
        await callback.message.answer('новый вип добавлен',  reply_markup=admin_actions().as_markup(resize_keyboard=True))
        await state.set_state(Admin.selection_state)
        log.info(f'add vip user succes, set selection_state')
    elif callback.data == 'NO':
        await callback.message.answer('отправь id')
        await state.set_state(Admin.add_vip_id)
        log.info('add vip user failed, set add vip id ')






