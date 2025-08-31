from datetime import datetime, timezone, timedelta
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import User, Entry, Payment, Limit

async def get_or_create_user(session: AsyncSession, user_id: int, *, name: str | None, lang: str):
    res = await session.execute(select(User).where(User.id == user_id))
    user = res.scalar_one_or_none()
    if user:
        return user
    user = User(id=user_id, name=name, lang=lang)
    session.add(user)
    await session.commit()
    return user

async def update_user_phone(session: AsyncSession, user_id: int, phone: str):
    res = await session.execute(select(User).where(User.id == user_id))
    user = res.scalar_one_or_none()
    if not user:
        # Agar user bo‘lmasa, uni yaratib qo‘yamiz
        user = User(id=user_id, phone=phone)
        session.add(user)
    else:
        user.phone = phone
    await session.commit()
    return user

async def add_entry(session: AsyncSession, user_id: int, type_: str, amount: float, category: str | None, note: str | None):
    e = Entry(user_id=user_id, type=type_, amount=amount, category=category, note=note)
    session.add(e)
    await session.commit()
    return e

async def set_monthly_limit(session: AsyncSession, user_id: int, value: int | None):
    res = await session.execute(select(Limit).where(Limit.user_id == user_id))
    lim = res.scalar_one_or_none()
    if not lim:
        lim = Limit(user_id=user_id, monthly_limit=value)
        session.add(lim)
    else:
        lim.monthly_limit = value
    await session.commit()
    return lim

async def monthly_expense_sum(session: AsyncSession, user_id: int, year: int, month: int) -> int:
    start = datetime(year, month, 1, tzinfo=timezone.utc)
    end = (start.replace(day=28) + timedelta(days=4)).replace(day=1)
    res = await session.execute(
        select(func.coalesce(func.sum(Entry.amount), 0)).where(
            Entry.user_id == user_id,
            Entry.type == "expense",
            Entry.ts >= start,
            Entry.ts < end,
        )
    )
    return int(res.scalar_one())

async def balance(session: AsyncSession, user_id: int):
    inc = await session.execute(select(func.coalesce(func.sum(Entry.amount), 0)).where(Entry.user_id == user_id, Entry.type == "income"))
    exp = await session.execute(select(func.coalesce(func.sum(Entry.amount), 0)).where(Entry.user_id == user_id, Entry.type == "expense"))
    return int(inc.scalar_one()) - int(exp.scalar_one())

async def create_payment(session: AsyncSession, user_id: int, plan: str, amount: int):
    p = Payment(user_id=user_id, plan=plan, amount=amount, status="pending")
    session.add(p)
    await session.commit()
    return p

async def list_pending_payments(session: AsyncSession):
    res = await session.execute(select(Payment).where(Payment.status == "pending").order_by(Payment.created_at.desc()))
    return res.scalars().all()

async def set_payment_status(session: AsyncSession, payment_id: int, status: str):
    res = await session.execute(select(Payment).where(Payment.id == payment_id))
    p = res.scalar_one()
    p.status = status
    if status == "approved":
        # 1m -> 30 kun, 3m -> 90 kun
        res = await session.execute(select(User).where(User.id == p.user_id))
        u = res.scalar_one()
        now = datetime.now(timezone.utc)
        add_days = 30 if p.plan == "1m" else 90
        u.premium_until = (u.premium_until or now) + timedelta(days=add_days)
    await session.commit()
    return p

async def user_is_premium(session: AsyncSession, user_id: int) -> bool:
    res = await session.execute(select(User.premium_until).where(User.id == user_id))
    dt = res.scalar_one_or_none()
    if not dt:
        return False
    return dt > datetime.now(timezone.utc)
