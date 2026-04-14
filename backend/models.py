from pydantic import BaseModel

class LoginPayLoad(BaseModel):
    pass

class AuthenticatePayLoad(LoginPayLoad):
    pass


#endpoint responses
login_response = {
    201: {"detail":"User registered"}, 
    401: {"description":"Invalid credentials"},
    409: {"detail":"user already in database"}
    }