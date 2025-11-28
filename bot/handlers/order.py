from aiogram import Router
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from django.utils.translation import gettext as _
from aiogram import F

from bot.keyboards.default.order import get_delivery_type_button, get_pick_up_buttons
from bot.keyboards.default.user import ORDER_BUTTON
from bot.utils.branch import get_all_branches_by_city
from bot.utils.city import get_all_cities
from bot.keyboards.default.branch import branches_keyboard
from bot.utils.product import get_all_categories
from bot.utils.branch import get_all_branches_by_city

router = Router()


class OrderButtonFilter(BaseFilter):
    async def __call__(self, message: Message):
        return message.text == ORDER_BUTTON


@router.message(OrderButtonFilter())
async def order_handler(message: Message, state: FSMContext):
    text = _("Pick up the order yourself 🙋‍♂️ or choose delivery 🚙.")
    await message.answer(text, reply_markup=await get_delivery_type_button())

    
@router.message(F.text == _("🏃 Pickup"))
async def pickup_handler(message: Message, state: FSMContext):
    text  = _("Where are you? Send your location and we determine the nearest branch to you.")
    keyboard = await get_pick_up_buttons()
    await message.answer(text, reply_markup=keyboard)
    
@router.message(F.text == _("Select branch"))
async def branch_selection_handler(message: Message, state: FSMContext):
    cities = await get_all_cities()

    if not cities:
        return await message.answer(_("No cities found."))

    city_id = cities[0].id

    branches = await get_all_branches_by_city(city_id)

    text = _("Choose the branch where you want to pick up the order")
    keyboard = await branches_keyboard(branches)
    await message.answer(text, reply_markup=keyboard)
    




