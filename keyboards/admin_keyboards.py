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
                 'изменить имя категории': 'change cat', 'изменить текст анекдота': 'change joke',
                 'удалить категорию': 'delete cat', 'удалить анекдот': 'delete joke', 'доп. функции': 'more options'}.items():
        bldr.button(text=k, callback_data=v)
    bldr.adjust(2,2,2,1)
    return bldr


ad_vip_us_key = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='VIP', callback_data='VIP')],
    [InlineKeyboardButton(text='USUAL', callback_data='USUAL')],
], resize_keyboard=True, sizes=2)


yn_key = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='YES', callback_data='YES')],
    [InlineKeyboardButton(text='NO', callback_data='NO')]
], resize_keyboard=True, sizes=2)


options_key = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='добавить ADMIN id', callback_data='add_admin')],
    [InlineKeyboardButton(text='добавить VIP id', callback_data='add_vip')],
    [InlineKeyboardButton(text='контакты разработчика', callback_data='contacts')],
], resize_keyboard=True, sizes=2)



contacts_key = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='GitHub', url='https://github.com/bvalsduo')],
    [InlineKeyboardButton(text='Telegram', url='https://web.telegram.org/k/#@some_gringo')],
    [InlineKeyboardButton(text='send email message', url='https://mail.google.com/mail/u/0/#inbox?compose=CllgCJvlqsDHPVfNTQpCwDktfcnKVNVxlCRhKMqQqCRzXHFXBSghFRsGGdSvPJnQSSlDfrbqfcg')]  # https://mail.google.com/
], resize_keyboard=True, sizes=1)


def dct_rename(cats, old_cat_name, new_cat_name):
    matrix_lst = []
    for k, v in cats.items():
        if k == old_cat_name:
            k = new_cat_name
        matrix_lst.append([k,v])

    dct_matrix_lst = {}
    for item in matrix_lst:
        dct_matrix_lst[item[0]] = item[1]

    return dct_matrix_lst






























