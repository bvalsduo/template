from aiogram.utils.keyboard import (InlineKeyboardButton, InlineKeyboardBuilder,
                                    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardBuilder)
from data.jokes import vip_cat_jokes


vip_lst_cats = ['Бородатые анекдоты', 'Злые анекдоты', 'Добрые анекдоты', 'Семейные анекдоты', 'По армейскому госту']

# keyboard with categories for vip user
def vip_cat_jokes_key(new_cat=''):
    if new_cat:
        vip_lst_cats.append(new_cat)
    bldr = ReplyKeyboardBuilder()
    for text in vip_lst_cats:
        bldr.add(KeyboardButton(text=text))

    bldr.adjust(1)
    return bldr


# inline key with inds for callback handlers
def vip_cat_jokes_inds(category):
    numbers = InlineKeyboardBuilder()
    for num in range(1, len(vip_cat_jokes[category]) + 1):
        numbers.add(InlineKeyboardButton(text=f'{num}', callback_data=f'{num - 1}-{category}'))
    return numbers.adjust(5, 5)


