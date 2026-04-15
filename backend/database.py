from dotenv import load_dotenv
import os
import asyncio
import asyncpg

load_dotenv()
DATABASEURL = os.getenv("DATABASE_URL")

def get_connection_pool(func):
    async def wrapper(*args, **kwargs):
        async with asyncpg.create_pool(DATABASEURL) as pool:
            async with pool.acquire() as conn:
                return await func(conn, *args, **kwargs)
    return wrapper

@get_connection_pool
async def main(conn):
    rows = await conn.fetch("SELECT * FROM users")
    print(rows)
    print("Connected successfully!")

asyncio.run(main())

