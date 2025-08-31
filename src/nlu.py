import re

AMOUNT_RE = re.compile(r"(?:(\d+[\s\.,]?)+)\s*(so'm|sum|сум)?", re.IGNORECASE)

INCOME_HINTS = [
    "daromad", "keldi", "oldim", "получил", "доход", "заработал"
]
EXPENSE_HINTS = [
    "sarfladim", "chiqdim", "to'ladim", "оплатил", "расход", "потратил"
]
DEBT_OUT_HINTS = [
    "qarz berdim", "долг дал", "занял кому"
]
DEBT_IN_HINTS = [
    "qarz oldim", "долг взял", "занял у"
]

CATEGORIES = {
    "transport": ["avtobus", "metro", "yo‘l", "yo'l", "benzin", "такси", "транспорт"],
    "food": ["ovqat", "oziq", "restoran", "кафе", "еда"],
    "debt": ["qarz", "долг"],
    "income": ["ish haqi", "daromad", "доход"],
}

def detect_type_and_amount(text: str):
    lower = text.lower()
    amt = None
    m = AMOUNT_RE.search(lower)
    if m:
        raw = m.group(1)
        amt = float(re.sub(r"[\s,]", "", raw).replace(".", ""))
    t = None
    if any(k in lower for k in INCOME_HINTS):
        t = "income"
    elif any(k in lower for k in DEBT_OUT_HINTS):
        t = "debt_out"
    elif any(k in lower for k in DEBT_IN_HINTS):
        t = "debt_in"
    elif any(k in lower for k in EXPENSE_HINTS):
        t = "expense"
    cat = None
    for c, keys in CATEGORIES.items():
        if any(k in lower for k in keys):
            cat = c
            break
    return t, amt, cat
