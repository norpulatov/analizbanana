from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton

def main_kb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="✍️ Yozuv")
    kb.button(text="📊 Hisobot")
    kb.button(text="💰 Balans")
    kb.button(text="🎯 Limit")
    kb.button(text="💳 To'lov qilish")
    kb.button(text="🌐 Til")
    kb.button(text="📞 Admin bilan bog'lanish")
    kb.adjust(2,2,3)
    return kb.as_markup(resize_keyboard=True)

def phone_kb():
    kb = ReplyKeyboardBuilder()
    kb.add(KeyboardButton(text="📱 Raqamni ulashish", request_contact=True))
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)

def pay_kb(url: str):
    b = InlineKeyboardBuilder()
    b.button(text="To'lovga o'tish", url=url)
    return b.as_markup()

def admin_kb():
    b = InlineKeyboardBuilder()
    b.button(text="👥 Foydalanuvchilar", callback_data="admin_users")
    b.button(text="⏳ To'lov kutyapti", callback_data="admin_payments")
    b.button(text="📣 Xabar yuborish", callback_data="admin_broadcast")
    b.button(text="📈 Statistika", callback_data="admin_stats")
    return b.as_markup()
