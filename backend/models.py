from pydantic import BaseModel

class LoginPayLoad(BaseModel):
    pass

class AuthenticatePayLoad(LoginPayLoad):
    pass


#endpoint responses
auth_responses = {
    201: {"detail":"User registered"}, 
    409: {"detail":"user already in database"}
    }

login_responses = {
    200: {"detail":"User logged in"},
    401: {"description":"Invalid credentials"}
}