from pydantic import BaseModel, field_validator
from typing import List, Dict, Any
from uuid import UUID
from datetime import datetime

#payloads

class RegisterPayLoad(BaseModel):
    first_name: str
    last_name: str
    password: str
    email: str
    
    @field_validator("email")
    @classmethod
    def check_valid_email(cls, v):
        cleaned_v = v.strip().lower()
        if "@gmail.com" not in cleaned_v:
            raise ValueError("Please enter a valid gmail address")
        return cleaned_v
    
class LoginPayLoad(BaseModel):
    email: str
    password: str
    
    @field_validator("email")
    @classmethod
    def check_valid_email(cls, v):
        cleaned_v = v.strip().lower()
        if "@gmail.com" not in cleaned_v:
            raise ValueError("Please enter a valid gmail address")
        return cleaned_v

#=========================================================
#response_models
class LoginAuthenticateResponseModel(BaseModel): #200/201
    detail: str
    token: str
    
class GetAllUsersResponseModel(BaseModel):
    all_users: List[Dict[str, Any]]

class GetUserResponseModel(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    created_at: datetime

#================================================
#error_models  
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

get_user_responses = {
    **login_responses
}