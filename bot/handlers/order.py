from aiogram import Router
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from django.utils.translation import gettext as _

from bot.keyboards.default.order import get_delivery_type_button
from bot.keyboards.default.user import ORDER_BUTTON

router = Router()


class OrderButtonFilter(BaseFilter):
    async def __call__(self, message: Message):
        return message.text == ORDER_BUTTON


@router.message(OrderButtonFilter())
async def order_handler(message: Message, state: FSMContext):
    text = _("Pick up the order yourself 🙋‍♂️ or choose delivery 🚙.")
    await message.answer(text, reply_markup=await get_delivery_type_button())

    