from pydantic import BaseModel
from typing import List

#payloads=====================
class LoginPayLoad(BaseModel):
    pass

class AuthenticatePayLoad(BaseModel):
    pass

#response_models====================


class LoginAuthenticateResponseModel(BaseModel): #200/201
    detail: str
    token: str
    
class GetAllUsersResponseModel(BaseModel):
    all_users: List[str|None]

#error_models===========    
class GeneralErrorModel(BaseModel): #500
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

get_all_users_responses = {
    **general_response
}