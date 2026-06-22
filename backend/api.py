from httpx import AsyncClient
import os 
import asyncio
from dotenv import load_dotenv

load_dotenv()
CAT_API = os.getenv("CATAPI")
BASE_URL = os.getenv("CATURL")

async def fetch_cats(limit: int = 45):
    SEARCH_URL = f"{BASE_URL}/images/search"
    header = {"x-api-key":CAT_API}
    try:
        async with AsyncClient() as client:
            res = await client.get(SEARCH_URL, headers=header, params={"limit":limit, "has_breeds":1})
            res.raise_for_status()
            data = res.json()
            normalized_fetch = []
            for cat in data:
                normalized_fetch.append({"url":cat["url"], "breed":cat["breeds"][0]["name"], "description":cat["breeds"][0]["description"]})
            return normalized_fetch
    except Exception:
        raise

