from exceptions import DatabaseError

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
    return rows


