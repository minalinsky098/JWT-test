from pydantic import BaseModel

class LoginPayLoad(BaseModel):
    pass

loginresponse = {
    201: {"detail":"User registered"}, 
    409: {"detail":"user already in database"}
    }

class AuthenticatePayLoad(LoginPayLoad):
    pass

