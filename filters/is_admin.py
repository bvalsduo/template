from aiogram.filters import BaseFilter
from aiogram.types import Message
from data.config import admin_ids


class IsAdmin(BaseFilter):
    def __call__(self, message: Message):
        return message.from_user.id in admin_ids


def IsAdmin_func(message: Message):
    return message.from_user.id in admin_ids