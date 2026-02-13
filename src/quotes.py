import random
from datetime import date
from src.sources.quotable_client import fetch_quote

FALLBACK_QUOTES = [
    ("Discipline beats motivation every day.", "Unknown"),
    ("Small steps every day become big results.", "Unknown"),
    ("Your future is created by what you do today.", "Unknown"),
    ("Consistency is a superpower.", "Unknown"),
    ("You don’t need to feel ready. You need to start.", "Unknown"),
]

def get_daily_quote():
    try:
        return fetch_quote()
    except Exception:
        d = date.today().isoformat()
        r = random.Random(d)
        return r.choice(FALLBACK_QUOTES)
