from aiogram import Router, F
from aiogram.types import Message
from src.db import async_session_maker
from sqlalchemy import select
from src.models import User

router = Router()

@router.message(F.text == "🌐 Til")
async def lang_menu(m: Message):
    await m.answer("Tilni tanlang: /uz yoki /ru")

@router.message(F.text.in_(["/uz", "/ru"]))
async def set_lang(m: Message):
    lang = m.text.strip("/")
    async with async_session_maker() as session:
        res = await session.execute(select(User).where(User.id==m.from_user.id))
        u = res.scalar_one()
        u.lang = lang
        await session.commit()
    await m.answer("✅ Til saqlandi")
