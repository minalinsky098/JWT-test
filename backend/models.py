from pydantic import BaseModel

def error_parser(model, description, example):
    return {
        "description":description, 
        "content":{
            "application/json": {
                "schema": model.model_json_schema(),
                "example": {"detail":example}
                }
            }
        }  

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
auth_responses = {
    409: error_parser(GeneralErrorModel, "Authentication Error", "User is in database already")
    }

login_responses = {
    401: error_parser(GeneralErrorModel, "Invalid credentials", "invalid username or password")
    }
