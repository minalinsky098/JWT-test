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
    
    @field_validator("password")
    @classmethod
    def check_password_length(cls, v):
        cleaned_v = v.strip()
        if len(cleaned_v) < 8:
            raise ValueError("Password must have 8 characters")
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

class UpdateUserPayload(BaseModel):
    first_name : str
    last_name : str
    
    @field_validator("first_name", "last_name")
    @classmethod
    def check_empty_input(cls, v):
        cleaned_v = v.strip()
        if not cleaned_v:
            raise ValueError("Please enter all fields")
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

class UpdateUserResponseModel(BaseModel):
    first_name : str
    last_name : str

class DeleteUserResponseModel(BaseModel):
    message: str
    id : UUID
    
class FetchCatsResponseModel(BaseModel):
    cats: list[dict]
    
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

update_user_responses = {
    **general_response,
    401 : {"model": GeneralErrorModel, "description" : "Invalid credentials"},
    404 : {"model": GeneralErrorModel, "description": "User not found"}
}

delete_user_responses = {
    **general_response,
    401 : {"model": GeneralErrorModel, "description" : "Invalid credentials"},
    404 : {"model": GeneralErrorModel, "description": "User not found"}
}

fetch_cats_responses= {
    **general_response,
    401 : {"model": GeneralErrorModel, "description" : "Invalid credentials"},
    404 : {"model": GeneralErrorModel, "description": "User not found"}
}