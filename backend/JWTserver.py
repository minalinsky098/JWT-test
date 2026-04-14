from fastapi import FastAPI
from models import LoginPayLoad, LoginResponseModel\
,AuthenticatePayLoad, AuthenticateResponseModel\
,auth_responses, login_responses

app = FastAPI()

@app.get("/")
def main():
    return {"message":"This is the root"}

@app.post("/api/v1/login", status_code = 200, response_model = LoginResponseModel, responses = login_responses)
async def login_user(payload: LoginPayLoad):
    pass

@app.post("/api/v1/register", status_code = 201, response_model = AuthenticateResponseModel, responses = auth_responses)
async def register_user(payload: AuthenticatePayLoad):
    pass