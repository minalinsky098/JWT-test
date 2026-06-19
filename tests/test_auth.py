import pytest
import backend.auth as auth
from datetime import datetime, timedelta, timezone
import jwt

# @pytest.mark.parametrize("password", ["Mypassword", "This password", "LMAOOOO"])
# @pytest.mark.parametrize("wrong_password", ["THIS ONE IS WRONG", "mypassword", "this password"])
@pytest.mark.parametrize("password, wrong_password", [
    ("Mypassword", "mypassword"), ("Wrongpassword", "wrongpassword"), ("misspple", "missapple")
    ])

async def test_hash_password(password, wrong_password):
    hashed = await auth.hash_password(password)
    correct_result = await auth.check_password(password, hashed)
    error_result = await auth.check_password(wrong_password, hashed)
    assert correct_result == True 
    assert error_result == False 
    
async def test_jwt():
    user_id = "USERID124"
    user_jwt = auth.generate_jwt(user_id)
    expired_jwt = jwt.encode({"user_id":"USERID124", "exp": datetime.now(timezone.utc)+timedelta(minutes=-5)}, auth.SECRET, algorithm=auth.ALGORITHM)
    
    tampered_jwt = list(user_jwt)
    tampered_jwt[0] = " "
    tampered_jwt = "".join(tampered_jwt)
    decoded_id = auth.decode_jwt_user_id(user_jwt)
        
    assert user_id == decoded_id
    with pytest.raises(jwt.InvalidTokenError):
        auth.decode_jwt_user_id(tampered_jwt)
        
    with pytest.raises(jwt.ExpiredSignatureError):
        auth.decode_jwt_user_id(expired_jwt)
    
    