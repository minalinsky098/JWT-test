import httpx 
import os 
from dotenv import load_dotenv
from exceptions import CatAPIError

load_dotenv()
CAT_API = os.getenv("CATAPI")
BASE_URL = os.getenv("CATURL")

async def fetch_cats(limit: int = 45):
    SEARCH_URL = f"{BASE_URL}/images/search"
    header = {"x-api-key":CAT_API}
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(SEARCH_URL, headers=header, params={"limit":limit, "has_breeds":1})
            print(res)
            res.raise_for_status()
            data = res.json()
            normalized_fetch = []
            for cat in data:
                normalized_fetch.append({"url":cat["url"], "breed":cat["breeds"][0]["name"], "description":cat["breeds"][0]["description"]})
            return normalized_fetch
    except (httpx.HTTPStatusError, httpx.RequestError) as e:
        raise CatAPIError from e
    except Exception as e:
        raise 

