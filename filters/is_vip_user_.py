from aiogram.filters import BaseFilter
from aiogram.types import Message
from data.config import vip_ids


class IsVipUser(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return int(message.from_user.id) in vip_ids


def IsVipUser_func(message: Message) -> bool:
    return message.from_user.id in vip_ids
