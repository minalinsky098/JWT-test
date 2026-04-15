from dotenv import load_dotenv
from exceptions import DatabaseError
import os
import asyncpg

load_dotenv()
DATABASEURL = os.getenv("DATABASE_URL")

#wrapper that returns a connection pool to a function
def get_connection_pool(func):
    async def wrapper(*args, **kwargs):
        async with asyncpg.create_pool(DATABASEURL) as pool:
            async with pool.acquire() as conn:
                return await func(conn, *args, **kwargs)
    return wrapper

def catch_database_error(func):
    async def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise DatabaseError from e
    return wrapper

@catch_database_error
@get_connection_pool
async def select_all_users(conn):
    rows = await conn.fetch("SELECT * FROM users")
    return rows


