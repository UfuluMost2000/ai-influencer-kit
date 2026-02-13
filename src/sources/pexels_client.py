import os
import requests
from datetime import date

PEXELS_SEARCH_URL = "https://api.pexels.com/v1/search"

def download_daily_background(
    api_key: str,
    query: str = "motivational abstract",
    out_dir: str = "downloads",
    orientation: str = "portrait",
    timeout: int = 25,
) -> tuple[str, str]:
    os.makedirs(out_dir, exist_ok=True)
    day = date.today().isoformat()
    out_path = os.path.join(out_dir, f"pexels_bg_{day}.jpg")

    # Cache by day
    if os.path.exists(out_path):
        return out_path, "cached"

    headers = {"Authorization": api_key}
    params = {
        "query": query,
        "per_page": 20,
        "orientation": orientation,
        "size": "large",
    }

    r = requests.get(PEXELS_SEARCH_URL, headers=headers, params=params, timeout=timeout)
    r.raise_for_status()
    data = r.json()

    photos = data.get("photos", [])
    if not photos:
        raise ValueError("Pexels returned no photos. Try a different query.")

    p = photos[0]
    src = p.get("src", {})
    img_url = src.get("large2x") or src.get("large") or src.get("original")
    page_url = p.get("url", "")

    if not img_url:
        raise ValueError("Pexels photo missing image URL.")

    img = requests.get(img_url, timeout=timeout)
    img.raise_for_status()

    with open(out_path, "wb") as f:
        f.write(img.content)

    return out_path, (page_url or img_url)
