from aiogram.utils.keyboard import (InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder,
                                    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardBuilder)
from data.jokes import vip_cat_jokes


usual_cat_jokes_key = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Бородатые анекдоты')],
    [KeyboardButton(text='Злые анекдоты')],
    [KeyboardButton(text='Добрые анекдоты')],
    [KeyboardButton(text='Семейные анекдоты')],
    [KeyboardButton(text='По армейскому госту')]
], resize_keyboard=True, input_field_placeholder='кнопки ниже')




# inline key with inds for callback handlers
def usual_cat_jokes_inds(category):
    numbers = InlineKeyboardBuilder()
    for num in range(1, len(vip_cat_jokes[category]) + 1):
        numbers.add(InlineKeyboardButton(text=f'{num}', callback_data=f'{num}-{category}'))
    return numbers.adjust(5, 5)



# reading state ReplyKeyboard
def read_keyboard(index=1, count=10):
    keyboard = ReplyKeyboardBuilder()
    buttons = [
    [KeyboardButton(text='Back')],
    [KeyboardButton(text='<<')],
    [KeyboardButton(text=f'{index}/{count}')],  # вот здесь надо как-то написать индексы анекдотов в котегории, пагинацию доделать
    [KeyboardButton(text='>>')]]
    for button in buttons:
        keyboard.add(*button)

    return keyboard.adjust(4)


# InlineKeyboard

# def reading_keyboard():






