from httpx import AsyncClient
import os 
import asyncio
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()
CAT_API = os.getenv("CATAPI")
BASE_URL = os.getenv("CATURL")

async def fetch_cats(limit: int):
    SEARCH_URL = f"{BASE_URL}/images/search"
    header = {"x-api-key":CAT_API}
    try:
        async with AsyncClient() as client:
            res = await client.get(SEARCH_URL, headers=header, params={"limit":limit})
            data = res.json()
            for _ in data:
                print(_["url"])
    except Exception as e:
        logger.exception(str(e))

asyncio.run(fetch_cats(5))