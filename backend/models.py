from pydantic import BaseModel, field_validator
from typing import List, Dict, Any

#payloads=====================
class LoginPayLoad(BaseModel):
    pass

class RegisterPayLoad(BaseModel):
    name: str
    password: str
    email: str
    
    @field_validator("email")
    @classmethod
    def check_valid_email(cls, v):
        if "@" not in v:
            raise ValueError("Please enter a valid email address")
        return v

#response_models====================
class LoginAuthenticateResponseModel(BaseModel): #200/201
    detail: str
    token: str
    
class GetAllUsersResponseModel(BaseModel):
    all_users: List[Dict[str, Any]]

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