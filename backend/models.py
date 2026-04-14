from pydantic import BaseModel

class LoginPayLoad(BaseModel):
    pass

class AuthenticatePayLoad(LoginPayLoad):
    pass