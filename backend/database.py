from exceptions import DatabaseError

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

@catch_database_error
async def select_all_users(conn):
    rows = await conn.fetch("SELECT * FROM users")
    return [dict(row) for row in rows]

@catch_database_error
async def create_new_user(conn):
    row = await conn.fetch("INSERT INTO users()")

