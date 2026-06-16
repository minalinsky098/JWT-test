import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from backend.exceptions import DatabaseError
from backend.auth import decode_jwt_user_id, SECRET, ALGORITHM


async def test_get_all_users(client):
    res = client.get("/api/v1/users")
    assert res.status_code == 200

async def test_login_wrong_email(client):
    payload = {"email": "thisismyemail", "password": "mypassword"}
    res = client.post("/api/v1/login",json = payload)
    assert res.status_code == 422
    
async def test_login_empty_payload(client):
    payload = {}
    res = client.post("/api/v1/login",json = payload)
    assert res.status_code == 422
    
async def test_login_empty_email(client):
    payload = {"email": "","password":"mypassword"}
    res = client.post("/api/v1/login",json = payload)
    assert res.status_code == 422
    
async def test_login_not_registered(client):
    payload = {"email": "email@gmail.com","password":"mypassword"}
    res = client.post("/api/v1/login", json = payload)
    data = res.json()
    assert res.status_code == 401
    assert data["detail"] == "User is not registered"
    
async def test_login_wrong_password(client):
    payload = {"email": "alboloter@gmail.com","password":"Mypassword"}
    res = client.post("/api/v1/login", json = payload)
    data = res.json()
    assert res.status_code == 401   
    assert data["detail"] == "Invalid password"
    
async def test_login_happy(client):
    payload = {"email": "alboloter@gmail.com","password":"mypassword"}
    res = client.post("/api/v1/login", json = payload)
    data = res.json()
    assert res.status_code == 200
    assert "token" in data
    assert data["token"] is not None
    assert data["token"] != ""
    assert data["detail"] == "User logged in"    
  
async def test_login_database_error(client):
    with patch("backend.JWTserver.select_user", new_callable=AsyncMock) as mock_select_user:
        mock_select_user.side_effect = DatabaseError
        
        payload = {"email": "alboloter@gmail.com","password":"mypassword"}
        res = client.post("/api/v1/login", json = payload)
        assert res.status_code == 500
        assert res.json()["detail"] == "Internal Server Error"
  
async def test_register_delete_duplicate(client):
    register_payload = {"first_name": "NEW", "last_name":"REGISTER", "email": "newregister@gmail.com","password":"mypassword"}
    res = client.post("/api/v1/register", json = register_payload)
    data = res.json()
    header = {"Authorization":f"Bearer {data["token"]}"}
    assert res.status_code == 201
    res2 = client.post("/api/v1/register", json = register_payload)
    assert res2.status_code == 409
    delete_res = client.delete("/api/v1/users", headers=header)
    assert delete_res.status_code == 200
    
async def test_register_create_new_user_error(client):
    payload = {"first_name": "RYC", "last_name":"ALB", "email": "alboloter@gmail.com","password":"mypassword"}
    with patch("backend.JWTserver.create_new_user", new_callable=AsyncMock) as mock:
        mock.side_effect = Exception
        res = client.post("/api/v1/register", json = payload)
        assert res.status_code == 409
        
async def test_update_user_name_happy(client, setup_header):
    update_payload = {"first_name": "Newfirstname", "last_name": "newlastname"}
    res = client.put("/api/v1/users", json = update_payload,headers=setup_header)
    assert res.status_code == 200
    
async def test_update_user_not_found(client, setup_header):
    update_payload = {"first_name": "Newfirstname", "last_name": "newlastname"}
    client.delete("/api/v1/users", headers=setup_header)
    res = client.put("/api/v1/users", json = update_payload,headers=setup_header)
    assert res.status_code == 404