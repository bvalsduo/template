from loguru import logger as log
from aiogram import Bot, Dispatcher
from aiogram.types import Message, BotCommand, CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext


from data.jokes import usual_cat_jokes, vip_cat_jokes
from filters.is_category import IsCategory
from filters.is_vip_user import IsVipUser, IsVipUser_func
from filters.is_admin import IsAdmin, IsAdmin_func
from keyboards.user_keyboards import usual_cat_jokes_key, usual_cat_jokes_inds, read_keyboard
from keyboards.vip_user_keyboards import vip_cat_jokes_key, vip_cat_jokes_inds
from states.FSM_reading import fsm_reading
from data.config import token
from routers import anecdots_classic, anecdots_vip, admin_panel




dis = Dispatcher()
bot = Bot(token=token)



# админ панель, а вот здесь вот эти Reply кнопки мешают. Наверное сделаю еще один модуль с роутером

### пока хз как
# оплату нужно сделать
# еще бы webhook сюда прицепить бы
# надо разобраться что такое Midleware, он вообще нужен этому проекту



# /start
@dis.message(CommandStart())
async def bot_start(message: Message):
    vip_usual = {True: 'VIP', False: 'USUAL'}
    ad_us_dct = {True: 'ADMIN', False: 'USUAL'}
    await bot.delete_webhook(drop_pending_updates=True)
    await message.answer(f'Hey! - {vip_usual[IsVipUser_func(message)]}\n and {ad_us_dct[IsAdmin_func(message)]}', reply_markup=usual_cat_jokes_key)
    log.info('Starting bot')


# commands - 'help', 'info', 'vip'
@dis.message(Command(commands=['help', 'info', 'vip']))
async def commands_answer(message: Message):
    dct_answer = {'/help': 'Нужно нажать на одну из кнопок внизу, для выбора котегории анекдотов',
                  '/info': 'Привет это бот-шутник, может в анекдоты, причем бородатые, и не только\nЖми на кнопки снизу чтобы выбрать котегорию',
                  '/vip': 'привет пока хз, кнопки должны быть снизу с оплатой'}
    await message.answer(dct_answer[message.text])
    log.info('answer for command')


# set commands
async def set_commands(bot: Bot):
    menu_commands = [
        BotCommand(command='info', description='Информация'),
        BotCommand(command='help', description='Помощь'),
        BotCommand(command='vip', description='VIP')
    ]
    await bot.set_my_commands(menu_commands)


# initialization
if __name__ == '__main__':
    dis.include_router(router=anecdots_classic.rout_us)
    dis.include_router(router=anecdots_vip.rout_vip)
    dis.include_router(router=admin_panel.rout_admin)

    dis.startup.register(set_commands)
    dis.run_polling(bot)

