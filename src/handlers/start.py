from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from src.db_utils import get_or_create_user

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession):
    # userni bazaga qo‘shish yoki olish
    await get_or_create_user(
        session,
        message.from_user.id,
        name=message.from_user.full_name,
        lang="uz"
    )

    await message.answer(
        f"Assalomu alaykum, {message.from_user.full_name}! Banalizga xush kelibsiz.\n\n"
        "Ro'yxatdan o'tish uchun telefon raqamingizni yuboring.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📱 Telefon yuborish", request_contact=True)]
            ],
            resize_keyboard=True
        )
    )

