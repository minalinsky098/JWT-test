import aiobcrypt
from dotenv import load_dotenv
import os
import jwt
import asyncio

load_dotenv()
DATABASEURL = os.getenv("DATABASE_URL")


async def hash_password(password: str):
    byte_pass = password.encode()
    hashed = await aiobcrypt.hashpw(byte_pass, await aiobcrypt.gensalt())
    return str(hashed)
    
async def check_password(password: str):
    pass

def generate_jwt(user_id, ):
    pass
    #jwt = 
    
#asyncio.run(hash_password("THIS PASSWORD"))