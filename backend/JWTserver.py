from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from contextlib import asynccontextmanager
from pathlib import Path
import asyncpg
import jwt
import os

from models import LoginPayLoad ,RegisterPayLoad, UpdateUserPayload\
,LoginAuthenticateResponseModel, GetAllUsersResponseModel, GetUserResponseModel, UpdateUserResponseModel\
,auth_responses, login_responses, get_all_users_responses, get_user_responses, update_user_responses
from database import logger, select_all_users, create_new_user, select_user, update_user
from exceptions import DatabaseError
from auth import generate_jwt, check_password, decode_jwt_user_id\
,DATABASEURL

DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with asyncpg.create_pool(DATABASEURL) as app.state.db_pool:
        yield
            
async def get_db_conn(request: Request):
    async with request.app.state.db_pool.acquire() as conn:
        yield conn
  
#dependency to get the user id given the frontend sends a bearer witht the token      
async def get_current_user_id(authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))):
    if DEV_MODE:
        return "f7bab17f-e834-4ee8-89ca-50638dbfd705"
    try:
        if not authorization:
            raise HTTPException(status_code=401, detail="No credentials provided")
        user_id = decode_jwt_user_id(authorization.credentials)
        return user_id
    except HTTPException:
        raise
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="User has been logged out automatically")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token is malformed")
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error") 
        
app = FastAPI(lifespan=lifespan)
frontend_path = Path(__file__).resolve().parent.parent/"frontend"

app.mount("/frontend", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def main():
    if DEV_MODE:
        return RedirectResponse(url="/home")
    return FileResponse(frontend_path/"pages"/"index.html")

@app.get("/home")
def homepage():
    return FileResponse(frontend_path/"pages"/"homepage.html")

@app.get("/favorites")
def homepage():
    #return {"message":"this is the favorites page"}
    return FileResponse(frontend_path/"pages"/"favorites.html")

@app.get("/profile")
def homepage():
    #return {"message":"this is the profile page"}
    return FileResponse(frontend_path/"pages"/"profile.html")

@app.post("/api/v1/login", status_code = 200, response_model = LoginAuthenticateResponseModel, responses = login_responses)
async def login_user(payload: LoginPayLoad, connection = Depends(get_db_conn)):
    try:
        user = await select_user(email=payload.email, conn=connection)
        if not(user):
            raise HTTPException(status_code = 401, detail = "User is not registered")
        if not (await check_password(payload.password, user["hashed_password"])):
            raise HTTPException(status_code = 401, detail = "Invalid password")
        token = generate_jwt(user["id"])
        return {"detail": "User logged in","token": token}
    except HTTPException:
        raise
    except DatabaseError as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/api/v1/register", status_code = 201, response_model = LoginAuthenticateResponseModel, responses = auth_responses)
async def register_user(payload: RegisterPayLoad, connection = Depends(get_db_conn)):
    try:
        if (await select_user(email=payload.email, conn=connection)):
            raise HTTPException(status_code = 409, detail = "This person already registered")
        row = await create_new_user(payload.first_name, payload.last_name, payload.password, payload.email, connection)
        token = generate_jwt(row["id"])
        return {"detail": "Successfully registered","token": token}
    except HTTPException:
        raise
    except DatabaseError as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
    except Exception as e:
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
    
@app.get("/api/v1/users/me", status_code = 200, response_model=GetUserResponseModel, responses= get_user_responses)
async def get_user(user_id = Depends(get_current_user_id), connection=Depends(get_db_conn)):
    try:
        user = await select_user(user_id=user_id, conn=connection)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except DatabaseError as e: 
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@app.put("/api/v1/users", status_code = 200, response_model=UpdateUserResponseModel, responses=update_user_responses)
async def update_user_name(payload: UpdateUserPayload, user_id = Depends(get_current_user_id), connection = Depends(get_db_conn)):
    try:
        updated_user = await update_user(first_name = payload.first_name, last_name = payload.last_name, user_id = user_id, conn = connection)
        print(updated_user)
        if not updated_user:
            print("raise 404")
            raise HTTPException(status_code = 404, detail="User not found")
        return updated_user 
    except HTTPException: 
        raise
    except DatabaseError as e: 
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal server error")