from aiogram import Router
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from django.utils.translation import gettext as _

from bot.keyboards.default.user import get_user_main_menu
from bot.utils.city import get_all_cities

router = Router()


class CityNameFilter(BaseFilter):
    async def __call__(self, message: Message):
        cities = await get_all_cities()
        for city in cities:
            if city.name == message.text:
                return {"selected_city": city}
        return False


@router.message(CityNameFilter())
async def city_selection(message: Message, state: FSMContext, selected_city):
    await state.update_data(city=selected_city)
    await message.answer(
        _("Welcome to main menu 😊"),
        reply_markup=await get_user_main_menu(),
    )





