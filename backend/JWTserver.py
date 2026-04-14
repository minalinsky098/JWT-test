from fastapi import FastAPI
from models import LoginPayLoad, AuthenticatePayLoad, login_response

app = FastAPI()

@app.get("/")
def main():
    return {"message":"This is the root"}

@app.post("/api/v1/login", responses=login_response)
async def login(payload: LoginPayLoad):
    pass

@app.post("/api/v1/auth")
async def authenticate(payload: AuthenticatePayLoad, response):
    pass