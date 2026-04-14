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
    
#responses
auth_responses = {
    409: {"detail":"user already in database"}
    }

login_responses = {
    401: error_parser(LoginErrorModel, "Invalid credentials", "invalid username or password")
    }

