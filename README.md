# Banaliz – Telegram bot (aiogram + PostgreSQL + Click + Admin + Self‑Ping)

## 1) Tayyorlash
```
cp .env.example .env
# .env dagi qiymatlarni to'ldiring
```

## 2) Docker bilan ishga tushirish
```
docker compose up --build
```

## 3) Lokal (Docker-siz)
```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.bot
```

## 4) Render
- New Web Service deploy qiling (Dockerfile bilan).
- Environment: .env dagi o'zgaruvchilarni qo'shing.
- Port: 8000 (FastAPI healthcheck uchun).
- HEALTHCHECK: GET /health
- SELF_URL ni Render dagi public URL ga qo'ying.

## 5) Admin
- /admin – panel
- To'lovlar: /appr_<id> yoki /rej_<id>
- Broadcast: /send <matn>

## 6) Foydalanuvchi oqimi
- /start -> telefon yuborish -> asosiy menyu
- Matn orqali: "Avtobus uchun 5 000 so'm sarfladim" yoki "100 000 so'm daromad oldim"
- Hisobot: /day, /month, /all
- Limit: "🎯 Limit" tugmasi orqali qiymat yuboring
- To'lov: "💳 To'lov qilish" -> reja tanlash -> Click havola -> admin tasdiq -> auto xabar
- Support: "📞 Admin bilan bog'lanish" -> @BanalizSupportBot
