from aiogram import Router
from aiogram.types import Message
from src.db import async_session_maker
from src.repo import update_user_phone

router = Router()

@router.message()
async def catch_contact(m: Message):
    if getattr(m, "contact", None) and m.contact.phone_number:
        async with async_session_maker() as session:
            await update_user_phone(session, m.from_user.id, m.contact.phone_number)
        await m.answer("✅ Ro'yxatdan o'tdingiz!", reply_markup=None)
