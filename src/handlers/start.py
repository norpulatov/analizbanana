from aiogram import Router, F
from aiogram.types import Message
from src.keyboards import main_kb, phone_kb
from src.texts import T
from src.config import settings

router = Router()

@router.message(F.text == "/start")
async def start(m: Message):
    lang = settings.default_lang
    await m.answer(T[lang]["start"].format(name=m.from_user.full_name), reply_markup=main_kb())
    if not m.contact:
        await m.answer(T[lang]["ask_phone"], reply_markup=phone_kb())
