from fastapi import FastAPI, HTTPException, Request, Depends
from contextlib import asynccontextmanager
import asyncpg

from models import LoginPayLoad ,RegisterPayLoad\
,LoginAuthenticateResponseModel, GetAllUsersResponseModel\
,auth_responses, login_responses, get_all_users_responses
from database import logger, select_all_users, create_new_user, select_user
from exceptions import DatabaseError
from utils import generate_jwt\
,DATABASEURL

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
async def login_user(payload: LoginPayLoad, connection = Depends(get_db_conn)):
    try:
        row = await select_user(payload.email, connection)
        if not(row):
            raise HTTPException(status_code = 401, detail = "User is not registered")
        token = generate_jwt(row["id"])
        return {"detail": "Successfully registered","token": token}
    except HTTPException:
        raise
    except DatabaseError as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/api/v1/register", status_code = 201, response_model = LoginAuthenticateResponseModel, responses = auth_responses)
async def register_user(payload: RegisterPayLoad, connection = Depends(get_db_conn)):
    try:
        if (await select_user(payload.email, connection)):
            raise HTTPException(status_code = 409, detail = "This person already registered")
        row = await create_new_user(payload.first_name, payload.last_name, payload.password, payload.email, connection)
        token = generate_jwt(row["id"])
        return {"detail": "Successfully registered","token": token}
    except HTTPException:
        raise
    except DatabaseError as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/api/v1/users", status_code = 200, response_model=GetAllUsersResponseModel, responses = get_all_users_responses)
async def get_users(connection = Depends(get_db_conn)):
    try:
        users = await select_all_users(connection)
        return {"all_users": users}
    except DatabaseError as e: 
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal server error")