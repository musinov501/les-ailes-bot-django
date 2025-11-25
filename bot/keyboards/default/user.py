from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.utils.city import get_all_cities


#
# async def get_user_main_menu():
#     keyboard = ReplyKeyboardMarkup(
#         keyboard=[
#             [
#                 KeyboardButton(text=_(""))
#             ]
#         ]
#     )
#


async def get_cities_keyboard():
    cities = await get_all_cities()
    keyboards = ReplyKeyboardBuilder()
    if cities:
        for city in cities:
            keyboards.button(text=city.name)
    else:
        keyboards.button(text="⬅️ Back")

    keyboards.adjust(2)
    return keyboards.as_markup(resize_keyboard=True)