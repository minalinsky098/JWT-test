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
      
class AuthenticateResponseModel(BaseModel):
    detail: str
    token: str
    
class GeneralErrorModel(BaseModel):
    detail: str
    
#responses
general_response = {
    500: {"model": GeneralErrorModel, "description": "General Error"}
}

auth_responses = {
    **general_response,
    409:{"model":GeneralErrorModel, "description":"Authentication Error"}
    }

login_responses = {
    **general_response,
    401: {"model":GeneralErrorModel, "description":"Invalid credentials"}
    }
