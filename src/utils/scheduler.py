import asyncio
import httpx
from src.config import settings
from src.utils.logging import logger

async def self_ping_loop():
    if not settings.self_url:
        logger.warning("SELF_URL not set; self-ping disabled")
        return
    while True:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(settings.self_url + "/health")
                logger.info("Self-ping: %s %s", r.status_code, r.text[:60])
        except Exception as e:
            logger.error("Self-ping error: %s", e)
        await asyncio.sleep(600)  # 10 daqiqa
