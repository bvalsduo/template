from aiogram.utils.keyboard import (InlineKeyboardButton, InlineKeyboardBuilder,
                                    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardBuilder)
from data.jokes import vip_cat_jokes

vip_cat_jokes_key = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Бородатые анекдоты')],
    [KeyboardButton(text='Злые анекдоты')],
    [KeyboardButton(text='Добрые анекдоты')],
    [KeyboardButton(text='Семейные анекдоты')],
    [KeyboardButton(text='Анекдоты по армейскому госту')]
], resize_keyboard=True, input_field_placeholder='кнопки ниже')


# inline key with inds for callback handlers
def vip_cat_jokes_inds(category):
    numbers = InlineKeyboardBuilder()
    for num in range(1, len(vip_cat_jokes[category]) + 1):
        numbers.add(InlineKeyboardButton(text=f'{num}', callback_data=f'{num}-{category}'))
    return numbers.adjust(5, 5)