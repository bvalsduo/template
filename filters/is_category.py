from aiogram.filters import BaseFilter
from aiogram.types import Message


from keyboards.user_keyboards import usual_lst_cats
from keyboards.vip_user_keyboards import vip_lst_cats
from filters.is_vip_user import IsVipUser_func

class IsCategory(BaseFilter):
    vip_usual = {True: vip_lst_cats, False: usual_lst_cats}
    async def __call__(self, message: Message) -> bool:
        return message.text in self.vip_usual[IsVipUser_func(message)]
