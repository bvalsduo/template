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
@rout_vip.message(IsCategory())
async def anecdots(message: Message, state: FSMContext):
    log.info('VIP user')
    await message.answer(f'{vip_cat_jokes[message.text][1]}',
                         reply_markup=read_keyboard(index=1, count=len(vip_cat_jokes[message.text])).as_markup(resize_keyboard=True))
    await state.update_data(index=1)
    await state.update_data(category=message.text)
    await state.update_data(count=len(usual_cat_jokes[message.text]))
    await state.update_data(count_vip=len(vip_cat_jokes[message.text]))
    await state.set_state(fsm_reading.reading)

    log.info(f'sending anecdots by category - {(await state.get_data())["category"]}')
    log.info('entering a reading state')


# entering reading state
# VIP USER
@rout_vip.message(StateFilter(fsm_reading.reading), lambda x: x.text != 'Back')
async def reading_state(message: Message, state: FSMContext):
    try:
        if not message.text.count('/'):
            dct_moves = {'<<': 1, '>>': -1}
            if ((await state.get_data())['index'] - dct_moves[message.text]) <= 0:
                await message.answer('Назад? только вперед!', reply_markup=read_keyboard(index=(await state.get_data())['index'],
                                                                   count=(await state.get_data())['count_vip']).as_markup(resize_keyboard=True))
                log.debug('error limits - protect')
            elif ((await state.get_data())['index'] - dct_moves[message.text]) >= int((await state.get_data())['count_vip']):
                await message.answer('Что бы смотреть больше анекдотов и больше категорий,\nжми- /vip  и покупай по скидке',
                                     reply_markup=read_keyboard(index=(await state.get_data())['index'],
                                                                count=(await state.get_data())['count_vip']).as_markup(resize_keyboard=True))
                log.debug('no vip user - protect')
            else:
                await state.update_data(index=(await state.get_data())['index'] - dct_moves[message.text])
                await message.answer(vip_cat_jokes[(await state.get_data())['category']][(await state.get_data())['index']],
                                     reply_markup=read_keyboard(index=(await state.get_data())['index'],
                                                                count=(await state.get_data())['count_vip']).as_markup(resize_keyboard=True))
                log.info(f'sending anecdot by new index - {(await state.get_data())["index"]}')
        else:
            await message.answer((await state.get_data())['category'], reply_markup=usual_cat_jokes_inds((await state.get_data())['category']).as_markup())
            log.info('sending keyboard with anecdots')
    except KeyError:
        await message.answer('Для перехода к другому анекдоту нужно нажать кнопку снизу')


# Back button
@rout_vip.message(StateFilter(fsm_reading.reading), lambda x: x.text == 'Back')
async def reading_state_cancel(message: Message, state: FSMContext):
    await state.clear()
    log.info('exit a reading state')
    await message.answer('You go to categories', reply_markup=vip_cat_jokes_key)


# indexes inline keyboard
@rout_vip.callback_query(StateFilter(fsm_reading.reading))
async def reading_state_callback_answer(callback: CallbackQuery, state: FSMContext):
    if callback.data.split('-')[1] == (await state.get_data())['category']:
        ind = int(callback.data.split('-')[0])
        await state.update_data(index=ind)
        await callback.message.answer(vip_cat_jokes[(await state.get_data())['category']][ind],
                                      reply_markup=read_keyboard(index=ind, count=(await state.get_data())['count_vip']).as_markup(resize_keyboard=True))

        log.info(f'callback is handled, index - {(await state.get_data())["index"]}')
    else:
        await callback.message.answer('Воспользуйтесь кнопками что ниже')
        log.debug(f'wrong inline keyboard - protected')






