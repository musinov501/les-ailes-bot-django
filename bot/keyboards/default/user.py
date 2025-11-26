from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from django.utils.translation import gettext as _

from bot.utils.city import get_all_cities




ORDER_BUTTON = _("🛍 Order")
HISTORY_BUTTON = _("📖 Buyurtmalar tarixi")
SETTINGS_BUTTON = _("⚙️Sozlash ℹ️ Ma'lumotlar")
PROMO_BUTTON = _("🔥Aksiya")
JOIN_BUTTON = _("🙋‍♂️Jamoamizga qo'shiling")
CONTACT_BUTTON = _("☎️Les Ailes bilan aloqa")
BACK_BUTTON = _("⬅️ Back")


async def get_user_main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=ORDER_BUTTON)
            ],
            [
                KeyboardButton(text=_(HISTORY_BUTTON))
            ],
            [
                KeyboardButton(text=_(SETTINGS_BUTTON)),
                KeyboardButton(text=_(PROMO_BUTTON)),
            ],
            [
                KeyboardButton(text=_(JOIN_BUTTON)),
                KeyboardButton(text=_(CONTACT_BUTTON)),
            ]
        ],
        resize_keyboard=True
    )
    return keyboard



async def get_cities_keyboard():
    cities = await get_all_cities()
    keyboards = ReplyKeyboardBuilder()
    if cities:
        for city in cities:
            keyboards.button(text=city.name)
    else:
        keyboards.button(text=BACK_BUTTON)

    keyboards.adjust(2)
    return keyboards.as_markup(resize_keyboard=True)