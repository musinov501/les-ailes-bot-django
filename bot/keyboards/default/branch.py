from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from bot.utils.branch import get_all_branches_by_city
from django.utils.translation import gettext as _


BACK_BUTTON = _("⬅️ Back")

async def branches_keyboard(branches):
    keyboards = ReplyKeyboardBuilder()
    if branches:
        for branch in branches:
            keyboards.button(text=branch.name)
    else:
        keyboards.button(text=BACK_BUTTON)

    keyboards.adjust(2)
    return keyboards.as_markup(resize_keyboard=True)