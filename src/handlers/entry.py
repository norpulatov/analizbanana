from aiogram import Router
from aiogram.types import Message
from src.db import async_session_maker
from src.repo import add_entry
from src.nlu import detect_type_and_amount
from src.handlers.limit import check_limit_and_warn

router = Router()

@router.message()
async def free_text(m: Message):
    if not m.text:
        return
    t, amt, cat = detect_type_and_amount(m.text)
    if not (t and amt):
        return  # boshqa handlerlar davom etadi
    note = m.text
    async with async_session_maker() as session:
        e = await add_entry(session, m.from_user.id, t, amt, cat, note)
        if t == "expense":
            await check_limit_and_warn(session, m.from_user.id, int(amt), m.answer)
    await m.answer(f"✅ Yozildi: {t} | {int(amt)} so'm | toifa: {cat or '-'}")
