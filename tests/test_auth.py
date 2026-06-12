import pytest
import backend.auth as auth

async def test_hash_password():
    hashed = await auth.hash_password("mypassword")
    correct_result = await auth.check_password("mypassword", hashed)
    error_result = await auth.check_password("wrongpassword", hashed)
    assert correct_result == True 
    assert error_result == False #now whcih directory do i run this, tests? or backend> or the parent JWT test