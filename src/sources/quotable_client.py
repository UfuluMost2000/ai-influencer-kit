import requests

def fetch_quote(timeout: int = 15) -> tuple[str, str]:
    url = "https://api.quotable.io/random"
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    quote = (data.get("content") or "").strip()
    author = (data.get("author") or "").strip()
    if not quote:
        raise ValueError("No quote returned from Quotable.")
    return quote, author
