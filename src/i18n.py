from aiogram.types import Message
from src.texts import T

async def t(msg: Message, key: str, **kw):
    lang = getattr(msg.from_user, "language_code", "uz")[:2]
    return T.get(lang, T["uz"]).get(key, key).format(**kw)
