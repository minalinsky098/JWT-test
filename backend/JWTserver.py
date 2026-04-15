from fastapi import FastAPI, HTTPException, Request, Depends
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
import asyncpg

from models import LoginPayLoad ,AuthenticatePayLoad\
,LoginAuthenticateResponseModel, GetAllUsersResponseModel\
,auth_responses, login_responses, get_all_users_responses
from database import select_all_users
from exceptions import DatabaseError


load_dotenv()
DATABASEURL = os.getenv("DATABASE_URL")

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with asyncpg.create_pool(DATABASEURL) as app.state.db_pool:
        yield
            
async def get_db_conn(request: Request):
    async with request.app.state.db_pool.acquire() as conn:
        yield conn
        
app = FastAPI(lifespan=lifespan)

@app.get("/")
def main():
    return {"message":"This is the root"}

@app.post("/api/v1/login", status_code = 200, response_model = LoginAuthenticateResponseModel, responses = login_responses)
async def login_user(payload: LoginPayLoad):
    pass

@app.post("/api/v1/register", status_code = 201, response_model = LoginAuthenticateResponseModel, responses = auth_responses)
async def register_user(payload: AuthenticatePayLoad):
    pass

@app.get("/api/v1/users", status_code = 200, response_model=GetAllUsersResponseModel, responses = get_all_users_responses)
async def get_users(connection = Depends(get_db_conn)):
    try:
        users = await select_all_users(connection)
        return {"all_users":users}
    except DatabaseError as e: #check for logging remove during prod
        raise HTTPException(status_code=500, detail=f"Server error: {e}")