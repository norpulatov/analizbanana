from aiogram import Router, F
from aiogram.types import Message
from src.db import async_session_maker
from src.repo import balance

router = Router()

@router.message(F.text == "💰 Balans")
async def show_balance(m: Message):
    async with async_session_maker() as session:
        b = await balance(session, m.from_user.id)
    await m.answer(f"💰 Balans: {b} so'm")
