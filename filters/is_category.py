from aiogram.filters import BaseFilter
from aiogram.types import Message

class IsCategory(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text in ['Бородатые анекдоты','Злые анекдоты','Добрые анекдоты','Семейные анекдоты', 'По армейскому госту']




