from aiogram.utils.keyboard import (InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder,
                                    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardBuilder)

# ФУНКЦИИ
# добавление/удаление категорий/анекдотов
# добавить админа/vip юзера по его id, наверное тогда надо пароль сделать,
# в случае если он его забыл, то отправлять первому(главному) админу в тг
# наверное надо сделать работу с сообщениями, надо их обрабатывать, типо
# если стоит --/: ставить перед знаком \n, вот такое
# выслать все категории/анекдоты которые есть


# нужно сделать генератор reply клавиатуры с категориями анекдотов

def admin_actions():
    bldr = InlineKeyboardBuilder()
    for k, v in {'добавить категорию': 'add cat', 'добавить анекдот': 'add joke',
                 'удалить категорию': 'delete cat', 'удалить анекдот': 'delete joke', 'доп. функции': 'more options'}.items():
        bldr.button(text=k, callback_data=v)
    bldr.adjust(2,2,1)
    return bldr


vip_us_key = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='VIP', callback_data='vip')],
    [InlineKeyboardButton(text='USUAL', callback_data='usual')],
], resize_keyboard=True, sizes=2)
vip_us_key = vip_us_key



