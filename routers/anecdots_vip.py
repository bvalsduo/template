from aiogram import Router
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from loguru import logger as log
from aiogram.filters import StateFilter


from data.jokes import usual_cat_jokes, vip_cat_jokes
from filters.is_category import IsCategory
from filters.is_vip_user import IsVipUser, IsVipUser_func
from keyboards.user_keyboards import usual_cat_jokes_key, usual_cat_jokes_inds, read_keyboard
from keyboards.vip_user_keyboards import vip_cat_jokes_key, vip_cat_jokes_inds
from states.FSM_reading import fsm_reading


rout_vip = Router()
rout_vip.message.filter(IsVipUser())
rout_vip.callback_query.filter(IsVipUser())

# category selection
@rout_vip.message(IsCategory(), StateFilter(default_state))
async def selection_cat(message: Message, state: FSMContext):
    log.info('VIP user')
    await message.answer(f'{vip_cat_jokes[message.text][0]}',
                         reply_markup=read_keyboard(index=1, count=len(vip_cat_jokes[message.text])).as_markup(resize_keyboard=True))
    await state.update_data(index=0)
    await state.update_data(category=message.text)
    # await state.update_data(count=len(usual_cat_jokes[message.text]))
    await state.update_data(count_vip=len(vip_cat_jokes[message.text]))
    await state.set_state(fsm_reading.reading)

    log.info(f'sending anecdots by category - {(await state.get_data())["category"]}')
    log.info('entering a reading state')


# entering reading state
# VIP USER
@rout_vip.message(StateFilter(fsm_reading.reading), lambda x: x.text != 'Back')
async def read_state(message: Message, state: FSMContext):
    ind = (await state.get_data())['index']
    count_us = (await state.get_data())['count_us']
    count_vip = (await state.get_data())['count_vip']
    cat = (await state.get_data())['category']
    try:
        if not message.text.count('/'):
            dct_moves = {'<<': 1, '>>': -1}
            if (ind - dct_moves[message.text]) <= -1:
                await message.answer('Назад? только вперед!',
                                     reply_markup=read_keyboard(index=ind + 1,
                                                                count=count_vip).as_markup(resize_keyboard=True))
                log.debug('error limits - protect')
            elif (ind - dct_moves[message.text]) > int((await state.get_data())['count_vip'] - 1):
                await message.answer('а больше нету',
                                     reply_markup=read_keyboard(index=(await state.get_data())['index'] + 1,
                                                                count=count_vip).as_markup(resize_keyboard=True))
                log.debug('error limits - protect')
            else:
                await state.update_data(index=(await state.get_data())['index'] - dct_moves[message.text])
                await message.answer(vip_cat_jokes[cat][(await state.get_data())['index']],
                                     reply_markup=read_keyboard(index=(await state.get_data())['index'] + 1,
                                                                count=count_vip).as_markup(resize_keyboard=True))
                log.info(f'sending anecdot by new index - {(await state.get_data())["index"]}')
        else:
            await message.answer(cat, reply_markup=vip_cat_jokes_inds(cat).as_markup())
            log.info('sending keyboard with anecdots')
    except KeyError:
        await message.answer('Для перехода к другому анекдоту нужно нажать кнопку снизу')


# Back button
@rout_vip.message(StateFilter(fsm_reading.reading), lambda x: x.text == 'Back')
async def read_state_exit(message: Message, state: FSMContext):
    await state.clear()
    log.info('exit a reading state')
    await message.answer('You go to categories',
                         reply_markup=vip_cat_jokes_key().as_markup(resize_keyboar=True,
                                                                    input_field_placeholder='Кнопки ниже'))


# indexes inline keyboard
@rout_vip.callback_query(StateFilter(fsm_reading.reading))
async def reading_state_callback_answer(callback: CallbackQuery, state: FSMContext):
    cat = (await state.get_data())['category']
    count_vip = (await state.get_data())['count_vip']
    if callback.data.split('-')[1] == cat:
        ind = int(callback.data.split('-')[0])
        await state.update_data(index=ind)
        await callback.message.answer(vip_cat_jokes[cat][ind],
                                      reply_markup=read_keyboard(index=ind + 1,
                                                                 count=count_vip).as_markup(resize_keyboard=True))

        log.info(f'callback is handled, index - {(await state.get_data())["index"]}')
    else:
        await callback.message.answer('Воспользуйтесь кнопками что ниже')
        log.debug(f'wrong inline keyboard - protected')






