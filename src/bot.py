import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from fastapi import FastAPI
import uvicorn

from src.config import settings
from src.db import init_db


from src.utils.logging import logger
from src.utils.scheduler import self_ping_loop

from src.handlers import start as h_start
from src.handlers import register as h_register
from src.handlers import entry as h_entry
from src.handlers import report as h_report
from src.handlers import balance as h_balance
from src.handlers import settings as h_settings
from src.handlers import payment as h_payment
from src.handlers import contact as h_contact
from src.handlers import admin as h_admin

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

async def run_bot():
    await init_db()
    bot = Bot(settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Routers
    dp.include_router(h_start.router)
    dp.include_router(h_register.router)
    dp.include_router(h_payment.router)
    dp.include_router(h_balance.router)
    dp.include_router(h_settings.router)
    dp.include_router(h_report.router)
    dp.include_router(h_contact.router)
    dp.include_router(h_admin.router)
    dp.include_router(h_entry.router)  # oxirida: free text

    logger.info("Starting bot...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

async def main():
    # Self-ping background task
    asyncio.create_task(self_ping_loop())

    # Run bot and web server concurrently (Render uchun HTTP port ochiq bo'lsin)
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)

    await asyncio.gather(
        run_bot(),
        server.serve(),
    )

if __name__ == "__main__":
    asyncio.run(main())
