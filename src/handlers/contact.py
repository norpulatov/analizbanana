from aiogram import Router, F
from aiogram.types import Message
from src.config import settings

router = Router()

@router.message(F.text == "📞 Admin bilan bog'lanish")
async def contact(m: Message):
    await m.answer(f"👉 {settings.support_bot}")
