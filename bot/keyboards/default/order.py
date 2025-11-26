from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from django.utils.translation import gettext as _



from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from django.utils.translation import gettext as _

async def get_delivery_type_button():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=_("🏃 Pickup")), 
             KeyboardButton(text=_("🚚 Delivery"))
             ],
            [KeyboardButton(text=_("⬅️ Back"))]
        ],
        resize_keyboard=True
    )
    return keyboard

async def get_pick_up_buttons():
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [
            KeyboardButton(text=_("⬅️ Back")),
            KeyboardButton(text=_("📍Determine nearest branch"))
            
        ],
            [
                KeyboardButton(text=_("Order here 🌐")),
                KeyboardButton(text=_("Select branch"))
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


