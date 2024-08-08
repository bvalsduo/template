from aiogram.filters import BaseFilter
from aiogram.types import Message
from data.config import admin_ids


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return int(message.from_user.id) in admin_ids


def IsAdmin_func(message: Message):
    return message.from_user.id in admin_ids