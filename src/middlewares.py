from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Awaitable, Dict, Any
from src.db import async_session_maker
from src.repo import get_or_create_user, user_is_premium
from src.config import settings

class UserMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]):
        async with async_session_maker() as session:
            data["session"] = session
            user = await get_or_create_user(session, event.from_user.id, name=event.from_user.full_name, lang=settings.default_lang)
            data["user"] = user
            return await handler(event, data)

class PremiumRequired(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        async with async_session_maker() as session:
            if not await user_is_premium(session, event.from_user.id):
                await event.answer("🔒 Bu funksiya premium foydalanuvchilar uchun. '💳 To'lov qilish' orqali obuna bo'ling.")
                return
        return await handler(event, data)
