from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, func
from src.config import settings
from src.db import async_session_maker
from src.models import User, Payment, Entry
from src.repo import list_pending_payments, set_payment_status
from src.keyboards import admin_kb

router = Router()

@router.message(F.text == "/admin")
async def admin_home(m: Message):
    if m.from_user.id not in settings.admins:
        return
    await m.answer("Admin panel", reply_markup=admin_kb())

@router.callback_query(F.data == "admin_payments")
async def admin_payments(c: CallbackQuery):
    if c.from_user.id not in settings.admins:
        return
    async with async_session_maker() as session:
        pend = await list_pending_payments(session)
    if not pend:
        await c.message.answer("⏳ Kutayotgan to'lov yo'q")
        return
    text = "\n".join([f"#{p.id} uid={p.user_id} plan={p.plan} amount={p.amount} status={p.status}" for p in pend])
    await c.message.answer(text + "\nTasdiqlash: /appr_<id> | Rad etish: /rej_<id>")

@router.message(F.text.regexp(r"^/appr_(\d+)$"))
async def approve(m: Message):
    if m.from_user.id not in settings.admins:
        return
    pid = int(m.text.split("_")[-1])
    async with async_session_maker() as session:
        await set_payment_status(session, pid, "approved")
    await m.answer(f"✅ Tasdiqlandi: #{pid}")

@router.message(F.text.regexp(r"^/rej_(\d+)$"))
async def reject(m: Message):
    if m.from_user.id not in settings.admins:
        return
    pid = int(m.text.split("_")[-1])
    async with async_session_maker() as session:
        await set_payment_status(session, pid, "rejected")
    await m.answer(f"❌ Rad etildi: #{pid}")

@router.callback_query(F.data == "admin_users")
async def admin_users(c: CallbackQuery):
    if c.from_user.id not in settings.admins:
        return
    async with async_session_maker() as session:
        res = await session.execute(select(func.count()).select_from(User))
        users = res.scalar_one()
    await c.message.answer(f"👥 Foydalanuvchilar: {users} ta")

@router.callback_query(F.data == "admin_stats")
async def admin_stats(c: CallbackQuery):
    if c.from_user.id not in settings.admins:
        return
    async with async_session_maker() as session:
        res = await session.execute(select(func.count()).select_from(Entry))
        entries = res.scalar_one()
    await c.message.answer(f"📈 Yozuvlar soni: {entries} ta")

@router.callback_query(F.data == "admin_broadcast")
async def admin_broadcast(c: CallbackQuery):
    await c.message.answer("Broadcast uchun: /send <matn>")

@router.message(F.text.startswith("/send "))
async def do_broadcast(m: Message, bot):
    if m.from_user.id not in settings.admins:
        return
    text = m.text[6:]
    async with async_session_maker() as session:
        res = await session.execute(select(User.id))
        ids = [x[0] for x in res.all()]
    ok = 0
    for uid in ids:
        try:
            await bot.send_message(uid, text)
            ok += 1
        except Exception:
            pass
    await m.answer(f"Yuborildi: {ok}/{len(ids)}")
