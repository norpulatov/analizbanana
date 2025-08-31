from aiogram import Router, F
from aiogram.types import Message
from src.config import settings
from src.db import async_session_maker
from src.repo import create_payment
from src.keyboards import pay_kb

router = Router()

BASE_CLICK_URL = "https://my.click.uz/services/pay"

@router.message(F.text == "💳 To'lov qilish")
async def payment_menu(m: Message):
    text = ("Obuna rejalari:\n"
            f"1 oy – {settings.premium_price_1m} so'm (/pay_1m)\n"
            f"3 oy – {settings.premium_price_3m} so'm (/pay_3m)")
    await m.answer(text)

@router.message(F.text.in_(["/pay_1m", "/pay_3m"]))
async def make_payment(m: Message):
    plan = "1m" if m.text.endswith("1m") else "3m"
    amount = settings.premium_price_1m if plan=="1m" else settings.premium_price_3m
    params = (
        f"?merchant_id={settings.click_merchant_id}"
        f"&service_id={settings.click_service_id}"
        f"&amount={amount}"
        f"&return_url={settings.click_return_url}"
        f"&transaction_param=uid_{m.from_user.id}_{plan}"
    )
    url = BASE_CLICK_URL + params
    async with async_session_maker() as session:
        await create_payment(session, m.from_user.id, plan, amount)
    await m.answer("To'lov havolasi tayyor. Admin tasdiqlaydi.", reply_markup=pay_kb(url))
