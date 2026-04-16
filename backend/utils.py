import aiobcrypt
import asyncio

async def hash_password(password: str):
    byte_pass = password.encode()
    hashed = await aiobcrypt.hashpw(byte_pass, await aiobcrypt.gensalt())
    return str(hashed)
    
async def check_password(password: str):
    pass
    
#asyncio.run(hash_password("THIS PASSWORD"))