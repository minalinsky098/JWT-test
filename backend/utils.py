import aiobcrypt
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from exceptions import ExpiredTokenError
import os
import jwt
import asyncio

load_dotenv()
DATABASEURL = os.getenv("DATABASE_URL")
SECRET = os.getenv("JWTSECRET")
ALGORITHM = os.getenv("JWTALGORITHM")

async def hash_password(password: str):
    byte_pass = password.encode()
    hashed = await aiobcrypt.hashpw(byte_pass, await aiobcrypt.gensalt())
    return hashed.decode()
    
async def check_password(password: str, hashed_password: str): 
    return await aiobcrypt.checkpw(password.encode(), hashed_password.encode())   

def generate_jwt(user_id):
    current_time = datetime.now(timezone.utc)
    expiry_time = current_time + timedelta(minutes=5)
    jwt_token = jwt.encode({"user_id": str(user_id), "exp": expiry_time}, SECRET, ALGORITHM)
    return jwt_token

def get_user_id(token):
    try:
        decoded = jwt.decode(token, SECRET, ALGORITHM)
        return decoded["user_id"]
    except jwt.ExpiredSignatureError:
        raise
    except jwt.InvalidTokenError:
        raise
    
#asyncio.run(hash_password("THIS PASSWORD"))