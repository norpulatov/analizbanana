from aiogram import Router, F
from aiogram.types import Message
from datetime import datetime
from src.db import async_session_maker
from sqlalchemy import select, func
from src.models import Entry

router = Router()

@router.message(F.text == "📊 Hisobot")
async def report_menu(m: Message):
    await m.answer("Hisobot: /day, /month, /all")

@router.message(F.text.in_(["/day", "/month", "/all"]))
async def report(m: Message):
    async with async_session_maker() as session:
        if m.text == "/day":
            today = datetime.utcnow().date()
            q = select(Entry.type, func.sum(Entry.amount)).where(Entry.user_id==m.from_user.id, func.date(Entry.ts)==today).group_by(Entry.type)
        elif m.text == "/month":
            now = datetime.utcnow()
            q = select(Entry.type, func.sum(Entry.amount)).where(
                Entry.user_id==m.from_user.id,
                func.extract('year', Entry.ts)==now.year,
                func.extract('month', Entry.ts)==now.month,
            ).group_by(Entry.type)
        else:
            q = select(Entry.type, func.sum(Entry.amount)).where(Entry.user_id==m.from_user.id).group_by(Entry.type)
        res = await session.execute(q)
        rows = res.all()
        text = "\n".join([f"{t}: {int(a)} so'm" for t,a in rows]) or "Ma'lumot yo'q"
        await m.answer("📊 Hisobot:\n"+text)
