from aiogram import Router, F
from aiogram.types import Message
from datetime import datetime
from src.db import async_session_maker
from src.repo import set_monthly_limit, monthly_expense_sum

router = Router()

@router.message(F.text == "🎯 Limit")
async def set_limit_prompt(m: Message):
    await m.answer("Oylik limitni kiriting (so'm) yoki 0 bekor qilish uchun:")

@router.message()
async def set_limit(m: Message):
    if not m.text or not m.text.isdigit():
        return
    value = int(m.text)
    async with async_session_maker() as session:
        await set_monthly_limit(session, m.from_user.id, None if value==0 else value)
    await m.answer("✅ Saqlandi")

async def check_limit_and_warn(session, user_id: int, amount: int, send):
    from sqlalchemy import select
    from src.models import Limit
    res = await session.execute(select(Limit).where(Limit.user_id==user_id))
    lim = res.scalar_one_or_none()
    if not lim or not lim.monthly_limit:
        return
    now = datetime.utcnow()
    spent = await monthly_expense_sum(session, user_id, now.year, now.month)
    if spent >= lim.monthly_limit:
        await send(f"⚠️ Diqqat! Oylik limitga yetdingiz: {lim.monthly_limit} so'm.")
