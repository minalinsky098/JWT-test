from pydantic import BaseModel

#payloads
class LoginPayLoad(BaseModel):
    pass

class AuthenticatePayLoad(BaseModel):
    pass

#response_models====================
class LoginResponseModel(BaseModel):
    detail: str
    token: str
    
class LoginErrorModel(BaseModel):
    detail: str
    
    
#responses
auth_responses = {
    201: {"detail":"User registered", "token":"jwt-token"}, 
    409: {"detail":"user already in database"}
    }

login_responses = {
    200: {"detail":"User logged in"},
    401: {"description":"Invalid credentials"}
}