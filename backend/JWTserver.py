from fastapi import FastAPI
from models import LoginPayLoad, AuthenticatePayLoad\
,auth_responses, login_responses

app = FastAPI()

@app.get("/")
def main():
    return {"message":"This is the root"}

@app.post("/api/v1/login", status_code = 200, responses=login_responses)
async def login(payload: LoginPayLoad):
    pass

@app.post("/api/v1/auth", status_code=201, responses=auth_responses)
async def authenticate(payload: AuthenticatePayLoad):
    pass