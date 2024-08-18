from aiogram.utils.keyboard import (InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder,
                                    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardBuilder)
from data.jokes import vip_cat_jokes, usual_cat_jokes

# usual_lst_cats = list(usual_cat_jokes.keys())


usual_lst_cats = ['Бородатые анекдоты', 'Злые анекдоты', 'Добрые анекдоты', 'Семейные анекдоты', 'По армейскому госту']
# keyboard with categories for usual user
def usual_cat_jokes_key(new_cat=''):
    if new_cat:
        usual_lst_cats.append(new_cat)
    bldr = ReplyKeyboardBuilder()
    for text in usual_lst_cats:
        bldr.add(KeyboardButton(text=text))

    bldr.adjust(1)
    return bldr


# inline key with inds for callback handlers
def usual_cat_jokes_inds(category):
    numbers = InlineKeyboardBuilder()
    for num in range(1, len(usual_cat_jokes[category]) + 1):
        numbers.add(InlineKeyboardButton(text=f'{num}', callback_data=f'{num - 1}-{category}'))
    return numbers.adjust(5, 5)



# reading state ReplyKeyboard
def read_keyboard(index=0, count=10):
    keyboard = ReplyKeyboardBuilder()
    buttons = [
    [KeyboardButton(text='Back')],
    [KeyboardButton(text='<<')],
    [KeyboardButton(text=f'{index}/{count}')],
    [KeyboardButton(text='>>')]]
    for button in buttons:
        keyboard.add(*button)

    return keyboard.adjust(4)


# InlineKeyboard

# def reading_keyboard():






