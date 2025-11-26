from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from django.utils.translation import gettext as _

from bot.keyboards.default.user import get_cities_keyboard
from bot.keyboards.inline.user import get_language_keyboard
from bot.utils.product import get_all_products
from bot.utils.translation import set_user_language, get_or_create_user

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Start command handler"""
    user = message.from_user

    # Create or update user in database (await async function)
    user, created = await get_or_create_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    if created:
        welcome_text = """
Assalomu alaykum! Les Ailes yetkazib berish xizmatiga xush kelibsiz.

Здравствуйте! Добро пожаловать в службу доставки Les Ailes.

Hello! Welcome to Les Ailes delivery service.
"""
        await message.answer(
            welcome_text,
            reply_markup=await get_language_keyboard()
        )
    else:
        text = _("Iltimos, shaharni tanlang:")
        await message.answer(
            text,
            reply_markup=await get_cities_keyboard()
        )


@router.callback_query(F.data.startswith("lang_"))
async def change_language(callback: CallbackQuery):
    """Handle language change"""
    language_code = callback.data.split("_")[1]
    user_id = callback.from_user.id


    await set_user_language(user_id, language_code)


    from django.utils.translation import activate
    activate(language_code)

    success_message = _("✅ Language changed successfully!")
    await callback.answer(success_message)


    menu_text = _(
        "🎉 Great! Now you can use the bot in your preferred language.\n\n"
        "Use /help to see available commands."
    )

    await callback.message.edit_text(menu_text)


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Help command with translated text"""
    help_text = _(
        "📚 <b>Available Commands:</b>\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/language - Change language\n\n"
        "If you have any questions, feel free to ask!"
    )

    await message.answer(help_text, parse_mode="HTML")


@router.message(Command("language"))
async def cmd_language(message: Message):
    """Language selection command"""
    text = _("🌐 Please select your language:")
    await message.answer(text, reply_markup=await get_language_keyboard())


@router.message(Command("photo"))
async def photos(message: Message):
    products = await get_all_products()
    for product in products:
        await message.answer_photo(
            photo=product.file_id,
            caption=product.caption
        )