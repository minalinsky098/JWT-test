from exceptions import DatabaseError
from utils import hash_password
import logging

"""
REMINDER always typecast your data as asyncpg returns a record object
and not a dictionary when using GET returns a [<record object>, <record object>]
FastAPI cannot return a record object as it is not JSON seriable so convert it to a dict first
"""

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

#wrapper to catch database errors
def catch_database_error(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.exception(str(e))
            raise DatabaseError from e
    return wrapper

#converts the fetch list of records into list of dicts 
def convert_fetch(records):
    return [dict(record) for record in records]

def convert_fetchrow(record):
    return dict(record) if record else None 

@catch_database_error
async def select_all_users(conn):
    rows = await conn.fetch("SELECT first_name, last_name, email FROM users")
    rows = convert_fetch(rows)
    return rows

@catch_database_error
async def select_user(email, conn):
    row = convert_fetchrow(await conn.fetchrow("SELECT * FROM users WHERE email = ($1)", email))
    return row    

@catch_database_error
async def verfify_user(email, password, conn):
    password = await hash_password(password)
    row = convert_fetchrow(await conn.fetchrow("SELECT * FROM users WHERE email = ($1) AND password = ($2)", email, password))
    return row    

@catch_database_error
async def create_new_user(first_name, last_name, password, email, conn):
    hashed_password = await hash_password(password)
    row = await conn.fetchrow(
        """
        INSERT INTO users(first_name, last_name, hashed_password, email)
        VALUES ($1, $2, $3, $4)
        RETURNING id, first_name, last_name, email 
        """, first_name, last_name, hashed_password, email
        )
    return convert_fetchrow(row)