import os
from dataclasses import dataclass

@dataclass
class Settings:
    bot_token: str = os.getenv("BOT_TOKEN", "")
    database_url: str = os.getenv("DATABASE_URL", "")
    admins: list[int] = tuple(int(x) for x in os.getenv("ADMINS", "").replace(" ", "").split(",") if x)
    support_bot: str = os.getenv("SUPPORT_BOT", "@BanalizSupportBot")
    self_url: str = os.getenv("SELF_URL", "")
    default_lang: str = os.getenv("DEFAULT_LANG", "uz")

    click_merchant_id: str = os.getenv("CLICK_MERCHANT_ID", "")
    click_service_id: str = os.getenv("CLICK_SERVICE_ID", "")
    click_return_url: str = os.getenv("CLICK_RETURN_URL", "")

    premium_price_1m: int = int(os.getenv("PREMIUM_PRICE_1M", "15000"))
    premium_price_3m: int = int(os.getenv("PREMIUM_PRICE_3M", "40000"))

settings = Settings()
