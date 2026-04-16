from exceptions import DatabaseError
from utils import hash_password

"""
REMINDER always typecast your data as asyncpg returns a record object
and not a dictionary when using GET returns a [<record object>, <record object>]
"""

def catch_database_error(func):
    
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            print(e)
            raise DatabaseError from e
    return wrapper

#converts the fetch list of records into list of dicts 
def convert_row(records):
    return [dict(record) for record in records]

@catch_database_error
async def select_all_users(conn):
    rows = await conn.fetch("SELECT * FROM users")
    rows = convert_row(rows)
    return rows

@catch_database_error
async def create_new_user(conn, first_name, last_name, password, email):
    hashed_password = hash_password(password)
    print(password, type(password))
    row = await conn.fetchrow(
        """
        INSERT INTO users(first_name, last_name, hashed_password, email)
        VALUES ($1, $2, $3, $4)
        RETURNING *
        """, first_name, last_name, hashed_password, email
        )
    return convert_row(row)