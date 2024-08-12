from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


# ## обычная
#
# # обычный способ
#
# simple_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='first button')],
#                                                 [KeyboardButton(text='second button')],
#                                                 [KeyboardButton(text='third button')]])
#
# # builder
#
# def get_reply_keyboard():
#     reply_keyboard_builder = ReplyKeyboardBuilder()
#     for item in ['<<', '0/0', '>>', 'Back', 'Home']:
#         reply_keyboard_builder.button(text=item)
#     reply_keyboard_builder.adjust(3, 2)
#
#     return reply_keyboard_builder.as_markup(resize_keyboard=True, input_place_holder='Выбери')
#
# ## Inline
#
# # обычный способ
#
# inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='youtube', url='https://www.youtube.com/')],
#                                                         [InlineKeyboardButton(text='monkey', url='https://monkeytype.com/')],
#                                                         [InlineKeyboardButton(text='stepic', url='https://stepik.org/learn')]])
#
# # генератор
#
# def get_inline_keyboard():
#     inline_keyboard_builder = InlineKeyboardBuilder()
#     for k, v in {'youtube': 'https://www.youtube.com/', 'monkey': 'https://monkeytype.com/', 'stepic': 'https://stepik.org/learn'}.items():
#         inline_keyboard_builder.button(text=k, url=v)
#     inline_keyboard_builder.adjust(3)
#
#     return inline_keyboard_builder.as_markup(resize_keyboard=True, input_place_holder='Выбери')


