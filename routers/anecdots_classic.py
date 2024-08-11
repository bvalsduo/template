from aiogram import Router
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from loguru import logger as log
from aiogram.filters import StateFilter


from data.jokes import usual_cat_jokes, vip_cat_jokes
from filters.is_category import IsCategory
from filters.is_vip_user import IsVipUser, IsVipUser_func
from filters.is_admin import IsAdmin
from keyboards.user_keyboards import usual_cat_jokes_key, usual_cat_jokes_inds, read_keyboard
from keyboards.vip_user_keyboards import vip_cat_jokes_key, vip_cat_jokes_inds
from states.FSM_reading import fsm_reading




rout_us = Router()
rout_us.message.filter(~IsVipUser())
rout_us.callback_query.filter(~IsVipUser())


# category selection
@rout_us.message(IsCategory(), StateFilter(default_state))
async def anecdots(message: Message, state: FSMContext):
    log.info('USUAL user')
    if message.text not in ['По армейскому госту']:
        await message.answer(f'{usual_cat_jokes[message.text][0]}',
                             reply_markup=read_keyboard(index=1, count=len(usual_cat_jokes[message.text])).as_markup(resize_keyboard=True))
        await state.update_data(index=0)
        await state.update_data(category=message.text)
        await state.update_data(count=len(usual_cat_jokes[message.text]))
        await state.update_data(count_vip=len(vip_cat_jokes[message.text]))
        await state.set_state(fsm_reading.reading)

        log.info(f'sending anecdots by category - {(await state.get_data())["category"]}')
        log.info('entering a reading state')
    else:
        await message.answer('Что бы открыть эту категорию анекдотов и другие - жми /vip и покупай по скидке')


# entering reading state
# USUAL USER
@rout_us.message(StateFilter(fsm_reading.reading), lambda x: x.text != 'Back')
async def reading_state(message: Message, state: FSMContext):
    try:
        if not message.text.count('/'):
            dct_moves = {'<<': 1, '>>': -1}
            if ((await state.get_data())['index'] - dct_moves[message.text]) <= -1:
                await message.answer('Назад? только вперед!', reply_markup=read_keyboard(index=(await state.get_data())['index'] + 1,
                                                                   count=(await state.get_data())['count_vip']).as_markup(resize_keyboard=True))
                log.debug('error limits - protect')
            elif ((await state.get_data())['index'] - dct_moves[message.text]) > ((int((await state.get_data())['count_vip']) // 2) - 1):
                await message.answer('Что бы смотреть больше анекдотов и больше категорий,\nжми- /vip  и покупай по скидке',
                                     reply_markup=read_keyboard(index=(await state.get_data())['index'] + 1,
                                                                   count=(await state.get_data())['count_vip']).as_markup(resize_keyboard=True))
                log.debug('no vip user - protect')
            else:
                await state.update_data(index=(await state.get_data())['index'] - dct_moves[message.text])
                await message.answer(usual_cat_jokes[(await state.get_data())['category']][(await state.get_data())['index']],
                                     reply_markup=read_keyboard(index=(await state.get_data())['index'] + 1,
                                                                   count=(await state.get_data())['count_vip']).as_markup(resize_keyboard=True))
                log.info(f'sending anecdot by new index - {(await state.get_data())["index"]}')
        else:
            await message.answer((await state.get_data())['category'], reply_markup=usual_cat_jokes_inds((await state.get_data())['category']).as_markup())
            log.info('sending keyboard with anecdots')
    except KeyError:
        await message.answer('Для перехода к другому анекдоту нужно нажать кнопку снизу')


# Back button
@rout_us.message(StateFilter(fsm_reading.reading), lambda x: x.text == 'Back')
async def reading_state_cancel(message: Message, state: FSMContext):
    await state.clear()
    log.info('exit a reading state')
    await message.answer('You go to categories', reply_markup=usual_cat_jokes_key().as_markup(resize_keyboar=True, input_field_placeholder='Кнопки ниже'))


# indexes inline keyboard
@rout_us.callback_query(StateFilter(fsm_reading.reading))
async def reading_state_callback_answer(callback: CallbackQuery, state: FSMContext):
    if int(callback.data.split('-')[0]) <= 4:
        if callback.data.split('-')[1] == (await state.get_data())['category']:
            ind = int(callback.data.split('-')[0])
            await state.update_data(index=ind)
            await callback.message.answer(usual_cat_jokes[(await state.get_data())['category']][ind],
                                          reply_markup=read_keyboard(index=ind + 1, count=(await state.get_data())['count_vip']).as_markup(resize_keyboard=True))
            log.info(f'callback is handled, index - {(await state.get_data())["index"]}')
        else:
            await callback.message.answer('Воспользуйтесь кнопками что ниже')
            log.debug(f'wrong inline keyboard - protected')
    else:
        await callback.message.answer('что-бы посмеятся с этого анекдота купи - /vip',
                                      reply_markup=read_keyboard(index=(await state.get_data())['index'] + 1, count=(await state.get_data())['count_vip']).as_markup(resize_keyboard=True))
        log.debug('inline indexes - protect')













